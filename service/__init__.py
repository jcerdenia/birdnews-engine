from api import ebird_api, groq_api, sanity_api
from scrapers import doc_scraper, ebird_scraper

from .ai import AIService
from .checklist import ChecklistService
from .content import ContentService

ai_service = AIService(groq_api, doc_scraper)

content_service = ContentService(sanity_api)

checklist_service = ChecklistService(
    ebird_api,
    ebird_scraper,
    content_service,
)
