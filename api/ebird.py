import requests

from misc.decorators import handle_error


class EBirdAPI:
    CHECKLISTS_URL = "https://api.ebird.org/v2/product/lists/PH"

    def __init__(self, api_key):
        self.headers = {"x-ebirdapitoken": api_key}

    @handle_error
    def get_recent_checklists(self, max_results=200):
        response = requests.get(
            self.CHECKLISTS_URL,
            params={"maxResults": max_results},
            headers=self.headers,
        )

        return response.json()
