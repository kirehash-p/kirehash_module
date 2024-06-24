from typing import Any
from oauth2client.service_account import ServiceAccountCredentials
import gspread

def get_spread_sheet(jsonf: str, sheet_key: str) -> gspread.Spreadsheet:
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
    spread_sheet = gspread.authorize(credentials).open_by_key(sheet_key)
    return spread_sheet