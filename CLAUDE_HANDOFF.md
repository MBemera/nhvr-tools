# NHVR MCP Handoff for Claude

## Summary
We scaffolded the NHVR MCP server + CLI and began implementing targeted scrapers.

## Repo Location
`/Users/brighthome/Desktop/NHVR MCP/nhvr-tools`

## Current Status
**All core parsers and knowledge base implemented.**

**Completed**
- MCP server with 12 tool endpoints wired (`nhvr_mcp/server.py`)
- CLI commands mirroring tools (`nhvr_mcp/cli.py`)
- API client for vehicle registration (`nhvr_mcp/api_client.py`)
- Scraper core with Playwright + BeautifulSoup (`nhvr_mcp/scraper.py`)
- Smart search routing for all topics (`nhvr_mcp/tools.py`)
- Dedicated section parsers for all major topics (`nhvr_mcp/section_parsers.py`)
- Knowledge base populated with real NHVR data (`nhvr_mcp/knowledge.py`)
- Recursive markdown formatter for nested data (`nhvr_mcp/formatters.py`)
- 26 tests passing

## Key Files
- `nhvr_mcp/tools.py`: MCP tool logic + search routing (all topics routed to dedicated scrapers)
- `nhvr_mcp/scraper.py`: HTTP + Playwright fetch and parsing helpers (9 scraper functions)
- `nhvr_mcp/section_parsers.py`: Parsers for all topics with h2/h3 extraction
- `nhvr_mcp/knowledge.py`: Authoritative NHVR data (fatigue, mass, dimension, CoR, breach, speed, NHVAS, permits, HML)
- `nhvr_mcp/formatters.py`: Recursive markdown/JSON formatter
- `tests/`: 26 tests across 7 test files

## Implemented Parsers (section_parsers.py)
- `parse_dimension_requirements` → DimensionRequirements
- `parse_mass_limits` → MassLimits
- `parse_cor_duties` → CorDuties (with sub-page fetching)
- `parse_cor_sub_page` → dict (for CoR sub-pages)
- `parse_fatigue_management` → FatigueManagement (with h2+h3 sub-sections)
- `parse_breach_categorisation` → BreachCategorisation (with h2+h3 sub-sections)
- `parse_speed_limits` → SpeedLimits
- `parse_nhvas_info` → NhvasInfo
- `parse_permit_types` → PermitTypes

## Scraper Functions (scraper.py)
- `scrape_dimension_requirements`
- `scrape_mass_limits`
- `scrape_cor_duties` (fetches main + 3 sub-pages)
- `scrape_fatigue_management`
- `scrape_breach_categorisation`
- `scrape_speed_limits`
- `scrape_nhvas_info`
- `scrape_permit_types`
- `scrape_nhvr_page` (generic fallback)

## Search Routing (tools.py)
All topics routed to dedicated scrapers:
- `dimension` → `scrape_dimension_requirements`
- `mass` → `scrape_mass_limits`
- `cor` / `chain of responsibility` → `scrape_cor_duties`
- `fatigue` / `work rest` / `work diary` → `scrape_fatigue_management`
- `breach` → `scrape_breach_categorisation`
- `speed` → `scrape_speed_limits`
- `nhvas` → `scrape_nhvas_info`
- `permits` → `scrape_permit_types`
- `pbs` / `hvnl` → generic scrape (no dedicated parser yet)

## Tests
Run: `pytest -q nhvr-tools/tests` (26 tests)

## Dependencies
- `beautifulsoup4`
- `playwright`

## Possible Future Work
- PBS (Performance Based Standards) dedicated parser
- HVNL dedicated parser
- Table extraction (some NHVR pages have data tables for fatigue/breach breakpoints)
- Sub-page crawling for fatigue work diary and counting time pages
- Integration tests with live NHVR website
