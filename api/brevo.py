import os

import brevo_python

from misc.decorators import handle_error


class BrevoAPI:
    def __init__(self):
        self.config = brevo_python.Configuration()
        self.config.api_key["api-key"] = os.getenv("BREVO_API_KEY")
        self.client = brevo_python.ApiClient(self.config)
        self.emails = brevo_python.EmailCampaignsApi(self.client)

    @handle_error
    def create_email_campaign(self, data):
        payload = brevo_python.CreateEmailCampaign(**data)
        result = self.emails.create_email_campaign(payload)

        return getattr(result, "id")

    @handle_error
    def send_email_campaign(self, campaign_id):
        self.emails.send_email_campaign_now(campaign_id)

        return True
