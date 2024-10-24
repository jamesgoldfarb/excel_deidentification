# excel_deidentification

## Project Description

The `excel_deidentification` project aims to provide a tool for de-identifying sensitive information in Excel files. The goal is to help users remove identifying columns from their Excel files to protect sensitive data.

## Installation Instructions

To run the `xls_deid.py` script, you need to have Python installed on your system. Additionally, you need to install the following dependencies:

- pandas
- openpyxl
- gradio

You can install these dependencies using pip:

```sh
pip install pandas openpyxl gradio
```

## Usage Instructions

To use the tool, follow these steps:

1. Upload an Excel file using the provided file upload interface.
2. Add or remove identifying strings that you want to use for identifying columns.
3. The tool will automatically identify columns containing the specified identifying strings.
4. Select the columns you want to remove.
5. Specify an output file name.
6. Click the "Process" button to generate a de-identified Excel file.

### Second Pass Identification

1. After the first pass, the tool will identify additional columns containing PII values based on the unique values from the selected columns in the first pass.
2. Select the additional columns you want to remove.
3. Click the "Process" button again to generate a de-identified Excel file with the additional columns removed.

## Examples and Usage Scenarios

### Example 1: Removing Name and Date of Birth Columns

1. Upload an Excel file containing columns such as "Name", "Date of Birth", "Address", etc.
2. Add "name" and "dob" to the identifying strings list.
3. The tool will identify the "Name" and "Date of Birth" columns.
4. Select the identified columns and specify an output file name.
5. Click "Process" to generate a de-identified Excel file without the "Name" and "Date of Birth" columns.

### Example 2: Custom Identifying Strings

1. Upload an Excel file containing columns such as "Patient ID", "Email", "Phone Number", etc.
2. Add custom identifying strings such as "patient id", "email", and "phone".
3. The tool will identify the "Patient ID", "Email", and "Phone Number" columns.
4. Select the identified columns and specify an output file name.
5. Click "Process" to generate a de-identified Excel file without the "Patient ID", "Email", and "Phone Number" columns.

### Example 3: Second Pass Identification

1. Upload an Excel file containing columns such as "Name", "Date of Birth", "Address", etc.
2. Add "name" and "dob" to the identifying strings list.
3. The tool will identify the "Name" and "Date of Birth" columns.
4. Select the identified columns and specify an output file name.
5. Click "Process" to generate a de-identified Excel file without the "Name" and "Date of Birth" columns.
6. The tool will then identify additional columns containing PII values based on the unique values from the selected columns in the first pass.
7. Select the additional columns and click "Process" again to generate a de-identified Excel file with the additional columns removed.

## Functionality of `xls_deid.py`

The `xls_deid.py` script provides the following main features:

- Uploading an Excel file for processing.
- Adding and removing identifying strings to customize the identification process.
- Automatically identifying columns containing the specified identifying strings.
- Previewing the original data and the columns to be deleted.
- Generating a de-identified Excel file with the selected columns removed.
- Identifying additional columns containing PII values based on the unique values from the selected columns in the first pass.
