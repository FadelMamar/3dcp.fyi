# Keyword Search Implementation Strategy for 3dcp.fyi (Python)

## Overview

This document outlines a progressive strategy to implement keyword search functionality for the 3dcp.fyi static site using **Python** as the programming language. The database contains ~4,000 scientific works across 164 markdown files, each containing structured bibliographic entries with titles, authors, abstracts, and metadata.

## Current State Analysis

- **Data Format**: Markdown files in `dat/md/` directory (YYYY-MM.md format)
- **Entry Structure**: Each entry includes:
  - Unique anchor ID (e.g., `ahadvali2025ZRMf3CP`)
  - Paper title with publication date
  - Author names with ORCID links
  - Publication metadata (journal/conference, volume, pages)
  - Collapsible abstract in `<details>` tags
  - Academic service links
- **Site Type**: Static site (likely GitHub Pages)
- **Data Volume**: ~4,000 entries, largest file 2.0 MB (2024-09.md)
- **Programming Language**: Python (as specified)

## Implementation Strategy: Simple to Robust

### Level 1: Python-Based Index Generation with Simple Client-Side Search

**Complexity**: Low | **Implementation Time**: 2-3 hours | **Performance**: Good for <5,000 entries

**Approach**: 
- Python script parses all markdown files
- Generates JSON index file
- Client-side JavaScript performs simple string matching
- No Python server required for search (static HTML)

**Implementation Plan**:

**Files to Create**:
```
scripts/
├── build_search_index.py          # Main Python script to parse markdown and generate JSON index
└── parser/
    ├── __init__.py
    ├── markdown_parser.py         # Markdown file parsing logic
    └── entry_extractor.py         # Entry data extraction logic

dat/
└── search-index.json              # Generated JSON index (~5MB)

search.html                        # Static HTML search page
js/
└── search.js                      # Client-side search JavaScript (uses generated JSON)
```

**Python Script Structure** (`scripts/build_search_index.py`):
- Use `pathlib` for file operations
- Use `re` (regex) for parsing HTML/markdown patterns
- Use `json` for output
- Parse markdown files from `dat/md/` directory
- Extract: ID, title, authors, abstract, publication date, venue, DOI
- Generate `dat/search-index.json` with all entries
- Include searchable text field (combined title, authors, abstract, venue)

**Key Functions**:
- `parse_markdown_file(file_path)` - Parse single markdown file
- `extract_entry_data(content)` - Extract entry from markdown content
- `extract_title(line)` - Extract title from h3 heading
- `extract_authors(lines)` - Extract author names
- `extract_abstract(lines)` - Extract abstract from details tag
- `extract_publication_metadata(line)` - Extract publication info
- `build_index()` - Main function to process all files

**Dependencies**:
- Python 3.8+ (stdlib only - no external packages)

**Usage**:
```bash
python scripts/build_search_index.py
# Generates dat/search-index.json
# Then serve search.html via static web server
```

**Pros**:
- Pure Python (stdlib only)
- Fast index generation
- Works with static hosting
- No server required for search

**Cons**:
- Client-side search is basic (no stemming, no fuzzy matching)
- Requires full JSON index to be loaded (~5MB)

---

### Alternative: MkDocs with Built-in Search

**Complexity**: Low-Medium | **Implementation Time**: 3-5 hours | **Performance**: Good for <10,000 entries

**Approach**:
- Use MkDocs static site generator to convert markdown files into a searchable documentation site
- Leverage MkDocs' built-in search plugin (uses Lunr.js for client-side full-text search)
- Python script reorganizes markdown files into MkDocs structure
- Generate static site with integrated search functionality
- No custom JavaScript required - search is built into MkDocs themes

**How MkDocs Search Works**:
- **Search Plugin**: Built-in plugin uses Lunr.js (JavaScript full-text search library)
- **Client-Side Indexing**: Search index is generated at build time and embedded in the static site
- **Full-Text Search**: Searches across page titles, headings, and content
- **Relevance Ranking**: Results ranked by relevance score
- **No Server Required**: Fully static, works with GitHub Pages and any static hosting

**Implementation Plan**:

