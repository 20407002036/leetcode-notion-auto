from .textParser import parse_leet_data_from_extracted_text
"""
File text extraction and text extraction

"""

def extract_file_text(file_path):
    content = ""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        leetId = parse_leet_data_from_extracted_text(content)
        return leetId
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")