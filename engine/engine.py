from misc.utils import Colors
from service import AIService, ChecklistService, ContentService, EmailService


class Engine:
    def __init__(
        self,
        ai_service: AIService,
        checklist_service: ChecklistService,
        content_service: ContentService,
        email_service: EmailService,
    ):
        self.ai = ai_service
        self.checklists = checklist_service
        self.content = content_service
        self.emails = email_service

    def _get_checklists(self):
        ids = self.checklists.get_checklist_ids()

        total = len(ids)
        print("Got", total, "checklist IDs.")

        checklists = []
        skipped_checklist_ids = []

        for i, id in enumerate(ids, 1):
            print(f"[{i}/{total}]", f"{id}: reading checklist.")
            checklist = self.checklists.get_checklist_detail(id)

            if not checklist or (
                checklists and self.checklists.is_duplicate(checklist, checklists[-1])
            ):
                which = "incomplete" if not checklist else "duplicate"
                print(f"[{i}/{total}]", f"{id}: skipping {which} checklist.")
                skipped_checklist_ids.append(id)
            else:
                checklists.append(checklist)

        self.checklists.mark_skipped(skipped_checklist_ids)
        print("Got", len(checklists), "complete checklists.")

        return checklists

    def _write_articles(self, checklists):
        articles = []

        for i, data in enumerate(checklists, 1):
            id = data.pop("id")
            source = data.pop("source")

            print(f"[{i}/{len(checklists)}]", f"{id}: writing article.")
            content = self.ai.write_article(data)
            data.update(content=content, source=source, id=id)

            articles.append(data)

        return articles

    def _publish_articles(self, articles):
        if self.content.publish(*articles):
            color = Colors.green if len(articles) else Colors.yellow
            print(color("Published", len(articles), "articles."))

    def run(self):
        print("Starting engine...")

        if checklists := self._get_checklists():
            if articles := self._write_articles(checklists):
                self._publish_articles(articles)

        if self.emails.run_campaign():
            print(Colors.green("Sent newsletter."))
