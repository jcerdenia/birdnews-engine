import pydash

from api.ebird import eBirdAPI
from misc.ebird_scraper import eBirdScraper
from misc.utils import is_from_last_24h


class ChecklistService:
    def __init__(self, content_service):
        self.ebird = eBirdAPI()
        self.ebird_scraper = eBirdScraper()
        self.content = content_service

    @staticmethod
    def is_duplicate(checklist1, checklist2):
        matches = []
        for field in ["location", "province", "date", "time"]:
            matches.append(checklist1.get(field) == checklist2.get(field))

        return all(matches)

    @staticmethod
    def same_difference(checklist, publication):
        comparison_map = [
            ("isoObsDate", "datetime"),
            ("loc.name", "metadata.location"),
            ("loc.subnational1Name", "metadata.province"),
        ]

        return all(
            pydash.get(checklist, field1) == pydash.get(publication, field2)
            for field1, field2 in comparison_map
        )

    def get_checklist_ids(self):
        data = self.ebird.get_recent_checklists()
        publications = self.content.get_published_data_from_last_24h()
        processed_ids = [pydash.get(item, "metadata.id") for item in publications]

        checklist_ids = []

        for item in data:
            if not is_from_last_24h(item["isoObsDate"]):
                break

            if item["subId"] in processed_ids or pydash.find(
                publications,
                lambda p: self.same_difference(item, p),
            ):
                continue

            checklist_ids.append(item["subId"])

        return list(reversed(checklist_ids))

    def get_checklist_detail(self, checklist_id):
        return self.ebird_scraper.get_checklist_detail(checklist_id)
