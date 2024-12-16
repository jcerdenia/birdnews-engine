from datetime import datetime

from api.ebird import eBirdAPI
from misc.ebird_scraper import eBirdScraper
from service.content import ContentService


class ChecklistService:
    def __init__(self):
        self.ebird = eBirdAPI()
        self.ebird_scraper = eBirdScraper()
        self.content = ContentService()

    @staticmethod
    def is_duplicate(checklist1, checklist2):
        matches = []
        for field in ["location", "province", "date", "time"]:
            matches.append(checklist1.get(field) == checklist2.get(field))

        return all(matches)

    def get_checklist_ids(self):
        data = self.ebird.get_recent_checklists()
        processed_ids = self.content.get_recent_processed_checklist_ids()

        checklist_ids = []

        for item in data:
            if item["subId"] in processed_ids:
                continue

            is_from_today = (
                datetime.strptime(item["obsDt"], "%d %b %Y").date()
                == datetime.today().date()
            )

            if not is_from_today:
                break

            checklist_ids.append(item["subId"])

        return list(reversed(checklist_ids))

    def get_checklist_detail(self, checklist_id):
        return self.ebird_scraper.get_checklist_detail(checklist_id)
