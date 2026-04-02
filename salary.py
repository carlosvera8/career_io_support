# salary.py
#
# Levels.fyi salary lookup for jobs that don't list compensation.
# Uses requests + BeautifulSoup to parse the Next.js __NEXT_DATA__ payload.
# Results are cached in memory to avoid redundant requests.

import json
import re
import time

import requests
from bs4 import BeautifulSoup

# ── Browser-like headers required to avoid 403 ────────────────────────────────

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/",
}

# ── In-memory cache: key = "{company_slug}:{role_keyword}" ────────────────────

_cache: dict[str, str | None] = {}

# ── Company name → Levels.fyi URL slug ────────────────────────────────────────

_SLUG_MAP: dict[str, str] = {
    # ── Core tech ─────────────────────────────────────────────────────────────
    "airbnb": "airbnb",
    "openai": "openai",
    "databricks": "databricks",
    "reddit": "reddit",
    "figma": "figma",
    "dropbox": "dropbox",
    "hubspot": "hubspot",
    "spotify": "spotify",
    "zoom": "zoom",
    "asana": "asana",
    "waymo": "waymo",
    "roblox": "roblox",
    "twilio": "twilio",
    "qualtrics": "qualtrics",
    "stripe": "stripe",
    "cloudflare": "cloudflare",
    "gitlab": "gitlab",
    "pagerduty": "pagerduty",
    "confluent": "confluent",
    "anthropic": "anthropic",
    "duolingo": "duolingo",
    "shopify": "shopify",
    "box": "box",
    "atlassian": "atlassian",
    "canva": "canva",
    "notion": "notion",
    "airtable": "airtable",
    "miro": "miro",
    "grammarly": "grammarly",
    "zapier": "zapier",
    "gusto": "gusto",
    "discord": "discord",
    "affirm": "affirm",
    "chime": "chime",
    "zillow": "zillow",
    "redfin": "redfin",
    "unity technologies": "unity",
    "riot games": "riot-games",
    "epic games": "epic-games",
    "toast": "toast",
    "procore": "procore",
    "freshworks": "freshworks",
    "lattice": "lattice",
    "gong": "gong",
    "mixpanel": "mixpanel",
    "fivetran": "fivetran",
    "airbyte": "airbyte",
    "palo alto networks": "palo-alto-networks",
    "crowdstrike": "crowdstrike",
    "snyk": "snyk",
    "uipath": "uipath",
    "celonis": "celonis",
    "postman": "postman",
    "collibra": "collibra",
    "alation": "alation",
    "thoughtworks": "thoughtworks",
    "slalom": "slalom",
    "fastly": "fastly",
    "netlify": "netlify",
    "braze": "braze",
    "klaviyo": "klaviyo",
    "intercom": "intercom",
    "fullstory": "fullstory",
    "pendo": "pendo",
    "loom": "loom",
    "culture amp": "culture-amp",
    "dbt labs": "dbt-labs",
    "airbyte": "airbyte",
    "glean": "glean",
    "weaviate": "weaviate",
    "pinecone": "pinecone",
    "vercel": "vercel",
    "linear": "linear",
    "posthog": "posthog",
    "retool": "retool",
    "replit": "replit",
    # ── AI / ML companies ─────────────────────────────────────────────────────
    "cohere": "cohere",
    "weights & biases": "weights-and-biases",
    "hugging face": "hugging-face",
    "mistral ai": "mistral",
    "scale ai": "scale-ai",
    "perplexity ai": "perplexity",
    "together ai": "together-ai",
    "groq": "groq",
    "elevenlabs": "elevenlabs",
    "sierra ai": "sierra",
    "imbue": "imbue",
    "runway ml": "runway",
    "character ai": "character-ai",
    "fireworks ai": "fireworks-ai",
    "replicate": "replicate",
    "modal labs": "modal",
    "anyscale": "anyscale",
    "snorkel ai": "snorkel-ai",
    "labelbox": "labelbox",
    "dataiku": "dataiku",
    "monte carlo": "monte-carlo",
    "hex technologies": "hex",
    "astronomer": "astronomer",
    # ── Mid-size tech ─────────────────────────────────────────────────────────
    "datadog": "datadog",
    "mongodb": "mongodb",
    "okta": "okta",
    "plaid": "plaid",
    "elastic": "elastic",
    "hashicorp": "hashicorp",
    "zendesk": "zendesk",
    "docusign": "docusign",
    "splunk": "splunk",
    "new relic": "new-relic",
    "nuro": "nuro",
    "veeva systems": "veeva",
    "samsara": "samsara",
    "amplitude": "amplitude",
    "benchling": "benchling",
    "applied intuition": "applied-intuition",
    "aurora innovation": "aurora",
    "10x genomics": "10x-genomics",
    "ginkgo bioworks": "ginkgo-bioworks",
    "moderna": "moderna",
    "illumina": "illumina",
    "recursion pharmaceuticals": "recursion",
    "marqeta": "marqeta",
    "sofi": "sofi",
    "block": "block",
    "joby aviation": "joby",
    "cruise": "cruise",
    "zoox": "zoox",
    "lucid motors": "lucid-motors",
    "rivian": "rivian",
    "moveworks": "moveworks",
    "highspot": "highspot",
    "outreach": "outreach",
    "salesloft": "salesloft",
    "clari": "clari",
    "servicetitan": "servicetitan",
    "remote.com": "remote",
    "vanta": "vanta",
    "epam systems": "epam",
    "globant": "globant",
    # ── Big tech ──────────────────────────────────────────────────────────────
    "google": "google",
    "microsoft": "microsoft",
    "meta": "meta",
    "apple": "apple",
    "salesforce": "salesforce",
    "adobe": "adobe",
    "nvidia": "nvidia",
    "ibm": "ibm",
    "linkedin": "linkedin",
    "intuit": "intuit",
    "servicenow": "servicenow",
    "workday": "workday",
    "qualcomm": "qualcomm",
    "dell technologies": "dell",
    "hp inc": "hp",
    # ── Finance ───────────────────────────────────────────────────────────────
    "visa": "visa",
    "mastercard": "mastercard",
    "fidelity investments": "fidelity",
    "capital one": "capital-one",
    "american express": "american-express",
    # ── Healthcare / Pharma ───────────────────────────────────────────────────
    "johnson & johnson": "johnson-and-johnson",
    "pfizer": "pfizer",
    "merck": "merck",
    "eli lilly": "eli-lilly",
    "abbvie": "abbvie",
    "abbott laboratories": "abbott",
    "bristol-myers squibb": "bristol-myers-squibb",
    "moderna": "moderna",
    "illumina": "illumina",
    # ── Defense ───────────────────────────────────────────────────────────────
    "lockheed martin": "lockheed-martin",
    "northrop grumman": "northrop-grumman",
}


