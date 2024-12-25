import os

from misc.utils import Colors, now
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
        self.email_send_hour = os.getenv("EMAIL_SEND_HOUR")

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

        if self.email_send_hour <= now.hour() < (self.email_send_hour + 1):
            self.send_newsletter()

    def send_newsletter(self):
        if self.emails.run_campaign():
            print(Colors.green("Sent newsletter."))
