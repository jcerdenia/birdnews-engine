import os

from api import GroqAPI
from scrapers import DocScraper


class AIService:
    def __init__(
        self,
        groq_api: GroqAPI,
        doc_scraper: DocScraper,
    ):
        self.groq = groq_api
        self.docs = doc_scraper

        self.prompt_id = os.getenv("PROMPT_DOCUMENT_ID")
        self.prompt_separator = "BEGIN PROMPT"
        self.base_prompt = None

    def _set_base_prompt(self):
        self.base_prompt = self.docs.get_content(
            self.prompt_id,
            self.prompt_separator,
        )

    def _get_prompt(self, data):
        if not self.base_prompt:
            self._set_base_prompt()

        return f"{self.base_prompt} {data}"

    def write_article(self, data):
        prompt = self._get_prompt(data)
        return self.groq.chat(prompt)
