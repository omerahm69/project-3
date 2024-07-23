import argparse
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import matplotlib.pyplot as plt
import seaborn as sns

# Define the scope
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Authenticate and create the client
CRED = Credentials.from_service_account_file('codersurvey.json')
SCOPED_CRED = CRED.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CRED)

def import_data():
    sheet = GSPREAD_CLIENT.open('2016-FCC-New-Coders-Survey-Data').sheet1
    data = pd.DataFrame(sheet.get_all_records())
    #data = pd.DataFrame({'Example': [1,2,3]})
    return data

def analyze_data(data):
    data.describe().to_csv("analysis_results.csv")
    plt.figure(figsize=(10, 6))
    sns.histplot(data['Age'], bins=20, kde=True)
    plt.title('Age Distribution of Survey Respondents')
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Survey Data Analysis")
    parser.add_argument('--import', action='store_true', help='Import Google Sheet Data')
    parser.add_argument('--analyze', action='store_true', help='Analyze Imported Data')

    args = parser.parse_args()

    #if args.import:
    data = import_data()
    print("Data imported successfully!")
    data.to_csv("imported_data.csv", index=False)
    print(data)
    
    #if args.analyze:
    data = pd.read_csv("imported_data.csv")
    analyze_data(data)

if __name__ == "__main__":
    main()


