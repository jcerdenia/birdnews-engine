import pydash

from api import EBirdAPI, SheetsAPI
from misc.clock import Clock
from scrapers import EBirdScraper

from .content import ContentService


class ChecklistService:
    PROCESSING_LIMIT = 15
    CLEAR_SKIPPED_IDS_AT_COUNT = 50

    def __init__(
        self,
        ebird_api: EBirdAPI,
        ebird_scraper: EBirdScraper,
        sheets_api: SheetsAPI,
        content_service: ContentService,
        worksheet_idx: int,
        clock: Clock,
    ):
        self.ebird_api = ebird_api
        self.ebird_scraper = ebird_scraper
        self.sheets = sheets_api
        self.content = content_service
        self.worksheet_idx = worksheet_idx
        self.clock = clock

    @staticmethod
    def is_duplicate(checklist1, checklist2):
        return all(
            checklist1.get(field) == checklist2.get(field)
            for field in ["location", "province", "date", "time"]
        )

    @staticmethod
    def _same_difference(checklist, publication):
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

        skipped_ids = self.sheets.read(self.worksheet_idx, True)
        if len(skipped_ids) >= self.CLEAR_SKIPPED_IDS_AT_COUNT:
            self.sheets.clear(self.worksheet_idx)
            recent_skipped_ids = skipped_ids[-(self.CLEAR_SKIPPED_IDS_AT_COUNT / 2) :]
            self.sheets.append(self.worksheet_idx, recent_skipped_ids)

        excluded_ids = list(set(processed_ids + skipped_ids))
        checklist_ids = []

        for item in data:
            if not self.clock.is_from_last_24h(item["isoObsDate"]):
                break

            if item["subId"] in excluded_ids or pydash.find(
                publications,
                lambda p: self._same_difference(item, p),
            ):
                continue

            checklist_ids.append(item["subId"])

        return list(reversed(checklist_ids))[:limit]

    def mark_skipped(self, checklist_ids):
        self.sheets.append(self.worksheet_idx, checklist_ids)

    def get_checklist_detail(self, checklist_id):
        return self.ebird_scraper.get_checklist_detail(checklist_id)

    @classmethod
    def from_config(cls, config):
        return cls(
            ebird_api=EBirdAPI.from_config(config),
            ebird_scraper=EBirdScraper.from_config(config),
            sheets_api=SheetsAPI.from_config(config),
            content_service=ContentService.from_config(config),
            worksheet_idx=config.CHECKLIST_WORKSHEET_IDX,
            clock=Clock.from_config(config),
        )
