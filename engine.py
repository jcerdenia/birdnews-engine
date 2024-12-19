from misc.utils import Colors
from service.ai import AIService
from service.checklist import ChecklistService
from service.content import ContentService


class Engine:
    def __init__(self):
        self.ai = AIService()
        self.content = ContentService()
        self.checklists = ChecklistService(self.content)

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

        if articles and self.content.publish(*articles):
            color = Colors.green if len(articles) else Colors.yellow
            print(color("Published", len(articles), "articles."))

    def sweep_duplicates(self):
        items = self.content.get_published_data_from_last_24h()
        ids_to_delete = []

        for i, item in enumerate(items):
            try:
                next_item = items[i + 1]
                if self.checklists.is_duplicate(
                    item["metadata"],
                    next_item["metadata"],
                ):
                    ids_to_delete.append(item["id"])
            except IndexError:
                pass
            except Exception as e:
                print(Colors.red(f"Error processing {item['id']}:", e))

        print("Found", len(ids_to_delete), "duplicates.")

        if ids_to_delete and self.content.delete_by_id(*ids_to_delete):
            color = Colors.green if len(ids_to_delete) else Colors.yellow
            print(color("Deleted", len(ids_to_delete), "duplicates."))
