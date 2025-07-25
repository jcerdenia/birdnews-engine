import gspread
import pydash
from google.auth import default
from google.auth.transport.requests import Request

from misc.decorators import handle_error


class SheetsAPI:
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    def __init__(self, spreadsheet_id):
        self.credentials, _ = default(scopes=self.SCOPES)

        if self.credentials.expired:
            self.credentials.refresh(Request())

        self.gc = gspread.authorize(self.credentials)
        self.spreadsheet = self.gc.open_by_key(spreadsheet_id)

    def _get_worksheet(self, worksheet_idx):
        if self.spreadsheet:
            return self.spreadsheet.get_worksheet(worksheet_idx)

    @handle_error
    def clear(self, worksheet_idx, col_idx=1):
        worksheet = self._get_worksheet(worksheet_idx)
        return worksheet.delete_columns(col_idx)

    @handle_error
    def read(self, worksheet_idx, flat=False):
        worksheet = self._get_worksheet(worksheet_idx)
        data = worksheet.get_all_values()
        return pydash.flatten(data) if flat else data

    @handle_error
    def append(self, worksheet_idx, data, flat=True):
        worksheet = self._get_worksheet(worksheet_idx)
        column_data = [[i] for i in data] if flat else data
        return worksheet.append_rows(column_data)

    @classmethod
    def from_config(cls, config):
        return cls(spreadsheet_id=config.SPREADSHEET_ID)
