# Bird News Engine

This is an AI-powered content generation engine designed to drive a `birdnews.xyz` site, an automated news feed of birding reports. Currently only [PH Bird News](https://ph.birdnews.xyz) is in production, but the code is location-agnostic and can be adapted to any region of the world.

The engine itself is simply an orchestrator that initiates requests to various services, starting with data retrieval and ending with the publication of articles to a CMS. The external services are:

- [eBird](https://ebird.org), a platform for sharing bird observations, which provides the raw data from which articles are based.

- [Groq](https://groq.com), providing LLM access.

- [Sanity](https://sanity.io), a CMS, which stores the generated articles and handles content delivery.

- [Brevo](https://app.brevo.com), which handles email campaigns.

- Google Sheets, acting as a store for prompts, settings, and other simple data.

The basic workflow is like this:

1. Fetch eBird checklists, filtering out incomplete or duplicated information.
2. Use AI to generate articles based on the checklists.
3. Publish articles.
4. If at the right hour, send out email campaign containing a selection of recent articles.

A single end-to-end process is designed to be triggered by an API call to `/run`. PH Bird News uses a cron job to call this endpoint hourly, but the engine itself is unaware about scheduling.

## Getting Started

The following environment variables are required:

```
# Self-defined API token protecting the /run endpoint
API_TOKEN=

# The engine's time zone, e.g. Asia/Manila
TZ=

# API keys and secrets to external services
EBIRD_API_KEY=  
EBIRD_REGION_CODE=
GROQ_API_KEY=
SANITY_PROJECT_ID=
SANITY_API_KEY=
BREVO_API_KEY=
BREVO_RECIPIENT_LIST_ID=

# Path to .json file containing service account credentials
GOOGLE_APPLICATION_CREDENTIALS= 

# ID of Google sheet
SPREADSHEET_ID=

# Indices of individual worksheets
PROMPT_WORKSHEET_IDX=
EMAIL_WORKSHEET_IDX=
CHECKLIST_WORKSHEET_IDX=
```

After cloning the repository, installing the required packages, and setting up the environment variables, run the server:

```bash
gunicorn wsgi:app
```

Then call the `/run` endpoint:
```
curl -X POST http://localhost:{PORT}/run \
-H "X-API-TOKEN: {API_TOKEN}"
```

Alternatively, create an instance of `Engine` and call `run`.

```
from config import Config
from engine import Engine

config = Config.from_env()
engine = Engine.from_config(config)
engine.run()

```
