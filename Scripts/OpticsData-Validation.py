import pandas as pd

# Read the CSV file into a Pandas dataframe
df = pd.read_csv("file.csv")

## Working Blocks ##

# Add the text 'UNDER_CONSTRUCTION' to the 'Post Deployment Status' column for the filtered data
df.loc[
    df["Camera Name"].str.startswith("uc_"), "Post Deployment Status"
] = "UNDER_CONSTRUCTION"

# Filter the data in the 'Camera Name' column
df["Camera Name"] = df["Camera Name"].apply(
    lambda x: x.replace("uc_", "") if x.startswith("uc_") else x
)

# Define the list of correct column names
correct_cols = [
    "Camera Name",
    "IP Address",
    "Post Deployment Status",
    "Network Fabric",
    "Building",
]

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


## Playground Below ##

# Check if the required columns are present in the dataframe
required_columns = ["Camera Name", "Post Deployment Status"]
if not set(required_columns).issubset(df.columns):
    raise ValueError(
        f"Required columns not found in the dataframe. Required columns: {required_columns}"
    )

# Strip any leading/trailing whitespaces from each cell in the dataframe
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Extract the pattern of interest using str.extract() method
df["camera_name"] = df["camera_name"].str.extract(r"^(\w{3}0)")

# Remove the rows where the extracted pattern is not NaN (i.e. the pattern exists in the cell)
df = df[df["camera_name"].isnull()]

# Drop the camera_name column since it's no longer needed
df = df.drop("camera_name", axis=1)

""" In the code above, r'^(\w{3}0)' is the regular expression pattern to extract 
 the text that starts with 3 letters and followed by a zero. 
 The ^ symbol in the pattern means to match the pattern only at the start of the string. 
 The \w symbol matches any word character (letter, digit, or underscore), and the {3} specifies that it should match exactly 3 times. 
 The (\w{3}0) is a capturing group that captures the whole pattern to extract it as a separate column. 
 The str.extract() method returns a new series that contains the extracted pattern or NaN (Not a Number) if the pattern is not found. 
 Finally, the df[df['camera_name'].isnull()] uses boolean indexing to filter 
 the dataframe to keep only the rows where the camera_name column does not contain the pattern. """

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

