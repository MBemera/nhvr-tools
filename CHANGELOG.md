# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-03-09

### Fixed

- Scraper bot detection — Playwright now uses real browser user agent, viewport, and anti-detection settings
- HTTP fallback scraper now sends proper browser headers
- All 12 SDK methods fully functional including `search()` and `scrape()`

### Changed

- Minimal base dependencies (httpx, beautifulsoup4 only) — MCP, CLI, and scraper are optional extras
- Improved README with install badges, CI status, and PyPI links

## [0.1.0] - 2025-03-09

### Added

- Python SDK (`NHVR` client class) with sync and async methods
- MCP server with 12 tools for AI assistant integration
- CLI with full command coverage
- Built-in knowledge base: fatigue rules, mass limits, dimension limits, breach categories, speed limits, chain of responsibility, accreditation, permit types, HML info
- Vehicle registration lookup via NHVR public API
- NHVR website scraper with topic-specific parsers
- Setup wizard for non-technical users
- Docker support
