import os
from datetime import date

import requests

from misc.decorators import handle_error


class SanityAPI:
    DATASET = "production"

    def __init__(self):
        self.project_id = os.getenv("SANITY_PROJECT_ID")
        token = os.getenv("SANITY_API_KEY")
        self.headers = {"Authorization": f"Bearer {token}"}

    @property
    def base_url(self):
        today = date.today().strftime("%Y-%m-%d")
        return f"https://{self.project_id}.api.sanity.io/v{today}/data"

    @handle_error
    def query(self, query_str):
        response = requests.get(
            url=f"{self.base_url}/query/{self.DATASET}",
            params={"query": query_str},
            headers=self.headers,
        )

        return response.json()

    @handle_error
    def mutate(self, data):
        response = requests.post(
            url=f"{self.base_url}/mutate/{self.DATASET}",
            json=data,
            headers=self.headers,
        )

        return response.json()
