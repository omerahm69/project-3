import argparse
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
    """This function import data from Google sheet."""
    sheet = GSPREAD_CLIENT.open('2016-FCC-New-Coders-Survey-Data').sheet1
    data =sheet.get_all_records()
    return data


def import_file(file_path):
    """This function import data from a file in a computer locally."""
    data= []
    if file_path.endswith('.csv'):
        with open(file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        #data=pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        #data=pd.read_excel(file_path)
        wb = load_workbook(file_path)
        ws = wb.active
        header = [cell.value for cell in ws[1]]
        for row in ws.iter_rows(min_row=2, values_only=True):
            data.append(dict(zip(header, row)))
    else:
        raise ValueError("Unsupported file type. Please use a csv or excel file.")
    
    return data

def basic_statistics(data):
    """This function deal with imported data types."""
    # changing data into a Pandas Dataframe
    print("Calculating basic statistics...")
    if not data:
        print("No data available to analyze.")
        return
    
    numerical_stats = {}
    categorical_counts = {}

    for key in data[0].keys():
        try:
            values = [float(row[key]) for row in data if row[key] is not None and row[key] != ""]
            if values:
                numerical_stats[key] = {
                    'count': len(values),
                    'mean': sum(values) / len(values),
                    'min': min(values),
                    'max': max(values)
                }
        except ValueError:
            values = [row[key] for row in data if row[key] is not None and row[key] != ""]
            categorical_counts[key] = {}
            for value in values:
                if value in categorical_counts[key]:
                    categorical_counts[key][value] += 1
                else:
                    categorical_counts[key][value] = 1

    print("Numerical Statistics:")
    for key, stats in numerical_stats.items():
        print(f"{key}: {stats}")

    print("Categorical Counts:")
    for key, counts in categorical_counts.items():
        print(f"{key}: {counts}")

    return numerical_stats, categorical_counts

"""def analyze_data(data):
    This function is for analyzing data.
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
    This function exports the analysis results to a csv file
    df_results = pd.DataFrame.from_dict(results, orient='index')
    df_results.to_csv(filename, header=False)
    print(f'Analysis results exported to {filename}')"""
def analyze_data(data):
    """This function analyzes the data."""
    print("Analyzing data...")
    if not data:
        print("No data available to analyze.")
        return

    ages = [float(row['Age']) for row in data if row['Age'] is not None and row['Age'] != ""]
    average_age = sum(ages) / len(ages) if ages else 0
    print(f"Average Age: {average_age}")

    incomes = [float(row['Income']) for row in data if row['Income'] is not None and row['Income'] != ""]
    average_income = sum(incomes) / len(incomes) if incomes else 0
    print(f"Average Income: {average_income}")

    commute_times = [float(row['CommuteTime']) for row in data if row['CommuteTime'] is not None and row['CommuteTime'] != ""]
    average_commute_time = sum(commute_times) / len(commute_times) if commute_times else 0
    print(f"Average Commute Time: {average_commute_time}")

    school_degrees = {}
    for row in data:
        degree = row['SchoolDegree']
        if degree in school_degrees:
            school_degrees[degree] += 1
        else:
            school_degrees[degree] = 1
    print(f"School Degrees: {school_degrees}")

    # Plot Age Distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(ages, bins=20, kde=True)
    plt.title('Age Distribution of Survey Respondents')
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    plt.show()
def main():
    parser = argparse.ArgumentParser(description="Survey Data Analysis")
    parser.add_argument('--import-google', action='store_true',
                        'help="Import Google Sheet Data')
    parser.add_argument('--import-file', action='store_true',
                        'help=Import data from a local file')
    parser.add_argument('--analyze', action='store_true',
                        'help=Analyze Imported Data')
    parser.add_argument('--sheet-name', type='str'
                        'help=Name of the Google Sheet to import')
    parser.add_argument('--file-path', type='str'
                        'help=Path to the local CSV or Excel file to import')
    args = parser.parse_args()
    data = import_data()

    file_path='C:/Users/omera/Desktop/codersurvey.xlsx'
    data=import_data()
    #print(data.head())
    
    print("Data imported successfully!")
    #data.to_csv("imported_data.csv", index=False)
    print(data)
    
    analyze_data(data)

if __name__ == "__main__":
    main()


    """if args.import_google:
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
                               '(yes/no):\n')
        if analyze_choice.lower() == 'yes':
            numerical_stats, categorical_counts = basic_statistics(data)
            results = analyze_data(data)
            export_results(results)
        else:
            print("Analysis skipped. Exiting.")


if __name__ == "__main__":
    main()"""