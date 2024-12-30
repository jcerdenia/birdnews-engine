import os

import gspread
import pydash
from google.oauth2.service_account import Credentials

from misc.decorators import handle_error


class SheetsAPI:
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    def __init__(self, spreadsheet_id):
        self.credentials = Credentials.from_service_account_file(
            os.environ.get("SERVICE_ACCOUNT_FILE_PATH"),
            scopes=self.SCOPES,
        )

        self.gc = gspread.authorize(self.credentials)
        self.spreadsheet = self.gc.open_by_key(spreadsheet_id)

    def _get_worksheet(self, worksheet_idx):
        if self.spreadsheet:
            return self.spreadsheet.get_worksheet(worksheet_idx)

    @handle_error
    def read(self, worksheet_idx, flatten=False):
        worksheet = self._get_worksheet(worksheet_idx)
        data = worksheet.get_all_values()
        return pydash.flatten(data) if flatten else data

    @handle_error
    def write(self, worksheet_idx, data, flatten=True):
        worksheet = self._get_worksheet(worksheet_idx)
        column_data = [[i] for i in data] if flatten else data
        return worksheet.update(column_data)
