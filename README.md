# FarmAdvisor Claude Plugins Marketplace

A curated collection of Claude plugins for agricultural and farm management applications. Each plugin connects Claude to the [FarmAdvisor](https://farmadvisor.com) platform via its MCP server, giving Claude access to live farm data — organizations, properties, files, GPS boundaries, acreage, and more.

**Owner**: IFC-NC | **License**: MIT | **MCP Server**: `https://ai.farmadvisor.com/mcp`

---

## Available Plugins

### form-filler

> Fill agriculture-related PDF forms automatically using your FarmAdvisor organization and property data.

| | |
|---|---|
| Version | 1.0.0 |
| Command | `/form-filler` |
| Directory | [`form-filler/`](./form-filler/) |

The form-filler plugin guides you through a 4-step interactive workflow:

1. **Select organization** — loads your FarmAdvisor organizations
2. **Select property** — lists properties for the chosen organization
3. **Select form** — upload your own PDF or pick one stored in FarmAdvisor
4. **Fill the form** — maps property data to PDF fields and returns the filled PDF

See [form-filler/README.md](./form-filler/README.md) for full documentation.

---

## Repository Structure

```
farmadvisor_claude_plugins/
├── .claude-plugin/
│   └── marketplace.json      # Marketplace registry
├── form-filler/              # form-filler plugin
│   ├── .claude-plugin/
│   │   └── plugin.json       # Plugin metadata
│   ├── .mcp.json             # MCP server connection config
│   ├── commands/
│   │   └── form-filler.md    # /form-filler slash command
│   ├── hooks/
│   │   └── hooks.json        # SessionStart hook
│   ├── scripts/
│   │   └── fill_pdf.py       # PDF form utility (Python 3)
│   └── skills/
│       └── form-filling/
│           └── SKILL.md      # Guided workflow + GraphQL queries
├── CLAUDE.md                 # AI assistant instructions
├── CONTRIBUTING.md           # Plugin submission guidelines
├── LICENSE                   # MIT License
└── README.md                 # This file
```

---

## Using Plugins in Claude

1. Open Claude Code (web or CLI)
2. Connect to this repository
3. Use the slash command for the plugin you want — e.g., `/form-filler`
4. Follow the interactive prompts

All plugins require the FarmAdvisor MCP server to be connected. The `.mcp.json` in each plugin directory handles this automatically.

---

## Contributing

Contributions are welcome. If you've built a Claude plugin for an agricultural use case, we'd love to include it.

**Quick checklist:**
- Plugin directory at repo root (e.g., `my-plugin/`)
- `.claude-plugin/plugin.json` with name, version, description, author
- `.mcp.json` pointing to `https://ai.farmadvisor.com/mcp`
- `README.md` inside the plugin directory
- Entry added to `.claude-plugin/marketplace.json`

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the full submission process.

---

## Security

- All plugins communicate over HTTPS only
- Files from FarmAdvisor are accessed via presigned URLs — no credentials in code
- Claude permissions are scoped in `.claude/settings.local.json`

Report security vulnerabilities privately to the maintainers via GitHub.

---

## License

[MIT](./LICENSE) — © IFC-NC
