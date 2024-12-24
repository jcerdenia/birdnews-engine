import requests

from misc.decorators import handle_error

from .base import BaseScraper


class DocScraper(BaseScraper):
    BASE_URL = "https://docs.google.com/document/d/e"

    @property
    def url(self):
        return f"{self.BASE_URL}/{self.document_id}"

    def _get_content(self, soup, separator):
        lines = soup.find("body").get_text(separator="\n").strip().split("\n")

        if separator in lines:
            index = lines.index(separator)
            return " ".join(lines[index + 1 :])

        return " ".join(lines)

    @handle_error
    def get_content(self, document_id, separator):
        url = f"{self.BASE_URL}/{document_id}"
        response = requests.get(url)

        soup = self._scrape(response.text)

        return self._get_content(soup, separator)
