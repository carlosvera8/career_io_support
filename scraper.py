# scraper.py
#
# Fetches job postings from four sources and normalizes them to a common schema.
#
# Normalized job schema:
# {
#     "company_name":       str,
#     "job_title":          str,
#     "url":                str,
#     "location_raw":       str,   # raw location string for remote detection
#     "tags":               list[str],
#     "employment_type_raw":str,   # raw commitment/type string
#     "description_text":   str,   # plain text for salary regex
#     "salary_min":         int | None,
#     "salary_max":         int | None,
#     "source":             str,   # "greenhouse" | "lever" | "jobicy" | "remoteok"
#     "raw_id":             str,   # source-specific ID for deduplication
# }

import re
import time
import warnings

import requests
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning

warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)

# ── Shared request wrapper ─────────────────────────────────────────────────────

_DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/html",
}


def safe_get(
    url: str,
    headers: dict | None = None,
    retries: int = 3,
    backoff: float = 2.0,
) -> requests.Response | None:
    """GET with retry + exponential backoff.

    Returns the Response on HTTP 200, None on permanent failures (403/404),
    and retries up to `retries` times on 429 / transient errors.
    """
    merged = {**_DEFAULT_HEADERS, **(headers or {})}
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=merged, timeout=15)
            if resp.status_code == 200:
                return resp
            if resp.status_code in (403, 404):
                return None
            if resp.status_code == 429:
                time.sleep(backoff * (2 ** attempt))
            else:
                time.sleep(backoff)
        except requests.exceptions.Timeout:
            time.sleep(backoff)
        except requests.exceptions.ConnectionError:
            return None
    return None


# ── HTML → plain text helper ───────────────────────────────────────────────────

def _html_to_text(html: str) -> str:
    """Strip HTML tags and return plain text."""
    if not html:
        return ""
    soup = BeautifulSoup(html, "lxml")
    return soup.get_text(separator=" ", strip=True)


# ── Greenhouse ─────────────────────────────────────────────────────────────────

def _greenhouse_salary_from_metadata(metadata: list) -> tuple[int | None, int | None]:
    """Extract salary from Greenhouse custom metadata fields."""
    if not metadata:
        return None, None

    for field in metadata:
        name = (field.get("name") or "").lower()
        if any(kw in name for kw in ("salary", "compensation", "pay", "comp")):
            value = field.get("value")
            if value:
                # Value may be a string like "$150,000 - $200,000" or a number
                from filters import extract_salary_from_text
                lo, hi = extract_salary_from_text(str(value))
                if lo or hi:
                    return lo, hi
    return None, None


def fetch_greenhouse_jobs(company: dict) -> list[dict]:
    """Fetch all open jobs from a company's Greenhouse board."""
    slug = company["greenhouse_slug"]
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"
    resp = safe_get(url)
    if resp is None:
        return []

    try:
        data = resp.json()
    except ValueError:
        return []

    results = []
    for job in data.get("jobs", []):
        location = (job.get("location") or {}).get("name", "")
        content_html = job.get("content", "") or ""
        description_text = _html_to_text(content_html)

        salary_min, salary_max = _greenhouse_salary_from_metadata(
            job.get("metadata") or []
        )

        results.append(
            {
                "company_name": company["name"],
                "job_title": job.get("title", ""),
                "url": job.get("absolute_url", ""),
                "location_raw": location,
                "tags": [],
                "employment_type_raw": "",  # Greenhouse board API lacks this field
                "description_text": description_text,
                "salary_min": salary_min,
                "salary_max": salary_max,
                "source": "greenhouse",
                "raw_id": str(job.get("id", "")),
            }
        )
    return results


# ── Lever ──────────────────────────────────────────────────────────────────────

def fetch_lever_jobs(company: dict) -> list[dict]:
    """Fetch all open jobs from a company's Lever board."""
    slug = company["lever_slug"]
    url = f"https://api.lever.co/v0/postings/{slug}?mode=json"
    resp = safe_get(url)
    if resp is None:
        return []

    try:
        data = resp.json()
    except ValueError:
        return []

    if not isinstance(data, list):
        return []

    results = []
    for job in data:
        categories = job.get("categories") or {}
        location = categories.get("location", "") or ""
        commitment = categories.get("commitment", "") or ""
        tags = job.get("tags") or []

        # Prefer plain text; fall back to stripping HTML description
        description_text = job.get("descriptionPlain", "") or _html_to_text(
            job.get("description", "")
        )

        results.append(
            {
                "company_name": company["name"],
                "job_title": job.get("text", ""),
                "url": job.get("hostedUrl", ""),
                "location_raw": location,
                "tags": tags,
                "employment_type_raw": commitment,
                "description_text": description_text,
                "salary_min": None,
                "salary_max": None,
                "source": "lever",
                "raw_id": str(job.get("id", "")),
            }
        )
    return results


# ── Jobicy ─────────────────────────────────────────────────────────────────────

_JOBICY_URL = (
    "https://jobicy.com/api/v2/remote-jobs"
    "?count=50&tag=data-science,machine-learning,artificial-intelligence"
)


