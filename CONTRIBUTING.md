# Contributing to farmadvisor-claude-plugins

Thank you for your interest in contributing a plugin to the FarmAdvisor marketplace!

## Adding a Plugin

To add a plugin to this marketplace, submit a pull request that adds an entry to `.claude-plugin/marketplace.json`.

### Plugin Entry Format

Each plugin entry in the `plugins` array should follow this structure:

```json
{
  "name": "your-plugin-name",
  "source": {
    "source": "url",
    "url": "https://github.com/owner/repo.git"
  },
  "description": "A brief description of what your plugin does",
  "version": "1.0.0",
  "strict": true
}
```

### Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique plugin identifier (kebab-case) |
| `source.source` | Yes | Source type (use `"url"`) |
| `source.url` | Yes | Git repository URL for the plugin |
| `source.ref` | No | Git ref (branch/tag) to use |
| `description` | Yes | Brief description of the plugin |
| `version` | Yes | Semantic version string |
| `strict` | No | Whether to use strict mode |

### Requirements

1. The plugin repository must be publicly accessible
2. The plugin must have a valid `.claude-plugin/plugin.json` manifest
3. Use [semantic versioning](https://semver.org/) for the `version` field
4. Provide a clear, concise description

### Validation

Before submitting, verify that your `marketplace.json` is valid JSON:

```bash
python3 -m json.tool .claude-plugin/marketplace.json
```

## Reporting Issues

If you find a problem with an existing plugin or the marketplace itself, please [open an issue](https://github.com/IFC-NC/farmadvisor-claude-plugins/issues).
