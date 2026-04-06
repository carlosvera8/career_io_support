# career_io_support

Find remote ML/AI/data science jobs at high work-life balance companies paying $200k+.

## Quick start

```bash
py main.py --output results.csv
```

## All options

```
py main.py [options]

  --output FILE         Save results to a CSV file
  --no-levels           Skip Levels.fyi salary lookups (faster)
  --min-salary AMOUNT   Minimum salary in USD (default: 200000)
  --min-wlb SCORE       Minimum Glassdoor WLB score for direct ATS companies (default: 4.0)
  --dice-cache FILE     Path to a dice_cache.json file (see below)
  --verbose, -v         Print per-source fetch stats and skip reasons
```

## Sources

The pipeline scrapes jobs from two categories of source:

**Direct ATS** (company-specific boards, filtered to curated high-WLB company list):
- Greenhouse, Lever, Ashby

**Aggregators** (broader job boards, filtered by title/remote/salary):
- Jobicy, RemoteOK, Remotive, Himalayas, Working Nomads, Arbeit Now, Dice (via cache)

## Dice integration (via Claude MCP)

Dice requires an extra step because it uses an MCP tool that only Claude can call — not a standalone Python script.

**Step 1 — Refresh the Dice cache (run inside Claude Code)**

Open this project in Claude Code and say:

> "refresh the Dice cache"

Claude will search Dice for remote full-time ML/AI roles across multiple keywords and write the results to `dice_cache.json`.

**Step 2 — Run the pipeline with the cache**

```bash
py main.py --dice-cache dice_cache.json --output results.csv
```

The cache is optional — omitting `--dice-cache` runs the pipeline as normal without Dice results. Refresh the cache whenever you want up-to-date Dice listings.
