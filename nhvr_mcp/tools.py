"""Tool implementations for NHVR MCP."""

from __future__ import annotations

from nhvr_mcp.api_client import NhvrApiClient
from nhvr_mcp.formatters import format_response
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
from nhvr_mcp.scraper import is_nhvr_url, scrape_nhvr_page


def get_fatigue_rules(scheme: str, output_format: str) -> str:
    data = FATIGUE_RULES.get(scheme, {"error": "Unknown scheme."})
    return format_response(data, output_format)


def get_mass_limits(include_hml: bool, output_format: str) -> str:
    data = {"general": MASS_LIMITS["general"]}
    if include_hml:
        data["hml"] = MASS_LIMITS["hml"]
    return format_response(data, output_format)


def get_dimension_limits(output_format: str) -> str:
    return format_response(DIMENSION_LIMITS, output_format)


def get_breach_categories(breach_type: str | None, output_format: str) -> str:
    data = BREACH_CATEGORIES
    if breach_type:
        data = {breach_type: BREACH_CATEGORIES.get(breach_type, "Unknown breach type.")}
    return format_response(data, output_format)


def get_speed_limits(output_format: str) -> str:
    return format_response(SPEED_LIMITS, output_format)


def get_cor_duties(role: str | None, output_format: str) -> str:
    data = COR_DUTIES
    if role:
        data = {role: COR_DUTIES.get(role, "Unknown role.")}
    return format_response(data, output_format)


def get_accreditation_info(module: str | None, output_format: str) -> str:
    data = ACCREDITATION_INFO
    if module:
        data = {module: ACCREDITATION_INFO.get(module, "Unknown module.")}
    return format_response(data, output_format)


def get_permit_types(permit_type: str | None, output_format: str) -> str:
    data = PERMIT_TYPES
    if permit_type:
        data = {permit_type: PERMIT_TYPES.get(permit_type, "Unknown permit type.")}
    return format_response(data, output_format)


def get_hml_info(output_format: str) -> str:
    return format_response(HML_INFO, output_format)


async def search_vehicle_registration(plate_number: str, output_format: str) -> str:
    client = NhvrApiClient()
    data = await client.search_vehicle_registration(plate_number)
    return format_response(data, output_format)


async def search_regulations(query: str, output_format: str) -> str:
    normalized_query = query.lower().strip()
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

    # Map topic keys to dedicated scraper functions
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
        "pbs": None,  # no dedicated parser yet
        "hvnl": None,
    }

    for key, url in topic_map.items():
        if key in normalized_query:
            scraper_name = dedicated_scrapers.get(key)

            if scraper_name:
                import nhvr_mcp.scraper as scraper_module

                scraper_fn = getattr(scraper_module, scraper_name)
                parsed = await scraper_fn(url, use_playwright=True)
                data = {
                    "query": query,
                    "matched_topic": key,
                    "url": url,
                    **parsed,
                }
                return format_response(data, output_format)

            page = await scrape_nhvr_page(url, use_playwright=True)
            data = {
                "query": query,
                "matched_topic": key,
                "url": page.url,
                "title": page.title,
                "text": page.text[:2000],
            }
            return format_response(data, output_format)

    data = {
        "query": query,
        "message": "No topic match. Use nhvr_scrape_page with a full NHVR URL.",
    }
    return format_response(data, output_format)


async def scrape_page(url: str, output_format: str) -> str:
    if not is_nhvr_url(url):
        return format_response({"error": "URL must be on nhvr.gov.au."}, output_format)

    page = await scrape_nhvr_page(url, use_playwright=True)
    data = {
        "url": page.url,
        "title": page.title,
        "text": page.text[:2000],
        "tables": page.tables[:5],
        "links": page.links[:20],
    }
    return format_response(data, output_format)
