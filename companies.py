# companies.py
#
# Curated list of companies to search for jobs.
# This list acts as the combined WLB + size filter — only companies on this
# list will appear in results. Add or remove entries freely.
#
# Fields:
#   name                    - Display name
#   greenhouse_slug         - Slug used in boards.greenhouse.io/{slug} (None if not on Greenhouse)
#   lever_slug              - Slug used in jobs.lever.co/{slug} (None if not on Lever)
#   glassdoor_wlb_score     - Glassdoor work-life balance score (0-5, informational only)
#   employee_count_estimate - Rough headcount
#   notes                   - Optional freeform notes

COMPANIES = [
    # ── GREENHOUSE ────────────────────────────────────────────────────────────
    {
        "name": "Airbnb",
        "greenhouse_slug": "airbnb",
        "lever_slug": None,
        "glassdoor_wlb_score": 4.1,
        "employee_count_estimate": 6000,
        "notes": "",
    },
    {
        "name": "Netflix",
        "greenhouse_slug": "netflix",
        "lever_slug": None,
        "glassdoor_wlb_score": 3.9,
        "employee_count_estimate": 13000,
        "notes": "",
    },
    {
        "name": "Lyft",
        "greenhouse_slug": "lyft",
        "lever_slug": None,
        "glassdoor_wlb_score": 3.8,
        "employee_count_estimate": 5000,
        "notes": "",
    },
    {
        "name": "DoorDash",
        "greenhouse_slug": "doordash",
        "lever_slug": None,
        "glassdoor_wlb_score": 3.6,
        "employee_count_estimate": 8000,
        "notes": "",
    },
    {
        "name": "OpenAI",
        "greenhouse_slug": "openai",
        "lever_slug": None,
        "glassdoor_wlb_score": 4.2,
        "employee_count_estimate": 1500,
        "notes": "",
    },
    {
        "name": "Databricks",
        "greenhouse_slug": "databricks",
        "lever_slug": None,
        "glassdoor_wlb_score": 4.3,
        "employee_count_estimate": 5000,
        "notes": "",
    },
    {
        "name": "Coinbase",
        "greenhouse_slug": "coinbase",
        "lever_slug": None,
        "glassdoor_wlb_score": 3.9,
        "employee_count_estimate": 3500,
        "notes": "",
    },
    {
        "name": "Reddit",
        "greenhouse_slug": "reddit",
        "lever_slug": None,
        "glassdoor_wlb_score": 4.0,
        "employee_count_estimate": 2000,
        "notes": "",
    },
    {
        "name": "Figma",
        "greenhouse_slug": "figma",
        "lever_slug": None,
        "glassdoor_wlb_score": 4.5,
        "employee_count_estimate": 1200,
        "notes": "",
    },
    {
        "name": "Robinhood",
        "greenhouse_slug": "robinhood",
        "lever_slug": None,
        "glassdoor_wlb_score": 3.7,
        "employee_count_estimate": 2000,
        "notes": "",
    },
    {
        "name": "Dropbox",
        "greenhouse_slug": "dropbox",
        "lever_slug": None,
        "glassdoor_wlb_score": 4.2,
        "employee_count_estimate": 2500,
        "notes": "Remote-first company",
    },
    {
        "name": "HubSpot",
        "greenhouse_slug": "hubspot",
        "lever_slug": None,
        "glassdoor_wlb_score": 4.5,
        "employee_count_estimate": 7000,
        "notes": "",
    },
    {
        "name": "Spotify",
        "greenhouse_slug": "spotify",
        "lever_slug": None,
        "glassdoor_wlb_score": 4.3,
        "employee_count_estimate": 9000,
        "notes": "",
    },
    {
        "name": "Snap",
        "greenhouse_slug": "snap",
        "lever_slug": None,
        "glassdoor_wlb_score": 3.8,
        "employee_count_estimate": 5000,
        "notes": "",
    },
    {
        "name": "Twilio",
        "greenhouse_slug": "twilio",
        "lever_slug": None,
        "glassdoor_wlb_score": 4.0,
        "employee_count_estimate": 6000,
        "notes": "",
    },
    {
        "name": "Zoom",
        "greenhouse_slug": "zoom",
        "lever_slug": None,
        "glassdoor_wlb_score": 4.1,
        "employee_count_estimate": 7000,
        "notes": "",
    },
    {
        "name": "Asana",
        "greenhouse_slug": "asana",
        "lever_slug": None,
        "glassdoor_wlb_score": 4.4,
        "employee_count_estimate": 1700,
        "notes": "",
    },
    {
        "name": "Waymo",
        "greenhouse_slug": "waymo",
        "lever_slug": None,
        "glassdoor_wlb_score": 4.2,
        "employee_count_estimate": 2500,
        "notes": "",
    },
    {
        "name": "Palantir",
        "greenhouse_slug": "palantir",
        "lever_slug": None,
        "glassdoor_wlb_score": 3.5,
        "employee_count_estimate": 4000,
        "notes": "Lower WLB score — remove if not desired",
    },
    {
        "name": "Twitch",
        "greenhouse_slug": "twitch",
        "lever_slug": None,
        "glassdoor_wlb_score": 3.9,
        "employee_count_estimate": 1000,
        "notes": "Amazon subsidiary",
    },
    {
        "name": "Qualtrics",
        "greenhouse_slug": "qualtrics",
        "lever_slug": None,
        "glassdoor_wlb_score": 4.0,
        "employee_count_estimate": 5000,
        "notes": "",
    },
    {
        "name": "Roblox",
        "greenhouse_slug": "roblox",
        "lever_slug": None,
        "glassdoor_wlb_score": 4.1,
        "employee_count_estimate": 2000,
        "notes": "",
    },

    # ── LEVER ─────────────────────────────────────────────────────────────────
    {
        "name": "Stripe",
        "greenhouse_slug": None,
        "lever_slug": "stripe",
        "glassdoor_wlb_score": 3.8,
        "employee_count_estimate": 8000,
        "notes": "",
    },
    {
        "name": "Cloudflare",
        "greenhouse_slug": None,
        "lever_slug": "cloudflare",
        "glassdoor_wlb_score": 4.1,
        "employee_count_estimate": 3500,
        "notes": "",
    },
    {
        "name": "GitLab",
        "greenhouse_slug": None,
        "lever_slug": "gitlab",
        "glassdoor_wlb_score": 4.3,
        "employee_count_estimate": 2000,
        "notes": "Fully remote company",
    },
    {
        "name": "PagerDuty",
        "greenhouse_slug": None,
        "lever_slug": "pagerduty",
        "glassdoor_wlb_score": 4.0,
        "employee_count_estimate": 1000,
        "notes": "",
    },
    {
        "name": "Instacart",
        "greenhouse_slug": None,
        "lever_slug": "instacart",
        "glassdoor_wlb_score": 3.9,
        "employee_count_estimate": 3000,
        "notes": "",
    },
    {
        "name": "Confluent",
        "greenhouse_slug": None,
        "lever_slug": "confluent",
        "glassdoor_wlb_score": 4.1,
        "employee_count_estimate": 3000,
        "notes": "",
    },
    {
        "name": "Anthropic",
        "greenhouse_slug": None,
        "lever_slug": "anthropic",
        "glassdoor_wlb_score": 4.5,
        "employee_count_estimate": 1000,
        "notes": "",
    },
    {
        "name": "Scale AI",
        "greenhouse_slug": None,
        "lever_slug": "scaleai",
        "glassdoor_wlb_score": 3.7,
        "employee_count_estimate": 1000,
        "notes": "",
    },
    {
        "name": "Duolingo",
        "greenhouse_slug": None,
        "lever_slug": "duolingo",
        "glassdoor_wlb_score": 4.4,
        "employee_count_estimate": 700,
        "notes": "Strong ML team; slightly under 1k employees",
    },
    {
        "name": "Replit",
        "greenhouse_slug": None,
        "lever_slug": "replit",
        "glassdoor_wlb_score": 4.2,
        "employee_count_estimate": 200,
        "notes": "Small but notable AI-first company; remove if strict about size",
    },

    # ── AGGREGATOR-ONLY (own portals — caught via Jobicy / RemoteOK) ──────────
    {
        "name": "Google",
        "greenhouse_slug": None,
        "lever_slug": None,
        "glassdoor_wlb_score": 4.2,
        "employee_count_estimate": 180000,
        "notes": "Uses own careers portal",
    },
    {
        "name": "Microsoft",
        "greenhouse_slug": None,
        "lever_slug": None,
        "glassdoor_wlb_score": 4.0,
        "employee_count_estimate": 220000,
        "notes": "Uses own careers portal",
    },
    {
        "name": "Meta",
        "greenhouse_slug": None,
        "lever_slug": None,
        "glassdoor_wlb_score": 3.9,
        "employee_count_estimate": 70000,
        "notes": "Uses own careers portal",
    },
    {
        "name": "Apple",
        "greenhouse_slug": None,
        "lever_slug": None,
        "glassdoor_wlb_score": 3.8,
        "employee_count_estimate": 160000,
        "notes": "Rarely fully remote; low yield expected",
    },
    {
        "name": "Salesforce",
        "greenhouse_slug": None,
        "lever_slug": None,
        "glassdoor_wlb_score": 4.1,
        "employee_count_estimate": 70000,
        "notes": "",
    },
    {
        "name": "Adobe",
        "greenhouse_slug": None,
        "lever_slug": None,
        "glassdoor_wlb_score": 4.2,
        "employee_count_estimate": 30000,
        "notes": "",
    },
    {
        "name": "Nvidia",
        "greenhouse_slug": None,
        "lever_slug": None,
        "glassdoor_wlb_score": 4.3,
        "employee_count_estimate": 30000,
        "notes": "",
    },
    {
        "name": "IBM",
        "greenhouse_slug": None,
        "lever_slug": None,
        "glassdoor_wlb_score": 3.8,
        "employee_count_estimate": 280000,
        "notes": "",
    },
    {
        "name": "LinkedIn",
        "greenhouse_slug": None,
        "lever_slug": None,
        "glassdoor_wlb_score": 4.2,
        "employee_count_estimate": 20000,
        "notes": "Microsoft subsidiary; uses own portal",
    },
    {
        "name": "Amazon",
        "greenhouse_slug": None,
        "lever_slug": None,
        "glassdoor_wlb_score": 3.2,
        "employee_count_estimate": 1500000,
        "notes": "Low WLB score — remove if not desired",
    },
    {
        "name": "Intuit",
        "greenhouse_slug": None,
        "lever_slug": None,
        "glassdoor_wlb_score": 4.3,
        "employee_count_estimate": 18000,
        "notes": "",
    },
    {
        "name": "ServiceNow",
        "greenhouse_slug": None,
        "lever_slug": None,
        "glassdoor_wlb_score": 4.2,
        "employee_count_estimate": 22000,
        "notes": "",
    },
    {
        "name": "Workday",
        "greenhouse_slug": None,
        "lever_slug": None,
        "glassdoor_wlb_score": 4.3,
        "employee_count_estimate": 18000,
        "notes": "",
    },
    {
        "name": "Snowflake",
        "greenhouse_slug": None,
        "lever_slug": None,
        "glassdoor_wlb_score": 3.9,
        "employee_count_estimate": 7000,
        "notes": "",
    },
]


def get_greenhouse_companies() -> list[dict]:
    """Return companies that have a Greenhouse slug."""
    return [c for c in COMPANIES if c["greenhouse_slug"]]


def get_lever_companies() -> list[dict]:
    """Return companies that have a Lever slug."""
    return [c for c in COMPANIES if c["lever_slug"]]


def get_all_company_names() -> set[str]:
    """Return a lowercase set of all company names for O(1) membership checks."""
    return {c["name"].lower() for c in COMPANIES}


def get_company_by_name(name: str) -> dict | None:
    """Case-insensitive lookup of a company entry by name."""
    name_lower = name.lower().strip()
    for c in COMPANIES:
        if c["name"].lower() == name_lower:
            return c
    return None
