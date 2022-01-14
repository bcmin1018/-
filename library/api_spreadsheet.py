import gspread
from library import cf

class spreadsheet:
    def __init__(self):
        self.scope = cf.scope
        self.json_file_name = cf.json_file_name
        self.credentials = cf.credentials
        self.gc = gspread.authorize(cf.credentials)
        self.spreadsheet_url = cf.spreadsheet_url
        self.doc = cf.gc.open_by_url(self.spreadsheet_url)

    def clear_sheet(self, sheet_name):
        worksheet = self.doc.worksheet(sheet_name)
        worksheet.clear()

    def data_insert(self, df, sheet_name):
        worksheet = self.doc.worksheet(sheet_name)
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())