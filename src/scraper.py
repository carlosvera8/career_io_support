# scraper.py
#
# Fetches job postings from multiple sources and normalizes them to a common schema.
# Sources: Greenhouse, Lever, Ashby (direct ATS APIs) + Jobicy, RemoteOK, Remotive,
#          Himalayas, Working Nomads, Arbeit Now, HN "Who's Hiring" (aggregators)
#          + Dice (MCP cache).
#
# Normalized job schema:
# {
#     "company_name":       str,
#     "job_title":          str,
#     "url":                str,
#     "location_raw":       str,
#     "tags":               list[str],
#     "employment_type_raw":str,
#     "description_text":   str,
#     "salary_min":         int | None,
#     "salary_max":         int | None,
#     "source":             str,  # "greenhouse"|"lever"|"ashby"|"jobicy"|"remoteok"|
#                                 # "remotive"|"himalayas"|"workingnomads"|"arbeitnow"|
#                                 # "hn_hiring"|"dice"
#     "raw_id":             str,
#     "is_aggregator":      bool,
# }

import re
import time
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

import requests
from bs4 import BeautifulSoup, MarkupResemblesLocatorWarning
from .filters import extract_salary_from_text, TITLE_PATTERN

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
                "employment_type_raw": "",
                "description_text": description_text,
                "salary_min": salary_min,
                "salary_max": salary_max,
                "source": "greenhouse",
                "raw_id": str(job.get("id", "")),
                "is_aggregator": False,
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
                "is_aggregator": False,
            }
        )
    return results


# ── Ashby ──────────────────────────────────────────────────────────────────────

def fetch_ashby_jobs(company: dict) -> list[dict]:
    """Fetch all open jobs from a company's Ashby board.

    API: https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true
    """
    slug = company["ashby_slug"]
    url = f"https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true"
    resp = safe_get(url)
    if resp is None:
        return []

    try:
        data = resp.json()
    except ValueError:
        return []

    jobs_list = data.get("jobs") or []
    if not isinstance(jobs_list, list):
        return []

    results = []
    for job in jobs_list:
        location = job.get("locationName", "") or ""
        is_remote = job.get("isRemote", False)
        if is_remote and not location:
            location = "Remote"

        # Employment type
        emp_type = job.get("employmentType", "") or ""

        # Description
        desc_html = job.get("descriptionHtml", "") or ""
        description_text = _html_to_text(desc_html)

        # Compensation from Ashby's compensation tiers
        salary_min = None
        salary_max = None
        comp_tiers = job.get("compensationTierSummary", "") or ""
        if comp_tiers:
            salary_min, salary_max = extract_salary_from_text(comp_tiers)

        # Also try description for salary
        if salary_min is None:
            salary_min, salary_max = extract_salary_from_text(description_text)

        # Build URL: prefer externalLink, fall back to Ashby hosted page
        job_url = (
            job.get("externalLink")
            or f"https://jobs.ashbyhq.com/{slug}/{job.get('id', '')}"
        )

        results.append(
            {
                "company_name": company["name"],
                "job_title": job.get("title", ""),
                "url": job_url,
                "location_raw": location,
                "tags": list(job.get("departmentName", "").split() if job.get("departmentName") else []),
                "employment_type_raw": emp_type,
                "description_text": description_text,
                "salary_min": salary_min,
                "salary_max": salary_max,
                "source": "ashby",
                "raw_id": str(job.get("id", "")),
                "is_aggregator": False,
            }
        )
    return results


# ── Jobicy ─────────────────────────────────────────────────────────────────────

_JOBICY_URLS = [
    "https://jobicy.com/api/v2/remote-jobs?count=50&tag=data-science",
    "https://jobicy.com/api/v2/remote-jobs?count=50&tag=machine-learning",
    "https://jobicy.com/api/v2/remote-jobs?count=50&tag=artificial-intelligence",
]


def fetch_jobicy_jobs() -> list[dict]:
    """Fetch remote ML/AI jobs from Jobicy's free API across multiple tags."""
    seen_ids: set[str] = set()
    results: list[dict] = []

    for url in _JOBICY_URLS:
        resp = safe_get(url)
        if resp is None:
            continue
        try:
            data = resp.json()
        except ValueError:
            continue

        for job in data.get("jobs", []):
            job_id = str(job.get("id", ""))
            if job_id in seen_ids:
                continue
            seen_ids.add(job_id)

            job_types = job.get("jobType") or []
            emp_type = ", ".join(job_types) if job_types else ""

            salary_min = job.get("annualSalaryMin")
            salary_max = job.get("annualSalaryMax")
            currency = job.get("salaryCurrency", "USD")
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
                    "raw_id": job_id,
                    "is_aggregator": True,
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
    for job in data[1:]:
        if not isinstance(job, dict):
            continue

        tags = list(job.get("tags") or [])
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
                "is_aggregator": True,
            }
        )
    return results


