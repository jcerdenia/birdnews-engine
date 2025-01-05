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
    worksheet_idx=0,
)

content_service = ContentService(sanity_api)

checklist_service = ChecklistService(
    ebird_api=ebird_api,
    ebird_scraper=ebird_scraper,
    sheets_api=sheets_api,
    content_service=content_service,
    worksheet_idx=1,
)

email_service = EmailService(
    brevo_api=brevo_api,
    sheets_api=sheets_api,
    ai_service=ai_service,
    content_service=content_service,
    recipient_list_id=int(os.getenv("BREVO_RECIPIENT_LIST_ID")),
    worksheet_idx=2,
)
