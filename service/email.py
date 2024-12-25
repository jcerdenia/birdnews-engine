import os

from api.brevo import BrevoAPI
from misc.utils import now
from service.content import ContentService


class EmailService:
    def __init__(
        self,
        brevo_api: BrevoAPI,
        content_service: ContentService,
    ):
        self.brevo = brevo_api
        self.content = content_service

        self.title = "Daily Digest"
        self.from_name = "PH Bird News"
        self.from_email = os.getenv("BREVO_SENDER_EMAIL_ADDRESS")
        self.recipient_list_id = int(os.getenv("BREVO_RECIPIENT_LIST_ID"))

    def _prepare_data(self):
        articles = self.content.curate_articles(
            self.content.publications or self.content.get_published_data_from_last_24h()
        )

        subject = f"{self.title}: {now().strftime("%B %d, %Y")}"

        digest = [
            f"<div>"
            f'<a href="https://ph.birdnews.xyz/{a["slug"]}">'
            f"<strong>{a["title"]}</strong></a>"
            f"<p>{a['lead']}</p>"
            f"</div>"
            for a in articles
        ]

        html_content = (
            '<html><body style="text-align: left;">'
            + "<div><p>Birding highlights from the last 24 hours.</p></div>"
            + "\n".join(digest)
            + "</body></html>"
        )

        return {
            "subject": subject,
            "name": subject,
            "recipients": {"listIds": [self.recipient_list_id]},
            "sender": {"name": self.from_name, "email": self.from_email},
            "reply_to": self.from_email,
            "html_content": html_content,
        }

    def run_campaign(self):
        data = self._prepare_data()
        if campaign_id := self.brevo.create_email_campaign(data):
            return self.brevo.send_email_campaign(campaign_id)

        return False