def fetch_jobicy_jobs() -> list[dict]:
    """Fetch remote ML/AI jobs from Jobicy's free API."""
    resp = safe_get(_JOBICY_URL)
    if resp is None:
        return []

    try:
        data = resp.json()
    except ValueError:
        return []

    results = []
    for job in data.get("jobs", []):
        job_types = job.get("jobType") or []
        emp_type = ", ".join(job_types) if job_types else ""

        salary_min = job.get("annualSalaryMin")
        salary_max = job.get("annualSalaryMax")
        currency = job.get("salaryCurrency", "USD")
        # Only use salary if it's in USD
        if currency and currency.upper() != "USD":
            salary_min = salary_max = None

        results.append(
            {
                "company_name": job.get("companyName", ""),
                "job_title": job.get("jobTitle", ""),
                "url": job.get("url", ""),
                "location_raw": job.get("jobGeo", ""),
                "tags": list(job.get("jobIndustry") or []),
                "employment_type_raw": emp_type,
                "description_text": _html_to_text(job.get("jobDescription", "")),
                "salary_min": int(salary_min) if salary_min else None,
                "salary_max": int(salary_max) if salary_max else None,
                "source": "jobicy",
                "raw_id": str(job.get("id", "")),
            }
        )
    return results


# ── RemoteOK ───────────────────────────────────────────────────────────────────

_REMOTEOK_URL = "https://remoteok.com/api"
_REMOTEOK_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def fetch_remoteok_jobs() -> list[dict]:
    """Fetch remote jobs from RemoteOK's free API.

    The response array has a legal disclaimer at index 0 — skip it.
    """
    resp = safe_get(_REMOTEOK_URL, headers=_REMOTEOK_HEADERS)
    if resp is None:
        return []

    try:
        data = resp.json()
    except ValueError:
        return []

    if not isinstance(data, list) or len(data) < 2:
        return []

    results = []
    for job in data[1:]:  # skip index 0 (legal object)
        if not isinstance(job, dict):
            continue

        tags = list(job.get("tags") or [])
        # RemoteOK tags sometimes encode employment type — pull them out
        type_tags = [t for t in tags if re.search(r"contract|part.time|intern", t, re.IGNORECASE)]
        emp_type = ", ".join(type_tags) if type_tags else ""

        salary_min = job.get("salary_min")
        salary_max = job.get("salary_max")

        results.append(
            {
                "company_name": job.get("company", ""),
                "job_title": job.get("position", ""),
                "url": job.get("url", ""),
                "location_raw": job.get("location", ""),
                "tags": tags,
                "employment_type_raw": emp_type,
                "description_text": _html_to_text(job.get("description", "")),
                "salary_min": int(salary_min) if salary_min else None,
                "salary_max": int(salary_max) if salary_max else None,
                "source": "remoteok",
                "raw_id": str(job.get("id", "")),
            }
        )
    return results


# ── Coordinator ────────────────────────────────────────────────────────────────

def scrape_all_jobs(companies: list[dict], verbose: bool = False) -> list[dict]:
    """Fetch jobs from all sources and return a flat normalized list.

    Greenhouse and Lever are queried per-company.
    Jobicy and RemoteOK are queried once globally.
    """
    all_jobs: list[dict] = []
    failed_companies: list[str] = []

    # Greenhouse
    greenhouse_companies = [c for c in companies if c.get("greenhouse_slug")]
    if verbose:
        print(f"[Greenhouse] Querying {len(greenhouse_companies)} companies...")
    for company in greenhouse_companies:
        try:
            jobs = fetch_greenhouse_jobs(company)
            if verbose:
                print(f"  {company['name']}: {len(jobs)} jobs")
            all_jobs.extend(jobs)
        except Exception as exc:
            failed_companies.append(f"{company['name']} (Greenhouse: {exc})")

    # Lever
    lever_companies = [c for c in companies if c.get("lever_slug")]
    if verbose:
        print(f"[Lever] Querying {len(lever_companies)} companies...")
    for company in lever_companies:
        try:
            jobs = fetch_lever_jobs(company)
            if verbose:
                print(f"  {company['name']}: {len(jobs)} jobs")
            all_jobs.extend(jobs)
        except Exception as exc:
            failed_companies.append(f"{company['name']} (Lever: {exc})")

    # Jobicy
    if verbose:
        print("[Jobicy] Fetching remote ML/AI jobs...")
    try:
        jobs = fetch_jobicy_jobs()
        if verbose:
            print(f"  {len(jobs)} jobs found")
        all_jobs.extend(jobs)
    except Exception as exc:
        failed_companies.append(f"Jobicy ({exc})")

    # RemoteOK
    if verbose:
        print("[RemoteOK] Fetching remote jobs...")
    try:
        jobs = fetch_remoteok_jobs()
        if verbose:
            print(f"  {len(jobs)} jobs found")
        all_jobs.extend(jobs)
    except Exception as exc:
        failed_companies.append(f"RemoteOK ({exc})")

    if failed_companies:
        print(f"\n[WARN] Failed sources: {', '.join(failed_companies)}")

    return all_jobs
