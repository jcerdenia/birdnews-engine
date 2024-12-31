from api import brevo_api, ebird_api, groq_api, sanity_api, sheets_api
from scrapers import ebird_scraper

from .ai import AIService
from .checklist import ChecklistService
from .content import ContentService
from .email import EmailService

ai_service = AIService(groq_api, sheets_api)

content_service = ContentService(sanity_api)

checklist_service = ChecklistService(
    ebird_api,
    ebird_scraper,
    sheets_api,
    content_service,
)

email_service = EmailService(
    brevo_api,
    ai_service,
    content_service,
)
