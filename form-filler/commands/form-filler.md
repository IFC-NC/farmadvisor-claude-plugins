| description | argument-hint |
|---|---|
| Pre-fill an agriculture-related form using FarmAdvisor organization and property data | |

# /form-filler

Pre-fill a form using your FarmAdvisor data. Follow the `form-filling` skill execution flow exactly — it is a guided, step-by-step process.

> **CRITICAL**: Do NOT write your own scripts to read or fill PDFs. Use the bundled script at `${CLAUDE_PLUGIN_ROOT}/scripts/fill_pdf.py` for all PDF operations. Use the FarmAdvisor MCP server's `execute` tool to run GraphQL queries for data. Wait for the user's response at each step before proceeding to the next.

## Steps

1. **Select organization** — Query the user's organizations. If multiple, ask them to pick one.
2. **Select property** — Load properties for the selected org. Ask the user to pick one.
3. **Select form source** — Ask the user whether to upload their own PDF or choose a file already stored in FarmAdvisor.
4. **Fill the form** — Map FarmAdvisor data to the PDF's form fields and produce the filled PDF.

See the `form-filling` skill for the full execution flow, queries, and field mappings.
