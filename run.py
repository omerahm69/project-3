import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
import gspread
from google.oauth2.service_account import Credentials
import matplotlib.pyplot as plt
import seaborn as sns

# Define scope once, at the top level
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
def import_data():
    print("Choose the data source:")
    print("1. CSV file")
    print("2. Excel file")
    print("3. Google Sheets")
    choice = input("Enter your choice (1/2/3): ").strip()
    if choice == "1":
        file_path = input("Enter the path to the CSV file: ").strip()
        df = pd.read_csv(file_path)
    elif choice == "2":
        file_path = input("Enter the path to the Excel file: ").strip()
        sheet_name = input("Enter the sheet name (leave blank for the first sheet): ").strip() or 0
        df = pd.read_excel(file_path, sheet_name=sheet_name)
    elif choice == "3":
        CRED = Credentials.from_service_account_file('cred.json')
        SCOPED_CRED = CRED.with_scopes(SCOPE)
        GSPREAD_CLIENT = gspread.authorize(SCOPED_CRED)
        creds = Credentials.from_service_account_file('cred.json', scopes=SCOPE)
        client = gspread.authorize(creds)
        sheet = GSPREAD_CLIENT.open('2016-FCC-New-Coders-Survey-Data').sheet1
        spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1V8nvA1cu7rkhW9fwn6lfU0ROm3RhzFIQ3a5onbLd1EQ/edit")
        worksheet = spreadsheet.sheet1  # or use: .worksheet("Sheet1") for named access
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        print(df.head())
        print("Invalid choice. Please try again.")
    df.to_pickle('data.pkl')
    print("Data imported successfully!")

def analyze_data():
    """This function analyzes the data."""
    try:
            df = pd.read_pickle('data.pkl')
    except FileNotFoundError:
        print("No data found! Please import data first.")
        return
    print("What analysis would you like to perform?")
    print("1. Show summary statistics")
    print("2. Filter data")
    print("3. Sort data")
    choice = input("Enter your choice (1/2/3): ")
    if choice == "1":
        print(df.describe(include='all'))
    elif choice == "2":
        column = input("Enter the column to filter by: ")
        value = input("Enter the value to filter by: ")
        filtered_data = df[df[column] == value]
        print(filtered_data)
        filtered_data.to_pickle('data.pkl')
    elif choice == "3":
        columns = input("Enter the columns to sort by (comma-separated): ").split(',')
        sorted_data = df.sort_values(by=columns)
        print(sorted_data)
        sorted_data.to_pickle('data.pkl')
    else:
        print("Invalid choice. Please try again.")
        return
    print("\nPerforming additional statistical analysis...")

    ages = df['Age'].dropna().astype(float)
    if not ages.empty:
        average_age = ages.mean()
        print(f"Average Age: {average_age:.2f}")
        sns.histplot(ages, bins=20, kde=True)
        plt.title('Age Distribution')
        plt.xlabel('Age')
        plt.ylabel('Frequency')
        plt.show()
    income=df['Income'].value_counts()
    average_income=sum(income)/len(income)
    print(average_income)
    commutetime=df['CommuteTime'].value_counts()
    average_commutetime=sum(commutetime)/len(commutetime)
    print(average_commutetime)
    schooldegree=df['SchoolDegree'].value_counts()
    print(schooldegree)
    df.describe().to_csv("analysis_results.csv")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Age'], bins=20, kde=True)
    plt.title('Age Distribution of Survey Respondents')
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    plt.show()
    income=df['Income'].value_counts()
    average_income=sum(income)/len(income)
    print(average_income)
    incomes = df['Income'].dropna().astype(float)
    if not incomes.empty:
            print(f"Average Income: {average_income:.2f}")
            sns.histplot(incomes, bins=20, kde=True)
            plt.title('Income Distribution')
            plt.xlabel('Income')
            plt.ylabel('Frequency')
            plt.show()
    degree_counts = df['SchoolDegree'].value_counts()
    print("School Degrees:")
    print(degree_counts)
    sns.histplot(degree_counts, bins=20, kde=True)
    plt.title('School Distribution')
    plt.xlabel('School Degree')
    plt.ylabel('Frequency')
    plt.show()
    #def export_data():
    #try:
        #data = pd.read_pickle('data.pkl')
    #except FileNotFoundError:
        #print("No data found! Please import and analyze data first.")
        #return
    #print("Choose the export format:")
    
    commute_times = df['Commute'].dropna().astype(float)
    if not commute_times.empty:
    average_commute_time = commute_times.mean()
    print(f"Average Commute Time: {average_commute_time:.2f}")
    sns.histplot(average_commute_time, bins=20, kde=True)
    plt.title('CommuteTime Distribution')
    plt.xlabel('CommuteTime')
    plt.ylabel('Frequency')
    plt.show()
    commutetime=df['CommuteTime'].value_counts()
    average_commutetime=sum(commutetime)/len(commutetime)
    print(average_commutetime)
    if 'SchoolDegree' in df.columns:
        degree_counts = df['SchoolDegree'].value_counts()
        print("School Degrees:")
        print(degree_counts)
def main():
    while True:
        print("\nData Tool Menu:")
        print("1. Import Data")
        print("2. Analyze Data")
        print("3. Export Data")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            import_data()
        elif choice == "2":
            analyze_data()
        elif choice == "3":
            export_data()
        elif choice == "4":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()