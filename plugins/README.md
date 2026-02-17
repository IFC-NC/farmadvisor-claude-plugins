# Plugins Directory

This directory contains all the plugin definitions for the FarmAdvisor Claude Plugins marketplace.

## Plugin Structure

Each plugin should be in its own subdirectory with the following structure:

```
plugins/
  my-plugin/
    plugin.json       # Plugin metadata and configuration
    README.md         # Plugin documentation
    icon.png          # (Optional) Plugin icon
```

## Plugin Definition (plugin.json)

Each plugin must have a `plugin.json` file with the following structure:

```json
{
  "id": "unique-plugin-id",
  "name": "Plugin Name",
  "version": "1.0.0",
  "description": "Brief description of what the plugin does",
  "author": "Author Name",
  "homepage": "https://github.com/username/plugin-repo",
  "repository": "https://github.com/username/plugin-repo",
  "capabilities": [
    "capability1",
    "capability2"
  ],
  "mcpServer": "https://ai.farmadvisor.com/mcp"
}
```

**Note:** All plugins must use the FarmAdvisor MCP server at `https://ai.farmadvisor.com/mcp`.

## Adding a Plugin

See [CONTRIBUTING.md](../CONTRIBUTING.md) for instructions on how to submit a plugin to this marketplace.
