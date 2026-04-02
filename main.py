#!/usr/bin/env python3
# main.py
#
# CLI entry point for the job scraper.
#
# Usage:
#   py -3 main.py                          # full run, print results
#   py -3 main.py --output results.csv     # also save to CSV
#   py -3 main.py --no-levels              # skip Levels.fyi lookups (faster)
#   py -3 main.py --min-salary 200000      # salary floor (default 200k)
#   py -3 main.py --min-wlb 4.0           # WLB floor for direct ATS companies
#   py -3 main.py --verbose                # print per-company fetch stats + skips
#
# Returns jobs that are:
#   - Remote, full-time, direct-hire
#   - Data scientist / ML / AI / applied scientist / MLOps / LLM roles
#   - At companies with Glassdoor WLB >= 4.0 (direct ATS), or any company (aggregators)
#   - Salary 200k+ (from posting or Levels.fyi estimate), or unknown (included)

import argparse
import csv
import sys
from urllib.parse import urlparse, urlunparse

from companies import get_high_wlb_companies, get_all_company_names
from filters import apply_all_filters, meets_salary_threshold
from salary import get_levels_salary, parse_salary_estimate
from scraper import scrape_all_jobs


# ── Deduplication ──────────────────────────────────────────────────────────────

_SOURCE_PRIORITY = {
    "greenhouse": 0,
    "lever": 1,
    "ashby": 2,
    "jobicy": 3,
    "remoteok": 4,
    "remotive": 5,
}


def _normalize_url(url: str) -> str:
    """Strip query params and trailing slash for stable URL comparison."""
    try:
        parsed = urlparse(url)
        return urlunparse(
            (parsed.scheme, parsed.netloc, parsed.path.rstrip("/"), "", "", "")
        )
    except Exception:
        return url.strip().rstrip("/")


def deduplicate(jobs: list[dict]) -> list[dict]:
    """Remove duplicate jobs across sources.

    Deduplication keys (in order):
    1. Normalized URL
    2. (company_name_lower, job_title_lower) pair

    When duplicates exist, the record from the higher-priority source is kept.
    """
    sorted_jobs = sorted(
        jobs, key=lambda j: _SOURCE_PRIORITY.get(j.get("source", ""), 99)
    )

    seen_urls: dict[str, dict] = {}
    seen_title_company: dict[tuple, dict] = {}
    unique: list[dict] = []

    for job in sorted_jobs:
        url_key = _normalize_url(job.get("url", ""))
        title_key = (
            job.get("company_name", "").lower().strip(),
            job.get("job_title", "").lower().strip(),
        )

        if url_key and url_key in seen_urls:
            continue
        if title_key[1] and title_key in seen_title_company:
            continue

        if url_key:
            seen_urls[url_key] = job
        if title_key[1]:
            seen_title_company[title_key] = job
        unique.append(job)

    return unique


# ── Output ─────────────────────────────────────────────────────────────────────

def print_results(results: list[dict]) -> None:
    """Print a formatted table of job results to stdout."""
    if not results:
        print("\nNo jobs found matching your criteria.")
        return

    sep = "-" * 110
    print(f"\n{sep}")
    print(f"  {'COMPANY':<25}  {'TITLE':<45}  {'SALARY':<22}  SOURCE")
    print(sep)

    for job in results:
        company = job.get("company_name", "")[:25]
        title = job.get("job_title", "")[:45]
        salary = job.get("salary_info", "unknown")[:22]
        source = job.get("source", "")
        url = job.get("url", "")
        # Use ascii-safe output to avoid Windows cp1252 errors
        line = f"  {company:<25}  {title:<45}  {salary:<22}  {source}"
        try:
            print(line)
            print(f"  {'':25}  {url}")
        except UnicodeEncodeError:
            print(line.encode("ascii", "replace").decode("ascii"))
            print(f"  {'':25}  {url}".encode("ascii", "replace").decode("ascii"))
        print()

    print(sep)
    print(f"  {len(results)} job(s) found.")


def write_csv(results: list[dict], path: str) -> None:
    """Write results to a CSV file."""
    fieldnames = ["company_name", "job_title", "url", "salary_info", "source", "glassdoor_wlb"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)
    print(f"\nResults saved to: {path}")


# ── Argument parsing ───────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find remote ML/AI jobs at high-WLB companies paying $200k+."
    )
    parser.add_argument(
        "--output", "-o",
        metavar="FILE",
        help="Save results to a CSV file at this path.",
    )
    parser.add_argument(
        "--no-levels",
        action="store_true",
        help="Skip Levels.fyi salary lookups (faster, but more 'unknown' salaries).",
    )
    parser.add_argument(
        "--min-salary",
        type=int,
        default=200_000,
        metavar="AMOUNT",
        help="Minimum salary threshold in USD (default: 200000).",
    )
    parser.add_argument(
        "--min-wlb",
        type=float,
        default=4.0,
        metavar="SCORE",
        help="Minimum Glassdoor WLB score for direct ATS companies (default: 4.0).",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print per-source fetch stats and reasons for skipped jobs.",
    )
    return parser.parse_args()


