from api import GroqAPI, SheetsAPI


class AIService:
    PROMPT_WORKSHEET_IDX = 0
    KEY_ARTICLE = "ARTICLE"
    KEY_CAMPAIGN = "CAMPAIGN"

    prompt_map = None

    def __init__(
        self,
        groq_api: GroqAPI,
        sheets_api: SheetsAPI,
    ):
        self.groq = groq_api
        self.sheets = sheets_api

    def _set_prompt_map(self):
        prompts = self.sheets.read(self.PROMPT_WORKSHEET_IDX)
        self.prompt_map = {k: v for k, v in prompts}

    def _get_prompt(self, key, data):
        if not self.prompt_map:
            self._set_prompt_map()

        return f"{self.prompt_map[key]} {data}"

    def write_article(self, data):
        prompt = self._get_prompt(self.KEY_ARTICLE, data)
        return self.groq.chat(prompt)

    def write_campaign_intro(self, titles):
        prompt = self._get_prompt(self.KEY_CAMPAIGN, titles)
        return self.groq.chat(prompt)