**Files to Create**:
```
mkdocs.yml                          # MkDocs configuration file
docs/                               # MkDocs documentation directory
├── index.md                        # Homepage
├── papers/                         # Papers organized by year/month
│   ├── 2024/
│   │   ├── 08.md                  # Converted from dat/md/2024-08.md
│   │   └── 09.md
│   └── 2025/
│       └── 05.md
└── search/                         # Optional: dedicated search page

scripts/
└── convert_to_mkdocs.py           # Python script to reorganize markdown files
```

**MkDocs Configuration** (`mkdocs.yml`):
- Enable search plugin (enabled by default)
- Configure navigation structure
- Set theme (default `mkdocs` or `readthedocs` theme)
- Configure site metadata
- Set up navigation menu structure

**Python Script Structure** (`scripts/convert_to_mkdocs.py`):
- Parse markdown files from `dat/md/` directory
- Extract entry structure (preserve anchors, titles, authors, abstracts)
- Reorganize into MkDocs `docs/` directory structure
- Option 1: Keep chronological organization (papers/YYYY/MM.md)
- Option 2: Create individual pages per entry (papers/YYYY/MM/entry-id.md)
- Generate `mkdocs.yml` navigation structure
- Preserve HTML formatting (icons, links, details tags)

**Key Considerations**:
- **File Organization**: Decide whether to keep one file per month or split into individual pages
- **Navigation Structure**: Create logical navigation menu (by year, by topic, etc.)
- **Entry Formatting**: MkDocs supports HTML in markdown, so existing formatting should work
- **Search Index Size**: Lunr.js index is generated at build time and embedded in site
- **Performance**: Client-side search works well for <10,000 pages; index size grows with content

**Dependencies**:
- `mkdocs>=1.5.0` - Static site generator
- Python 3.8+ (stdlib for conversion script)

**Usage**:
```bash
# Install MkDocs
pip install mkdocs

# Convert markdown files to MkDocs structure
python scripts/convert_to_mkdocs.py

# Build static site
mkdocs build

# Serve locally for testing
mkdocs serve

# Deploy to GitHub Pages
mkdocs gh-deploy
```

**Search Features**:
- Full-text search across all pages
- Relevance ranking
- Search highlights in results
- Search bar in navigation (theme-dependent)
- No server-side processing required

**Pros**:
- Built-in search functionality (no custom implementation)
- Professional documentation site appearance
- Easy navigation structure
- Works with static hosting (GitHub Pages compatible)
- Full-text search with relevance ranking
- No additional JavaScript libraries to maintain
- Active community and well-documented

**Cons**:
- Requires restructuring markdown files into MkDocs format
- Search index embedded in site (adds to page load)
- Less control over search behavior compared to custom solutions
- May need theme customization to match existing site design
- Client-side search performance degrades with very large sites (>10,000 pages)

**Integration with Existing Site**:
- Option A: Replace existing static site with MkDocs-generated site
- Option B: Use MkDocs for search functionality only, embed in existing site
- Option C: Generate MkDocs site alongside existing site, link between them

**Example MkDocs Structure for 3dcp.fyi**:
- Homepage: Overview of database
- Navigation by year: 1997-2025
- Navigation by month within each year
- Search page: Dedicated search interface
- Each paper entry as a page or section within monthly pages

**Comparison to Level 1**:
- **Similarities**: Both are static, client-side search solutions
- **Differences**: 
  - MkDocs provides full documentation site framework
  - MkDocs search uses Lunr.js (more advanced than simple string matching)
  - MkDocs requires file reorganization
  - MkDocs provides navigation structure automatically

---

### Level 2: Python with Whoosh Full-Text Search Engine

**Complexity**: Medium | **Implementation Time**: 4-6 hours | **Performance**: Excellent for <10,000 entries

**Approach**:
- Python script uses Whoosh library for full-text indexing
- Generate Whoosh index directory
- Python script serves search API (Flask/FastAPI) OR generates static search page
- Whoosh provides relevance ranking, stemming, and full-text search

**Implementation Plan**:

