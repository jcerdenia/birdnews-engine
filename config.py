import os

from dotenv import load_dotenv


class Config:
    EBIRD_API_KEY = None
    EBIRD_REGION_CODE = None
    GROQ_API_KEY = None
    SANITY_API_KEY = None
    SANITY_PROJECT_ID = None
    BREVO_API_KEY = None
    BREVO_RECIPIENT_LIST_ID = None
    SPREADSHEET_ID = None
    EMAIL_WORKSHEET_IDX = None
    PROMPT_WORKSHEET_IDX = None
    CHECKLIST_WORKSHEET_IDX = None
    API_TOKEN = None
    TZ = None

    def __init__(self):
        load_dotenv()

        for var in self.get_env_vars():
            value = os.environ[var]

            if value.isnumeric():
                value = int(value)

            setattr(self, var, value)

    @classmethod
    def get_env_vars(cls):
        return [
            key
            for key, value in vars(cls).items()
            if not key.startswith("_") and value is None
        ]

    @classmethod
    def from_env(cls):
        return cls()
