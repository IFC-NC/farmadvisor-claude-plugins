#!/usr/bin/env python3
"""
Validation script for FarmAdvisor Claude Plugins marketplace.
Validates the structure and format of plugins in the marketplace.
"""

import json
import os
import sys
from pathlib import Path


def validate_json_file(file_path):
    """Validate that a file contains valid JSON."""
    try:
        with open(file_path, 'r') as f:
            json.load(f)
        return True, None
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except Exception as e:
        return False, f"Error reading file: {e}"


def validate_plugin(plugin_dir):
    """Validate a single plugin directory."""
    errors = []
    warnings = []
    
    plugin_path = Path(plugin_dir)
    
    # Check required files
    plugin_json = plugin_path / "plugin.json"
    readme = plugin_path / "README.md"
    
    if not plugin_json.exists():
        errors.append(f"Missing required file: plugin.json")
        return errors, warnings
    
    if not readme.exists():
        warnings.append(f"Missing recommended file: README.md")
    
    # Validate plugin.json
    is_valid, error = validate_json_file(plugin_json)
    if not is_valid:
        errors.append(f"plugin.json: {error}")
        return errors, warnings
    
    # Check plugin.json structure
    with open(plugin_json, 'r') as f:
        plugin_data = json.load(f)
    
    required_fields = ['id', 'name', 'version', 'description', 'author', 'mcpServer']
    for field in required_fields:
        if field not in plugin_data:
            errors.append(f"plugin.json: Missing required field '{field}'")
    
    # Validate mcpServer value
    if 'mcpServer' in plugin_data:
        expected_mcp = 'https://ai.farmadvisor.com/mcp'
        if plugin_data['mcpServer'] != expected_mcp:
            errors.append(f"plugin.json: mcpServer must be '{expected_mcp}', got '{plugin_data['mcpServer']}'")
    
    recommended_fields = ['homepage', 'repository', 'capabilities']
    for field in recommended_fields:
        if field not in plugin_data:
            warnings.append(f"plugin.json: Missing recommended field '{field}'")
    
    return errors, warnings


def validate_marketplace():
    """Validate the entire marketplace structure."""
    print("Validating FarmAdvisor Claude Plugins marketplace...\n")
    
    root = Path(__file__).parent
    all_errors = []
    all_warnings = []
    
    # Validate marketplace.json
    print("Checking marketplace.json...")
    marketplace_json = root / "marketplace.json"
    if not marketplace_json.exists():
        print("❌ ERROR: marketplace.json not found!")
        return 1
    
    is_valid, error = validate_json_file(marketplace_json)
    if not is_valid:
        print(f"❌ ERROR: marketplace.json - {error}")
        return 1
    
    with open(marketplace_json, 'r') as f:
        marketplace_data = json.load(f)
    
    required_fields = ['name', 'description', 'version', 'plugins']
    for field in required_fields:
        if field not in marketplace_data:
            print(f"❌ ERROR: marketplace.json missing required field '{field}'")
            all_errors.append(f"marketplace.json: Missing field '{field}'")
    
    if not all_errors:
        print("✓ marketplace.json is valid\n")
    
    # Validate plugins directory
    print("Checking plugins directory...")
    plugins_dir = root / "plugins"
    if not plugins_dir.exists():
        print("❌ ERROR: plugins directory not found!")
        return 1
    
    # Find all plugin directories (skip README.md and other files)
    plugin_dirs = [d for d in plugins_dir.iterdir() if d.is_dir()]
    
    if not plugin_dirs:
        print("⚠️  WARNING: No plugins found in plugins directory\n")
    else:
        print(f"Found {len(plugin_dirs)} plugin(s)\n")
    
    # Validate each plugin
    for plugin_dir in plugin_dirs:
        plugin_name = plugin_dir.name
        print(f"Validating plugin: {plugin_name}")
        
        errors, warnings = validate_plugin(plugin_dir)
        
        if errors:
            print(f"  ❌ Errors:")
            for error in errors:
                print(f"     - {error}")
            all_errors.extend([f"{plugin_name}: {e}" for e in errors])
        
        if warnings:
            print(f"  ⚠️  Warnings:")
            for warning in warnings:
                print(f"     - {warning}")
            all_warnings.extend([f"{plugin_name}: {w}" for w in warnings])
        
        if not errors and not warnings:
            print(f"  ✓ Plugin is valid")
        
        print()
    
    # Summary
    print("=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    if all_errors:
        print(f"\n❌ Found {len(all_errors)} error(s):")
        for error in all_errors:
            print(f"  - {error}")
    
    if all_warnings:
        print(f"\n⚠️  Found {len(all_warnings)} warning(s):")
        for warning in all_warnings:
            print(f"  - {warning}")
    
    if not all_errors and not all_warnings:
        print("\n✓ All validations passed!")
        return 0
    elif not all_errors:
        print("\n✓ No errors found (warnings only)")
        return 0
    else:
        print(f"\n❌ Validation failed with {len(all_errors)} error(s)")
        return 1


if __name__ == "__main__":
    sys.exit(validate_marketplace())
