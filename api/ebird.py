import os

import requests

from misc.decorators import handle_error


class _eBirdAPI:
    CHECKLISTS_URL = "https://api.ebird.org/v2/product/lists/PH"

    def __init__(self):
        self.headers = {"x-ebirdapitoken": os.getenv("EBIRD_API_KEY")}

    @handle_error
    def get_recent_checklists(self, max_results=200):
        response = requests.get(
            self.CHECKLISTS_URL,
            params={"maxResults": max_results},
            headers=self.headers,
        )

        return response.json()


eBirdAPI = _eBirdAPI()
