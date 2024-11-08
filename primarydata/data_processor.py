import os
import pandas as pd
import requests
import json
from typing import Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataProcessor:
    def __init__(self, folder_path: str, api_url: str, token: str):
        self.folder_path: str = folder_path
        self.api_url: str = api_url
        self.token: str = token

    def xls_to_json(self, xls_file_path: str) -> Optional[str]:
        """
        Convert .xls file to JSON format and save it to a file.
        
        :param xls_file_path: Path to the .xls file
        :return: Path to the generated .json file or None if there was an error
        """
        try:
            df: pd.DataFrame = pd.read_excel(xls_file_path)
            json_data: str = df.to_json(orient='records')
            json_file_path: str = os.path.splitext(xls_file_path)[0] + '.json'

            # Write the JSON data to a file
            with open(json_file_path, 'w') as json_file:
                json_file.write(json_data)

            logging.info(f"Data successfully converted to JSON and saved to {json_file_path}")
            return json_file_path

        except Exception as e:
            logging.error(f"Error converting {xls_file_path} to JSON: {e}")
            return None

    def post_json_to_api(self, json_file_path: str) -> None:
        """
        Post JSON file to the API and save the response to a CSV file.
        
        :param json_file_path: Path to the .json file
        """
        try:
            # Read the JSON file
            with open(json_file_path, 'r') as json_file:
                json_data = json.load(json_file)

            headers: dict = {
                'token': self.token,
                'Content-Type': 'application/json',
                'Cookie': 'cf4803=xlqTqX3RS7aAFw/AZIDifaEkVHAwFgjlRIyxCRBxOWGZ86FS9ykuhbzSVRhdGYXXL+nmDiEmTHqRELnrnzqA/TDc60yqMlnzxuuh0kFCTfQJDLSNRzm7ss7EtvBvckg77M43Uyxy9aGNwWOYmnpcJ5pGJtSbAFGURy2gQ/O8G8jfQNqY'
            }
            

            # Make the POST request to the API
            response: requests.Response = requests.post(self.api_url, headers=headers, json=json_data)

            # Check the response
            if response.status_code == 200:
                json_response = response.json()

                if 'data' in json_response:
                    df: pd.DataFrame = pd.DataFrame(json_response['data'])
                    csv_file_name: str = os.path.splitext(json_file_path)[0] + ".csv"
                    # Save the DataFrame to a CSV file
                    df.to_csv(csv_file_name, index=False)

                    logging.info(f"Data successfully saved to {csv_file_name}")
                else:
                    logging.warning("No 'data' field found in the response.")
            else:
                logging.error(f"Failed to post data. Status code: {response.status_code}")
                logging.error(f"Response: {response.text}")

        except Exception as e:
            logging.error(f"Error posting JSON data to the API: {e}")

    def process_folder(self) -> None:
        """
        Process all .xls files in a folder by converting them to JSON and posting to the API.
        """
        try:
            for filename in os.listdir(self.folder_path):
                if filename.endswith(".xls"):
                    xls_file_path: str = os.path.join(self.folder_path, filename)
                    json_file_path: Optional[str] = self.xls_to_json(xls_file_path)

                    if json_file_path:
                        self.post_json_to_api(json_file_path)

        except Exception as e:
            logging.error(f"Error processing folder: {e}")

# Example usage:
if __name__ == "__main__":
    folder_path: str = '/home/tsp/Documents/Script_baz_lol/primarydata/dotyfy'  # Path to your folder containing .xls files
    api_url: str = 'enter ur api url'
    token: str = 'ur token'  # Your token

    data_processor = DataProcessor(folder_path, api_url, token)
    data_processor.process_folder()
