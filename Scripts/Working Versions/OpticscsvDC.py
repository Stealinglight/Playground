import csv
import os.path

# Prompt the user for the file name
file_name = input('Enter the file name: ')

# Open the original CSV file and read the data
with open(file_name, 'r', encoding="utf-8") as csv_file:
  csv_reader = csv.reader(csv_file)
  
  # Extract the file name and extension from the original file path
  file_base_name, file_extension = os.path.splitext(file_name)
  
  # Create a new file path with the updated file name
  new_file_name = file_base_name + '_filtered' + file_extension
  
  # Create a new CSV file to write the updated data
  with open(new_file_name, 'w') as new_csv_file:
    csv_writer = csv.writer(new_csv_file)
    
    # Iterate through each row in the original data
    for i, row in enumerate(csv_reader):
      # Check if this is the first row (i.e. the header row)
      if i == 0:
        # Write the row to the new CSV file
        csv_writer.writerow(row)
        continue
      
      # Check if the 3rd column has data
      if row[2]:
        # Skip the row and do not write it to the new CSV file
        continue
      # If the 3rd column does not have data, write the row to the new CSV file
      else:
        csv_writer.writerow(row)

# Save the updated CSV file
new_csv_file.close()
