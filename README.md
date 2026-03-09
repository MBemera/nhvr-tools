# NHVR Tools

> Python SDK, MCP server, and CLI for Australian heavy vehicle compliance data.

[![PyPI version](https://img.shields.io/pypi/v/nhvr-tools.svg)](https://pypi.org/project/nhvr-tools/)
[![Python](https://img.shields.io/pypi/pyversions/nhvr-tools.svg)](https://pypi.org/project/nhvr-tools/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

NHVR Tools gives you instant access to Australian heavy vehicle compliance information — fatigue rules, mass limits, dimension limits, breach categories, chain of responsibility duties, accreditation, permits, and more.

**Three ways to use it:**

| Interface | For | Install |
|-----------|-----|---------|
| **Python SDK** | Developers building apps | `pip install nhvr-tools` |
| **MCP Server** | AI assistants (Claude, etc.) | `pip install nhvr-tools[mcp]` |
| **CLI** | Terminal users | `pip install nhvr-tools[cli]` |

---

## Quick Start

### Install

```bash
# SDK only (minimal dependencies)
pip install nhvr-tools

# Everything (SDK + MCP server + CLI + scraper)
pip install nhvr-tools[all]
```

### Python SDK

```python
from nhvr_mcp import NHVR

client = NHVR()

# Fatigue rules
rules = client.fatigue_rules(scheme="standard")
print(rules["solo_driver"])

# Mass limits (with HML)
limits = client.mass_limits(include_hml=True)
print(limits["hml"]["b_double_gross"])  # "Up to 62.5 t"

# Dimension limits
dims = client.dimension_limits()
print(dims["height"])  # "4.3 m maximum ..."

# Breach categories
breaches = client.breach_categories(breach_type="mass")

# Chain of Responsibility
cor = client.cor_duties(role="operator")

# All other lookups
speed = client.speed_limits()
accred = client.accreditation(module="mass")
permits = client.permit_types(permit_type="class_1")
hml = client.hml_info()
```

#### Async Methods (Network)

```python
import asyncio
from nhvr_mcp import NHVR

client = NHVR(api_key="your-nhvr-api-key")  # or set NHVR_API_KEY env var

# Vehicle registration lookup
rego = asyncio.run(client.search_registration("ABC123"))

# Search NHVR regulations (scrapes nhvr.gov.au)
results = asyncio.run(client.search("fatigue management"))

# Scrape a specific NHVR page
page = asyncio.run(client.scrape("https://www.nhvr.gov.au/road-access/mass-and-dimension/mass-limits"))
```

---

## API Reference

### `NHVR(api_key=None)`

Create a client. The API key is optional — only needed for vehicle registration lookups. Falls back to the `NHVR_API_KEY` environment variable.

### Sync Methods

All sync methods return Python dicts from the built-in knowledge base. No network calls, no API key required.

| Method | Parameters | Returns |
|--------|-----------|---------|
| `fatigue_rules(scheme)` | `scheme`: `"standard"`, `"bfm"`, or `"afm"` | Fatigue work/rest rules |
| `mass_limits(include_hml)` | `include_hml`: bool (default `False`) | General + optional HML limits |
| `dimension_limits()` | — | Height, width, length limits |
| `breach_categories(breach_type)` | `breach_type`: `"mass"`, `"dimension"`, `"fatigue"`, `"speed"`, `"loading"`, or `None` for all | Breach severity categories |
| `speed_limits()` | — | Speed limits and limiter rules |
| `cor_duties(role)` | `role`: `"operator"`, `"driver"`, `"primary_duty"`, etc. or `None` for all | Chain of Responsibility duties |
| `accreditation(module)` | `module`: `"mass"`, `"maintenance"`, `"fatigue"`, or `None` for all | NHVAS accreditation info |
| `permit_types(permit_type)` | `permit_type`: `"class_1"`, `"class_2"`, `"class_3"`, `"hml"`, `"oversize"`, or `None` for all | Access permit information |
| `hml_info()` | — | Higher Mass Limits eligibility, limits, application |

### Async Methods

These methods make network requests and must be `await`ed.

| Method | Parameters | Returns |
|--------|-----------|---------|
| `search_registration(plate_number)` | `plate_number`: str | Vehicle registration data from NHVR API |
| `search(query)` | `query`: str (e.g. `"fatigue"`, `"mass"`, `"cor"`) | Scraped NHVR page matching the topic |
| `scrape(url)` | `url`: str (must be nhvr.gov.au) | Parsed page content (text, tables, links) |

---

## MCP Server (for AI Assistants)

### Easy Setup

```bash
pip install nhvr-tools[mcp]
python setup.py
```

The setup wizard handles everything — installs dependencies, configures Claude Desktop, and verifies the server works.

### Manual Setup

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "nhvr-tools": {
      "command": "python3",
      "args": ["/path/to/nhvr-tools/nhvr_mcp/server.py"]
    }
  }
}
```

### Run Standalone

```bash
# stdio (default, for Claude Desktop)
python -m nhvr_mcp.server

# HTTP (for remote/web clients)
NHVR_MCP_TRANSPORT=streamable_http NHVR_MCP_PORT=8080 python -m nhvr_mcp.server
```

### Available MCP Tools

| Tool | Description |
|------|-------------|
| `nhvr_get_fatigue_rules` | Work/rest hour requirements by scheme |
| `nhvr_get_mass_limits` | General and HML mass limits |
| `nhvr_get_dimension_limits` | Vehicle height, width, length limits |
| `nhvr_get_breach_categories` | Breach severity categories |
| `nhvr_get_speed_limits` | Speed limits and speed limiter rules |
| `nhvr_get_cor_duties` | Chain of Responsibility duties |
| `nhvr_get_accreditation_info` | NHVAS accreditation modules |
| `nhvr_get_permit_types` | Access permit types |
| `nhvr_get_hml_info` | Higher Mass Limits info |
| `nhvr_search_vehicle_registration` | Look up a vehicle by plate number |
| `nhvr_search_regulations` | Search NHVR topics by keyword |
| `nhvr_scrape_page` | Scrape any nhvr.gov.au page |

### Example Questions for Claude

- "What are the standard fatigue rules for heavy vehicle drivers?"
- "What are the mass limits for a B-double?"
- "Explain chain of responsibility duties for a consignor"
- "What are the breach categories for mass offences?"
- "What do I need for NHVAS mass management accreditation?"

---

## CLI

```bash
pip install nhvr-tools[cli]
```

```bash
nhvr fatigue rules                        # Standard fatigue rules
nhvr fatigue rules --scheme bfm           # BFM fatigue rules
nhvr mass limits                          # General mass limits
nhvr mass limits --include-hml            # Include HML
nhvr mass hml                             # HML details
nhvr dimension limits                     # Dimension limits
nhvr breach categories                    # All breach categories
nhvr breach categories --type mass        # Mass breaches only
nhvr speed                                # Speed limits
nhvr cor duties                           # All CoR duties
nhvr cor duties --role operator           # Operator duties
nhvr accreditation                        # All NHVAS modules
nhvr accreditation --module mass          # Mass management
nhvr permits                              # All permit types
nhvr permits --type class_1               # Class 1 permits
nhvr rego ABC123                          # Vehicle registration lookup
nhvr search "fatigue management"          # Search NHVR topics
nhvr scrape "https://www.nhvr.gov.au/..." # Scrape a page

# Output as JSON
nhvr --format json fatigue rules
```

---

## Docker

```bash
docker build -t nhvr-tools .
docker run nhvr-tools
```

---

## Development

```bash
# Clone and install with dev dependencies
git clone https://github.com/MBemera/nhvr-tools.git
cd nhvr-tools
pip install -e ".[dev]"

# Run tests
pytest

# Lint
ruff check .
ruff format .
```

---

## Data Sources

All built-in knowledge base data is sourced from:

- [NHVR website](https://www.nhvr.gov.au/) (nhvr.gov.au)
- [Heavy Vehicle National Law](https://www.nhvr.gov.au/law-policies/heavy-vehicle-national-law-and-regulations) (HVNL)
- [NHVR Developer Portal](https://api-portal.nhvr.gov.au/) (vehicle registration API)

This is an **unofficial** tool. It is not affiliated with or endorsed by the NHVR. Always verify compliance information against official NHVR sources.

---

## License

[MIT](LICENSE)
