#!/usr/bin/env python3
# main.py
#
# CLI entry point for the job scraper.
#
# Usage:
#   python main.py                          # full run, print results
#   python main.py --output results.csv     # also save to CSV
#   python main.py --no-levels              # skip Levels.fyi lookups (faster)
#   python main.py --min-salary 250000      # raise the salary floor
#   python main.py --verbose                # print per-company fetch stats + skips
#
# Returns jobs that are:
#   - Remote, full-time, direct-hire
#   - Data scientist / ML / AI / applied scientist roles
#   - At companies on our curated WLB + size list
#   - Salary 200k+ (from posting or Levels.fyi estimate)

import argparse
import csv
import sys
from urllib.parse import urlparse, urlunparse

from companies import COMPANIES, get_all_company_names
from filters import apply_all_filters, meets_salary_threshold
from salary import get_levels_salary, parse_salary_estimate
from scraper import scrape_all_jobs


# ── Deduplication ──────────────────────────────────────────────────────────────

_SOURCE_PRIORITY = {"greenhouse": 0, "lever": 1, "jobicy": 2, "remoteok": 3}


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

    When duplicates exist, the record from the higher-priority source is kept:
    Greenhouse > Lever > Jobicy > RemoteOK
    """
    # Sort so higher-priority sources come first
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

    print(f"\n{'─' * 100}")
    print(f"  {'COMPANY':<20}  {'TITLE':<40}  {'SALARY':<25}  SOURCE")
    print(f"{'─' * 100}")

    for job in results:
        company = job.get("company_name", "")[:20]
        title = job.get("job_title", "")[:40]
        salary = job.get("salary_info", "unknown")[:25]
        source = job.get("source", "")
        url = job.get("url", "")
        print(f"  {company:<20}  {title:<40}  {salary:<25}  {source}")
        print(f"  {'':20}  {url}")
        print()

    print(f"{'─' * 100}")
    print(f"  {len(results)} job(s) found.")


def write_csv(results: list[dict], path: str) -> None:
    """Write results to a CSV file."""
    fieldnames = ["company_name", "job_title", "url", "salary_info", "source"]
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
        "--verbose", "-v",
        action="store_true",
        help="Print per-source fetch stats and reasons for skipped jobs.",
    )
    return parser.parse_args()


# ── Main pipeline ──────────────────────────────────────────────────────────────

def main() -> None:
    args = parse_args()
    company_names = get_all_company_names()

    # ── 1. Fetch ───────────────────────────────────────────────────────────────
    print("Fetching jobs...")
    all_jobs = scrape_all_jobs(COMPANIES, verbose=args.verbose)
    print(f"  {len(all_jobs)} total postings retrieved.")

    # ── 2. Apply title / remote / employment-type / company-list filters ───────
    candidates = []
    skip_counts = {"company": 0, "title": 0, "remote": 0, "employment": 0}

    for job in all_jobs:
        # Run each filter individually in verbose mode so we can report why
        if args.verbose:
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
    print("\nApplying salary filter..." + (" (Levels.fyi lookups enabled)" if not args.no_levels else " (--no-levels: skipping Levels.fyi)"))

    results = []
    for job in candidates:
        passes, salary_info = meets_salary_threshold(job, threshold=args.min_salary)

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
                # Estimate exists but unparseable — include with label
                job["salary_info"] = levels_salary
                results.append(job)
        else:
            # No Levels.fyi data — include with unknown label so user can decide
            job["salary_info"] = "unknown (not on Levels.fyi)"
            results.append(job)

    # ── 5. Output ──────────────────────────────────────────────────────────────
    print_results(results)

    if args.output:
        write_csv(results, args.output)


if __name__ == "__main__":
    main()
