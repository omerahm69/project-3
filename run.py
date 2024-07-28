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


def import_data(sheet_name):
    """This function import data from Google sheet."""
    sheet = GSPREAD_CLIENT.open(sheet_name).sheet1
    data = pd.DataFrame(sheet.get_all_records())
    return data


def import_file(file_path):
    """This function import data from a file in a computer locally."""
    if file_path.endswith('.csv'):
        data = pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        data = pd.read_excel(file_path)
    else:
        raise ValueError(
            "Unsupported file type. Please use a csv or excel file."
        )
    return data


def basic_statistics(data):
    """This function deal with imported data types."
    "and separated it into numerical and categorical."""
    # changing data into a Pandas Dataframe
    df = pd.DataFrame(data)
    print(df.describe())
    numerical_features = df.select_dtypes(include='int64')
    categorical_features = df.select_dtypes(include='object')

    numerical_stats = numerical_features.describe()

    categorical_counts = {}
    for col in categorical_features.columns:
        categorical_counts[col] = data[col].value_counts()

    return numerical_stats, categorical_counts


def analyze_data(data):
    """This function is for analyzing data."""
    df = pd.DataFrame(data)
    summary_stats = df.select_dtypes('object')
    print(summary_stats)
    average_age = df['Age'].mean()
    print(f"Average Age: {average_age}")
    average_income = df['Income'].mean()
    print(f"Average Income: {average_income}")
    average_commutetime = df['CommuteTime'].mean()
    print(f"Average Commute Time: {average_commutetime}")
    schooldegree_counts = df['SchoolDegree'].value_counts()
    print(schooldegree_counts)
    gender_counts = df['Gender'].value_counts()
    print(gender_counts)
    haschildren_accounts = df['HasChildren'].value_counts()
    print(haschildren_accounts)
    children_number = df['ChildrenNumber'].value_counts()
    print(children_number)

    # Plotting age distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(data['Age'], bins=20, kde=True)
    plt.title('Age Distribution of Survey Respondents')
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.histplot(data['SchoolDegree'], bins=20, kde=True)
    plt.title('School Degree Distribution of Survey Respondents')
    plt.xlabel('School Degree')
    plt.ylabel('Frequency')
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.histplot(data['Gender'], bins=20, kde=True)
    plt.title('Gender Distribution of Survey Respondents')
    plt.xlabel('Gender')
    plt.ylabel('Frequency')
    plt.show()

    return {
        'average_age': average_age,
        'average_income': average_income,
        'average_commutetime': average_commutetime,
        'schoolDegree': schooldegree_counts.to_dict()
    }


def export_results(results, filename='analysis_results.csv'):
    """This function exports the analysis results to a csv file"""
    df_results = pd.DataFrame.from_dict(results, orient='index')
    df_results.to_csv(filename, header=False)
    print(f'Analysis results exported to {filename}')


def main():
    parser = argparse.ArgumentParser(description="Survey Data Analysis")
    parser.add_argument('--import-google', action='store_true'
                        'help="Import Google Sheet Data')
    parser.add_argument('--import-file', action='store_true'
                        'help=Import data from a local file')
    parser.add_argument('--analyze', action='store_true'
                        'help=Analyze Imported Data')
    parser.add_argument('--sheet-name', type='str'
                        'help=Name of the Google Sheet to import')
    parser.add_argument('--file-path', type='str'
                        'help=Path to the local CSV or Excel file to import')
    args = parser.parse_args()
    data = None

    if args.import_google:
        if not args.sheet_name:
            raise ValueError("Please provide the name of"
                             'the Google Sheet using --sheet-name')
        data = import_data(args.sheet_name)
    elif args.import_file:
        if not args.file_path:
            raise ValueError("Please provide the file path using --file-path")
        data = import_file(args.file_path)
    else:
        # Prompt user for import method if no arguments are given
        print("How would you like to import data?")
        print("1. Google Sheet")
        print("2. Local file")
        choice = input("Enter 1 or 2: ")
        if choice == '1':
            sheet_name = input("Please enter the Google Sheet name:\n ")
            data = import_data(sheet_name)
        elif choice == '2':
            file_path = input("Please enter the local"
                              'file path (csv or xlsx):\n')
            data = import_file(file_path)
        else:
            print("Invalid choice. Exiting.")
            return

    print("Data imported successfully!")
    print(data.head())
    data.to_csv("imported_data.csv", index=False)
    print("Data saved to imported_data.csv")

    if args.analyze:
        numerical_stats, categorical_counts = basic_statistics(data)
        results = analyze_data(data)
        export_results(results)
    else:
        # Prompt user for analysis if no arguments are given
        analyze_choice = input("Would you like to analyze the data?"
                               '(yes/no):')
        if analyze_choice.lower() == 'yes':
            numerical_stats, categorical_counts = basic_statistics(data)
            results = analyze_data(data)
            export_results(results)
        else:
            print("Analysis skipped. Exiting.")


if __name__ == "__main__":
    main()