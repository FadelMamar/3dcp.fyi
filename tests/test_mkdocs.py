"""Tests for MkDocs implementation."""

import tempfile
import importlib
from pathlib import Path

convert_module = importlib.import_module('3dcp.mkdocs.convert')
nav_module = importlib.import_module('3dcp.mkdocs.nav')

# Import functions from modules
parse_year_month = convert_module.parse_year_month
update_asset_paths = convert_module.update_asset_paths
parse_markdown_file = convert_module.parse_markdown_file
organize_files = convert_module.organize_files
convert_file = convert_module.convert_file
convert_to_mkdocs = convert_module.convert_to_mkdocs
sync_assets = convert_module.sync_assets
generate_navigation = nav_module.generate_navigation
generate_nav_yaml = nav_module.generate_nav_yaml


def test_parse_year_month():
    """Test parsing year and month from filename."""
    assert parse_year_month("2024-08.md") == (2024, 8)
    assert parse_year_month("1997-02.md") == (1997, 2)
    assert parse_year_month("2025-12.md") == (2025, 12)
    
    # Test invalid formats
    try:
        parse_year_month("invalid.md")
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    try:
        parse_year_month("2024-8.md")
        assert False, "Should raise ValueError"
    except ValueError:
        pass


def test_update_asset_paths():
    """Test updating asset paths in content."""
    content = 'src="ico/dm/test.svg" srcset="ico/wm/test.svg" src="fig/test.svg"'
    updated = update_asset_paths(content)
    
    assert '../../../ico/dm/test.svg' in updated
    assert '../../../ico/wm/test.svg' in updated
    assert '../../../fig/test.svg' in updated
    
    # Test with Windows-style paths
    content_win = 'src="fig\\test.svg"'
    updated_win = update_asset_paths(content_win)
    assert '../../../fig/test.svg' in updated_win


def test_parse_markdown_file():
    """Test parsing markdown file into entries."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write("Entry 1\n-----\nEntry 2\n-----\nEntry 3")
        temp_path = Path(f.name)
    
    try:
        entries = parse_markdown_file(temp_path)
        assert len(entries) == 3
        assert "Entry 1" in entries[0]
        assert "Entry 2" in entries[1]
        assert "Entry 3" in entries[2]
    finally:
        temp_path.unlink()


def test_organize_files():
    """Test organizing files by year."""
    with tempfile.TemporaryDirectory() as tmpdir:
        source_dir = Path(tmpdir) / "source"
        source_dir.mkdir()
        
        # Create test files
        (source_dir / "2024-08.md").write_text("Content 1")
        (source_dir / "2024-09.md").write_text("Content 2")
        (source_dir / "2023-01.md").write_text("Content 3")
        (source_dir / "invalid.md").write_text("Content 4")
        
        files_by_year = organize_files(source_dir)
        
        assert 2024 in files_by_year
        assert 2023 in files_by_year
        assert len(files_by_year[2024]) == 2
        assert len(files_by_year[2023]) == 1
        
        # Check sorting
        months_2024 = [month for _, month, _ in files_by_year[2024]]
        assert months_2024 == [8, 9]


def test_convert_file():
    """Test converting a single file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        source_file = Path(tmpdir) / "2024-08.md"
        target_file = Path(tmpdir) / "output" / "2024" / "08.md"
        
        # Create source file with entries using HTML attributes (actual format)
        source_file.write_text(
            'Entry 1 with <img src="ico/dm/test.svg">\n-----\nEntry 2 with <img src="fig/test.svg">'
        )
        
        entry_count = convert_file(source_file, target_file)
        
        assert entry_count == 2
        assert target_file.exists()
        
        content = target_file.read_text(encoding='utf-8')
        assert "Entry 1" in content
        assert "Entry 2" in content
    assert "../../../ico/dm/test.svg" in content
    assert "../../../fig/test.svg" in content


