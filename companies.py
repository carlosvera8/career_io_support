# companies.py
#
# Curated list of companies to search for jobs.
# All entries have glassdoor_wlb_score >= 4.0.
#
# Fields:
#   name                    - Display name
#   greenhouse_slug         - Slug for boards-api.greenhouse.io/{slug}
#   lever_slug              - Slug for api.lever.co/v0/postings/{slug}
#   ashby_slug              - Slug for api.ashbyhq.com/posting-api/job-board/{slug}
#   glassdoor_wlb_score     - Glassdoor work-life balance score (0-5)
#   employee_count_estimate - Rough headcount
#   notes                   - Optional notes

COMPANIES = [

    # ── GREENHOUSE ────────────────────────────────────────────────────────────

    {"name": "Airbnb", "greenhouse_slug": "airbnb", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 6000, "notes": ""},
    {"name": "OpenAI", "greenhouse_slug": "openai", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 1500, "notes": ""},
    {"name": "Databricks", "greenhouse_slug": "databricks", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 5000, "notes": ""},
    {"name": "Reddit", "greenhouse_slug": "reddit", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 2000, "notes": ""},
    {"name": "Figma", "greenhouse_slug": "figma", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.5, "employee_count_estimate": 1200, "notes": ""},
    {"name": "Dropbox", "greenhouse_slug": "dropbox", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 2500, "notes": "Remote-first"},
    {"name": "HubSpot", "greenhouse_slug": "hubspot", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.5, "employee_count_estimate": 7000, "notes": ""},
    {"name": "Spotify", "greenhouse_slug": "spotify", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 9000, "notes": ""},
    {"name": "Zoom", "greenhouse_slug": "zoom", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 7000, "notes": ""},
    {"name": "Asana", "greenhouse_slug": "asana", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.4, "employee_count_estimate": 1700, "notes": ""},
    {"name": "Waymo", "greenhouse_slug": "waymo", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 2500, "notes": ""},
    {"name": "Roblox", "greenhouse_slug": "roblox", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 2000, "notes": ""},
    {"name": "Twilio", "greenhouse_slug": "twilio", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 6000, "notes": ""},
    {"name": "Qualtrics", "greenhouse_slug": "qualtrics", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 5000, "notes": ""},
    {"name": "Datadog", "greenhouse_slug": "datadog", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 5000, "notes": ""},
    {"name": "MongoDB", "greenhouse_slug": "mongodb", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 5000, "notes": ""},
    {"name": "Okta", "greenhouse_slug": "okta", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 6000, "notes": ""},
    {"name": "Plaid", "greenhouse_slug": "plaid", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 1000, "notes": ""},
    {"name": "Elastic", "greenhouse_slug": "elastic", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 3500, "notes": "Remote-first"},
    {"name": "HashiCorp", "greenhouse_slug": "hashicorp", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 2000, "notes": "Remote-first"},
    {"name": "Zendesk", "greenhouse_slug": "zendesk", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 6000, "notes": ""},
    {"name": "DocuSign", "greenhouse_slug": "docusign", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 7000, "notes": ""},
    {"name": "New Relic", "greenhouse_slug": "newrelic", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 2500, "notes": ""},
    {"name": "Dataiku", "greenhouse_slug": "dataiku", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 1000, "notes": "ML platform"},
    {"name": "Weights & Biases", "greenhouse_slug": "wandb", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.4, "employee_count_estimate": 500, "notes": "ML tooling"},
    {"name": "Cohere", "greenhouse_slug": "cohere", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 500, "notes": "AI/LLM"},
    {"name": "Nuro", "greenhouse_slug": "nuro", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 1000, "notes": "Autonomous delivery"},
    {"name": "Splunk", "greenhouse_slug": "splunk", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 8000, "notes": "Now Cisco subsidiary"},
    {"name": "Perplexity AI", "greenhouse_slug": "perplexityai", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 300, "notes": "AI search"},
    # New Greenhouse additions
    {"name": "Shopify", "greenhouse_slug": "shopify", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 12000, "notes": "Remote-first"},
    {"name": "Box", "greenhouse_slug": "box", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 2000, "notes": ""},
    {"name": "Atlassian", "greenhouse_slug": "atlassian", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 12000, "notes": "Team Anywhere (remote-first)"},
    {"name": "Canva", "greenhouse_slug": "canva", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.5, "employee_count_estimate": 4000, "notes": ""},
    {"name": "Notion", "greenhouse_slug": "notion", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 700, "notes": ""},
    {"name": "Airtable", "greenhouse_slug": "airtable", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 800, "notes": ""},
    {"name": "Miro", "greenhouse_slug": "miro", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.4, "employee_count_estimate": 1800, "notes": ""},
    {"name": "Grammarly", "greenhouse_slug": "grammarly", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 1000, "notes": ""},
    {"name": "Zapier", "greenhouse_slug": "zapier", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.5, "employee_count_estimate": 800, "notes": "Fully remote"},
    {"name": "Gusto", "greenhouse_slug": "gusto", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 2500, "notes": ""},
    {"name": "Benchling", "greenhouse_slug": "benchling", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 1000, "notes": "Life science R&D platform"},
    {"name": "Applied Intuition", "greenhouse_slug": "appliedintuition", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 500, "notes": "Autonomous vehicle software"},
    {"name": "Aurora Innovation", "greenhouse_slug": "aurora", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 1500, "notes": "Self-driving trucks"},
    {"name": "Planet Labs", "greenhouse_slug": "planetlabs", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 900, "notes": "Earth observation / geospatial ML"},
    {"name": "Recursion Pharmaceuticals", "greenhouse_slug": "recursionpharma", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 600, "notes": "AI drug discovery"},
    {"name": "Checkr", "greenhouse_slug": "checkr", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 1000, "notes": ""},
    {"name": "Oscar Health", "greenhouse_slug": "oscar", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 800, "notes": ""},
    {"name": "dbt Labs", "greenhouse_slug": "dbtlabs", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.4, "employee_count_estimate": 500, "notes": "Remote-first; data transformation platform"},
    {"name": "Pinecone", "greenhouse_slug": "pinecone", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 300, "notes": "Vector database; remote-first"},
    {"name": "Discord", "greenhouse_slug": "discord", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 600, "notes": ""},
    {"name": "Affirm", "greenhouse_slug": "affirm", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 2500, "notes": "BNPL fintech"},
    {"name": "Chime", "greenhouse_slug": "chime", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 1500, "notes": "Neobank"},
    {"name": "Opendoor", "greenhouse_slug": "opendoor", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 2000, "notes": ""},
    {"name": "Redfin", "greenhouse_slug": "redfin", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 2000, "notes": ""},
    {"name": "Zillow", "greenhouse_slug": "zillow", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 5000, "notes": ""},
    {"name": "Unity Technologies", "greenhouse_slug": "unity", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 7000, "notes": ""},
    {"name": "Riot Games", "greenhouse_slug": "riotgames", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 4000, "notes": ""},
    {"name": "Epic Games", "greenhouse_slug": "epicgames", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 5000, "notes": ""},
    {"name": "Toast", "greenhouse_slug": "toasttab", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 4000, "notes": "Restaurant tech"},
    {"name": "Procore", "greenhouse_slug": "procore", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 4000, "notes": "Construction tech"},
    {"name": "Freshworks", "greenhouse_slug": "freshworks", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 5000, "notes": ""},
    {"name": "Lattice", "greenhouse_slug": "lattice", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 600, "notes": "HR platform"},
    {"name": "Gong", "greenhouse_slug": "gong", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 1500, "notes": "Revenue intelligence"},
    {"name": "Mixpanel", "greenhouse_slug": "mixpanel", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 400, "notes": "Product analytics"},
    {"name": "Fivetran", "greenhouse_slug": "fivetran", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 1200, "notes": "Data integration"},
    {"name": "Airbyte", "greenhouse_slug": "airbyte", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 300, "notes": "Open-source data integration; remote-first"},
    {"name": "Monte Carlo", "greenhouse_slug": "montecarlodata", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 300, "notes": "Data observability"},
    {"name": "Pendo", "greenhouse_slug": "pendo", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 800, "notes": "Product analytics"},
    {"name": "FullStory", "greenhouse_slug": "fullstory", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 400, "notes": "Digital experience platform"},
    {"name": "Intercom", "greenhouse_slug": "intercom", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 800, "notes": "Customer messaging"},
    {"name": "Palo Alto Networks", "greenhouse_slug": "paloaltonetworks", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 14000, "notes": "Cybersecurity"},
    {"name": "CrowdStrike", "greenhouse_slug": "crowdstrike", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 8000, "notes": "Cybersecurity"},
    {"name": "Snyk", "greenhouse_slug": "snyk", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 1000, "notes": "Developer security"},
    {"name": "UiPath", "greenhouse_slug": "uipath", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 4000, "notes": "RPA / automation"},
    {"name": "Celonis", "greenhouse_slug": "celonis", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 3000, "notes": "Process mining"},
    {"name": "Postman", "greenhouse_slug": "postman", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 900, "notes": "API development"},
    {"name": "Collibra", "greenhouse_slug": "collibra", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 1000, "notes": "Data governance"},
    {"name": "Alation", "greenhouse_slug": "alation", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 500, "notes": "Data catalog"},
    {"name": "10x Genomics", "greenhouse_slug": "10xgenomics", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 700, "notes": "Genomics / biotech ML"},
    {"name": "Ginkgo Bioworks", "greenhouse_slug": "ginkgobioworks", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 700, "notes": "Synthetic biology"},
    {"name": "Moderna", "greenhouse_slug": "modernatx", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 5000, "notes": "mRNA biotech; strong ML in drug discovery"},
    {"name": "Illumina", "greenhouse_slug": "illumina", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 9000, "notes": "Genomics instrumentation"},
    {"name": "Marqeta", "greenhouse_slug": "marqeta", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 800, "notes": "Card issuing platform"},
    {"name": "SoFi", "greenhouse_slug": "sofi", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 4000, "notes": "Fintech"},
    {"name": "Block", "greenhouse_slug": "squareup", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 12000, "notes": "Formerly Square; remote-first"},
    {"name": "Joby Aviation", "greenhouse_slug": "joby", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 1500, "notes": "eVTOL / air taxi"},
    {"name": "Cruise", "greenhouse_slug": "cruise", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 2000, "notes": "Autonomous vehicle (GM subsidiary)"},
    {"name": "Zoox", "greenhouse_slug": "zoox", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 2000, "notes": "Autonomous vehicle (Amazon subsidiary)"},
    {"name": "AlphaSense", "greenhouse_slug": "alphasense", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 1000, "notes": "Market intelligence / NLP"},
    {"name": "Blend Labs", "greenhouse_slug": "blend360", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 500, "notes": "Mortgage / fintech"},
    {"name": "Loom", "greenhouse_slug": "loom", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 400, "notes": "Async video; now Atlassian"},
    {"name": "Culture Amp", "greenhouse_slug": "cultureamp", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 800, "notes": "HR analytics"},
    {"name": "Klaviyo", "greenhouse_slug": "klaviyo", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 2000, "notes": "Marketing automation"},
    {"name": "Braze", "greenhouse_slug": "braze", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 1800, "notes": "Customer engagement platform"},
    {"name": "Fastly", "greenhouse_slug": "fastly", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 1000, "notes": "Edge cloud"},
    {"name": "Thoughtworks", "greenhouse_slug": "thoughtworks", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 12000, "notes": "Tech consulting; strong data practice"},
    {"name": "EPAM Systems", "greenhouse_slug": "epam", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 55000, "notes": "Tech consulting"},
    {"name": "Globant", "greenhouse_slug": "globant", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 26000, "notes": "Tech services"},
    {"name": "Slalom", "greenhouse_slug": "slalom", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 13000, "notes": "Consulting / data analytics"},
    {"name": "Lucid Motors", "greenhouse_slug": "lucidmotors", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 7000, "notes": "EV manufacturer"},
    {"name": "Rivian", "greenhouse_slug": "rivian", "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 14000, "notes": "EV manufacturer"},

    # ── LEVER ─────────────────────────────────────────────────────────────────

    {"name": "Cloudflare", "greenhouse_slug": None, "lever_slug": "cloudflare", "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 3500, "notes": ""},
    {"name": "GitLab", "greenhouse_slug": None, "lever_slug": "gitlab", "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 2000, "notes": "Fully remote"},
    {"name": "PagerDuty", "greenhouse_slug": None, "lever_slug": "pagerduty", "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 1000, "notes": ""},
    {"name": "Confluent", "greenhouse_slug": None, "lever_slug": "confluent", "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 3000, "notes": ""},
    {"name": "Anthropic", "greenhouse_slug": None, "lever_slug": "anthropic", "ashby_slug": None, "glassdoor_wlb_score": 4.5, "employee_count_estimate": 1000, "notes": ""},
    {"name": "Duolingo", "greenhouse_slug": None, "lever_slug": "duolingo", "ashby_slug": None, "glassdoor_wlb_score": 4.4, "employee_count_estimate": 700, "notes": ""},
    {"name": "Replit", "greenhouse_slug": None, "lever_slug": "replit", "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 200, "notes": "AI-first IDE"},
    {"name": "Hugging Face", "greenhouse_slug": None, "lever_slug": "huggingface", "ashby_slug": None, "glassdoor_wlb_score": 4.5, "employee_count_estimate": 300, "notes": "Fully remote; ML hub"},
    {"name": "Mistral AI", "greenhouse_slug": None, "lever_slug": "mistral", "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 200, "notes": "LLM startup"},
    {"name": "Veeva Systems", "greenhouse_slug": None, "lever_slug": "veeva", "ashby_slug": None, "glassdoor_wlb_score": 4.4, "employee_count_estimate": 7000, "notes": "Healthcare SaaS; excellent WLB"},
    {"name": "Samsara", "greenhouse_slug": None, "lever_slug": "samsara", "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 3000, "notes": ""},
    {"name": "Amplitude", "greenhouse_slug": None, "lever_slug": "amplitude", "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 700, "notes": "Product analytics"},
    # New Lever additions
    {"name": "Remote.com", "greenhouse_slug": None, "lever_slug": "remote", "ashby_slug": None, "glassdoor_wlb_score": 4.5, "employee_count_estimate": 1000, "notes": "Fully remote company; HR platform"},
    {"name": "Outreach", "greenhouse_slug": None, "lever_slug": "outreach", "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 1200, "notes": "Sales engagement"},
    {"name": "Highspot", "greenhouse_slug": None, "lever_slug": "highspot", "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 1000, "notes": "Sales enablement"},
    {"name": "15Five", "greenhouse_slug": None, "lever_slug": "15five", "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 300, "notes": "Performance management; remote-first"},
    {"name": "Moveworks", "greenhouse_slug": None, "lever_slug": "moveworks", "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 600, "notes": "AI for IT support"},
    {"name": "Descript", "greenhouse_slug": None, "lever_slug": "descript", "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 200, "notes": "AI video/audio editing"},
    {"name": "Jasper", "greenhouse_slug": None, "lever_slug": "jasper", "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 300, "notes": "AI writing assistant"},
    {"name": "Writer", "greenhouse_slug": None, "lever_slug": "writer", "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 200, "notes": "Enterprise AI writing"},
    {"name": "Retool", "greenhouse_slug": None, "lever_slug": "retool", "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 500, "notes": "Low-code internal tools"},
    {"name": "Salesloft", "greenhouse_slug": None, "lever_slug": "salesloft", "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 1000, "notes": "Sales engagement"},
    {"name": "Clari", "greenhouse_slug": None, "lever_slug": "clari", "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 700, "notes": "Revenue operations AI"},
    {"name": "ServiceTitan", "greenhouse_slug": None, "lever_slug": "servicetitan", "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 2500, "notes": "Field service management"},
    {"name": "Gorgias", "greenhouse_slug": None, "lever_slug": "gorgias", "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 400, "notes": "Customer service AI"},
    {"name": "Customer.io", "greenhouse_slug": None, "lever_slug": "customerio", "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 300, "notes": "Fully remote; messaging platform"},
    {"name": "Front", "greenhouse_slug": None, "lever_slug": "frontapp", "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 400, "notes": "Shared inbox platform"},
    {"name": "Rudderstack", "greenhouse_slug": None, "lever_slug": "rudderstack", "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 300, "notes": "Data pipeline / CDP"},
    {"name": "Atlan", "greenhouse_slug": None, "lever_slug": "atlan", "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 400, "notes": "Data workspace"},
    {"name": "Linear", "greenhouse_slug": None, "lever_slug": "linear", "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 100, "notes": "Issue tracking; remote-first"},
    {"name": "Vercel", "greenhouse_slug": None, "lever_slug": "vercel", "ashby_slug": None, "glassdoor_wlb_score": 4.4, "employee_count_estimate": 400, "notes": "Frontend cloud; remote-first"},
    {"name": "PostHog", "greenhouse_slug": None, "lever_slug": "posthog", "ashby_slug": None, "glassdoor_wlb_score": 4.5, "employee_count_estimate": 100, "notes": "Fully remote; product analytics"},
    {"name": "Netlify", "greenhouse_slug": None, "lever_slug": "netlify", "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 400, "notes": "Web development platform; remote-first"},
    {"name": "Attentive", "greenhouse_slug": None, "lever_slug": "attentive", "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 1000, "notes": "Mobile marketing"},
    {"name": "Iterable", "greenhouse_slug": None, "lever_slug": "iterable", "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 500, "notes": "Cross-channel marketing"},
    {"name": "Weaviate", "greenhouse_slug": None, "lever_slug": "weaviate", "ashby_slug": None, "glassdoor_wlb_score": 4.4, "employee_count_estimate": 200, "notes": "Vector database; remote-first"},
    {"name": "Glean", "greenhouse_slug": None, "lever_slug": "glean", "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 500, "notes": "Enterprise AI search"},
    {"name": "Matillion", "greenhouse_slug": None, "lever_slug": "matillion", "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 500, "notes": "Data integration"},
    {"name": "Orca Security", "greenhouse_slug": None, "lever_slug": "orca-security", "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 500, "notes": "Cloud security"},
    {"name": "Wiz", "greenhouse_slug": None, "lever_slug": "wiz", "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 1500, "notes": "Cloud security"},

    # ── ASHBY ─────────────────────────────────────────────────────────────────
    # Many fast-growing AI/tech startups use Ashby ATS

    {"name": "Together AI", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": "together", "glassdoor_wlb_score": 4.3, "employee_count_estimate": 100, "notes": "AI inference platform"},
    {"name": "Groq", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": "groq", "glassdoor_wlb_score": 4.3, "employee_count_estimate": 300, "notes": "AI inference chips"},
    {"name": "ElevenLabs", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": "elevenlabs", "glassdoor_wlb_score": 4.3, "employee_count_estimate": 200, "notes": "AI voice synthesis"},
    {"name": "Sierra AI", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": "sierra", "glassdoor_wlb_score": 4.3, "employee_count_estimate": 200, "notes": "Customer AI"},
    {"name": "Imbue", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": "imbue", "glassdoor_wlb_score": 4.3, "employee_count_estimate": 100, "notes": "AI reasoning research"},
    {"name": "Runway ML", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": "runwayml", "glassdoor_wlb_score": 4.2, "employee_count_estimate": 200, "notes": "Generative AI for video"},
    {"name": "Magic.dev", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": "magic", "glassdoor_wlb_score": 4.2, "employee_count_estimate": 100, "notes": "AI coding assistant"},
    {"name": "Character AI", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": "character", "glassdoor_wlb_score": 4.2, "employee_count_estimate": 200, "notes": "Conversational AI"},
    {"name": "Fireworks AI", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": "fireworks-ai", "glassdoor_wlb_score": 4.2, "employee_count_estimate": 100, "notes": "AI model serving"},
    {"name": "Replicate", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": "replicate", "glassdoor_wlb_score": 4.4, "employee_count_estimate": 100, "notes": "ML model hosting"},
    {"name": "Modal Labs", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": "modal", "glassdoor_wlb_score": 4.3, "employee_count_estimate": 50, "notes": "Serverless GPU compute"},
    {"name": "Anyscale", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": "anyscale", "glassdoor_wlb_score": 4.5, "employee_count_estimate": 300, "notes": "Ray / distributed ML"},
    {"name": "Snorkel AI", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": "snorkelai", "glassdoor_wlb_score": 4.3, "employee_count_estimate": 200, "notes": "Data-centric AI / labeling"},
    {"name": "LangChain", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": "langchain", "glassdoor_wlb_score": 4.2, "employee_count_estimate": 50, "notes": "LLM application framework"},
    {"name": "Arc / The Browser Company", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": "thebrowsercompany", "glassdoor_wlb_score": 4.4, "employee_count_estimate": 100, "notes": "Web browser; strong remote culture"},
    {"name": "Livekit", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": "livekit", "glassdoor_wlb_score": 4.2, "employee_count_estimate": 50, "notes": "Real-time communications infrastructure"},
    {"name": "Vanta", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": "vanta", "glassdoor_wlb_score": 4.2, "employee_count_estimate": 500, "notes": "Security compliance automation"},
    {"name": "Astronomer", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": "astronomer", "glassdoor_wlb_score": 4.2, "employee_count_estimate": 400, "notes": "Apache Airflow managed; data orchestration"},
    {"name": "Hex Technologies", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": "hex", "glassdoor_wlb_score": 4.4, "employee_count_estimate": 100, "notes": "Collaborative data notebooks"},
    {"name": "Labelbox", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": "labelbox", "glassdoor_wlb_score": 4.1, "employee_count_estimate": 300, "notes": "AI training data platform"},
    {"name": "Scale AI", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": "scaleai", "glassdoor_wlb_score": 4.0, "employee_count_estimate": 1000, "notes": "AI data platform"},
    {"name": "Weights & Biases (Ashby)", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": "wandb", "glassdoor_wlb_score": 4.4, "employee_count_estimate": 500, "notes": "Try Ashby as fallback"},

    # ── AGGREGATOR-ONLY (own portals — caught via Jobicy / RemoteOK / Remotive) ─

    # Big Tech
    {"name": "Google", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 180000, "notes": "Own portal"},
    {"name": "Microsoft", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 220000, "notes": "Own portal"},
    {"name": "Meta", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 70000, "notes": "Own portal"},
    {"name": "Salesforce", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 70000, "notes": "Own portal"},
    {"name": "Adobe", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 30000, "notes": "Own portal"},
    {"name": "Nvidia", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 30000, "notes": "Own portal"},
    {"name": "LinkedIn", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 20000, "notes": "Microsoft subsidiary"},
    {"name": "Intuit", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 18000, "notes": ""},
    {"name": "ServiceNow", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 22000, "notes": ""},
    {"name": "Workday", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 18000, "notes": ""},
    {"name": "Qualcomm", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 51000, "notes": "Strong ML/AI chip research"},
    {"name": "Dell Technologies", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 120000, "notes": ""},
    {"name": "HP Inc", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 58000, "notes": ""},
    # Financial (WLB ≥ 4.0 only)
    {"name": "Visa", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 26000, "notes": "Strong ML team for fraud/payments"},
    {"name": "Mastercard", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 32000, "notes": "Strong data science and AI team"},
    {"name": "Fidelity Investments", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 70000, "notes": "Strong quant/ML team"},
    {"name": "Capital One", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 55000, "notes": "Tech-forward bank; strong data culture"},
    {"name": "American Express", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 77000, "notes": "Strong data science team"},
    # Healthcare / Pharma (WLB ≥ 4.0 only)
    {"name": "Johnson & Johnson", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 150000, "notes": "Strong data science and AI team"},
    {"name": "Pfizer", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 88000, "notes": "Strong ML in drug discovery"},
    {"name": "Merck", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.2, "employee_count_estimate": 68000, "notes": ""},
    {"name": "Eli Lilly", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.3, "employee_count_estimate": 43000, "notes": "Expanding AI/ML team"},
    {"name": "AbbVie", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 50000, "notes": ""},
    {"name": "Abbott Laboratories", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 115000, "notes": ""},
    {"name": "Bristol-Myers Squibb", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.1, "employee_count_estimate": 34000, "notes": ""},
    # Defense (WLB ≥ 4.0 only)
    {"name": "Lockheed Martin", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 114000, "notes": "Large ML/AI team (US citizenship often required)"},
    {"name": "Northrop Grumman", "greenhouse_slug": None, "lever_slug": None, "ashby_slug": None, "glassdoor_wlb_score": 4.0, "employee_count_estimate": 95000, "notes": ""},
]


def get_greenhouse_companies() -> list[dict]:
    """Return companies that have a Greenhouse slug."""
    return [c for c in COMPANIES if c.get("greenhouse_slug")]


def get_lever_companies() -> list[dict]:
    """Return companies that have a Lever slug."""
    return [c for c in COMPANIES if c.get("lever_slug")]


def get_ashby_companies() -> list[dict]:
    """Return companies that have an Ashby slug."""
    return [c for c in COMPANIES if c.get("ashby_slug")]


def get_high_wlb_companies(min_wlb: float = 4.0) -> list[dict]:
    """Return companies with glassdoor_wlb_score >= min_wlb."""
    return [c for c in COMPANIES if c.get("glassdoor_wlb_score", 0) >= min_wlb]


def get_all_company_names(min_wlb: float = 4.0) -> set[str]:
    """Return a lowercase set of company names for O(1) membership checks.

    Only includes companies with WLB score >= min_wlb.
    """
    return {c["name"].lower() for c in get_high_wlb_companies(min_wlb)}


def get_company_by_name(name: str) -> dict | None:
    """Case-insensitive lookup of a company entry by name."""
    name_lower = name.lower().strip()
    for c in COMPANIES:
        if c["name"].lower() == name_lower:
            return c
    return None