# ── Main pipeline ──────────────────────────────────────────────────────────────

def main() -> None:
    args = parse_args()

    # Companies with WLB >= threshold (used for direct ATS and for name-matching aggregator results)
    wlb_companies = get_high_wlb_companies(args.min_wlb)
    company_names = get_all_company_names(args.min_wlb)

    print(f"Company list: {len(wlb_companies)} companies with WLB >= {args.min_wlb}")
    greenhouse_count = sum(1 for c in wlb_companies if c.get("greenhouse_slug"))
    lever_count = sum(1 for c in wlb_companies if c.get("lever_slug"))
    ashby_count = sum(1 for c in wlb_companies if c.get("ashby_slug"))
    print(
        f"  Direct ATS: {greenhouse_count} Greenhouse, {lever_count} Lever, {ashby_count} Ashby"
    )

    # ── 1. Fetch ───────────────────────────────────────────────────────────────
    print("\nFetching jobs (concurrent for direct ATS sources)...")
    all_jobs = scrape_all_jobs(wlb_companies, verbose=args.verbose)
    print(f"  {len(all_jobs)} total raw postings retrieved.")

    # ── 2. Apply title / remote / employment-type / company-list filters ───────
    candidates = []
    skip_counts = {
        "company": 0, "title": 0, "remote": 0, "employment": 0,
    }

    for job in all_jobs:
        is_aggregator = job.get("is_aggregator", False)

        if args.verbose:
            # Verbose: track skip reasons individually
            if not is_aggregator:
                company_ok = job.get("company_name", "").lower().strip() in company_names
                if not company_ok:
                    skip_counts["company"] += 1
                    continue

            from filters import matches_title, is_remote, is_full_time
            if not matches_title(job):
                skip_counts["title"] += 1
                continue
            if not is_remote(job):
                skip_counts["remote"] += 1
                continue
            if not is_full_time(job):
                skip_counts["employment"] += 1
                continue
            candidates.append(job)
        else:
            if apply_all_filters(job, company_names):
                candidates.append(job)

    if args.verbose:
        print(
            f"\n  Filtered out: {skip_counts['company']} wrong company, "
            f"{skip_counts['title']} wrong title, "
            f"{skip_counts['remote']} not remote, "
            f"{skip_counts['employment']} not full-time."
        )
    print(f"  {len(candidates)} candidates after filtering.")

    # ── 3. Deduplicate ─────────────────────────────────────────────────────────
    candidates = deduplicate(candidates)
    print(f"  {len(candidates)} candidates after deduplication.")

    # ── 4. Salary filter + Levels.fyi fallback ─────────────────────────────────
    levels_label = " (Levels.fyi lookups enabled)" if not args.no_levels else " (--no-levels: skipping Levels.fyi)"
    print(f"\nApplying salary filter...{levels_label}")

    results = []
    for job in candidates:
        passes, salary_info = meets_salary_threshold(job, threshold=args.min_salary, tolerance=30_000)

        # Attach WLB score for CSV output
        job["glassdoor_wlb"] = ""
        from companies import get_company_by_name
        company_entry = get_company_by_name(job.get("company_name", ""))
        if company_entry:
            job["glassdoor_wlb"] = company_entry.get("glassdoor_wlb_score", "")

        if passes is True:
            job["salary_info"] = salary_info
            results.append(job)
            continue

        if passes is False:
            if args.verbose:
                print(f"  SKIP (salary too low): {job['company_name']} — {job['job_title']} ({salary_info})")
            continue

        # passes is None: salary unknown — try Levels.fyi unless --no-levels
        if args.no_levels:
            job["salary_info"] = "unknown (salary not listed)"
            results.append(job)
            continue

        if args.verbose:
            print(f"  Querying Levels.fyi for: {job['company_name']} / {job['job_title']}")

        levels_salary = get_levels_salary(job["company_name"], job["job_title"])
        if levels_salary:
            estimated = parse_salary_estimate(levels_salary)
            if estimated and estimated >= args.min_salary:
                job["salary_info"] = levels_salary
                results.append(job)
            elif estimated and estimated < args.min_salary:
                if args.verbose:
                    print(f"  SKIP (Levels.fyi estimate below threshold): {job['company_name']} — {levels_salary}")
            else:
                job["salary_info"] = levels_salary
                results.append(job)
        else:
            job["salary_info"] = "unknown (not on Levels.fyi)"
            results.append(job)

    # ── 5. Output ──────────────────────────────────────────────────────────────
    print_results(results)

    if args.output:
        write_csv(results, args.output)


if __name__ == "__main__":
    main()