def test_sync_assets():
    """Ensure asset folders are mirrored into docs directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        source_dir = project_root / "dat" / "md"
        docs_dir = project_root / "docs"

        fig_dir = source_dir / "fig"
        fig_dir.mkdir(parents=True)
        (fig_dir / "sample.svg").write_text("<svg></svg>")

        ico_dm_dir = source_dir / "ico" / "dm"
        ico_dm_dir.mkdir(parents=True)
        (ico_dm_dir / "icon.svg").write_text("<svg></svg>")

        sync_assets(source_dir, docs_dir)

        assert (docs_dir / "fig" / "sample.svg").exists()
        assert (docs_dir / "ico" / "dm" / "icon.svg").exists()


def test_generate_navigation():
    """Test generating navigation structure."""
    files_by_year = {
        2024: [(2024, 8, Path("2024-08.md")), (2024, 9, Path("2024-09.md"))],
        2023: [(2023, 1, Path("2023-01.md"))],
    }
    
    nav = generate_navigation(files_by_year)
    
    assert len(nav) == 3
    assert 'Home' in nav[0]
    assert 'Overview' in nav[1]
    assert nav[1]['Overview'] == 'overview/readme-overview.md'
    assert 'Papers' in nav[2]
    
    papers_nav = nav[2]['Papers']
    assert len(papers_nav) == 2  # Two years
    
    # Check that years are sorted reverse (most recent first)
    assert '2024' in str(papers_nav[0])
    assert '2023' in str(papers_nav[1])


def test_generate_nav_yaml():
    """Test generating navigation YAML."""
    with tempfile.TemporaryDirectory() as tmpdir:
        docs_dir = Path(tmpdir) / "papers"
        docs_dir.mkdir()
        
        # Create year directories
        year_2024 = docs_dir / "2024"
        year_2024.mkdir()
        (year_2024 / "08.md").write_text("Content")
        (year_2024 / "09.md").write_text("Content")
        
        year_2023 = docs_dir / "2023"
        year_2023.mkdir()
        (year_2023 / "01.md").write_text("Content")
        
        yaml_output = generate_nav_yaml(docs_dir)
        
        assert "Home: index.md" in yaml_output
        assert "Papers:" in yaml_output
        assert "Overview: overview/readme-overview.md" in yaml_output
        assert "2024" in yaml_output
        assert "2023" in yaml_output
        assert "2024-08" in yaml_output
        assert "2024-09" in yaml_output
        assert "2023-01" in yaml_output


def test_convert_to_mkdocs_integration():
    """Test the full conversion process."""
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        
        # Create source directory structure
        source_dir = project_root / "dat" / "md"
        source_dir.mkdir(parents=True)
        
        # Create test files
        (source_dir / "2024-08.md").write_text("Entry 1\n-----\nEntry 2")
        (source_dir / "2024-09.md").write_text("Entry 3")
        (source_dir / "2023-01.md").write_text("Entry 4")

        # Create asset folders with dummy files
        fig_dir = source_dir / "fig"
        fig_dir.mkdir()
        (fig_dir / "figure.svg").write_text("<svg></svg>")

        ico_dir = source_dir / "ico"
        (ico_dir / "dm").mkdir(parents=True)
        (ico_dir / "wm").mkdir(parents=True)
        (ico_dir / "dm" / "icon.svg").write_text("<svg></svg>")
        (ico_dir / "wm" / "icon.svg").write_text("<svg></svg>")
        
        # Run conversion
        total_files, total_entries, files_by_year = convert_to_mkdocs(project_root)
        
        assert total_files == 3
        assert total_entries == 4  # 2 + 1 + 1
        assert len(files_by_year) == 2
        assert 2024 in files_by_year
        assert 2023 in files_by_year
        
        # Check output files exist
        target_base = project_root / "docs" / "papers"
        assert (target_base / "2024" / "08.md").exists()
        assert (target_base / "2024" / "09.md").exists()
        assert (target_base / "2023" / "01.md").exists()

        # Asset folders should be copied
        assets_base = project_root / "docs"
        assert (assets_base / "fig" / "figure.svg").exists()
        assert (assets_base / "ico" / "dm" / "icon.svg").exists()
        assert (assets_base / "ico" / "wm" / "icon.svg").exists()


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])

