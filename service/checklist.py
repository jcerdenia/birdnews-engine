from datetime import datetime

from api.ebird import eBirdAPI
from misc.ebird_scraper import eBirdScraper
from service.content import ContentService


class _ChecklistService:
    def __init__(self):
        self.ebird = eBirdAPI
        self.ebird_scraper = eBirdScraper
        self.content = ContentService

    def get_checklist_ids(self):
        data = self.ebird.get_recent_checklists()
        last_saved_id = self.content.get_last_saved_checklist_id()

        checklist_ids = []

        for item in data:
            is_today = (
                datetime.strptime(item["obsDt"], "%d %b %Y").date()
                == datetime.today().date()
            )

            if item["subId"] == last_saved_id or not is_today:
                break

            checklist_ids.append(item["subId"])

        return list(reversed(checklist_ids))

    def get_checklist_detail(self, checklist_id):
        return self.ebird_scraper.get_checklist_detail(checklist_id)


ChecklistService = _ChecklistService()
