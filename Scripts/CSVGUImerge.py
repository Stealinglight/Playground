import tkinter as tk
import tkinter.filedialog as filedialog
import csv

# Create a function to select the input files and merge the data
def merge_files():
    # Use the filedialog module to open a file selection dialog
    file1 = filedialog.askopenfilename()
    file2 = filedialog.askopenfilename()

    # Set the name of the column with the relational information
    column_name = entry.get()

    # Create an empty list to store the merged rows
    merged_rows = []

    # Open the first input file and read the rows
    with open(file1, "r") as f:
        reader = csv.DictReader(f)
        rows1 = list(reader)

    # Open the second input file and read the rows
    with open(file2, "r") as f:
        reader = csv.DictReader(f)
        rows2 = list(reader)

    # Iterate through the rows in the first input file
    for row1 in rows1:
        # Get the value from the column with the relational information
        value = row1[column_name]

        # Find the matching row in the second input file
        matching_row = next((row2 for row2 in rows2 if row2[column_name] == value), None)

        # If a matching row was found, merge the two rows
        if matching_row is not None:
            merged_row = {**row1, **matching_row}
            merged_rows.append(merged_row)

    # Use the filedialog module to open a save file dialog
    output_file = filedialog.asksaveasfilename()

    # Write the merged rows to the output file
    with open(output_file, "w") as f:
        writer = csv.DictWriter(f, fieldnames=row1.keys())
        writer.writeheader()
        writer.writerows(merged_rows)

# Create the GUI
root = tk.Tk()
root.title("CSV Merger")

# Create a label and text entry widget to input the column name
label = tk.Label(root, text="Enter column name:")
entry = tk.Entry(root)

# Create a button to run the merge function
button = tk.Button(root, text="Merge files", command=merge_files)

# Add the widgets to the root window
label.pack()
entry.pack()
button.pack()

# Run the main loop
root.mainloop()
