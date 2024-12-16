from misc.utils import Colors
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
        print("Got", total, "checklist IDs.")

        checklists = []
        for i, id in enumerate(ids, 1):
            print(f"[{i}/{total}]", f"{id}: reading checklist.")
            if checklist := self.checklists.get_checklist_detail(id):
                checklists.append(checklist)
            else:
                print(f"[{i}/{total}]", f"{id}: skipping incomplete checklist.")

        print("Got", len(checklists), "complete checklists.")

        articles = []
        for i, checklist in enumerate(checklists, 1):
            id = checklist.pop("id")
            source = checklist.pop("source")

            print(f"[{i}/{total}]", f"{id}: writing article.")
            content = self.ai.write_article(checklist)
            checklist.update(content=content, source=source, id=id)

            articles.append(checklist)

        print("Created", len(articles), "articles.")

        if self.content.publish(*articles):
            color = Colors.green if len(articles) else Colors.yellow
            print(color("Published", len(articles), "articles."))
