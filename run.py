import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


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

df.info()

Summary_stats=df.describe(include='all')
print(Summary_stats)

#headers=df.loc[0]
#print(headers)
#Shape=df.shape
#print(Shape)
#pd.set_option("display.max.columns", None)

My_data=pd.DataFrame(df, columns=["Age", "SchoolDegree", "MaritalStatus", "Income", "Gender","HasChildren","ChildrenNumber"])

print("My_data:\n", My_data)
#for col in My_data.select_dtypes(include='object').columns:
        #print(My_data[col].value_counts())

Summary_stats=df.describe(include='object')
print(Summary_stats)

NumberOfChildren = df.value_counts("ChildrenNumber")
print(NumberOfChildren)
NumberOfChildren.plot(kind="bar", color='yellow')

Numerical_data=df.select_dtypes("Int64", "Float64")
print(Numerical_data)

#ages=df.["Age"]
#average=df.groupby('Age').mean()
#print(average)

ages = My_data["Age"].value_counts()
bins=np.array([0,25,50,75,100])
groups=My_data.groupedby(pd.cut.age,bins)
output=groups.sum()
average=output/len(ages)
print(average)


gender = My_data["Gender"].value_counts(normalize='True')
gender.plot(kind='bar',  color='blue')
plt.show()

schooLdegree = My_data["SchoolDegree"].value_counts(normalize='True')
gender.plot(kind='bar',  color='red')
plt.show()



Maritalstatus = My_data["MaritalStatus"].value_counts(normalize='True')
Maritalstatus.plot(kind='bar', color='green')
plt.show()












