"""Convert markdown files from dat/md/ to MkDocs structure."""

import re
import shutil
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Tuple, Optional


def parse_year_month(filename: str) -> Tuple[int, int]:
    """Extract year and month from filename like '2024-08.md'."""
    match = re.match(r'(\d{4})-(\d{2})\.md$', filename)
    if match:
        return int(match.group(1)), int(match.group(2))
    raise ValueError(f"Invalid filename format: {filename}")


def update_asset_paths(content: str) -> str:
    """
    Update asset paths in content to work from MkDocs structure.
    """
    # Update icon paths (both dm and wm)
    content = re.sub(r'srcset="ico/(dm|wm)/', r'srcset="../../../ico/\1/', content)
    content = re.sub(r'src="ico/(dm|wm)/', r'src="../../../ico/\1/', content)
    
    # Update figure paths
    content = re.sub(r'src="fig\\', r'src="../../../fig/', content)
    content = re.sub(r'src="fig/', r'src="../../../fig/', content)
    
    return content


def sync_assets(source_dir: Path, docs_dir: Path) -> None:
    """
    Ensure that asset folders referenced by the converted markdown files
    are available within the MkDocs docs directory.
    """
    asset_target_base = docs_dir #/ 'dat' / 'md'
    asset_target_base.mkdir(parents=True, exist_ok=True)

    for folder in ('fig', 'ico'):
        source_path = source_dir / folder
        target_path = asset_target_base / folder

        if not source_path.exists():
            print(f"Warning: Asset folder not found, skipping: {source_path}")
            continue

        shutil.copytree(source_path, target_path, dirs_exist_ok=True)


def parse_markdown_file(file_path: Path) -> List[str]:
    """
    Parse a markdown file and return list of entries.
    
    Entries are separated by '-----' lines.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by entry separator (-----)
    entries = re.split(r'\n-----\n', content)
    
    # Filter out empty entries
    entries = [entry.strip() for entry in entries if entry.strip()]
    
    return entries


def organize_files(source_dir: Path) -> Dict[int, List[Tuple[int, int, Path]]]:
    """
    Organize markdown files by year.
    
    Returns: Dict mapping year to list of (year, month, file_path) tuples
    """
    files_by_year = defaultdict(list)
    
    # Find all markdown files matching YYYY-MM.md pattern
    for file_path in source_dir.glob('*.md'):
        try:
            year, month = parse_year_month(file_path.name)
            files_by_year[year].append((year, month, file_path))
        except ValueError:
            print(f"Warning: Skipping file with invalid name format: {file_path.name}")
            continue
    
    # Sort months within each year
    for year in files_by_year:
        files_by_year[year].sort(key=lambda x: (x[0], x[1]))
    
    return files_by_year


def convert_file(source_file: Path, target_file: Path) -> int:
    """
    Convert a single markdown file to MkDocs format.
    
    Returns: Number of entries converted
    """
    # Ensure target directory exists
    target_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Parse entries from source file
    entries = parse_markdown_file(source_file)
    
    # Update asset paths and combine entries
    converted_entries = []
    for entry in entries:
        converted_entry = update_asset_paths(entry)
        converted_entries.append(converted_entry)
    
    # Write to target file with separators
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write('\n\n-----\n\n'.join(converted_entries))
        f.write('\n')
    
    return len(entries)


def _extract_overview_block(readme_content: str) -> Optional[str]:
    """
    Extract the overview section (table) from README content.
    """
    match = re.search(r'## Overview\s*(.*?)\n## ', readme_content, re.DOTALL)
    if not match:
        return None
    return match.group(1).strip()


def _rewrite_table_links(block: str) -> str:
    """
    Rewrite README table links from dat/md paths to MkDocs papers paths.
    """
    def _repl(match: re.Match) -> str:
        year = match.group(1)
        month = match.group(2)
        return f"(../../papers/{year}/{month}.md)"

    rewritten = re.sub(r'\(dat/md/(\d{4})-(\d{2})\.md\)', _repl, block)
    rewritten = rewritten.replace('<div align="center">', '<div align="center" markdown>')
    return rewritten


def create_readme_overview_page(project_root: Path) -> Optional[Path]:
    """
    Generate docs/overview/readme-overview.md from README.md overview section.
    """
    readme_path = project_root / 'README.md'
    if not readme_path.exists():
        print(f"README not found at {readme_path}, skipping overview page generation.")
        return None

    content = readme_path.read_text(encoding='utf-8')
    overview_block = _extract_overview_block(content)
    if not overview_block:
        print("Overview section not found in README, skipping overview page generation.")
        return None

    overview_block = _rewrite_table_links(overview_block)

    target_dir = project_root / 'docs' / 'overview'
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / 'readme-overview.md'

    header_lines = [
        "# Overview",
        #"_Auto-generated from README.md. Run `uv run python scripts/convert_to_mkdocs.py` to refresh._",
        "",
        overview_block,
        ""
    ]
    target_path.write_text('\n'.join(header_lines), encoding='utf-8')
    print(f"Overview page written to {target_path.relative_to(project_root)}")
    return target_path


def convert_to_mkdocs(project_root: Path) -> Tuple[int, int, Dict[int, List[Tuple[int, int, Path]]]]:
    """
    Convert markdown files from dat/md/ to MkDocs structure.
    
    Args:
        project_root: Root directory of the project.
    
    Returns:
        Tuple of (total_files, total_entries, files_by_year)
    """    
    source_dir = project_root / 'dat' / 'md'
    target_base = project_root / 'docs' / 'papers'
    
    if not source_dir.exists():
        raise ValueError(f"Source directory does not exist: {source_dir}")
    
    # Organize files by year
    files_by_year = organize_files(source_dir)
    
    # Convert files
    total_entries = 0
    total_files = 0
    
    for year, file_list in sorted(files_by_year.items()):
        year_dir = target_base / str(year)
        year_dir.mkdir(parents=True, exist_ok=True)
        
        for year_val, month, source_file in file_list:
            target_file = year_dir / f"{month:02d}.md"
            
            try:
                entry_count = convert_file(source_file, target_file)
                total_entries += entry_count
                total_files += 1
                print(f"Converted {source_file.name} -> {target_file.relative_to(project_root)} ({entry_count} entries)")
            except Exception as e:
                print(f"Error converting {source_file.name}: {e}")
    
    # Ensure shared assets (icons, figures) are copied for MkDocs to serve
    docs_dir = project_root / 'docs'
    sync_assets(source_dir, docs_dir)

    # Ensure README overview page is generated for MkDocs navigation.
    create_readme_overview_page(project_root)

    return total_files, total_entries, files_by_year

