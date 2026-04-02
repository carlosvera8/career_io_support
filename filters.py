# filters.py
#
# Pure filtering functions — no I/O, no side effects.
# All functions accept a normalized job dict (see scraper.py for schema).

import re

# ── Title matching ─────────────────────────────────────────────────────────────

TITLE_PATTERN = re.compile(
    r"(data\s+scientist"
    r"|machine\s+learning"
    r"|ml\s+engineer"
    r"|ml\s+researcher"
    r"|ai\s+engineer"
    r"|ai\s+researcher"
    r"|applied\s+(ml\s+)?scientist"
    r"|research\s+scientist"
    r"|applied\s+research"
    r"|nlp\s+engineer"
    r"|nlp\s+researcher"
    r"|computer\s+vision\s+engineer"
    r"|deep\s+learning"
    r"|mlops"
    r"|ml\s+ops"
    r"|llm\s+engineer"
    r"|generative\s+ai"
    r"|gen\s*ai"
    r"|quantitative\s+(researcher|scientist|analyst)"
    r"|quant\s+(researcher|scientist|analyst)"
    r"|staff\s+data\s+scientist"
    r"|principal\s+data\s+scientist"
    r"|senior\s+data\s+scientist"
    r"|lead\s+data\s+scientist"
    r"|data\s+science\s+lead"
    r"|algorithm\s+engineer"
    r"|decision\s+science"
    r"|reinforcement\s+learning"
    r"|rl\s+researcher"
    r"|multimodal"
    r"|foundation\s+model"
    r"|large\s+language\s+model"
    r"|ai\s+safety"
    r"|ai\s+alignment"
    r"|autonomous\s+(vehicle|driving|systems)"
    r"|robotics\s+engineer"
    r"|perception\s+engineer"
    r"|speech\s+(scientist|engineer|researcher)"
    r"|recommendation\s+system"
    r"|search\s+(scientist|engineer|researcher)"
    r"|ranking\s+engineer"
    r"|personalization\s+engineer"
    r"|forecast(ing)?\s+(scientist|engineer|researcher)"
    r"|causal\s+(inference|scientist)"
    r"|experimentation\s+(scientist|engineer)"
    r"|a/b\s+test"
    r"|computational\s+biolog"
    r"|bioinformatics"
    r"|genomics\s+(scientist|engineer|researcher))",
    re.IGNORECASE,
)


def matches_title(job: dict) -> bool:
    """Return True if the job title or tags match a target role."""
    title = job.get("job_title", "")
    tags = " ".join(job.get("tags", []))
    return bool(TITLE_PATTERN.search(title) or TITLE_PATTERN.search(tags))


# ── Remote detection ───────────────────────────────────────────────────────────

REMOTE_PATTERN = re.compile(
    r"\b(remote|anywhere|distributed|worldwide|work\s+from\s+home|wfh|global"
    r"|fully\s+remote|100%\s+remote|location\s+flexible|location.agnostic"
    r"|us[\s\-]remote|usa[\s\-]remote|north\s+america)\b",
    re.IGNORECASE,
)


def is_remote(job: dict) -> bool:
    """Return True if the job location, tags, or description indicate remote work."""
    location = job.get("location_raw", "")
    tags = " ".join(job.get("tags", []))
    if REMOTE_PATTERN.search(location) or REMOTE_PATTERN.search(tags):
        return True
    # Many Greenhouse postings leave location blank but say "Remote" in description
    if not location:
        description = job.get("description_text", "")[:2000]  # check first 2000 chars
        if REMOTE_PATTERN.search(description):
            return True
    return False


# ── Employment type ────────────────────────────────────────────────────────────

EXCLUDE_TYPE_PATTERN = re.compile(
    r"\b(contract|contractor|temp(orary)?|freelance|c2h|c2c|part[\s\-]?time|intern(ship)?|co[\s\-]?op)\b",
    re.IGNORECASE,
)

INCLUDE_TYPE_PATTERN = re.compile(
    r"\b(full[\s\-]?time|permanent|direct[\s\-]?hire|fte)\b",
    re.IGNORECASE,
)