**Option A: Python API Server (Recommended)**:
```
scripts/
├── build_whoosh_index.py          # Build Whoosh index from markdown files
└── api/
    ├── __init__.py
    ├── search_api.py              # Flask/FastAPI search endpoint
    └── config.py                  # API configuration

dat/
└── whoosh_index/                  # Whoosh index directory (generated)

requirements.txt                   # Python dependencies

api_server.py                      # Main API server script
```

**Option B: Static Search with Pre-built Index**:
```
scripts/
├── build_whoosh_index.py          # Build Whoosh index
└── build_static_search.py         # Generate static HTML with embedded search

dat/
└── whoosh_index/                  # Whoosh index (client-side via Pyodide?)

search-whoosh.html                 # Static search page
```

**Python Script Structure** (`scripts/build_whoosh_index.py`):
- Use `whoosh` library for indexing
- Define schema: title, authors, abstract, venue, year, publication_type
- Set field boosts: title (10x), authors (5x), venue (2x), abstract (1x)
- Index all entries from markdown files
- Save index to `dat/whoosh_index/`

**Search API** (`api/search_api.py`):
- Flask or FastAPI endpoint: `/api/search?q=<query>`
- Use Whoosh index to perform searches
- Return JSON results with relevance scores
- Support pagination, filtering by year/venue/author

**Dependencies**:
- `whoosh>=2.7.4` - Full-text search library
- `flask>=2.0.0` OR `fastapi>=0.68.0` - Web framework (for API server)

**Usage (API Server)**:
```bash
# Build index
python scripts/build_whoosh_index.py

# Start API server
python api_server.py

# Search via API: http://localhost:5000/api/search?q=rheology
```

**Usage (Static)**:
```bash
# Build index and generate static search page
python scripts/build_whoosh_index.py
python scripts/build_static_search.py

# Serve static files
```

**Pros**:
- Full-text search with relevance ranking
- Stemming support (English)
- Field boosting (title matches rank higher)
- Python-native solution
- Can serve as API or generate static pages

**Cons**:
- Requires Whoosh library
- API server requires hosting (or use static generation)
- Index generation takes more time

---

### Level 3: Python with Fuzzy Matching and Advanced Features

**Complexity**: Medium-High | **Implementation Time**: 8-12 hours | **Performance**: Excellent

**Approach**:
- Extend Level 2 with fuzzy matching capabilities
- Use Whoosh's fuzzy search OR integrate RapidFuzz/Levenshtein
- Add advanced filtering (year, venue, author)
- Add autocomplete/suggestions
- Enhanced search API or static generation

**Implementation Plan**:

**Files to Create**:
```
scripts/
├── build_advanced_index.py        # Build enhanced index with metadata
└── api/
    ├── search_api.py              # Enhanced search API with filters
    ├── autocomplete.py            # Autocomplete endpoint
    └── filters.py                 # Filter utilities

dat/
├── whoosh_index/                  # Whoosh index
└── search-metadata.json           # Metadata for filtering (venues, authors, years)

requirements.txt                   # Python dependencies

api_server.py                      # Enhanced API server
```

**Python Script Structure** (`scripts/build_advanced_index.py`):
- Build Whoosh index (same as Level 2)
- Extract metadata: unique venues, authors, years
- Generate `search-metadata.json` for filter dropdowns
- Store fuzzy matching configuration

**Enhanced Search API** (`api/search_api.py`):
- Fuzzy search using Whoosh's fuzzy queries OR RapidFuzz
- Filter endpoints: `/api/filter?year=2024&venue=...&author=...`
- Autocomplete: `/api/autocomplete?q=concre`
- Combined search: `/api/search?q=...&year=2024&venue=...`

**Fuzzy Matching Options**:
1. **Whoosh Fuzzy Terms**: `whoosh.query.FuzzyTerm`
2. **RapidFuzz**: Fast fuzzy string matching
   - `rapidfuzz>=2.0.0`
   - Calculate similarity scores
   - Post-filter results by similarity threshold
3. **Levenshtein**: Edit distance calculation
   - `python-Levenshtein>=0.12.0`

**Dependencies**:
- `whoosh>=2.7.4`
- `rapidfuzz>=2.0.0` OR `python-Levenshtein>=0.12.0` (optional)
- `flask>=2.0.0` OR `fastapi>=0.68.0`
- `ujson>=5.0.0` (optional, faster JSON)

