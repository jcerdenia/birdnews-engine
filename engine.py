from service.ai import AIService
from service.checklist import ChecklistService
from service.content import ContentService


class Engine:
    def __init__(self):
        self.ai = AIService()
        self.checklists = ChecklistService()
        self.content = ContentService()

    def run(self):
        ids = self.checklists.get_checklist_ids()

        total = len(ids)
        print("Got", total, "checklist IDs")

        for i, id in enumerate(ids, 1):
            counter = f"{i}/{total}"
            print(counter, "Fetching checklist", id)
            data = self.checklists.get_checklist_detail(id)

            if data:
                print(counter, "Writing article for", id)
                content = self.ai.write_article(data)
                data["content"] = content

                print(counter, "Publishing article", id)
                data["id"] = id
                self.content.publish(data)

            else:
                print(counter, "Skipping checklist", id)
