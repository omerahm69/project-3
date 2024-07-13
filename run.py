import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CODER=Credentials.from_service_account_file('codersurvey.json')
SCOPED_CODER=CODER.with_scopes(SCOPE)
GSPREAD_CODER=gspread.authorize(SCOPED_CODER)
SHEET=GSPREAD_CODER.open('codersurvey')