**Pros**:
- Typo tolerance (finds "concrete" when searching "concret")
- Advanced filtering capabilities
- Autocomplete suggestions
- Professional search experience
- Python-native solution

**Cons**:
- More complex implementation
- Requires additional libraries
- API server requires hosting (unless static generation)

---

### Level 4: Python with Flask/FastAPI Web Application

**Complexity**: Medium-High | **Implementation Time**: 12-16 hours | **Performance**: Excellent

**Approach**:
- Full Python web application using Flask or FastAPI
- Serve search interface as web pages
- Search API endpoints
- Admin interface for index management
- Can be deployed as static site generator OR web server

**Implementation Plan**:

**Files to Create**:
```
app/
├── __init__.py
├── main.py                        # Flask/FastAPI app entry point
├── config.py                      # Configuration
├── routes/
│   ├── __init__.py
│   ├── search.py                  # Search routes
│   ├── index.py                   # Index management routes
│   └── api.py                     # API endpoints
├── models/
│   ├── __init__.py
│   └── entry.py                   # Entry data models
├── services/
│   ├── __init__.py
│   ├── search_service.py          # Search logic
│   ├── index_service.py           # Index management
│   └── parser_service.py          # Markdown parsing
└── templates/
    ├── base.html                  # Base template
    ├── search.html                # Search page
    └── results.html               # Results page

scripts/
└── build_index.py                 # Index generation script

requirements.txt                   # Python dependencies

run.py                             # Application runner
```

**Application Structure**:
- **Flask** (simpler) OR **FastAPI** (modern, async, auto-docs)
- Whoosh index loaded at startup
- RESTful API endpoints
- HTML templates for search interface
- Static file serving for assets

**Key Features**:
- Search page with live results
- API endpoints: `/api/v1/search`, `/api/v1/filters`, `/api/v1/autocomplete`
- Admin endpoints for index rebuilding (protected)
- Optional: User authentication for admin features
- Optional: Search analytics/logging

**Dependencies (Flask)**:
- `flask>=2.0.0`
- `whoosh>=2.7.4`
- `python-dotenv>=0.19.0` (configuration)

**Dependencies (FastAPI)**:
- `fastapi>=0.68.0`
- `uvicorn>=0.15.0` (ASGI server)
- `whoosh>=2.7.4`
- `jinja2>=3.0.0` (templates)
- `python-dotenv>=0.19.0`

**Usage**:
```bash
# Install dependencies
pip install -r requirements.txt

# Build index
python scripts/build_index.py

# Run application
python run.py

# Or with uvicorn (FastAPI)
uvicorn app.main:app --reload
```

**Pros**:
- Full control over search experience
- Can serve as static site generator
- Can serve as web API
- Admin interface for management
- Python-native end-to-end solution

**Cons**:
- Requires web server hosting (unless static generation)
- More complex than simple scripts
- Deployment considerations

**Static Site Generation Option**:
- Generate static HTML files from templates
- Include pre-built search index
- Deploy as static site (GitHub Pages compatible)

---

### Level 5: Python Integration with Server-Side Search Engines

**Complexity**: High | **Implementation Time**: 20-40 hours | **Performance**: Excellent, Scalable

**Approach**:
- Python scripts/indexing for Meilisearch or Typesense
- Python API wrapper using SDKs
- Index management and synchronization
- Advanced features: faceting, analytics, synonyms

**Implementation Plan**:

#### Option A: Meilisearch with Python

**Files to Create**:
```
scripts/
├── index_meilisearch.py           # Index entries to Meilisearch
└── sync_meilisearch.py            # Sync/update index

api/
├── meilisearch_client.py          # Meilisearch client wrapper
└── search_api.py                  # Search API using Meilisearch

requirements.txt                   # Python dependencies
```

**Python Script Structure** (`scripts/index_meilisearch.py`):
- Use `meilisearch-python-sdk` library
- Connect to Meilisearch instance (local or cloud)
- Configure searchable attributes and ranking rules
- Index all entries from markdown files
- Set up synonyms, filters, faceting

**Dependencies**:
- `meilisearch>=0.19.0` - Meilisearch Python SDK
- `flask>=2.0.0` OR `fastapi>=0.68.0` - Web framework

