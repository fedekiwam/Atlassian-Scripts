import pandas as pd
import os

# To initilize this script you need to have admin permission or access to the confluence application folder.

# Input and output file names
input_xlsx_file = 'PathWithThexlsxFileFromCCMA' # You need to change the file from csv to xlsx to be able to make this script work propertly.
output_xlsx_file = 'output.xlsx'

# Read the XLSX file into a DataFrame
df = pd.read_excel(input_xlsx_file)

# Concatenate "File path" and "Attachment Name" columns
df['Full Path'] = df['File path'] + '/' + df['Attachment Name']

# Initialize a list to store the results (exist or not exist)
file_existence_results = []

# Check for the existence of each file in the "Full Path" column
for _, row in df.iterrows():
    file_path = row['Full Path']
    
    try:
        file_exists = os.path.exists(file_path)
        if file_exists:
            file_existence_results.append('exist')
        else:
            file_existence_results.append('not exist')
    except Exception as e:
        print(f"Error checking file existence: {str(e)}")
        file_existence_results.append('error')

# Add the "File Exist" column to the DataFrame
df['File Exist'] = file_existence_results

# Create a new XLSX file with the results
df.to_excel(output_xlsx_file, index=False)

print(f"Results saved to {output_xlsx_file}")
