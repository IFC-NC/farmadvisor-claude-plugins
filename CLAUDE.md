# CLAUDE.md — FarmAdvisor Claude Plugins

This file documents the repository structure, conventions, and development workflows for AI assistants working in this codebase.

## Repository Overview

This is the **FarmAdvisor Claude Plugins Marketplace** — a curated collection of Claude plugins for agricultural and farm management applications. Plugins integrate with the FarmAdvisor platform via its MCP server to give Claude access to farm data (organizations, properties, files, GPS boundaries, acreage, etc.).

- **Owner**: IFC-NC
- **MCP Server**: `https://ai.farmadvisor.com/mcp` (required by all plugins)
- **License**: MIT (see `LICENSE`)

---

## Repository Structure

```
farmadvisor_claude_plugins/
├── .claude/
│   └── settings.local.json       # Claude permission settings
├── .claude-plugin/
│   └── marketplace.json          # Marketplace registry (lists all plugins)
├── form-filler/                  # The "form-filler" plugin
│   ├── .claude-plugin/
│   │   └── plugin.json           # Plugin metadata
│   ├── .mcp.json                 # MCP server connection config
│   ├── commands/
│   │   └── form-filler.md        # /form-filler slash command definition
│   ├── hooks/
│   │   └── hooks.json            # SessionStart hook (installs pypdf)
│   ├── scripts/
│   │   └── fill_pdf.py           # PDF form manipulation utility (Python 3)
│   └── skills/
│       └── form-filling/
│           └── SKILL.md          # Full guided workflow + GraphQL queries
├── CONTRIBUTING.md               # Plugin submission guidelines
├── LICENSE                       # MIT License
└── README.md                     # Marketplace overview
```

---

## Technology Stack

| Layer | Technology |
|---|---|
| Plugin runtime | Claude Code (web) |
| Data access | FarmAdvisor MCP server (HTTP, GraphQL) |
| PDF manipulation | Python 3 + `pypdf` library |
| Configuration | JSON |
| Documentation | Markdown |

---

## Plugin System Concepts

### Marketplace Registry (`marketplace.json`)

Located at `.claude-plugin/marketplace.json`. Lists all plugins in the marketplace. To add a new plugin, add an entry to the `plugins` array pointing to its directory.

### Plugin Metadata (`plugin.json`)

Each plugin directory contains `.claude-plugin/plugin.json` with:
- `name`, `version`, `description`, `author`
- `hooks` — path to `hooks.json` for lifecycle hooks

### MCP Server Config (`.mcp.json`)

Each plugin directory contains `.mcp.json` that connects Claude to the FarmAdvisor MCP server. All plugins **must** use `https://ai.farmadvisor.com/mcp`.

### Commands (`commands/<name>.md`)

Defines slash commands (e.g., `/form-filler`). The command file uses a two-row Markdown table header for metadata (`description`, `argument-hint`) followed by the command body.

### Skills (`skills/<skill-name>/SKILL.md`)

Skills are multi-step guided workflows invoked from commands. The SKILL.md file begins with a two-column Markdown table (`name`, `description`) that registers it, followed by the full workflow documentation.

### Hooks (`hooks/hooks.json`)

Lifecycle hooks that run automatically. Currently used to install Python dependencies at session start:
- `SessionStart`: runs `pip install pypdf -q`

---

## The `form-filler` Plugin

The only plugin currently in the marketplace. It guides users through filling agricultural PDF forms with data from FarmAdvisor.

### Workflow (4 steps)

1. **Select Organization** — Query `myUserContext` via MCP `execute` tool. Auto-select default org; prompt if multiple.
2. **Select Property** — Query `properties` filtered by org ID. Prompt user if multiple.
3. **Select Form Source** — Ask user: upload a PDF, or pick one from FarmAdvisor (org templates, org files, or property files).
4. **Fill the Form** — List PDF fields → map FarmAdvisor data → fill using `fill_pdf.py` → return filled PDF.

### Critical Rules for AI Assistants

> These rules are enforced in both `commands/form-filler.md` and `skills/form-filling/SKILL.md`:

1. **Never write custom PDF code.** Always use the bundled script: `${CLAUDE_PLUGIN_ROOT}/scripts/fill_pdf.py`
2. **Use the MCP `execute` tool** for all GraphQL queries. The server is pre-connected.
3. **This is an interactive flow.** Present results to the user and wait for their input at each step. Do not skip ahead.
4. **Return the filled PDF file** to the user — not just text.
5. **Only fill fields with clearly matching data.** Do not guess or fabricate values.

