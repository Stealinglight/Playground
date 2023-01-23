import openpyxl

# Prompt the user for the file name
file_name = input('Enter the file name: ')

# Open the Excel file
wb = openpyxl.load_workbook(file_name)

# Get the sheet with the same name as the file
sheet = wb.get_sheet_by_name(file_name)

# Loop through the rows in the sheet and remove any rows where the
# third column is empty
for row in sheet.rows:
    if row[2].value is None:
        sheet.delete_rows(row)

# Save the changes to the Excel file
wb.save(file_name)
