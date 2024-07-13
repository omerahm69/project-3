import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CRED= Credentials.from_service_account_file('codersurvey.json')
SCOPED_CRED=CRED.with_scopes(SCOPE)
GSPREAD_CLIENT=gspread.authorize(SCOPED_CRED)

SHEET=GSPREAD_CLIENT.open('2016-FCC-New-Coders-Survey-Data')

worksheet=SHEET.sheet1
data=worksheet.get_all_records()
print(data)












