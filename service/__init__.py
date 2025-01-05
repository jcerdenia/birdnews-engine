import os

from api import brevo_api, ebird_api, groq_api, sanity_api, sheets_api
from scrapers import ebird_scraper

from .ai import AIService
from .checklist import ChecklistService
from .content import ContentService
from .email import EmailService

ai_service = AIService(
    groq_api=groq_api,
    sheets_api=sheets_api,
    worksheet_idx=int(os.getenv("PROMPT_WORKSHEET_IDX")),
)

content_service = ContentService(sanity_api)

checklist_service = ChecklistService(
    ebird_api=ebird_api,
    ebird_scraper=ebird_scraper,
    sheets_api=sheets_api,
    content_service=content_service,
    worksheet_idx=int(os.getenv("CHECKLIST_WORKSHEET_IDX")),
)

email_service = EmailService(
    brevo_api=brevo_api,
    sheets_api=sheets_api,
    ai_service=ai_service,
    content_service=content_service,
    recipient_list_id=int(os.getenv("BREVO_RECIPIENT_LIST_ID")),
    worksheet_idx=int(os.getenv("EMAIL_WORKSHEET_IDX")),
)
