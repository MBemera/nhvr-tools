"""NHVR Python SDK for programmatic access to heavy vehicle compliance data."""

from __future__ import annotations

import os

from nhvr_mcp.knowledge import (
    ACCREDITATION_INFO,
    BREACH_CATEGORIES,
    COR_DUTIES,
    DIMENSION_LIMITS,
    FATIGUE_RULES,
    HML_INFO,
    MASS_LIMITS,
    PERMIT_TYPES,
    SPEED_LIMITS,
)


class NHVR:
    """Client for querying NHVR heavy vehicle compliance data.

    Sync methods return dicts from the built-in knowledge base.
    Async methods (search_registration, search, scrape) require ``await``.
    """

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("NHVR_API_KEY")

    # -- Sync knowledge-base lookups --

    def fatigue_rules(self, scheme: str = "standard") -> dict:
        return FATIGUE_RULES.get(scheme, {"error": f"Unknown scheme: {scheme}"})

    def mass_limits(self, include_hml: bool = False) -> dict:
        data: dict = {"general": MASS_LIMITS["general"]}
        if include_hml:
            data["hml"] = MASS_LIMITS["hml"]
        return data

    def dimension_limits(self) -> dict:
        return dict(DIMENSION_LIMITS)

    def breach_categories(self, breach_type: str | None = None) -> dict:
        if breach_type:
            return {breach_type: BREACH_CATEGORIES.get(breach_type, f"Unknown breach type: {breach_type}")}
        return dict(BREACH_CATEGORIES)

    def speed_limits(self) -> dict:
        return dict(SPEED_LIMITS)

    def cor_duties(self, role: str | None = None) -> dict:
        if role:
            return {role: COR_DUTIES.get(role, f"Unknown role: {role}")}
        return dict(COR_DUTIES)

    def accreditation(self, module: str | None = None) -> dict:
        if module:
            return {module: ACCREDITATION_INFO.get(module, f"Unknown module: {module}")}
        return dict(ACCREDITATION_INFO)

    def permit_types(self, permit_type: str | None = None) -> dict:
        if permit_type:
            return {permit_type: PERMIT_TYPES.get(permit_type, f"Unknown permit type: {permit_type}")}
        return dict(PERMIT_TYPES)

    def hml_info(self) -> dict:
        return dict(HML_INFO)

    # -- Async methods (network) --

    async def search_registration(self, plate_number: str) -> dict:
        from nhvr_mcp.api_client import NhvrApiClient

        client = NhvrApiClient()
        if self.api_key:
            client.api_key = self.api_key
        return await client.search_vehicle_registration(plate_number)

    async def search(self, query: str) -> dict:
        from nhvr_mcp.scraper import scrape_nhvr_page

        normalized = query.lower().strip()
        topic_map = {
            "work rest": "https://www.nhvr.gov.au/safety-accreditation-compliance/fatigue-management/work-and-rest-requirements",
            "fatigue": "https://www.nhvr.gov.au/safety-accreditation-compliance/fatigue-management",
            "work diary": "https://www.nhvr.gov.au/safety-accreditation-compliance/fatigue-management/work-diary",
            "mass": "https://www.nhvr.gov.au/road-access/mass-and-dimension/mass-limits",
            "dimension": "https://www.nhvr.gov.au/road-access/mass-and-dimension/dimension-requirements",
            "chain of responsibility": "https://www.nhvr.gov.au/safety-accreditation-compliance/chain-of-responsibility",
            "cor": "https://www.nhvr.gov.au/safety-accreditation-compliance/chain-of-responsibility",
            "nhvas": "https://www.nhvr.gov.au/safety-accreditation-compliance/national-heavy-vehicle-accreditation-scheme",
            "permits": "https://www.nhvr.gov.au/road-access/access-permits",
            "pbs": "https://www.nhvr.gov.au/road-access/performance-based-standards",
            "hvnl": "https://www.nhvr.gov.au/law-policies/heavy-vehicle-national-law-and-regulations",
            "breach": "https://www.nhvr.gov.au/safety-accreditation-compliance/on-road-compliance-and-enforcement/breach-categorisation",
            "speed": "https://www.nhvr.gov.au/safety-accreditation-compliance/on-road-compliance-and-enforcement/speeding",
        }
        dedicated_scrapers = {
            "dimension": "scrape_dimension_requirements",
            "mass": "scrape_mass_limits",
            "chain of responsibility": "scrape_cor_duties",
            "cor": "scrape_cor_duties",
            "work rest": "scrape_fatigue_management",
            "fatigue": "scrape_fatigue_management",
            "work diary": "scrape_fatigue_management",
            "breach": "scrape_breach_categorisation",
            "speed": "scrape_speed_limits",
            "nhvas": "scrape_nhvas_info",
            "permits": "scrape_permit_types",
            "pbs": None,
            "hvnl": None,
        }

        for key, url in topic_map.items():
            if key in normalized:
                scraper_name = dedicated_scrapers.get(key)
                if scraper_name:
                    import nhvr_mcp.scraper as scraper_module

                    scraper_fn = getattr(scraper_module, scraper_name)
                    parsed = await scraper_fn(url, use_playwright=True)
                    return {"query": query, "matched_topic": key, "url": url, **parsed}

                page = await scrape_nhvr_page(url, use_playwright=True)
                return {
                    "query": query,
                    "matched_topic": key,
                    "url": page.url,
                    "title": page.title,
                    "text": page.text[:2000],
                }

        return {"query": query, "message": "No topic match. Provide a full NHVR URL to scrape()."}

    async def scrape(self, url: str) -> dict:
        from nhvr_mcp.scraper import is_nhvr_url, scrape_nhvr_page

        if not is_nhvr_url(url):
            return {"error": "URL must be on nhvr.gov.au."}

        page = await scrape_nhvr_page(url, use_playwright=True)
        return {
            "url": page.url,
            "title": page.title,
            "text": page.text[:2000],
            "tables": page.tables[:5],
            "links": page.links[:20],
        }
