import pydash

from api import GroqAPI, SheetsAPI


class AIService:
    PROMPT_WORKSHEET_IDX = 0
    KEY_ARTICLE = "ARTICLE"

    base_prompt = None

    def __init__(
        self,
        groq_api: GroqAPI,
        sheets_api: SheetsAPI,
    ):
        self.groq = groq_api
        self.sheets = sheets_api

    def _set_base_prompt(self):
        data = self.sheets.read(self.PROMPT_WORKSHEET_IDX)
        predicate = lambda i: i[0] == self.KEY_ARTICLE
        self.base_prompt = pydash.find(data, predicate)[1]

    def _get_prompt(self, data):
        if not self.base_prompt:
            self._set_base_prompt()

        return f"{self.base_prompt} {data}"

    def write_article(self, data):
        prompt = self._get_prompt(data)
        return self.groq.chat(prompt)
