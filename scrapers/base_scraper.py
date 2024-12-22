from bs4 import BeautifulSoup


class BaseScraper:
    PARSER = "html.parser"

    def scrape(self, content):
        return BeautifulSoup(content, self.PARSER)