**Meilisearch Setup**:
```python
from meilisearch import Client

client = Client('http://localhost:7700', 'masterKey')
index = client.index('papers')

# Configure searchable attributes
index.update_searchable_attributes([
    'title',
    'authors',
    'abstract',
    'venue'
])

# Configure ranking rules
index.update_ranking_rules([
    'words',
    'typo',
    'proximity',
    'attribute',
    'sort',
    'exactness'
])
```

**Pros**:
- Best search quality and features
- Highly scalable
- Typo tolerance built-in
- Advanced analytics
- Python SDK available
- Can self-host or use cloud

**Cons**:
- Requires Meilisearch server
- Ongoing maintenance
- Hosting costs (or self-hosting setup)

#### Option B: Typesense with Python

**Files to Create**:
```
scripts/
├── index_typesense.py             # Index entries to Typesense
└── sync_typesense.py              # Sync/update index

api/
├── typesense_client.py            # Typesense client wrapper
└── search_api.py                  # Search API using Typesense

requirements.txt                   # Python dependencies
```

**Python Script Structure** (`scripts/index_typesense.py`):
- Use `typesense` library
- Connect to Typesense server (local or cloud)
- Define collection schema
- Index all entries

**Dependencies**:
- `typesense>=0.15.0` - Typesense Python client
- `flask>=2.0.0` OR `fastapi>=0.68.0` - Web framework

**Pros**:
- Open-source, typo-tolerant
- Fast and simple API
- Self-hosted or cloud options
- Python SDK available

**Cons**:
- Requires Typesense server
- Ongoing maintenance
- Hosting considerations

#### Option C: Elasticsearch with Python

**Files to Create**:
```
scripts/
├── index_elasticsearch.py         # Index entries to Elasticsearch
└── sync_elasticsearch.py          # Sync/update index

api/
├── elasticsearch_client.py        # Elasticsearch client wrapper
└── search_api.py                  # Search API using Elasticsearch

requirements.txt                   # Python dependencies
```

**Python Script Structure** (`scripts/index_elasticsearch.py`):
- Use `elasticsearch` library
- Connect to Elasticsearch cluster
- Create index with mapping
- Index all entries using bulk API

**Dependencies**:
- `elasticsearch>=8.0.0` - Elasticsearch Python client
- `flask>=2.0.0` OR `fastapi>=0.68.0` - Web framework

**Pros**:
- Most powerful and flexible
- Industry standard
- Very scalable
- Advanced features

**Cons**:
- Complex setup and maintenance
- Resource-intensive
- Steep learning curve
- May be overkill for this use case

---

## Recommended Implementation Path

**Phase 1 (Quick Win)**: Choose one of the following static approaches:
- **Option A - Level 1**: Python index generation with simple client-side search
  - Python script parses markdown and generates JSON index
  - Client-side JavaScript performs search (static HTML)
  - Minimal dependencies (Python stdlib only)
  - Works with static hosting (GitHub Pages)
  - Can be enhanced later
- **Option B - MkDocs**: Use MkDocs with built-in search
  - Leverage existing static site generator with Lunr.js search
  - Requires file reorganization but provides full documentation framework
  - Built-in navigation and professional appearance
  - Full-text search with relevance ranking out of the box
  - Good choice if you want a complete documentation site solution

**Phase 2 (Enhanced)**: Upgrade to Level 2 - Whoosh full-text search
- Better search quality with relevance ranking
- Python API server OR static generation
- Full-text indexing with stemming
- Good balance of features vs. complexity

**Phase 3 (Advanced)**: Add Level 3 - Fuzzy matching and filters
- Typo tolerance
- Advanced filtering
- Autocomplete suggestions
- Professional search experience

**Phase 4 (Full Web App)**: Consider Level 4 - Flask/FastAPI application
- Full control over search experience
- Can serve as static site generator or web server
- Admin interface for index management
- More deployment flexibility

**Phase 5 (Future)**: Level 5 - Server-side engines only if:
- Site grows beyond 10,000+ entries
- Need advanced analytics
- Require real-time updates
- Have infrastructure resources

---

## Technical Considerations

