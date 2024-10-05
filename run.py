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
    elif file_path.endswith('.xlsx'):
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
    parser.add_argument('--import-google', action='store_true', help="Import Google Sheet Data")
    parser.add_argument('--import-file', action='store_true', help="Import data from a local file")
    parser.add_argument('--analyze', action='store_true', help="Analyze Imported Data")
    parser.add_argument('--sheet-name', type=str, help="Name of the Google Sheet to import")
    parser.add_argument('--file-path', type=str, help="Path to the local CSV or Excel file to import")
    args = parser.parse_args()

    if args.import_google:
        data = import_data()
    elif args.import_file and args.file_path:
        data = import_file(args.file_path)
    else:
        print("Please specify a data source to import.")
        return

    if args.analyze:
        analyze_data(data)

    print("Data imported successfully!")
    print(data)


if __name__ == "__main__":
    main()
