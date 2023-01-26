import csv
import os.path

# Prompt the user for the file name
file_name = input('Enter the file name: ')

# Open the original CSV file and read the data
with open(file_name, 'r', encoding="utf-8") as csv_file:
  csv_reader = csv.reader(csv_file)
  
  # Extract the file name and extension from the original file path
  file_base_name, file_extension = os.path.splitext(file_name)
  
  # Create a new file path with the updated file name 1
  new_file_name_1 = file_base_name + '_archived' + file_extension
  
  # Create a new file path with the updated file name 2
  new_file_name_2 = 'OpticsCameraCoverage-current' + file_extension
  
  # Create a new CSV file to write the updated data 1
  with open(new_file_name_1, 'w') as new_csv_file_1:
    csv_writer_1 = csv.writer(new_csv_file_1)
    
    # Create a new CSV file to write the updated data 2
    with open(new_file_name_2, 'w') as new_csv_file_2:
      csv_writer_2 = csv.writer(new_csv_file_2)
      
      # Iterate through each row in the original data
      for i, row in enumerate(csv_reader):
        # Check if this is the first row (i.e. the header row)
        if i == 0:
          # Write the row to both new CSV files
          csv_writer_1.writerow(row)
          csv_writer_2.writerow(row)
          continue
        
        # Check if the 3rd column has data
        if row[2]:
          # Skip the row and do not write it to the new CSV file
          continue
        else:
          # If the 3rd column does not have data, write the row to CSV files
          csv_writer_1.writerow(row)
          csv_writer_2.writerow(row)

# Close the updated CSV files
new_csv_file_1.close()
new_csv_file_2.close()
