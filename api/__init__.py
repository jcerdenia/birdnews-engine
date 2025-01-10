import os

from .brevo import BrevoAPI
from .ebird import EBirdAPI
from .groq import GroqAPI
from .sanity import SanityAPI
from .sheets import SheetsAPI

brevo_api = BrevoAPI(os.getenv("BREVO_API_KEY"))

ebird_api = EBirdAPI(
    api_key=os.getenv("EBIRD_API_KEY"),
    region_code=os.getenv("EBIRD_REGION_CODE"),
)

groq_api = GroqAPI(os.getenv("GROQ_API_KEY"))

sanity_api = SanityAPI(
    project_id=os.getenv("SANITY_PROJECT_ID"),
    token=os.getenv("SANITY_API_KEY"),
)

sheets_api = SheetsAPI(os.getenv("SPREADSHEET_ID"))
