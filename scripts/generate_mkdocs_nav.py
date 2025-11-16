#!/usr/bin/env python3
"""Generate navigation YAML for mkdocs.yml from converted files."""

import yaml
import importlib
from pathlib import Path

repo_root = Path(__file__).parent.parent
nav_module = importlib.import_module('3dcp.mkdocs.nav')

generate_nav_structure = nav_module.generate_nav_structure


def update_mkdocs_nav():
    """Update the nav section in mkdocs.yml with generated navigation."""
    mkdocs_path = repo_root / 'mkdocs.yml'
    docs_dir = repo_root / 'docs' / 'papers'
    docs_base = repo_root / 'docs'
    
    # Read existing mkdocs.yml
    with open(mkdocs_path, 'r', encoding='utf-8') as f:
        mkdocs_config = yaml.safe_load(f)
    
    # Generate new navigation structure with index files
    nav = generate_nav_structure(docs_dir, generate_index=True, docs_base=docs_base)
    
    # Update the nav section
    mkdocs_config['nav'] = nav
    
    # Write back to mkdocs.yml
    with open(mkdocs_path, 'w', encoding='utf-8') as f:
        yaml.dump(
            mkdocs_config,
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=1000  # Prevent line wrapping for long paths
        )
    
    print(f"Updated navigation in {mkdocs_path}")


def generate_nav_yaml():
    """Generate navigation structure in YAML format for mkdocs.yml."""
    docs_dir = repo_root / 'docs' / 'papers'
    docs_base = repo_root / 'docs'
    nav = generate_nav_structure(docs_dir, generate_index=True, docs_base=docs_base)
    return yaml.dump(nav, default_flow_style=False, sort_keys=False, allow_unicode=True)


if __name__ == '__main__':
    update_mkdocs_nav()

