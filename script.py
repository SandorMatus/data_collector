import requests
import json
import openpyxl

# Open the Excel file
wb = openpyxl.load_workbook('urls.xlsx')

# Select the desired worksheet
worksheet = wb['Sheet1']  # Replace 'Sheet1' with the name of your worksheet

# Get the URLs from column A starting from row 2
urls = [cell.value for cell in worksheet['A'][1:]]

# Loop through the URLs
for url in urls:
    if url is None:
        print("Skipping None URL")
        continue

    # Send GET request
    response = requests.get(url)

    # Check response status code
    if response.status_code == 200:
        # Get the response content
        response_content = response.text

        # Find the index of "classifications" in the response content
        start_index = response_content.find('"classifications"')

        # Find the index of the next closing square bracket "]" after "classifications"
        end_index = response_content.find(']', start_index)

        # Extract the text with "classifications"
        extracted_data = response_content[start_index:end_index + 1]

        # Add a comma after "classifications" to separate it from the following dictionary
        extracted_data = extracted_data.replace('"classifications":[', '[{' + '"' + url.split('/')[-2] + '"' + ':[')

        extracted_data = extracted_data.replace("'", "\"")
        # Add the closing square bracket to complete the JSON array
        if abs(-2) < len(extracted_data):
            if extracted_data[-2] == '}':
                extracted_data += '}]'
            else:
                extracted_data += '"}]}]'
        try:
            # Parse extracted data as JSON
            extracted_json = json.loads(extracted_data)

            # Save the extracted data to a file in JSON format
            filename = url.split('/')[-2] + ".json"  # Generate a unique filename based on the URL
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(extracted_json, file, ensure_ascii=False, indent=4)

            print("Response data for", url, "saved to", filename)
        except json.decoder.JSONDecodeError as e:
            print("Error parsing JSON for", url, ":", e)
            print(extracted_data)
    else:
        print("Request failed for", url, "with status code:", response.status_code)