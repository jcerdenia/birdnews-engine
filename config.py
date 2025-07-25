import os

from dotenv import load_dotenv


class Config:
    ENV_VARS = [
        "EBIRD_API_KEY",
        "EBIRD_REGION_CODE",
        "GROQ_API_KEY",
        "SANITY_API_KEY",
        "SANITY_PROJECT_ID",
        "BREVO_API_KEY",
        "BREVO_RECIPIENT_LIST_ID",
        "SPREADSHEET_ID",
        "EMAIL_WORKSHEET_IDX",
        "PROMPT_WORKSHEET_IDX",
        "CHECKLIST_WORKSHEET_IDX",
        "API_TOKEN",
        "TZ",
    ]

    def __init__(self):
        load_dotenv()

        for var in self.ENV_VARS:
            value = os.environ[var]

            if value.isnumeric():
                value = int(value)

            setattr(self, var, value)

    @classmethod
    def from_env(cls):
        return cls()
