import re

import requests
from bs4 import BeautifulSoup

from misc.decorators import handle_error


class eBirdScraper:
    BASE_URL = "https://ebird.org/checklist"

    EFFORT_COMPLETE = "complete"
    EFFORT_KEYS = ["protocol", "observers", "duration", "distance"]

    def __init__(self):
        self.primary_detail_parsers = [
            self._parse_datetime,
            self._parse_location,
            self._parse_region,
        ]

        self.general_detail_parsers = [
            self._parse_checklist_comments,
            self._parse_participants,
            self._parse_species_count,
            self._parse_observations,
        ]

    @staticmethod
    def _parse_checklist_type(soup):
        status_info_button = soup.find("button", attrs={"aria-controls": "status-info"})
        return status_info_button.get_text(strip=True)

    @staticmethod
    def _parse_datetime(section):
        date, time = section.find("time").get("datetime").split("T")
        return {"date": date, "time": time}

    @staticmethod
    def _parse_location(section):
        location = section.find("div", attrs={"data-locationname": True}).get_text()
        return {"location": location}

    @staticmethod
    def _parse_region(section):
        region_list = section.find("span", text="Region").find_next("ul")
        values = [li.get_text(strip=True) for li in region_list.find_all("li")]
        province, country = values
        return {"province": province, "country": country}

    @staticmethod
    def _parse_checklist_comments(soup):
        tag = soup.find("h3", id="checklist-comments")
        comments = tag.find_next("p").get_text(strip=True) if tag else None
        return {"comments": comments} if comments else {}

    @staticmethod
    def _parse_species_count(soup):
        count = soup.find("span", class_="StatsIcon-stat-count").get_text()
        return {"species_count": int(count) if count.isdigit() else count}

    @staticmethod
    def _parse_participants(soup):
        return {
            "participants": [
                p.get_text().title()
                for p in soup.find_all(
                    "span",
                    attrs={"data-participant-userdisplayname": True},
                )
            ]
        }

    @staticmethod
    def _parse_observations(soup):
        observations = []

        for ele in soup.find_all("section", class_="Observation"):
            species = ele.find("span", class_="Heading-main").get_text()
            if " sp." in species:
                continue

            count_span = ele.find("span", string=re.compile("Number observed"))
            count = count_span.find_next_sibling("span").get_text(strip=True)

            comment_tag = ele.find("h4", string=re.compile("Details"))
            comment = (
                comment_tag.find_next().get_text(strip=True) if comment_tag else None
            )

            observations.append(
                {
                    "species": species,
                    "count": int(count) if count.isdigit() else count,
                    **({"comment": comment} if comment else {}),
                }
            )

        return {"observations": observations}

    @staticmethod
    def _parse(ele, handlers):
        data = {}
        for func in handlers:
            try:
                data.update(**func(ele))
            except Exception as e:
                print(f"Error in {func.__name__}: {e}")

        return data

    def _parse_primary_details(self, soup):
        section = soup.find(
            "section",
            attrs={"aria-labelledby": "primary-details"},
        )

        return self._parse(section, self.primary_detail_parsers)

    def _parse_effort_details(self, soup):
        section = soup.find(
            "section",
            attrs={"aria-labelledby": "other-details-effort"},
        )

        details = {}
        for key in self.EFFORT_KEYS:
            try:
                string = re.compile(key.capitalize())
                span = section.find("span", string=string).find_next()
                value = span.get_text() if span else None
                details[key] = int(value) if value.isdigit() else value
            except Exception as e:
                print(f"Error parsing {key}: {e}")

        return details

    def _parse_general_details(self, ele):
        return self._parse(ele, self.general_detail_parsers)

    def _scrape_checklist(self, url, content):
        soup = BeautifulSoup(content, "html.parser")

        checklist_type = self._parse_checklist_type(soup)
        if checklist_type.lower() != self.EFFORT_COMPLETE:
            return None

        primary_details = self._parse_primary_details(soup)
        effort_details = self._parse_effort_details(soup)
        general_details = self._parse_general_details(soup)

        return {
            **primary_details,
            **effort_details,
            **general_details,
            "source": url,
        }

    def _get_checklist_page(self, checklist_id):
        url = f"{self.BASE_URL}/{checklist_id}"
        response = requests.get(url)
        return url, response.content

    @handle_error
    def get_checklist_detail(self, checklist_id):
        url, content = self._get_checklist_page(checklist_id)
        return self._scrape_checklist(url, content)
