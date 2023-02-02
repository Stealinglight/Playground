import pandas as pd

# Read the CSV file into a Pandas dataframe
df = pd.read_csv("file.csv")

# Check if the required columns are present in the dataframe
required_columns = ['Camera Name', 'Post Deployment Status']
if not set(required_columns).issubset(df.columns):
    raise ValueError(f"Required columns not found in the dataframe. Required columns: {required_columns}")

# Filter the data in the 'Camera Name' column
df['Camera Name'] = df['Camera Name'].apply(lambda x: x.replace('uc_', '') if x.startswith('uc_') else x)

# Add the text 'UNDER_CONSTRUCTION' to the 'Post Deployment Status' column for the filtered data
df.loc[df['Camera Name'].str.startswith('uc_'), 'Post Deployment Status'] = 'UNDER_CONSTRUCTION'

# Save the modified dataframe to a new CSV file
df.to_csv('modified_file.csv', index=False)

# This code loads the CSV file into a pandas dataframe, 
# then applies the .strip() function to each cell in the dataframe 
# that is an instance of str. This will remove any leading or trailing whitespaces. 
# Finally, the modified dataframe is written back to a new CSV file.

# Strip any leading/trailing whitespaces from each cell in the dataframe
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Write the modified dataframe back to a CSV file
df.to_csv("file_stripped.csv", index=False)

# ----------------------------------- #

# Extract the pattern of interest using str.extract() method
df['camera_name'] = df['camera_name'].str.extract(r'^(\w{3}0)')

# Remove the rows where the extracted pattern is not NaN (i.e. the pattern exists in the cell)
df = df[df['camera_name'].isnull()]

# Drop the camera_name column since it's no longer needed
df = df.drop('camera_name', axis=1)

# Save the cleaned data back to a CSV file
df.to_csv('cleaned_file.csv', index=False)

# In the code above, r'^(\w{3}0)' is the regular expression pattern to extract 
# the text that starts with 3 letters and followed by a zero. 
# The ^ symbol in the pattern means to match the pattern only at the start of the string. 
# The \w symbol matches any word character (letter, digit, or underscore), and the {3} specifies that it should match exactly 3 times. 
# The (\w{3}0) is a capturing group that captures the whole pattern to extract it as a separate column. 
# The str.extract() method returns a new series that contains the extracted pattern or NaN (Not a Number) if the pattern is not found. 
# Finally, the df[df['camera_name'].isnull()] uses boolean indexing to filter 
# the dataframe to keep only the rows where the camera_name column does not contain the pattern.

# ----------------------------------- #

expected_columns = ['camera name', 'IP addresses', 'Post Deployment Status', 'Network Fabric', 'Building']

# Read in the csv file and store it as a dataframe
df = pd.read_csv('file.csv')

# Get the actual column names of the dataframe
columns = list(df.columns)

# Check if the actual column names match the expected column names
for i, col in enumerate(columns):
    if col.lower() != expected_columns[i].lower():
        # Column name doesn't match, correct it
        df.rename(columns={col: expected_columns[i]}, inplace=True)

# Save the corrected dataframe to a new csv file
df.to_csv('corrected_file.csv', index=False)

# In the code above, the expected_columns variable contains the expected column names.
# The list(df.columns) returns a list of the actual column names of the dataframe.
# The for loop iterates through the actual column names and compares them with the expected column names.
# If the actual column name doesn't match the expected column name, the rename() method is used to rename the column.
# The rename() method takes a dictionary as an argument, where the key is the current column name and the value is the new column name.
# The inplace=True argument is used to modify the dataframe in place, instead of returning a new dataframe.
# Finally, the corrected dataframe is saved to a new CSV file.

# ----------------------------------- #

# Define the list of correct column names
correct_cols = ['Camera Name', 'IP Address', 'Post Deployment Status', 'Network Fabric', 'Building']

# Read the CSV file into a dataframe
df = pd.read_csv("file.csv")

# Get a list of the current column names
current_cols = df.columns.tolist()

# Loop through the current columns
for col in current_cols:
    # Check if the column name is in the correct names list
    if col in correct_cols:
        continue
    # Check if a similar named column exists in the correct names list
    for correct_col in correct_cols:
        if col.lower() == correct_col.lower():
            df.rename(columns={col: correct_col}, inplace=True)
            break

# Write the dataframe back to the CSV file
df.to_csv("file.csv", index=False)

# In the code above, the correct_cols variable contains the correct column names.
# The list(df.columns) returns a list of the current column names of the dataframe.
# The for loop iterates through the current column names and compares them with the correct column names.
# If the current column name is in the correct column names list, the continue statement is used to skip to the next iteration.
# If the current column name is not in the correct column names list, the for loop iterates through the correct column names list.
# If the current column name is similar to a column name in the correct column names list, the rename() method is used to rename the column.
# The rename() method takes a dictionary as an argument, where the key is the current column name and the value is the new column name.
# The inplace=True argument is used to modify the dataframe in place, instead of returning a new dataframe.
# Finally, the corrected dataframe is saved to the CSV file.

# ----------------------------------- #

import requests

# Replace with the URL to download the attached CSV file from the ticket
url = "https://issues.amazon.com/attachment/download/TICKET_ID/ATTACHMENT_ID"

# Make the GET request to download the attachment
response = requests.get(url)

# Check that the request was successful
if response.status_code == 200:
    # Save the CSV data to a file
    with open("attachment.csv", "wb") as f:
        f.write(response.content)
    print("Attachment downloaded successfully")
else:
    print(f"Error downloading attachment: {response.status_code}")

#     Connect to the Amazon Issues API and retrieve the ticket information and attached files.
# Use the requests library to download the attached CSV file.
# Use pandas to validate the data in the CSV file and make any necessary changes.
# Use pandas to write the modified data to a new CSV file.
# Use the Amazon Issues API to upload the new CSV file as an attachment to the ticket.
# Use the Amazon Issues API to update the correspondence of the ticket with the results of the data validation.

# You could then use pandas to validate the data in the CSV file and make any necessary changes, 
# followed by using pandas to write the modified data to a new CSV file. 
# To upload the new CSV file as an attachment to the ticket, 
# you would need to use the Amazon Issues API to make a POST request with the contents of the new CSV file. 
# To update the correspondence of the ticket, you would need to use 
# the Amazon Issues API to make a PUT request with the updated information.


