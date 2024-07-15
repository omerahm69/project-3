import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import matplotlib.pyplot as plt



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
df = pd.DataFrame(data)
print(df[:10])
headers=df.loc[0]
print(headers)
Shape=df.shape
print(Shape)

Summary_stats=df.describe(include='all')
print(Summary_stats)


ser1=df.filter(["Age", "SchoolDegree", "MaritalStatus", "Income", "Gender","HasChildren","ChildrenNumber"]).head()
print(ser1)

ser1.plot()
plt.show()

plt.imshow(ser1.corr() , cmap = 'autumn' , interpolation = 'nearest' )

plt.title("Heat Map")
plt.show()




    










