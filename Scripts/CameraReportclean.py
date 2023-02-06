import csv
import os


def get_output_file_name(input_file):
    file_base_name, file_extension = os.path.splitext(input_file)
    return file_base_name + "_archived" + file_extension


def clean_rows(rows, header_indexes_to_skip):
    cleaned_rows = []
    for row in rows:
        cleaned_row = [
            value for i, value in enumerate(row) if i not in header_indexes_to_skip
        ]
        cleaned_rows.append(cleaned_row)
    return cleaned_rows


def clean_csv(file_path):
    header_indexes_to_skip = [2]
    rows = []
    headers = None

    with open(file_path, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        for row in reader:
            if row[2]:
                continue
            rows.append(row)

    cleaned_headers = [
        header for i, header in enumerate(headers) if i not in header_indexes_to_skip
    ]
    cleaned_rows = clean_rows(rows, header_indexes_to_skip)

    output_file = get_output_file_name(file_path)
    with open(output_file, "w", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(cleaned_headers)
        for row in cleaned_rows:
            writer.writerow(row)


input_file = input("Enter the path to the CSV file: ")
clean_csv(input_file)
