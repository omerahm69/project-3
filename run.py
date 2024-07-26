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
    """ This function import data from Google sheet """

    print(f"Please import data from Google sheet: ")
    sheet = GSPREAD_CLIENT.open('2016-FCC-New-Coders-Survey-Data').sheet1
    data = pd.DataFrame(sheet.get_all_records())
    return data


def import_file (file_path):
    """This function import data from a file in a computer locally"""
    print (f'Importing data from file: {file_path}')

    if file_path.endswith('.csv'):
        data=pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        data=pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file type. Please use a csv or excel file.")
    
    return data


def basic_statistics(data):

    df=pd.DataFrame(data)
    print(df.describe())
    
    numerical_features=df.select_dtypes(include='int64')
    categorical_features=df.select_dtype(include='object')

    numerical_stats=numerical_features.describe()

    categorical_counts={}
    for col in categorical_features.columns:
        categorical_counts[col]=data[col].value_counts()

    return numerical_stats, categorical_counts


def analyze_data(data):
    """ This function is for analyzing data """

    df=pd.DataFrame(data)
    
    Summary_stats=df.select_dtypes('object')
    print(Summary_stats)

    df['Age']=pd.to_numeric(df['Age'],errors='coerce')
    df['Age'].fillna(df['Age'].mean(),inplace=True)
    average_age=df['Age'].mean()
    print(f"Average Age: {average_age}")

    
    average_income=df['Income'].mean()
    print(f"Average_income): {average_income}")

    
    average_commutetime=df['CommuteTime'].mean()
    print(f"Average_commutetime): {average_commutetime}")

    schooldegree_counts=df['SchoolDegree'].value_counts()
    print(schooldegree_counts)

    #Plotting age distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(data['Age'], bins=20, kde=True)
    plt.title('Age Distribution of Survey Respondents')
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    plt.show()

    return {
        'average_age':average_age,
        'average_income':average_income,
        'average_commutetime':average_commutetime,
        'schoolDegree':schooldegree_counts.to_dict()
    }

def export_results(results,filename='analysis_results.csv'):
    """ This function exports the analysis results to a csv file"""
    df_results=pd.DataFrame.from_dict(results,orient='index')
    df_results.to_csv(filename, header=False)
    print(f"Analysis results exported to {filename}")


def main():
    parser = argparse.ArgumentParser(description="Survey Data Analysis")
    parser.add_argument('--import', action='store_true', help='Import Google Sheet Data')
    parser.add_argument('--analyze', action='store_true', help='Analyze Imported Data')
    parser.add_argument('--sheet-name', type=str, help='Name of the Google Sheet to import')
    parser.add_argument('--file-path', type=str, help='Path to the local CSV or Excel file to import')

    args = parser.parse_args()
    data = import_data()
    
    file_path='C:/Users/omera/Desktop/codersurvey.xlsx'
    data=import_data()
    print(data.head())
    
    print("Data imported successfully!")
    data.to_csv("imported_data.csv", index=False)
    print(data)

    numerical_stats, categorical_counts = basic_statistics(data)
    results = analyze_data(data)

    export_results(results)
    
    analyze_data(data)

if __name__ == "__main__":
    main()


