import os

from api import GroqAPI
from scrapers import DocScraper


class AIService:
    def __init__(self):
        self.groq = GroqAPI()
        prompt_id = os.getenv("PROMPT_DOCUMENT_ID")
        self.docs = DocScraper(prompt_id, "BEGIN PROMPT")

        self._set_base_prompt()

    def _set_base_prompt(self):
        self.base_prompt = self.docs.get_content()

    def _get_prompt(self, data):
        if not self.base_prompt:
            self._set_base_prompt()

        return f"{self.base_prompt} {data}"

    def write_article(self, data):
        prompt = self._get_prompt(data)
        return self.groq.chat(prompt)
