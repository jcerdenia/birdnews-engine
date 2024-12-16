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
            checklist = self.checklists.get_checklist_detail(id)

            if not checklist:
                print(f"[{i}/{total}]", f"{id}: skipping incomplete checklist.")
            elif checklists and self.checklists.is_duplicate(checklist, checklists[-1]):
                print(f"[{i}/{total}]", f"{id}: skipping duplicate checklist.")
            else:
                checklists.append(checklist)

        print("Got", len(checklists), "complete checklists.")

        articles = []
        for i, data in enumerate(checklists, 1):
            id = data.pop("id")
            source = data.pop("source")

            print(f"[{i}/{len(checklists)}]", f"{id}: writing article.")
            content = self.ai.write_article(data)
            data.update(content=content, source=source, id=id)

            articles.append(data)

        print("Created", len(articles), "articles.")

        if self.content.publish(*articles):
            color = Colors.green if len(articles) else Colors.yellow
            print(color("Published", len(articles), "articles."))