# ── Remotive ───────────────────────────────────────────────────────────────────

_REMOTIVE_URLS = [
    "https://remotive.com/api/remote-jobs?category=data&limit=200",
    "https://remotive.com/api/remote-jobs?category=software-dev&limit=200",
    "https://remotive.com/api/remote-jobs?category=product&limit=100",
]

_REMOTIVE_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}


def fetch_remotive_jobs() -> list[dict]:
    """Fetch remote jobs from Remotive's free API across multiple categories."""
    seen_ids: set[str] = set()
    results: list[dict] = []

    for url in _REMOTIVE_URLS:
        resp = safe_get(url, headers=_REMOTIVE_HEADERS)
        if resp is None:
            continue

        try:
            data = resp.json()
        except ValueError:
            continue

        for job in data.get("jobs", []):
            job_id = str(job.get("id", ""))
            if job_id in seen_ids:
                continue
            seen_ids.add(job_id)

            # Salary: Remotive sometimes provides a salary string like "$150K-200K"
            salary_str = job.get("salary", "") or ""
            salary_min: int | None = None
            salary_max: int | None = None
            if salary_str:
                salary_min, salary_max = extract_salary_from_text(salary_str)

            # Location
            location = job.get("candidate_required_location", "") or ""
            if not location:
                location = "Remote"

            # Employment type
            job_type = job.get("job_type", "") or ""

            results.append(
                {
                    "company_name": job.get("company_name", ""),
                    "job_title": job.get("title", ""),
                    "url": job.get("url", ""),
                    "location_raw": location,
                    "tags": list(job.get("tags") or []),
                    "employment_type_raw": job_type,
                    "description_text": _html_to_text(job.get("description", "")),
                    "salary_min": salary_min,
                    "salary_max": salary_max,
                    "source": "remotive",
                    "raw_id": job_id,
                    "is_aggregator": True,
                }
            )

    return results


# ── Himalayas ─────────────────────────────────────────────────────────────────

_HIMALAYAS_URLS = [
    "https://himalayas.app/api/jobs?limit=100&skills=machine-learning",
    "https://himalayas.app/api/jobs?limit=100&skills=data-science",
    "https://himalayas.app/api/jobs?limit=100&skills=deep-learning",
    "https://himalayas.app/api/jobs?limit=100&skills=artificial-intelligence",
    "https://himalayas.app/api/jobs?limit=100&skills=natural-language-processing",
]


def fetch_himalayas_jobs() -> list[dict]:
    """Fetch remote jobs from Himalayas.app free API. Has structured salary fields."""
    seen_ids: set[str] = set()
    results: list[dict] = []

    for url in _HIMALAYAS_URLS:
        resp = safe_get(url)
        if resp is None:
            continue
        try:
            data = resp.json()
        except ValueError:
            continue

        jobs_list = data.get("jobs") or []
        for job in jobs_list:
            job_id = str(job.get("id", "") or job.get("guid", ""))
            if job_id in seen_ids:
                continue
            seen_ids.add(job_id)

            # Salary — Himalayas provides numeric min/max
            salary_min = job.get("minSalary") or job.get("salaryMin")
            salary_max = job.get("maxSalary") or job.get("salaryMax")
            currency = job.get("currency", "USD") or "USD"
            if currency.upper() != "USD":
                salary_min = salary_max = None

            # Location / remote
            location = job.get("locationRestrictions") or job.get("location") or "Remote"
            if isinstance(location, list):
                location = ", ".join(location)

            emp_type = job.get("employmentType") or job.get("jobType") or ""

            desc_html = job.get("description") or job.get("descriptionHtml") or ""
            description = _html_to_text(desc_html)

            job_url = (
                job.get("applicationLink")
                or job.get("url")
                or job.get("applyUrl")
                or ""
            )

            results.append(
                {
                    "company_name": job.get("companyName") or job.get("company") or "",
                    "job_title": job.get("title") or "",
                    "url": job_url,
                    "location_raw": str(location),
                    "tags": list(job.get("categories") or []),
                    "employment_type_raw": str(emp_type),
                    "description_text": description,
                    "salary_min": int(salary_min) if salary_min else None,
                    "salary_max": int(salary_max) if salary_max else None,
                    "source": "himalayas",
                    "raw_id": job_id,
                    "is_aggregator": True,
                }
            )

    return results