### Index Build Process
- Python scripts should be idempotent (can run multiple times safely)
- Consider GitHub Actions for automated index generation
- Index file size: ~5MB for 4,000 entries (JSON) or ~10-20MB (Whoosh directory)

### Search Fields Priority
1. **Title** (highest weight) - Most important for finding papers
2. **Authors** (high weight) - Important for author searches
3. **Abstract** (medium weight) - Provides context
4. **Journal/Conference** (low weight) - Useful for filtering

### Python Version
- Minimum: Python 3.8+
- Recommended: Python 3.10+
- Use type hints for better code quality
- Consider using `dataclasses` or `pydantic` for entry models

### Dependencies Management
- Use `requirements.txt` for pip
- Consider `pyproject.toml` with Poetry or pip-tools
- Pin versions for reproducibility
- Separate dev and production dependencies

### Deployment Options

**Static Hosting** (Levels 1-3 with static generation):
- GitHub Pages
- Netlify
- Vercel
- Any static file host

**Web Server** (Levels 2-5):
- Heroku
- Railway
- Render
- DigitalOcean App Platform
- AWS/GCP/Azure
- Self-hosted (VPS, Docker)

**Static Site Generation** (Level 4):
- Generate static HTML from Flask/FastAPI templates
- Include pre-built search index
- Deploy as static site
- Best of both worlds

---

## File Structure (Proposed)

```
3dcp.fyi/
├── scripts/
│   ├── build_search_index.py      # Level 1: Simple JSON index
│   ├── build_whoosh_index.py      # Level 2: Whoosh index
│   ├── build_advanced_index.py    # Level 3: Advanced index
│   └── parser/
│       ├── __init__.py
│       ├── markdown_parser.py
│       └── entry_extractor.py
├── app/                            # Level 4: Web application
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── routes/
│   ├── models/
│   ├── services/
│   └── templates/
├── api/                            # Level 5: API integration
│   ├── meilisearch_client.py
│   ├── typesense_client.py
│   └── search_api.py
├── dat/
│   ├── search-index.json          # Level 1 index
│   ├── whoosh_index/              # Level 2+ index
│   └── search-metadata.json       # Level 3+ metadata
├── search.html                     # Level 1: Static search page
├── js/
│   └── search.js                  # Level 1: Client-side search
├── requirements.txt                # Python dependencies
├── run.py                          # Application runner (Level 4+)
└── DEV.md                          # This file
```

---

## Next Steps

1. **Review this plan** - Confirm approach and priorities
2. **Set up Python environment** - Create virtual environment
3. **Start with Level 1** - Implement simple index generation
4. **Test parsing** - Verify markdown parsing with sample files
5. **Generate index** - Build initial JSON index
6. **Create search UI** - Static HTML + JavaScript client
7. **Test search** - Verify search functionality
8. **Iterate** - Move to Level 2+ based on needs

---

## References and Resources

### Python Libraries
- **Whoosh**: https://whoosh.readthedocs.io/
- **RapidFuzz**: https://github.com/maxbachmann/rapidfuzz
- **Meilisearch Python SDK**: https://github.com/meilisearch/meilisearch-python
- **Typesense Python Client**: https://github.com/typesense/typesense-python
- **Elasticsearch Python Client**: https://github.com/elastic/elasticsearch-py

### Web Frameworks
- **Flask**: https://flask.palletsprojects.com/
- **FastAPI**: https://fastapi.tiangolo.com/

### Static Site Generation
- **Pelican**: https://getpelican.com/
- **MkDocs**: https://www.mkdocs.org/
  - **MkDocs Search Plugin**: Built-in search using Lunr.js (client-side full-text search)
  - **MkDocs Documentation**: https://www.mkdocs.org/user-guide/configuration/#plugins
  - **Lunr.js**: https://lunrjs.com/ (JavaScript full-text search library used by MkDocs)

### Deployment
- **GitHub Actions**: https://docs.github.com/en/actions
- **Docker**: https://www.docker.com/
- **Poetry**: https://python-poetry.org/ (dependency management)

---

This plan provides a comprehensive roadmap for implementing keyword search using Python, progressing from simple static solutions to advanced server-side search engines.

