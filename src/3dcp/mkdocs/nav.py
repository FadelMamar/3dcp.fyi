"""Generate navigation structure for MkDocs."""

from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional


OVERVIEW_PAGE = 'overview/readme-overview.md'


def generate_navigation(files_by_year: Dict[int, List[Tuple[int, int, Path]]]) -> List[Dict[str, Any]]:
    """
    Generate navigation structure for mkdocs.yml.
    
    Args:
        files_by_year: Dict mapping year to list of (year, month, file_path) tuples
    
    Returns: List of navigation items
    """
    nav = [
        {'Home': 'index.md'},
        {'Overview': OVERVIEW_PAGE},
        {'Papers': []}
    ]
    
    # Sort years
    sorted_years = sorted(files_by_year.keys(), reverse=True)  # Most recent first
    
    papers_nav = []
    for year in sorted_years:
        year_files = files_by_year[year]
        year_items = []
        
        for _, month, _ in year_files:
            # Create path relative to docs/
            rel_path = f"papers/{year}/{month:02d}.md"
            month_name = f"{year}-{month:02d}"
            year_items.append({month_name: rel_path})
        
        papers_nav.append({str(year): year_items})
    
    nav[2]['Papers'] = papers_nav
    
    return nav


def generate_year_index(year: int, month_files: List[Path], docs_base: Path) -> Path:
    """
    Generate an index.md file for a year directory listing all months.
    
    Args:
        year: Year number
        month_files: List of month file paths
        docs_base: Base path to docs directory
    
    Returns: Path to the generated index file
    """
    year_dir = docs_base / 'papers' / str(year)
    index_path = year_dir / 'index.md'
    
    # Get month numbers and sort them
    month_nums = sorted([int(f.stem) for f in month_files if f.stem.isdigit()])
    
    # Generate markdown content
    lines = [f"# Papers from {year}\n"]
    lines.append(f"This page lists all papers published in {year}.\n")
    lines.append("## Months\n")
    
    # Month names for display
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    
    for month_num in month_nums:
        month_name = month_names[month_num - 1]
        month_link = f"{month_num:02d}.md"
        lines.append(f"- [{month_name} ({year}-{month_num:02d})]({month_link})")
    
    # Write the index file
    index_path.write_text('\n'.join(lines), encoding='utf-8')
    return index_path


def generate_nav_structure(docs_dir: Path, generate_index: bool = False, docs_base: Optional[Path] = None) -> List[Dict[str, Any]]:
    """
    Generate navigation structure as Python dict for mkdocs.yml.
    
    Args:
        docs_dir: Path to docs/papers directory
        generate_index: Whether to generate index.md files for each year
        docs_base: Base path to docs directory (required if generate_index is True)
    
    Returns: List of navigation items
    """
    nav = [
        {'Home': 'index.md'},
        {'Overview': OVERVIEW_PAGE},
        {'Papers': []}
    ]
    
    # Find all year directories, sorted reverse (most recent first)
    year_dirs = []
    for year_dir in sorted(docs_dir.iterdir(), reverse=True):
        if year_dir.is_dir() and year_dir.name.isdigit():
            year_dirs.append((int(year_dir.name), year_dir))
    
    # Group recent years (2021-2025) separately
    recent_years = []
    other_years = []
    
    for year, year_dir in year_dirs:
        # Get all markdown files and filter out index.md and other non-numeric files
        month_files = [f for f in year_dir.glob('*.md') if f.stem.isdigit()]
        # Sort by numeric month value (not string order)
        month_files.sort(key=lambda f: int(f.stem),reverse=True)
        
        if month_files:
            # Generate index.md for this year if requested
            if generate_index and docs_base:
                generate_year_index(year, month_files, docs_base)
            
            # Create navigation structure with year linking to index.md
            months = []
            for month_file in month_files:
                month_num = int(month_file.stem)
                months.append({f'{year}-{month_num:02d}': f'papers/{year}/{month_num:02d}.md'})
            
            # Year links to its index.md, with months nested
            # In MkDocs, to have a section with a page and children, structure it as:
            # - Section Name:
            #   - Section Name: page.md
            #   - Child 1: child1.md
            year_dict = {
                str(year): [
                    {str(year): f'papers/{year}/index.md'}
                ] + months
            }
            if year >= 2021:
                recent_years.append(year_dict)
            else:
                other_years.append(year_dict)
    
    # Build papers navigation
    papers_nav = []
    
    # Add recent years section
    if recent_years:
        papers_nav.append({'Recent Years': recent_years})
    
    # Separate 2020-2015 from older years
    mid_years = []
    older_years = []
    
    for year_dict in other_years:
        year = int(list(year_dict.keys())[0])
        if year >= 2015:
            mid_years.append(year_dict)
        else:
            older_years.append(year_dict)
    
    # Add mid years (2020-2015)
    papers_nav.extend(mid_years)
    
    # Add older years section
    if older_years:
        papers_nav.append({'Older Years': older_years})
    
    nav[2]['Papers'] = papers_nav
    
    return nav


def generate_nav_yaml(docs_dir: Path) -> str:
    """
    Generate navigation structure in YAML format for mkdocs.yml.
    
    This is a simple version that outputs YAML strings directly.
    For more sophisticated navigation with index files, use generate_nav_structure().
    
    Args:
        docs_dir: Path to docs/papers directory
    
    Returns: YAML string for navigation
    """
    nav_lines = ['- Home: index.md', f'- Overview: {OVERVIEW_PAGE}']
    papers_nav = ['- Papers:']
    
    # Find all year directories, sorted reverse (most recent first)
    year_dirs = []
    for year_dir in sorted(docs_dir.iterdir(), reverse=True):
        if year_dir.is_dir() and year_dir.name.isdigit():
            year_dirs.append((int(year_dir.name), year_dir))
    
    # Group recent years (2021-2025) separately
    recent_years = []
    other_years = []
    
    for year, year_dir in year_dirs:
        months = []
        for month_file in sorted(year_dir.glob('*.md')):
            # Skip index.md and other non-numeric files
            if not month_file.stem.isdigit():
                continue
            month_num = int(month_file.stem)
            months.append(f"    - '{year}-{month_num:02d}': papers/{year}/{month_num:02d}.md")
        
        if months:
            year_nav = f"  - '{year}':"
            for month_entry in months:
                year_nav += f"\n{month_entry}"
            
            if year >= 2021:
                recent_years.append((year, year_nav))
            else:
                other_years.append((year, year_nav))
    
    # Add recent years section
    if recent_years:
        papers_nav.append("    - Recent Years:")
        for year, year_nav in recent_years:
            papers_nav.append(year_nav)
    
    # Add other years
    for year, year_nav in other_years:
        papers_nav.append(year_nav)
    
    nav_lines.extend(papers_nav)
    
    return '\n'.join(nav_lines)

