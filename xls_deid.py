import gradio as gr
import pandas as pd
import os

# Initialize the identifying strings list
identifying_strings = ["name", "dob"]

def update_identifying_list_add(new_string):
    """
    Adds a string to the identifying strings list.
    """
    global identifying_strings
    if new_string:
        new_string = new_string.lower()
        if new_string not in identifying_strings:
            identifying_strings.append(new_string)
    return ", ".join(identifying_strings)

def update_identifying_list_remove(new_string):
    """
    Removes a string from the identifying strings list.
    """
    global identifying_strings
    if new_string:
        new_string = new_string.lower()
        if new_string in identifying_strings:
            identifying_strings.remove(new_string)
    return ", ".join(identifying_strings)

def identify_columns(df):
    """
    Identifies columns that contain any of the identifying strings.
    """
    identified = []
    normalized_columns = [col.lower().strip() for col in df.columns]
    for idx, col in enumerate(normalized_columns):
        for id_str in identifying_strings:
            if id_str in col:
                identified.append(df.columns[idx])
                break
    return identified

def process_file(file, output_file_name, selected_columns):
    """
    Processes the uploaded Excel file to remove selected columns.
    """
    if not file:
        return "No file uploaded."
    if not output_file_name:
        return "Please specify an output file name."

    # Read the Excel file
    try:
        df = pd.read_excel(file.name, engine='openpyxl')
    except Exception as e:
        return f"Error reading Excel file: {e}"

    # Remove selected columns
    df_deidentified = df.drop(columns=selected_columns, errors='ignore')

    # Ensure the output file does not overwrite the input file
    input_file_name = os.path.basename(file.name)
    if output_file_name == input_file_name:
        output_file_name = f"deidentified_{output_file_name}"

    # Save the de-identified DataFrame to a new Excel file
    try:
        df_deidentified.to_excel(output_file_name, index=False)
    except Exception as e:
        return f"Error writing Excel file: {e}"

    return f"File processed successfully. De-identified file saved as {output_file_name}."

def update_identifying_list():
    """
    Returns the updated identifying strings as a string.
    """
    return ", ".join(identifying_strings)

def main(file):
    """
    Main function to handle the GUI interactions.
    """
    # Initialize output file name
    output_file_default = ""
    original_df_preview = None

    if file is not None:
        try:
            df = pd.read_excel(file.name, engine='openpyxl')
            original_df_preview = df.head(10)  # Display only the first 10 rows
        except Exception as e:
            return (
                f"Error reading Excel file: {e}",
                gr.update(),
                gr.update(),
                gr.update(value=""),
                None  # Original Data Preview
            )

        # Identify columns
        identified_columns = identify_columns(df)

        # Generate default output file name
        input_file_name = os.path.basename(file.name)
        name, ext = os.path.splitext(input_file_name)
        output_file_default = f"{name}_deidentified{ext}"

        return (
            "",
            gr.update(choices=identified_columns),
            gr.update(value=update_identifying_list()),
            gr.update(value=output_file_default),
            original_df_preview  # Original Data Preview
        )
    else:
        return (
            "",
            gr.update(choices=[]),
            gr.update(value=update_identifying_list()),
            gr.update(value=""),
            None  # Original Data Preview
        )

def reset():
    """
    Resets all inputs and outputs to their default states.
    """
    global identifying_strings
    identifying_strings = ["name", "dob"]
    return (
        None,  # file_input
        "",    # new_string
        "",    # result
        gr.update(choices=[]),  # identified_columns
        ", ".join(identifying_strings),  # identifying_list
        gr.update(value=""),  # output_file_name
        None,  # Original Data Preview
        None,  # Columns to be Deleted Preview
    )

def update_identified_columns(file):
    """
    Updates the list of identified columns based on the current identifying strings.
    """
    if file is not None:
        try:
            df = pd.read_excel(file.name, engine='openpyxl')
            identified_columns = identify_columns(df)
            return gr.update(choices=identified_columns)
        except:
            return gr.update(choices=[])
    else:
        return gr.update(choices=[])

def update_columns_preview(file, selected_columns):
    """
    Updates the preview of the columns to be deleted.
    """
    if file is not None and selected_columns:
        try:
            df = pd.read_excel(file.name, engine='openpyxl')
            columns_to_delete = df[selected_columns].head(10)
            return columns_to_delete
        except Exception as e:
            return None
    else:
        return None

# Gradio Interface Components
with gr.Blocks() as demo:
    gr.Markdown("# Excel De-identification Tool")

    # Section 1: File Upload
    with gr.Row():
        file_input = gr.File(label="Upload Excel File", file_types=['.xlsx', '.xls'])

    # Original Data Preview
    original_data_preview = gr.Dataframe(
        label="Original Data Preview",
        interactive=False
    )

    # Section 2: Identifying Strings
    with gr.Row():
        new_string = gr.Textbox(label="Add/Remove Identifying String")
        add_button = gr.Button("Add")
        remove_button = gr.Button("Remove")
    identifying_list = gr.Textbox(
        label="Current Identifying Strings",
        value=", ".join(identifying_strings),
        interactive=False
    )

    # Section 3: Column Identification
    with gr.Row():
        identified_columns = gr.CheckboxGroup(choices=[], label="Identified Columns to Remove")

    # Columns to be Deleted Preview
    columns_to_delete_preview = gr.Dataframe(
        label="Columns to be Deleted Preview",
        interactive=False
    )

    # Section 4: Output Settings
    with gr.Row():
        output_file_name = gr.Textbox(label="Output File Name")

    # Section 5: Actions
    with gr.Row():
        process_button = gr.Button("Process")
        reset_button = gr.Button("Reset")

    # Outputs
    result = gr.Textbox(label="Status")

    # Interactions
    file_input.change(
        main,
        inputs=[file_input],
        outputs=[
            result,
            identified_columns,
            identifying_list,
            output_file_name,
            original_data_preview
        ]
    )

    # Update Columns to be Deleted Preview when columns are selected
    identified_columns.change(
        update_columns_preview,
        inputs=[file_input, identified_columns],
        outputs=columns_to_delete_preview
    )

    # Add and Remove buttons for Identifying Strings
    add_button.click(
        update_identifying_list_add,
        inputs=[new_string],
        outputs=identifying_list
    )

    remove_button.click(
        update_identifying_list_remove,
        inputs=[new_string],
        outputs=identifying_list
    )

    # Update Identified Columns and Preview when Identifying Strings change
    add_button.click(
        update_identified_columns,
        inputs=[file_input],
        outputs=identified_columns
    )

    add_button.click(
        update_columns_preview,
        inputs=[file_input, identified_columns],
        outputs=columns_to_delete_preview
    )

    remove_button.click(
        update_identified_columns,
        inputs=[file_input],
        outputs=identified_columns
    )

    remove_button.click(
        update_columns_preview,
        inputs=[file_input, identified_columns],
        outputs=columns_to_delete_preview
    )

    # Process Button
    process_button.click(
        process_file,
        inputs=[file_input, output_file_name, identified_columns],
        outputs=result
    )

    # Reset Button
    reset_button.click(
        reset,
        outputs=[
            file_input,
            new_string,
            result,
            identified_columns,
            identifying_list,
            output_file_name,
            original_data_preview,
            columns_to_delete_preview
        ]
    )

demo.launch()