def _company_to_levels_slug(company_name: str) -> str:
    key = company_name.lower().strip()
    return _SLUG_MAP.get(key, key.replace(" ", "-"))


# ── Core fetch + parse ─────────────────────────────────────────────────────────

def _fetch_levels_page(url: str, retries: int = 3) -> str | None:
    """Fetch a Levels.fyi page with retry + exponential backoff."""
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=_HEADERS, timeout=20)
            if resp.status_code == 200:
                return resp.text
            if resp.status_code in (403, 404):
                return None
            if resp.status_code == 429:
                wait = 4.0 * (2 ** attempt)
                time.sleep(wait)
                continue
        except requests.exceptions.RequestException:
            time.sleep(2.0 * (2 ** attempt))
    return None


def _extract_tc_from_next_data(html: str, role_keyword: str) -> str | None:
    """Try to extract total compensation from the __NEXT_DATA__ JSON blob."""
    soup = BeautifulSoup(html, "lxml")
    script = soup.find("script", {"id": "__NEXT_DATA__"})
    if not script or not script.string:
        return None

    try:
        data = json.loads(script.string)
    except json.JSONDecodeError:
        return None

    page_props = data.get("props", {}).get("pageProps", {})

    # The salary page embeds a list of role breakdowns; look for the one
    # closest to the requested role keyword.
    role_kw_lower = role_keyword.lower()
    candidates = []

    # Walk all values recursively looking for compensation-like dicts
    def _walk(obj: object, depth: int = 0) -> None:
        if depth > 8:
            return
        if isinstance(obj, dict):
            # A compensation entry often has keys like "totalCompensation", "baseSalary", "title"
            title = obj.get("title") or obj.get("name") or obj.get("jobTitle") or ""
            tc = (
                obj.get("totalCompensation")
                or obj.get("tc")
                or obj.get("medianTotalComp")
                or obj.get("medianComp")
                or obj.get("baseSalary")
            )
            if isinstance(tc, (int, float)) and tc > 50_000:
                candidates.append((str(title).lower(), int(tc)))
            for v in obj.values():
                _walk(v, depth + 1)
        elif isinstance(obj, list):
            for item in obj:
                _walk(item, depth + 1)

    _walk(page_props)

    if not candidates:
        return None

    # Prefer entries whose title matches the role keyword
    role_matches = [(t, tc) for t, tc in candidates if role_kw_lower in t]
    chosen = role_matches[0] if role_matches else candidates[0]
    return f"~${chosen[1]:,} TC (Levels.fyi estimate)"


def _extract_tc_from_html_text(html: str) -> str | None:
    """Fallback: regex scan for salary figures in the raw HTML."""
    # Look for patterns like $200,000 or $250K appearing in the page
    matches = re.findall(r"\$\s?(\d{1,3}(?:,\d{3})+|\d{3,})\s*[kK]?", html)
    values = []
    for m in matches:
        try:
            v = int(m.replace(",", ""))
            if 80_000 <= v <= 2_000_000:
                values.append(v)
        except ValueError:
            continue

    if not values:
        return None

    # Return the median value to avoid outliers
    values.sort()
    median = values[len(values) // 2]
    return f"~${median:,} TC (Levels.fyi estimate)"


# ── Public API ─────────────────────────────────────────────────────────────────

def get_levels_salary(company_name: str, role_keyword: str) -> str | None:
    """Look up approximate compensation on Levels.fyi for a company + role.

    Returns a human-readable string like "~$220,000 TC (Levels.fyi estimate)"
    or None if the lookup fails or finds no data.

    Results are cached per (company, role) to avoid duplicate requests.
    A 2-second courtesy delay is added between cache-miss fetches.
    """
    slug = _company_to_levels_slug(company_name)
    cache_key = f"{slug}:{role_keyword.lower()}"

    if cache_key in _cache:
        return _cache[cache_key]

    url = f"https://www.levels.fyi/companies/{slug}/salaries/"
    html = _fetch_levels_page(url)

    result = None
    if html:
        result = _extract_tc_from_next_data(html, role_keyword)
        if result is None:
            result = _extract_tc_from_html_text(html)

    _cache[cache_key] = result
    time.sleep(2)  # courtesy delay between requests
    return result


def parse_salary_estimate(salary_str: str) -> int | None:
    """Extract the numeric value from a Levels.fyi estimate string.

    E.g. "~$220,000 TC (Levels.fyi estimate)" → 220000
    """
    if not salary_str:
        return None
    match = re.search(r"\$\s?([\d,]+)", salary_str)
    if match:
        try:
            return int(match.group(1).replace(",", ""))
        except ValueError:
            pass
    return None
