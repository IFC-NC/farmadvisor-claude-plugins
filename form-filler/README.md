# form-filler

A Claude plugin that fills agriculture-related PDF forms using live data from your FarmAdvisor organization and properties.

**Version**: 1.0.0 | **Author**: IFC-NC | **Command**: `/form-filler`

---

## What it does

Given a PDF form with fillable fields, this plugin:

1. Loads your FarmAdvisor organizations and lets you select one
2. Lists properties in that organization and lets you select one
3. Asks whether you want to upload a PDF or use one already stored in FarmAdvisor
4. Inspects the PDF's AcroForm fields, maps them to your property data, and returns the filled PDF

---

## Usage

Run the slash command in Claude:

```
/form-filler
```

Claude will guide you through each step interactively. At no point will it skip ahead or fill fields without your confirmation.

---

## Data mapped to form fields

| Form Field | FarmAdvisor Source |
|---|---|
| Farm / Property Name | `property.name` |
| Organization Name | `property.organization.name` |
| Location / Address | `property.location` |
| Total Acres / Gross Acres | `property.grossAcres` |
| USDA Region | `property.usdaRegion.region` |
| NCREIF Region | `property.ncreifRegion.region` |
| GPS Coordinates | `property.centroid.geojson` |
| Farm Boundary | `property.surveyBoundary.geojson` |

Only fields with a clearly matching value are filled. No values are guessed or fabricated.

---

## Supported PDF types

- PDFs with interactive AcroForm fields (standard fillable forms)
- Flat or scanned PDFs are **not** supported for electronic filling — Claude will present the data as formatted text instead

---

## Plugin structure

```
form-filler/
├── .claude-plugin/
│   └── plugin.json        # Plugin metadata (name, version, author, hooks)
├── .mcp.json              # MCP server config — connects to https://ai.farmadvisor.com/mcp
├── commands/
│   └── form-filler.md     # /form-filler command definition
├── hooks/
│   └── hooks.json         # SessionStart hook: installs pypdf
├── scripts/
│   └── fill_pdf.py        # PDF utility script (Python 3 + pypdf)
└── skills/
    └── form-filling/
        └── SKILL.md       # Full step-by-step workflow with GraphQL queries
```

---

## Dependencies

- **Python 3** — used by `fill_pdf.py`
- **pypdf** — installed automatically at session start via the `SessionStart` hook; also auto-installed by `fill_pdf.py` itself if missing

No manual installation is needed.

---

## `fill_pdf.py` reference

The bundled script handles all PDF operations. It should always be invoked via `${CLAUDE_PLUGIN_ROOT}/scripts/fill_pdf.py` — never replaced with custom code.

```bash
# List all fillable fields in a PDF
python "${CLAUDE_PLUGIN_ROOT}/scripts/fill_pdf.py" --list-fields form.pdf

# Fill fields with inline JSON
python "${CLAUDE_PLUGIN_ROOT}/scripts/fill_pdf.py" --fill form.pdf filled.pdf \
  --data '{"PropertyName": "Willow Creek Farm", "GrossAcres": "1240"}'

# Fill fields from a JSON file (preferred for many fields)
python "${CLAUDE_PLUGIN_ROOT}/scripts/fill_pdf.py" --fill form.pdf filled.pdf \
  --data-file /tmp/field_mappings.json
```

All output is JSON. `--list-fields` returns `{"fields": [...]}`. `--fill` returns statistics on matched and unmatched fields.

---

## MCP tools used

| Tool | Purpose |
|---|---|
| `execute` | Run GraphQL queries to fetch org/property data |
| `search` | Discover available data types |
| `introspect` | Inspect the GraphQL schema |
| `validate` | Validate data before use |

---

## License

[MIT](../LICENSE) — © IFC-NC