### `fill_pdf.py` — PDF Utility Script

Located at `form-filler/scripts/fill_pdf.py`. Entry points:

```bash
# List all fillable AcroForm fields in a PDF
python "${CLAUDE_PLUGIN_ROOT}/scripts/fill_pdf.py" --list-fields input.pdf

# Fill form fields using inline JSON
python "${CLAUDE_PLUGIN_ROOT}/scripts/fill_pdf.py" --fill input.pdf output.pdf \
  --data '{"FieldName": "value"}'

# Fill form fields using a JSON file (preferred for large mappings)
python "${CLAUDE_PLUGIN_ROOT}/scripts/fill_pdf.py" --fill input.pdf output.pdf \
  --data-file /tmp/mappings.json
```

Output is always JSON. `--list-fields` returns `{"fields": [...]}`. `--fill` returns fill statistics including matched/unmatched field names.

The script auto-installs `pypdf` if missing via `ensure_pypdf()`.

### Common FarmAdvisor Field Mappings

| PDF Form Field | FarmAdvisor Data Source |
|---|---|
| Farm / Property Name | `property.name` |
| Organization Name | `property.organization.name` |
| Location / Address | `property.location` |
| Total Acres / Gross Acres | `property.grossAcres` |
| USDA Region | `property.usdaRegion.region` |
| NCREIF Region | `property.ncreifRegion.region` |
| GPS Coordinates | `property.centroid.geojson` |
| Farm Boundary | `property.surveyBoundary.geojson` |

### MCP Tools Available

| Tool | Purpose |
|---|---|
| `execute` | Run GraphQL queries against FarmAdvisor |
| `search` | Discover available data |
| `introspect` | Schema introspection |
| `validate` | Data validation |

---

## Claude Permissions

Defined in `.claude/settings.local.json`:

```json
{
  "permissions": {
    "allow": [
      "mcp__claude_ai_FarmAdvisor__introspect",
      "mcp__claude_ai_FarmAdvisor__search",
      "mcp__claude_ai_FarmAdvisor__validate",
      "WebSearch",
      "WebFetch(domain:raw.githubusercontent.com)"
    ]
  }
}
```

Note: `mcp__claude_ai_FarmAdvisor__execute` is not listed here but is used by the skill — add it if permissions errors occur.

---

## Adding a New Plugin

1. Create a directory at the repo root (e.g., `my-plugin/`)
2. Add `.claude-plugin/plugin.json` with required metadata fields
3. Add `.mcp.json` pointing to `https://ai.farmadvisor.com/mcp`
4. Add `commands/`, `skills/`, `hooks/`, and `scripts/` as needed
5. Register the plugin in `.claude-plugin/marketplace.json`
6. Document in a `README.md` inside the plugin directory

All plugins **must** be relevant to agriculture/farm management and use the FarmAdvisor MCP server.

See `CONTRIBUTING.md` for the full submission checklist and PR process.

---

## Development Workflow

### Branch Strategy

- Development branches: `claude/<name>-<session-id>`
- Main branch: `master`
- Never push directly to `master`

### Git Operations

```bash
# Push to feature branch
git push -u origin claude/<branch-name>

# Fetch specific branch
git fetch origin <branch-name>
```

### No Build System

This repo has no build step, test suite, or CI pipeline currently. Validation is manual:
- JSON files must be valid JSON
- Python script can be tested by running it directly
- Documentation should be clear and complete before submitting a PR

### Environment / Dependencies

- Python 3 (for `fill_pdf.py`)
- `pypdf` (auto-installed by the `SessionStart` hook and by `fill_pdf.py` itself)
- No `requirements.txt` — dependency is managed inline

---

## File Conventions

- **JSON config files**: 2-space indentation, no trailing commas
- **Markdown**: Use ATX headers (`#`, `##`). Tables for structured data. Code blocks with language hints.
- **Python**: PEP 8, `#!/usr/bin/env python3` shebang, docstrings on all functions, `argparse` for CLI, `json` output for structured results
- **Skill/Command files**: Begin with a Markdown table registering the skill/command metadata, then the body
- **No secrets in code**: Use environment variables or presigned URLs; never hardcode credentials
