import json
import os

def get_data(folder_name: str, file_name: str) -> dict:
    utils_path = os.path.dirname(__file__)
    project_path = os.path.dirname(utils_path)
    data_file_path = os.path.join(project_path, folder_name, file_name)

    with open(data_file_path, "r", encoding="utf-8") as file:
        return json.load(file)
