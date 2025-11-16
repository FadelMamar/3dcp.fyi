#!/usr/bin/env python3
"""Generate navigation structure for mkdocs.yml from converted files."""

import sys
import importlib
from pathlib import Path

convert_module = importlib.import_module('3dcp.mkdocs.convert')
nav_module = importlib.import_module('3dcp.mkdocs.nav')

project_root = Path(__file__).parent.parent

def main():
    """Generate navigation structure."""    
    docs_dir = project_root / 'docs' / 'papers'
        
    if not docs_dir.exists():
        print(f"Error: docs/papers directory does not exist: {docs_dir}", file=sys.stderr)
        sys.exit(1)
    
    nav_yaml = nav_module.generate_nav_yaml(docs_dir)
    print(nav_yaml)


if __name__ == '__main__':
    main()
