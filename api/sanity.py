from datetime import date

import requests

from misc.decorators import handle_error


class SanityAPI:
    DATASET = "production"

    def __init__(self, project_id, token):
        self.project_id = project_id
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

    @classmethod
    def from_config(cls, config):
        return cls(
            project_id=config.SANITY_PROJECT_ID,
            token=config.SANITY_API_KEY,
        )
