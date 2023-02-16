import os

import pandas as pd


def RemoveDups_csv(file_name):
    df = pd.read_csv(
        file_name, usecols=range(18), low_memory=False
    )  # Load only the first 18 columns
    df = df[df["Description"].isnull()]  # Filter the rows based on the condition
    df = df.drop("Description", axis=1)  # Drop the "Description" column
    file_base_name, file_extension = os.path.splitext(file_name)
    new_file_name = file_base_name + "_filtered" + file_extension
    df.to_csv(new_file_name, index=False)
    print(f"\033[32m\nDuplicates successfully removed.\nNew file location: {new_file_name}")


# Prompt the user for the file name
file_name = input('Enter file location of "OpticsCameraCoverage" report: ')

RemoveDups_csv(file_name)