# ── Working Nomads ─────────────────────────────────────────────────────────────

_WORKINGNOMADS_URL = "https://www.workingnomads.com/api/exposed_jobs/"


def fetch_workingnomads_jobs() -> list[dict]:
    """Fetch remote jobs from Working Nomads free public API."""
    resp = safe_get(_WORKINGNOMADS_URL)
    if resp is None:
        return []
    try:
        data = resp.json()
    except ValueError:
        return []

    if not isinstance(data, list):
        data = data.get("jobs") or data.get("results") or []

    results = []
    for job in data:
        if not isinstance(job, dict):
            continue

        job_id = str(job.get("id", ""))
        description = _html_to_text(job.get("description") or "")
        salary_min, salary_max = extract_salary_from_text(description)

        results.append(
            {
                "company_name": job.get("company_name") or job.get("company") or "",
                "job_title": job.get("title") or "",
                "url": job.get("url") or "",
                "location_raw": job.get("location") or "Remote",
                "tags": [job.get("category_name")] if job.get("category_name") else [],
                "employment_type_raw": "",
                "description_text": description,
                "salary_min": salary_min,
                "salary_max": salary_max,
                "source": "workingnomads",
                "raw_id": job_id,
                "is_aggregator": True,
            }
        )
    return results


# ── Arbeit Now ─────────────────────────────────────────────────────────────────

_ARBEITNOW_URL = "https://arbeitnow.com/api/job-board-api"


def fetch_arbeitnow_jobs() -> list[dict]:
    """Fetch remote jobs from Arbeit Now free API."""
    resp = safe_get(_ARBEITNOW_URL)
    if resp is None:
        return []
    try:
        data = resp.json()
    except ValueError:
        return []

    jobs_list = data.get("data") or data.get("jobs") or []
    if isinstance(data, list):
        jobs_list = data

    results = []
    for job in jobs_list:
        if not isinstance(job, dict):
            continue

        # Only include explicitly remote jobs
        if not job.get("remote", False):
            continue

        job_id = str(job.get("slug") or job.get("id") or "")
        description = _html_to_text(job.get("description") or "")
        salary_min, salary_max = extract_salary_from_text(description)

        job_types = job.get("job_types") or []
        emp_type = ", ".join(job_types) if job_types else ""

        results.append(
            {
                "company_name": job.get("company_name") or "",
                "job_title": job.get("title") or "",
                "url": job.get("url") or "",
                "location_raw": job.get("location") or "Remote",
                "tags": list(job.get("tags") or []),
                "employment_type_raw": emp_type,
                "description_text": description,
                "salary_min": salary_min,
                "salary_max": salary_max,
                "source": "arbeitnow",
                "raw_id": job_id,
                "is_aggregator": True,
            }
        )
    return results


# ── HN "Who's Hiring" ─────────────────────────────────────────────────────────

_HN_API_BASE = "https://hacker-news.firebaseio.com/v0"
_HN_WHOISHIRING_USER = "whoishiring"
_HN_MAX_COMMENTS = 500

_HN_ML_KEYWORDS = re.compile(
    r"\b(machine\s+learning|deep\s+learning|data\s+scien|MLOps|NLP|LLM|"
    r"applied\s+scien|artificial\s+intelligence|data\s+engineer|"
    r"computer\s+vision|reinforcement\s+learning|generative\s+AI|GenAI|"
    r"\bML\b|\bAI\b)\b",
    re.IGNORECASE,
)


def _fetch_hn_item(item_id: int) -> dict | None:
    """Fetch a single HN item by ID."""
    resp = safe_get(f"{_HN_API_BASE}/item/{item_id}.json")
    if resp is None:
        return None
    try:
        return resp.json()
    except ValueError:
        return None


def _parse_hn_post(first_line: str) -> tuple[str, str]:
    """Extract (company_name, job_title) from the first line of an HN hiring post.

    HN convention: 'Company | Role | Location | ...'
    Falls back to the whole first line as company name with empty title.
    """
    parts = [p.strip() for p in first_line.split("|")]
    if len(parts) >= 2:
        company = re.sub(r"\s*\(.*?\)\s*$", "", parts[0]).strip()
        return company, parts[1].strip()
    return first_line.strip()[:80], ""


