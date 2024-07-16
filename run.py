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

Summary_stats=df.describe(include='object')
print(Summary_stats)

age=df.value_counts("Age")
print(age)
school=df.value_counts("SchoolDegree")
print(school)
school.plot()
plt.show()

ser1=df.filter(["Age", "SchoolDegree", "MaritalStatus", "Income", "Gender","HasChildren","ChildrenNumber"]).head()
print(ser1)

for col in ser1.select_dtypes(include='object').columns:
    print(df[col].value_counts())

contingency_table = pd.crosstab(df['Age'], df['SchoolDegree'])
print(contingency_table )

ser1.plot()
plt.show()

NumberOfChildren = df.value_counts("ChildrenNumber")
print(NumberOfChildren)
NumberOfChildren.plot()
plt.show()


gender = df.value_counts("Gender")
print(gender)
gender.plot()
plt.show()

Maritalstatus = df.value_counts("MaritalStatus")
print(Maritalstatus)
Maritalstatus.plot()
plt.show()












    










