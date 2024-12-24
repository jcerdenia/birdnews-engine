from bs4 import BeautifulSoup


class BaseScraper:
    PARSER = "html.parser"

    def _scrape(self, content):
        return BeautifulSoup(content, self.PARSER)
