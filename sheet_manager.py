import csv
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class SheetManager:
    def __init__(self, sheet_key, source_table="CA Test", result_table="Data"):
        self.sheet_key = sheet_key
        self.source_table = source_table
        self.result_table = result_table
        self.file_path = os.path.join(
            Path(__file__).resolve().parent,
            f'SerpAPI Spreadsheet - {self.source_table}.csv'
        )
        self.file_path_res = os.path.join(
            Path(__file__).resolve().parent,
            f'SerpAPI Spreadsheet - {self.result_table}.csv'
        )

    def get_google_sheet_data(self):
        file_data = []
        with open(self.file_path, 'r', newline='', encoding='utf-8') as csv_file:
            fieldnames = ["Keyword", "City", "Population", "State"]
            csv_reader = csv.DictReader(csv_file, fieldnames=fieldnames)
            for row in csv_reader:
                file_data.append(row)
        logger.info(f'Found {len(file_data)} items in file, extracting...')
        return file_data

    def get_data(self, serp_api_engine):
        sheet_data = self.get_google_sheet_data()
        serpapi_data = None
        for row in sheet_data[1:]:
            keyword, city = row['Keyword'], row['City']
            serpapi_data = serp_api_engine.get_serpapi_data(keyword, city)
            serpapi_data = serp_api_engine.extract_serpapi_data(serpapi_data)

        if serpapi_data:
            self.write_serp_api_results_to_csv(serpapi_data)
            logger.info(f"Script result: \n{serpapi_data}")
        else:
            logger.info(f"Error during sheet reading process")

    def write_serp_api_results_to_csv(self, data, sheet_name='Data'):
        with open(self.file_path_res, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Business Name', 'Ranking Position', 'URL', 'Number of Reviews']
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csv_writer.writeheader()
            for row in data:
                csv_writer.writerow(row)
        logger.info(f'Data has been written to "{sheet_name}" in {self.file_path_res}')
