from htbuilder import a, body, div, html, p, strong

from api import BrevoAPI, SheetsAPI
from misc.clock import Clock
from service import AIService, ContentService


class EmailService:
    def __init__(
        self,
        brevo_api: BrevoAPI,
        sheets_api: SheetsAPI,
        ai_service: AIService,
        content_service: ContentService,
        recipient_list_id: int,
        worksheet_idx: int,
        clock: Clock,
    ):
        self.brevo = brevo_api
        self.sheets = sheets_api
        self.ai = ai_service
        self.content = content_service
        self.recipient_list_id = recipient_list_id
        self.worksheet_idx = worksheet_idx
        self.clock = clock

        self.config = None

    def _set_config(self):
        if items := self.sheets.read(self.worksheet_idx):
            self.config = {k.lower(): int(v) if v.isdigit() else v for k, v in items}

    def _prepare_data(self):
        articles = self.content.curate_articles(
            self.content.publications or self.content.get_published_data_from_last_24h()
        )

        titles = [a["title"] for a in articles]
        intro = self.ai.write_campaign_intro(titles) or self.config["description"]
        subject = f"{self.config['title']}: {self.clock.now().strftime('%B %-d, %Y')}"

        digest = []
        for art in articles:
            url = f"{self.config['site_url']}/{art['slug']}"
            ele = div()(strong()(a(href=url)(art["title"])), p()(art["lead"]))
            digest.append(str(ele))

        html_content = html()(
            body(style="text-align: left; max-width: 600px; margin: 0 auto;")(
                div()(*[p()(par.strip()) for par in intro.split("\n") if len(par)]),
                div()("\n".join(digest)),
            )
        )

        return {
            "subject": subject,
            "name": subject,
            "recipients": {"listIds": [self.recipient_list_id]},
            "sender": {
                "name": self.config["sender_name"],
                "email": self.config["sender_email"],
            },
            "reply_to": self.config["sender_email"],
            "html_content": str(html_content),
        }

    def _send(self):
        data = self._prepare_data()
        if campaign_id := self.brevo.create_email_campaign(data):
            return self.brevo.send_email_campaign(campaign_id)

    def run_campaign(self, force=False):
        try:
            if not self.config:
                self._set_config()

            if force or self.clock.now().hour == self.config.get("send_hour"):
                return self._send()
        except Exception as e:
            print("Failed to run campaign:", e)

        return False

    @classmethod
    def from_config(cls, config):
        return cls(
            brevo_api=BrevoAPI.from_config(config),
            sheets_api=SheetsAPI.from_config(config),
            ai_service=AIService.from_config(config),
            content_service=ContentService.from_config(config),
            recipient_list_id=config.BREVO_RECIPIENT_LIST_ID,
            worksheet_idx=config.EMAIL_WORKSHEET_IDX,
            clock=Clock.from_config(config),
        )
