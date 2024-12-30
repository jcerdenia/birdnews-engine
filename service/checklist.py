import pydash

from api import EBirdAPI, SheetsAPI
from misc.utils import is_from_last_24h
from scrapers import EBirdScraper

from .content import ContentService


class ChecklistService:
    PROCESSING_LIMIT = 15
    QUERIED_IDS_WORKSHEET_IDX = 1

    def __init__(
        self,
        ebird_api: EBirdAPI,
        ebird_scraper: EBirdScraper,
        sheets_api: SheetsAPI,
        content_service: ContentService,
    ):
        self.ebird_api = ebird_api
        self.ebird_scraper = ebird_scraper
        self.sheets = sheets_api
        self.content = content_service

    @staticmethod
    def is_duplicate(checklist1, checklist2):
        return all(
            checklist1.get(field) == checklist2.get(field)
            for field in ["location", "province", "date", "time"]
        )

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

    def get_checklist_ids(self, limit=PROCESSING_LIMIT):
        data = self.ebird_api.get_recent_checklists()
        publications = self.content.get_published_data_from_last_24h()

        processed_ids = [pydash.get(item, "metadata.id") for item in publications]
        last_queried_ids = self.sheets.read(self.QUERIED_IDS_WORKSHEET_IDX, True)
        excluded_ids = list(set(processed_ids + last_queried_ids))

        checklist_ids = []

        for item in data:
            if not is_from_last_24h(item["isoObsDate"]):
                break

            if item["subId"] in excluded_ids or pydash.find(
                publications,
                lambda p: self.same_difference(item, p),
            ):
                continue

            checklist_ids.append(item["subId"])

        result = list(reversed(checklist_ids))[:limit]
        self.sheets.write(self.QUERIED_IDS_WORKSHEET_IDX, result)

        return result

    def get_checklist_detail(self, checklist_id):
        return self.ebird_scraper.get_checklist_detail(checklist_id)
