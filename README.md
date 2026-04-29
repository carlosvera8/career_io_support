# career_io_support

Find remote, US-eligible ML/AI/data science jobs at high work-life balance companies paying $200k+.

## Quick start

```bash
run.bat
```

> **Note:** Always use `run.bat` instead of `python main.py`. The script requires the project's virtual environment (`venv/`), and running it with your system Python will fail because `lxml` is only installed in the venv.
>
> **PowerShell users:** Run `.\run.bat` (with the `.\` prefix). PowerShell won't find `run.bat` without it.

Results are always saved to `output/results_YYYYMMDD_HHMMSS.csv` so past runs are never overwritten.

## All options

```
run.bat [options]

  --no-levels           Skip Levels.fyi salary lookups (faster)
  --min-salary AMOUNT   Minimum salary in USD (default: 200000)
  --min-wlb SCORE       Minimum Glassdoor WLB score for direct ATS companies (default: 4.0)
  --no-us-filter        Include roles not explicitly open to US applicants (worldwide search)
  --dice-cache FILE     Path to a dice_cache.json file (see below)
  --verbose, -v         Print per-source fetch stats and skip reasons
```

## Sources

The pipeline scrapes jobs from two categories of source:

**Direct ATS** (company-specific boards, filtered to curated high-WLB company list of 300+ companies):
- Greenhouse, Lever, Ashby

**Aggregators** (broader job boards, filtered by title/remote/salary):
- Jobicy, RemoteOK, Remotive, Himalayas, Working Nomads, Arbeit Now, HN "Who's Hiring" (official HN API), Dice (via cache)

All results are filtered to US-eligible roles by default (drops jobs restricted to Europe, UK, APAC, EMEA, etc.). Use `--no-us-filter` to include worldwide listings.

## Dice integration (via Claude MCP)

Dice requires an extra step because it uses an MCP tool that only Claude can call — not a standalone Python script.

**Step 1 — Refresh the Dice cache (run inside Claude Code)**

Open this project in Claude Code and say:

> "refresh the Dice cache"

Claude will search Dice for remote full-time ML/AI roles across multiple keywords and write the results to `output/dice_cache.json`.

**Step 2 — Run the pipeline with the cache**

```bash
.\run.bat --dice-cache output/dice_cache.json
```

The cache is optional — omitting `--dice-cache` runs the pipeline as normal without Dice results. Refresh the cache whenever you want up-to-date Dice listings.