def fetch_hn_hiring_jobs() -> list[dict]:
    """Fetch ML/AI remote jobs from the HN 'Ask HN: Who is hiring?' thread.

    Uses the official HN Firebase API — no auth, no ToS concerns.
    Only returns comments that mention 'remote' and at least one ML/AI keyword.
    """
    # Find the most recent "Ask HN: Who is hiring?" post
    user_resp = safe_get(f"{_HN_API_BASE}/user/{_HN_WHOISHIRING_USER}.json")
    if user_resp is None:
        return []
    try:
        user_data = user_resp.json()
    except ValueError:
        return []

    hiring_post_id: int | None = None
    for item_id in user_data.get("submitted") or []:
        item = _fetch_hn_item(item_id)
        if item and "who is hiring" in (item.get("title") or "").lower():
            hiring_post_id = item_id
            break

    if hiring_post_id is None:
        return []

    post = _fetch_hn_item(hiring_post_id)
    if post is None:
        return []

    kids = (post.get("kids") or [])[:_HN_MAX_COMMENTS]
    if not kids:
        return []

    # Concurrently fetch all top-level comments
    comments: list[dict] = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(_fetch_hn_item, kid_id): kid_id for kid_id in kids}
        for future in as_completed(futures):
            result = future.result()
            if result and isinstance(result, dict):
                comments.append(result)

    results: list[dict] = []
    for comment in comments:
        if comment.get("deleted") or comment.get("dead"):
            continue

        text_html = comment.get("text") or ""
        if not text_html:
            continue

        text = _html_to_text(text_html)

        if not re.search(r"\bremote\b", text, re.IGNORECASE):
            continue
        if not _HN_ML_KEYWORDS.search(text):
            continue

        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        first_line = lines[0] if lines else ""
        company_name, job_title = _parse_hn_post(first_line)

        # If the parsed title isn't a recognizable role, scan the text for one
        if not TITLE_PATTERN.search(job_title):
            m = TITLE_PATTERN.search(text)
            if m:
                job_title = m.group(0)

        salary_min, salary_max = extract_salary_from_text(text)

        emp_type = ""
        if re.search(r"\bfull[\s-]time\b", text, re.IGNORECASE):
            emp_type = "Full-time"
        elif re.search(r"\bcontract\b", text, re.IGNORECASE):
            emp_type = "Contract"
        elif re.search(r"\bpart[\s-]time\b", text, re.IGNORECASE):
            emp_type = "Part-time"

        comment_id = comment.get("id", "")
        results.append(
            {
                "company_name": company_name,
                "job_title": job_title,
                "url": f"https://news.ycombinator.com/item?id={comment_id}",
                "location_raw": "Remote",
                "tags": [],
                "employment_type_raw": emp_type,
                "description_text": text,
                "salary_min": salary_min,
                "salary_max": salary_max,
                "source": "hn_hiring",
                "raw_id": str(comment_id),
                "is_aggregator": True,
            }
        )

    return results


# ── Dice (MCP cache) ───────────────────────────────────────────────────────────

