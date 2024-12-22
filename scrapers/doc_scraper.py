import requests

from misc.decorators import handle_error

from .base_scraper import BaseScraper


class DocScraper(BaseScraper):
    BASE_URL = "https://docs.google.com/document/d/e"

    def __init__(self, document_id, separator):
        self.document_id = document_id
        self.separator = separator

    @property
    def url(self):
        return f"{self.BASE_URL}/{self.document_id}"

    def _get_content(self, soup):
        lines = soup.find("body").get_text(separator="\n").strip().split("\n")

        if self.separator in lines:
            index = lines.index(self.separator)
            return " ".join(lines[index + 1 :])

        return " ".join(lines)

    @handle_error
    def get_content(self):
        response = requests.get(self.url)
        soup = self.scrape(response.text)

        return self._get_content(soup)
