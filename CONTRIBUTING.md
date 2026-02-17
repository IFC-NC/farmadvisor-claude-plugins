# Contributing to FarmAdvisor Claude Plugins

Thank you for your interest in contributing to the FarmAdvisor Claude Plugins marketplace! This document provides guidelines for submitting plugins to the marketplace.

## How to Submit a Plugin

### 1. Fork the Repository

Fork this repository to your GitHub account and clone it locally.

### 2. Create Your Plugin

Create a new directory in the `plugins/` folder with your plugin name:

```bash
mkdir plugins/my-awesome-plugin
```

### 3. Add Plugin Files

Your plugin directory must contain at minimum:

- `plugin.json` - Plugin metadata and configuration (required)
- `README.md` - Plugin documentation (required)
- `icon.png` - Plugin icon (optional, but recommended)

### 4. Plugin Metadata (plugin.json)

Create a `plugin.json` file with the following structure:

```json
{
  "id": "unique-plugin-id",
  "name": "Your Plugin Name",
  "version": "1.0.0",
  "description": "A clear, concise description of what your plugin does",
  "author": "Your Name or Organization",
  "homepage": "https://your-plugin-homepage.com",
  "repository": "https://github.com/username/plugin-repo",
  "capabilities": [
    "list",
    "of",
    "capabilities"
  ],
  "category": "agriculture|weather|data-analysis|integration|other",
  "tags": [
    "relevant",
    "tags",
    "for",
    "discovery"
  ],
  "entrypoint": "https://your-plugin-api.com/endpoint",
  "authentication": {
    "type": "api_key|oauth|none",
    "required": true
  }
}
```

### 5. Plugin Documentation (README.md)

Your plugin's README.md should include:

- **Description**: What does your plugin do?
- **Features**: List of main features
- **Installation**: How to install and configure
- **Usage**: Examples of how to use the plugin
- **Configuration**: Required settings or environment variables
- **API Documentation**: If applicable
- **Support**: How to get help or report issues
- **License**: License information

### 6. Update marketplace.json

Add your plugin to the `plugins` array in `marketplace.json`:

```json
{
  "plugins": [
    "plugins/my-awesome-plugin"
  ]
}
```

### 7. Test Your Plugin

Before submitting, ensure:

- [ ] All required files are present
- [ ] `plugin.json` is valid JSON
- [ ] Documentation is clear and complete
- [ ] Plugin ID is unique
- [ ] All URLs are accessible
- [ ] Plugin follows security best practices

### 8. Submit a Pull Request

1. Commit your changes with a clear message:
   ```bash
   git add plugins/my-awesome-plugin
   git commit -m "Add my-awesome-plugin"
   ```

2. Push to your fork:
   ```bash
   git push origin main
   ```

3. Open a Pull Request with:
   - Clear title: "Add [Plugin Name]"
   - Description of what your plugin does
   - Any special considerations or requirements

## Plugin Requirements

### Technical Requirements

- Plugin must be accessible via HTTPS
- API endpoints must be stable and versioned
- Must follow security best practices
- Should handle errors gracefully
- Must respect rate limits

### Content Requirements

- Description must be clear and accurate
- Documentation must be in English
- Must include usage examples
- Should include support/contact information

### Quality Standards

- Plugin should be well-tested
- Should follow REST API best practices
- Must respect user privacy
- Should not collect unnecessary data
- Must comply with relevant regulations (GDPR, etc.)

## Plugin Categories

- **agriculture**: Farm management, crop monitoring, livestock
- **weather**: Weather forecasting, climate data
- **data-analysis**: Analytics, reporting, insights
- **integration**: Third-party service integrations
- **other**: Other relevant categories

## Review Process

1. **Automated Checks**: Basic validation of structure and format
2. **Manual Review**: Team review for quality, security, and relevance
3. **Testing**: Verification that plugin works as described
4. **Approval**: Plugin is merged and becomes available in marketplace

## Code of Conduct

- Be respectful and professional
- Provide accurate information
- Respond to feedback constructively
- Follow community guidelines

## Questions?

If you have questions about contributing, please:

- Open an issue in this repository
- Contact the maintainers
- Check existing plugins for examples

Thank you for contributing to the FarmAdvisor Claude Plugins marketplace!