def is_full_time(job: dict) -> bool:
    """Return True if the job appears to be full-time / direct hire.

    Logic:
    - If employment_type_raw explicitly matches an exclusion pattern → False
    - If employment_type_raw explicitly matches an inclusion pattern → True
    - If empty / ambiguous → True (most Greenhouse/Lever postings are FTE)
    Also scans the description for contract language as a secondary signal.
    """
    emp_type = job.get("employment_type_raw", "") or ""
    if EXCLUDE_TYPE_PATTERN.search(emp_type):
        return False
    if INCLUDE_TYPE_PATTERN.search(emp_type):
        return True

    # Fallback: check description for contract-only language
    description = job.get("description_text", "") or ""
    strong_contract = re.search(
        r"\b(this is a contract (role|position)|contract[\s\-]only|w2 contract|1099)\b",
        description,
        re.IGNORECASE,
    )
    return not bool(strong_contract)


# ── Salary extraction and threshold ───────────────────────────────────────────

# Matches patterns like: $200k, $200,000, $200K/yr, $150k-$200k, 200000 to 250000
_SALARY_NUMBER_PATTERN = re.compile(
    r"\$\s?(\d{1,3}(?:,\d{3})*|\d+)\s*([kK])?"
    r"(?:\s*[-–to]+\s*\$?\s?(\d{1,3}(?:,\d{3})*|\d+)\s*([kK])?)?",
    re.IGNORECASE,
)


def _parse_salary_number(num_str: str, k_suffix: str | None) -> int:
    """Convert a salary string like '200,000' or '200' (with k_suffix='k') to int."""
    value = int(num_str.replace(",", ""))
    if k_suffix and value < 10000:
        value *= 1000
    return value


def extract_salary_from_text(text: str) -> tuple[int | None, int | None]:
    """Extract the first salary range found in free text.

    Returns (min_salary, max_salary). Either may be None.
    """
    if not text:
        return None, None

    for match in _SALARY_NUMBER_PATTERN.finditer(text):
        low_str, low_k, high_str, high_k = match.groups()
        try:
            low = _parse_salary_number(low_str, low_k) if low_str else None
            high = _parse_salary_number(high_str, high_k) if high_str else None
            # Sanity check: salaries should be between $20k and $2M
            if low and not (20_000 <= low <= 2_000_000):
                continue
            if high and not (20_000 <= high <= 2_000_000):
                high = None
            if low:
                return low, high
        except (ValueError, TypeError):
            continue

    return None, None


def meets_salary_threshold(
    job: dict, threshold: int = 200_000, tolerance: int = 30_000
) -> tuple[bool | None, str]:
    """Check whether a job meets the salary threshold.

    Returns:
        (True,  salary_info_string)  — confirmed meets threshold
        (False, salary_info_string)  — confirmed does NOT meet threshold
        (None,  "unknown")           — salary not found; caller should try Levels.fyi
    """
    # 1. Structured salary fields (Jobicy, RemoteOK provide these)
    s_min = job.get("salary_min")
    s_max = job.get("salary_max")
    if s_min is not None or s_max is not None:
        best = max(v for v in (s_min, s_max) if v is not None)
        salary_str = _format_salary_range(s_min, s_max) + " (listed)"
        # Allow tolerance — base salary near threshold likely = $200k+ TC with equity/bonus
        return best >= (threshold - tolerance), salary_str

    # 2. Regex extraction from description text
    text_min, text_max = extract_salary_from_text(job.get("description_text", ""))
    if text_min is not None or text_max is not None:
        best = max(v for v in (text_min, text_max) if v is not None)
        salary_str = _format_salary_range(text_min, text_max) + " (listed)"
        return best >= (threshold - tolerance), salary_str

    return None, "unknown"


def _format_salary_range(low: int | None, high: int | None) -> str:
    if low and high:
        return f"${low:,} - ${high:,}"
    if low:
        return f"${low:,}+"
    if high:
        return f"up to ${high:,}"
    return "unknown"


# ── Combined filter ────────────────────────────────────────────────────────────

def apply_all_filters(job: dict, company_names: set[str]) -> bool:
    """Run title, remote, full-time, and company-list filters.

    For aggregator sources (jobicy, remoteok, remotive) the company-list filter
    is skipped — those sources are already category-filtered by the API.

    Salary is intentionally excluded here — it's handled in main.py.
    """
    is_aggregator = job.get("is_aggregator", False)

    # Company list filter applies only to direct ATS sources
    if not is_aggregator:
        if job.get("company_name", "").lower().strip() not in company_names:
            return False

    if not matches_title(job):
        return False

    if not is_remote(job):
        return False

    if not is_full_time(job):
        return False

    return True
