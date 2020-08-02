import json

class configManager:
    config_properties = {}

    def __init__(self):
        with open("config.json") as json_file:
            self.config_properties = json.load(json_file)

    def retrieve_csv_filepath(self):
        return self.config_properties["CSV_FILEPATH"]

    def retrieve_xlsx_filepath(self):
        return self.config_properties["XLSX_FILEPATH"]

    def set_csv_filepath(self, new_filepath):
        self.config_properties["CSV_FILEPATH"] = new_filepath

    def set_xlsx_filepath(self, new_filepath):
        self.config_properties["XLSX_FILEPATH"] = new_filepath