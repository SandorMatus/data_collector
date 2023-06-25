import os
import json

def combine_json_files(folder_path, output_file):
    combined_data = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                combined_data.extend(data)

    with open(output_file, "w", encoding="utf-8") as output:
        json.dump(combined_data, output, ensure_ascii=False, indent=4)

# Usage example:
folder_path = './'  # Specify the folder containing the JSON files
output_file = './output.json'  # Specify the output file path

combine_json_files(folder_path, output_file)
