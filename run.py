import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.service_account import Credentials
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

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
        data = pd.read_csv(file_path)
    elif choice == "2":
        file_path = input("Enter the path to the Excel file: ").strip()
        sheet_name = input("Enter the sheet name (leave blank for the first sheet): ").strip() or 0
        data = pd.read_excel(file_path, sheet_name=sheet_name)
    elif choice == "3":
        CRED = Credentials.from_service_account_file('creds.json')
        SCOPED_CRED = CRED.with_scopes(SCOPE)
        GSPREAD_CLIENT = gspread.authorize(SCOPED_CRED)
        creds = Credentials.from_service_account_file('creds.json', scopes=SCOPE)
        client = gspread.authorize(creds)
        sheet = GSPREAD_CLIENT.open('2016-FCC-New-Coders-Survey-Data').sheet1
        data =sheet.get_all_records()
        file_name = input("Enter the name of the Google Sheet: ").strip()
        sheet_name = input("Enter the sheet name: ").strip()
        data = pd.DataFrame(sheet.get_all_records())
    else:
        print("Invalid choice. Please try again.")
        return
    data.to_pickle('data.pkl')
    print("Data imported successfully!")
def analyze_data():
    try:
        data = pd.read_pickle('data.pkl')
    except FileNotFoundError:
        print("No data found! Please import data first.")
        return
    print("What analysis would you like to perform?")
    print("1. Show summary statistics")
    print("2. Filter data")
    print("3. Sort data")
    choice = input("Enter your choice (1/2/3): ")
    if choice == "1":
        print(data.describe())
    elif choice == "2":
        column = input("Enter the column to filter by: ")
        value = input("Enter the value to filter by: ")
        filtered_data = data[data[column] == value]
        print(filtered_data)
        filtered_data.to_pickle('data.pkl')  # Save the filtered data
    elif choice == "3":
        columns = input("Enter the columns to sort by (comma-separated): ").split(',')
        sorted_data = data.sort_values(by=columns)
        print(sorted_data)
        sorted_data.to_pickle('data.pkl')  # Save the sorted data
    else:
        print("Invalid choice. Please try again.")
        return
    print("Data analysis completed!")
def export_data():
    try:
        data = pd.read_pickle('data.pkl')
    except FileNotFoundError:
        print("No data found! Please import and analyze data first.")
        return
    print("Choose the export format:")
    print("1. CSV file")
    print("2. Excel file")
    choice = input("Enter your choice (1/2): ")
    output_path = input("Enter the output file path: ")
    if choice == "1":
        data.to_csv(output_path, index=False)
    elif choice == "2":
        data.to_excel(output_path, index=False)
    else:
        print("Invalid choice. Please try again.")
        return
    print("Data exported successfully!")

#def basic_statistics(data):
 #   """This function deal with imported data types."""
  #  print("Calculating basic statistics...")
   # df=pd.DataFrame(data)
    #print(df.describe())
    
    #numerical_features=df.select.dtypes(include='int64')
    #categorical_features=df.select.dtype(include='object')

    #numerical_stats=numerical_features.describe()

    #categorical_counts={}
    #for col in categorical_features.column:
     #   categorical_counts[col]=data[col].value_counts()

   # return numerical_stats, categorical_counts

    #if not data:
     #   print("No data available to analyze.")
      #  return
#def calculate_statistics(data):
 #   """Calculate numerical statistics and categorical counts for a dataset."""
    # Convert data to a DataFrame if it's not already one
  #  df = pd.DataFrame(data)

    # Separate numerical and categorical columns
   # numerical_columns = df.select_dtypes(include='number')
    #categorical_columns = df.select_dtypes(include='object')

    # Calculate numerical statistics
    #numerical_stats = {}
    #for col in numerical_columns.columns:
     #   numerical_stats[col] = {
      #      'count': numerical_columns[col].count(),
       #     'mean': numerical_columns[col].mean(),
        #    'min': numerical_columns[col].min(),
         #   'max': numerical_columns[col].max()
        #}

    # Calculate categorical counts
    #categorical_counts = {}
    #for col in categorical_columns.columns:
     #   categorical_counts[col] = categorical_columns[col].value_counts().to_dict()

    # Print results
    #print("Numerical Statistics:")
    #for key, stats in numerical_stats.items():
       # print(f"{key}: {stats}")

    #print("\nCategorical Counts:")
    #for key, counts in categorical_counts.items():
     #   print(f"{key}: {counts}")

    #return numerical_stats, categorical_counts


#def analyze_data(data):
 #   """This function analyzes the data."""
  #  print("Analyzing data...")
   # if not data:
    #   print("No data available to analyze.")
     #   return

    #ages = []
    #for row in data:
     #   try:
      #      if 'Age' in row and row['Age'] not in (None, ""):
       #         ages.append(float(row['Age']))
        #except ValueError as e:
         #   print(f"Error converting age: {row['Age']} - {e}")

    #ages = [float(row['Age']) for row in data if row['Age'] is not None and row['Age'] != ""]
    
    
#average_age = sum(ages) / len(ages) if ages else 0
 #   print(f"Average Age: {average_age}")

  #  Incomes = [float(row['Income']) for row in data if row['Income'] is not None and row['Income'] != ""]
   # average_income = sum(incomes) / len(incomes) if incomes else 0
    #print(f"Average Income: {average_income}")

    #commute_times = [float(row['CommuteTime']) for row in data if row['CommuteTime'] is not None and row['CommuteTime'] != ""]
    #average_commute_time = sum(commute_times) / len(commute_times) if commute_times else 0
    #print(f"Average Commute Time: {average_commute_time}")

    
    #school_degrees = {}
    #for row in data:
     #   degree = row['SchoolDegree']
      #  if degree in school_degrees:
       #     school_degrees[degree] += 1
        #else:
         #   school_degrees[degree] = 1
    #print(f"School Degrees: {school_degrees}")
    # Plot Age Distribution
    #plt.figure(figsize=(10, 6))
    #sns.histplot(ages, bins=20, kde=True)
    #plt.title('Age Distribution of Survey Respondents')
    #plt.xlabel('Age')
    #plt.ylabel('Frequency')
    #plt.show()
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