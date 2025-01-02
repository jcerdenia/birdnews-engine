# PH Bird News Engine

This is the content engine behind [PH Bird News](https://ph.birdnews.xyz), an automated news feed of AI-generated birding reports. The engine itself is an orchestrator that initiates requests to various services, ending with the publication of articles to a content management system (in this case, Sanity).

## Architecture and Components

The system follows a modular architecture with the following main components:

### Services
1. **`AIService`:** Handles AI-powered article generation.
2. **`ChecklistService`:** Manages checklist data retrieval and validation.
3. **`ContentService`:** Publishes articles to Sanity.
4. **`EmailService`:** Automates email campaigns.

### Engine
The `Engine` class orchestrates the main workflow of the system, including:
- Reading checklist data
- Filtering incomplete or duplicate checklists
- Generating articles using `AIService`
- Publishing articles via `ContentService`
- Sending email campaigns with `EmailService`

The `run` method is the main entry point that executes the end-to-end process.

## How It Works
1. **Checklist Retrieval:**
   - Fetch eBird checklist IDs from `ChecklistService`.
   - Validate and filter checklists to ensure quality and uniqueness.

2. **Article Generation:**
   - Use `AIService` to create articles based on checklist data.

3. **Content Publishing:**
   - Publish generated articles using `ContentService`.

4. **Email Campaigns:**
   - At a specific hour, send a newsletter with a selection of the latest articles.

## Configuration

The following environment variables are required:

- `API_TOKEN`: the API key used to trigger an engine run via an API endpoint

- `EBIRD_API_KEY`: for fetching [eBird](https://ebird.org/) checklist data

- `GROQ_API_KEY`: for chat completions via [Groq](https://groq.com/)

- `SANITY_API_KEY`: for publishing articles to [Sanity](https://sanity.io/)

- `BREVO_API_KEY`: for creating and sending email campaigns via [Brevo](https://app.brevo.com/)

- `BREVO_SENDER_EMAIL_ADDRESS`: the email address from which to send newsletters

- `BREVO_RECIPIENT_LIST_ID`: List ID to send newsletters to

- `GOOGLE_APPLICATION_CREDENTIALS`: credentials for accessing resources on Google Cloud

- `SPREADSHEET_ID`: ID of Google spreadsheet that stores AI prompts and skipped checklist IDs


## Getting Started
1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the server:
```bash
gunicorn wsgi:app
```
4. Call the `/run` endpoint:
```
curl -X POST http://localhost:{PORT}/run \
-H "X-API-TOKEN: {API_TOKEN}"
```

Alternatively, simply run `main()`.

```
from engine import main

main()
```