def load_dice_cache(cache_path: str) -> list[dict]:
    """Load pre-fetched Dice jobs written by Claude's MCP tool.

    The cache is a JSON array of objects already normalized to the standard schema.
    Returns an empty list if the file is missing or malformed.
    """
    try:
        with open(cache_path, encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
        return data
    except (OSError, ValueError):
        return []


# ── Coordinator ────────────────────────────────────────────────────────────────

def scrape_all_jobs(
    companies: list[dict],
    verbose: bool = False,
    dice_cache_path: str | None = None,
) -> list[dict]:
    """Fetch jobs from all sources and return a flat normalized list.

    Greenhouse, Lever, and Ashby are queried per-company using a thread pool.
    Jobicy, RemoteOK, Remotive, and other aggregators are queried once globally.
    If dice_cache_path is provided, pre-fetched Dice jobs are loaded from that file.
    """
    all_jobs: list[dict] = []
    failed_companies: list[str] = []

    # ── Direct ATS sources (concurrent) ───────────────────────────────────────

    greenhouse_companies = [c for c in companies if c.get("greenhouse_slug")]
    lever_companies = [c for c in companies if c.get("lever_slug")]
    ashby_companies = [c for c in companies if c.get("ashby_slug")]

    total_direct = len(greenhouse_companies) + len(lever_companies) + len(ashby_companies)
    if verbose:
        print(
            f"[Direct ATS] {len(greenhouse_companies)} Greenhouse + "
            f"{len(lever_companies)} Lever + "
            f"{len(ashby_companies)} Ashby companies "
            f"({total_direct} total, fetching concurrently)..."
        )

    def _fetch_company(company: dict, ats: str) -> tuple[str, list[dict]]:
        try:
            if ats == "greenhouse":
                return company["name"], fetch_greenhouse_jobs(company)
            elif ats == "lever":
                return company["name"], fetch_lever_jobs(company)
            elif ats == "ashby":
                return company["name"], fetch_ashby_jobs(company)
        except Exception as exc:
            return company["name"], [{"__error__": str(exc)}]
        return company["name"], []

    tasks = (
        [(c, "greenhouse") for c in greenhouse_companies]
        + [(c, "lever") for c in lever_companies]
        + [(c, "ashby") for c in ashby_companies]
    )

    # Use up to 20 threads — enough concurrency without hammering servers
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {
            executor.submit(_fetch_company, company, ats): (company["name"], ats)
            for company, ats in tasks
        }
        for future in as_completed(futures):
            name, ats = futures[future]
            try:
                company_name, jobs = future.result()
                # Check for error sentinel
                if jobs and isinstance(jobs[0], dict) and "__error__" in jobs[0]:
                    failed_companies.append(f"{company_name} ({ats}: {jobs[0]['__error__']})")
                else:
                    if verbose and jobs:
                        print(f"  [{ats}] {company_name}: {len(jobs)} jobs")
                    all_jobs.extend(jobs)
            except Exception as exc:
                failed_companies.append(f"{name} ({ats}: {exc})")

    if verbose:
        print(f"  Direct ATS total: {len(all_jobs)} raw jobs")

    # ── Aggregator sources ─────────────────────────────────────────────────────

    if verbose:
        print("[Jobicy] Fetching remote ML/AI jobs...")
    try:
        jobs = fetch_jobicy_jobs()
        if verbose:
            print(f"  {len(jobs)} jobs found")
        all_jobs.extend(jobs)
    except Exception as exc:
        failed_companies.append(f"Jobicy ({exc})")

    if verbose:
        print("[RemoteOK] Fetching remote jobs...")
    try:
        jobs = fetch_remoteok_jobs()
        if verbose:
            print(f"  {len(jobs)} jobs found")
        all_jobs.extend(jobs)
    except Exception as exc:
        failed_companies.append(f"RemoteOK ({exc})")

    if verbose:
        print("[Remotive] Fetching remote ML/AI jobs (data + software-dev categories)...")
    try:
        jobs = fetch_remotive_jobs()
        if verbose:
            print(f"  {len(jobs)} jobs found")
        all_jobs.extend(jobs)
    except Exception as exc:
        failed_companies.append(f"Remotive ({exc})")

    if verbose:
        print("[Himalayas] Fetching remote ML/AI jobs by skill...")
    try:
        jobs = fetch_himalayas_jobs()
        if verbose:
            print(f"  {len(jobs)} jobs found")
        all_jobs.extend(jobs)
    except Exception as exc:
        failed_companies.append(f"Himalayas ({exc})")

    if verbose:
        print("[Working Nomads] Fetching remote jobs...")
    try:
        jobs = fetch_workingnomads_jobs()
        if verbose:
            print(f"  {len(jobs)} jobs found")
        all_jobs.extend(jobs)
    except Exception as exc:
        failed_companies.append(f"WorkingNomads ({exc})")

    if verbose:
        print("[Arbeit Now] Fetching remote jobs...")
    try:
        jobs = fetch_arbeitnow_jobs()
        if verbose:
            print(f"  {len(jobs)} jobs found")
        all_jobs.extend(jobs)
    except Exception as exc:
        failed_companies.append(f"ArbeitNow ({exc})")

    if verbose:
        print("[HN Hiring] Fetching remote ML/AI jobs from 'Who is hiring?' thread...")
    try:
        jobs = fetch_hn_hiring_jobs()
        if verbose:
            print(f"  {len(jobs)} jobs found")
        all_jobs.extend(jobs)
    except Exception as exc:
        failed_companies.append(f"HN Hiring ({exc})")

    if dice_cache_path:
        if verbose:
            print(f"[Dice] Loading cache from {dice_cache_path}...")
        try:
            jobs = load_dice_cache(dice_cache_path)
            if verbose:
                print(f"  {len(jobs)} jobs loaded")
            all_jobs.extend(jobs)
        except Exception as exc:
            failed_companies.append(f"Dice cache ({exc})")

    if failed_companies:
        print(f"\n[WARN] Failed sources ({len(failed_companies)}): {', '.join(failed_companies[:20])}")
        if len(failed_companies) > 20:
            print(f"  ... and {len(failed_companies) - 20} more")

    return all_jobs
