import requests

from misc.decorators import handle_error


class EBirdAPI:
    CHECKLISTS_BASE_URL = "https://api.ebird.org/v2/product/lists"

    def __init__(self, api_key, region_code):
        self.headers = {"x-ebirdapitoken": api_key}
        self.region_code = region_code

    @property
    def checklists_url(self):
        return f"{self.CHECKLISTS_BASE_URL}/{self.region_code}"

    @handle_error
    def get_recent_checklists(self, max_results=200):
        response = requests.get(
            self.checklists_url,
            params={"maxResults": max_results},
            headers=self.headers,
        )

        return response.json()

    @classmethod
    def from_config(cls, config):
        return cls(
            api_key=config.EBIRD_API_KEY,
            region_code=config.EBIRD_REGION_CODE,
        )
