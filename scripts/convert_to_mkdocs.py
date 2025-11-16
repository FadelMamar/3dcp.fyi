#!/usr/bin/env python3
"""
Convert markdown files from dat/md/ to MkDocs structure.

This script uses the 3dcp package to convert markdown files.
"""

import sys
import importlib
from pathlib import Path

convert_module = importlib.import_module('3dcp.mkdocs.convert')
nav_module = importlib.import_module('3dcp.mkdocs.nav')

convert_to_mkdocs = convert_module.convert_to_mkdocs
generate_navigation = nav_module.generate_navigation

project_root = Path(__file__).parent.parent

def main():
    """Main conversion function."""    
    
    print(f"Project root: {project_root}")
    print(f"Source directory: {project_root / 'dat' / 'md'}")
    print(f"Target directory: {project_root / 'docs' / 'papers'}")
    
    try:
        # Convert files
        total_files, total_entries, files_by_year = convert_to_mkdocs(project_root)
        
        print(f"\nConversion complete!")
        print(f"  Total files converted: {total_files}")
        print(f"  Total entries: {total_entries}")
        
        # Generate navigation structure
        nav = generate_navigation(files_by_year)
        
        # Save navigation to a file for mkdocs.yml
        nav_file = project_root / 'navigation_structure.txt'
        with open(nav_file, 'w', encoding='utf-8') as f:
            import json
            f.write(json.dumps(nav, indent=2))
        
        print(f"\nNavigation structure saved to: {nav_file}")
        print("Note: You'll need to manually integrate this into mkdocs.yml")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
