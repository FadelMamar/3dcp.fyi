# Development Findings Report

## Project Overview

**3dcp.fyi** is a comprehensive, manually curated database of scientific works related to 3D Concrete Printing (3DCP) and additive construction. The project serves as an exhaustive citation network graph documenting the state-of-the-art in 3D printing within the construction industry, primarily focusing on cementitious materials and extrusion-based manufacturing.

### Key Characteristics

- **Not a review paper**: This is a curated database, not a traditional academic review
- **Manual curation**: Each entry has been manually curated over the years to ensure quality and consistency
- **Comprehensive coverage**: Documents research from 1997 to present (2025)
- **Citation network analysis**: Publications are evaluated by their centralities in the citation network over multiple topological generations

## Repository Structure

### Root Directory

```
3dcp.fyi/
├── README.md              # Main project documentation
├── LICENSE                # License file (CC BY-NC-SA 4.0)
├── CITATION.cff           # Citation metadata
└── dat/                   # Data directory
    ├── 3dcp.fyi.bib       # BibTeX database (8 MB)
    ├── 3dcpfyix.svg       # Project logo
    └── md/                 # Markdown files directory
```

### dat/md Directory Structure

The `dat/md` directory contains:
- **164 markdown files** (`.md` format)
- **3,173 SVG figure files** in `fig/` subdirectory
- **Icon assets** in `ico/` subdirectory with two variants:
  - `dm/` - Dark mode icons (27 SVG files)
  - `wm/` - White/light mode icons (27 SVG files)

## dat/md Directory Analysis

### File Count
- **Total markdown files**: 164 files
- **Date range**: February 1997 to July 2025 (28+ years of coverage)

### File Naming Convention
Files follow a strict naming pattern: `YYYY-MM.md`
- Format: 4-digit year, hyphen, 2-digit month
- Examples:
  - `1997-02.md` (February 1997)
  - `2025-07.md` (July 2025)
  - `2024-09.md` (September 2024)

### Temporal Distribution
Based on the README overview table:
- **Earliest entry**: February 1997 (`1997-02.md`)
- **Latest entry**: July 2025 (`2025-07.md`)
- **Peak activity**: Recent years show significant growth:
  - 2024-09: 305 entries (largest single month)
  - 2024-07: 113 entries
  - 2024-11: 113 entries
  - 2025-05: 77 entries
- **Sparse early years**: 1997-2013 have very few entries per month (1-6 entries)
- **Growth phase**: 2014-2018 show gradual increase
- **Mature phase**: 2019-2025 show consistent high activity

## File Structure Analysis

### Bibliographic Entry Format

Each markdown file contains multiple bibliographic entries separated by horizontal rules (`-----`). Each entry follows a structured format:

#### 1. Entry Header
```markdown
<a id="uniqueEntryID"></a>
### [Icons] Paper Title (YYYY-MM)
```

**Components:**
- **Anchor ID**: Unique identifier (e.g., `ahadvali2025ZRMf3CP`)
- **Icons**: Multiple icon links with dark/light mode support:
  - Open/Closed Access indicator
  - BibTeX entry link
  - DOI link
  - Crossmark link
  - PDF download link (if available)
- **Title**: Paper title with publication month/year in parentheses

#### 2. Author Information
```markdown
<a href="ORCID_URL">Author Name <b>Lastname</b> <ORCID_ICON></a>,
[Additional authors...]
<br>Publication Type – Journal/Conference Name, Vol. X, No. Y, pp. Z
```

**Features:**
- Authors linked to ORCID profiles when available
- Author names formatted with bold last names
- ORCID icons with dark/light mode support
- Publication metadata (type, venue, volume, issue, pages)

#### 3. Abstract
```markdown
<details><summary>Abstract</summary>
[Abstract text here]
</details>
```

- Abstracts are collapsible using HTML `<details>` tag
- Allows for clean presentation while preserving full content

#### 4. Academic Service Links
Each entry includes links to multiple academic databases and services:
- Google Scholar
- Web of Science (when available)
- Scopus
- PlumX
- Crossref
- OpenAlex
- Semantic Scholar
- Open Citations
- ResearchGate
- Scite
- Connected Papers (Inciteful)

**Icon System:**
- All icons support dark/light mode via `<picture>` tags
- Icons stored in `ico/dm/` (dark mode) and `ico/wm/` (white/light mode)
- Blank spacer icons used for alignment
- 16x16 pixel SVG icons

#### 5. Entry Separator
Entries are separated by horizontal rules:
```markdown
-----
```

### Example Entry Structure

```markdown
<a id="ahadvali2025ZRMf3CP"></a>
### [Icons] Zigzag Reinforcement Method for 3D Concrete Printing (2025-05)
[Author information with ORCID links]
[Publication details]
<details><summary>Abstract</summary>...</details>
[Academic service links with icons]
-----
```

## Key Statistics

Based on README analysis:

- **Scientific Works**: ~4,000 entries
- **Evaluated Citations**: ~69,285 citations
- **Last Update**: 2025-06-08
- **Dataset Size**: 8 MB (BibTeX file)
- **License**: CC BY-NC-SA 4.0 (Creative Commons Attribution-NonCommercial-ShareAlike 4.0)

## Observations

### Manual Curation Process
- Each entry is manually curated (not automated)
- Authors are identified through ORCID profiles
- Ensures data quality and consistency

### ORCID Integration
- Authors are linked to their ORCID profiles when available
- ORCID icons displayed next to author names
- Supports researcher identification and disambiguation

### Citation Network Analysis
- Publications evaluated by centralities in citation network
- Analysis performed over multiple topological generations
- Enables identification of influential works

### Open Access Tagging
- Papers tagged as open access or closed access
- Open access papers can be downloaded directly via PDF links
- Visual indicators (icons) distinguish access types

### Publication Metadata Enhancement
- Year of publication enhanced with month information
- Enables temporal analysis of research trends
- Supports chronological browsing

### Icon System
- Comprehensive icon set for academic services (27 different services)
- Dark/light mode support for all icons
- Consistent 16x16 pixel SVG format
- Organized in separate directories (`dm/` and `wm/`)

### Figure Assets
- 3,173 SVG figure files stored in `fig/` subdirectory
- Likely contains citation network graphs and metrics visualizations
- Referenced in entries via `<img>` tags

### Future Features (Not Yet Implemented)
According to README:
- University ROR tagging (upcoming)
- Semantic weight for citations (upcoming)
- Community detection for related works (upcoming)
- Note: Graphs for latest publications are missing due to GitHub size limitations

## Technical Notes

### Markdown Format
- Uses HTML extensively within markdown files
- `<picture>` tags for responsive icon display
- `<details>` tags for collapsible abstracts
- Anchor links for internal navigation

### File Sizes
- Individual markdown files range from small (7.2 KB) to very large (2.0 MB)
- Largest file: `2024-09.md` (2.0 MB, 305 entries)
- Recent files (2025-05.md) are substantial (514 KB, 1655 lines)

### BibTeX Integration
- All entries have corresponding BibTeX entries in `dat/3dcp.fyi.bib`
- BibTeX links point to specific line ranges in the BibTeX file
- Enables citation management and export

## Conclusion

The 3dcp.fyi repository represents a meticulously curated, comprehensive database of 3D concrete printing research spanning nearly three decades. The structure demonstrates careful attention to:
- Data quality through manual curation
- Researcher identification via ORCID
- Accessibility through open access tagging
- Integration with academic services
- User experience through responsive design (dark/light mode)
- Citation network analysis capabilities

The project serves as both a research database and a citation network analysis tool, making it a valuable resource for the 3D concrete printing research community.

