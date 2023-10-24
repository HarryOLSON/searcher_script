import argparse
import sys
import logging
from environs import Env
from searcher import SerpApiSearcher
from sheet_manager import SheetManager

"""
python import-google-locations.py --source-table “CA Test” —results-table “Data”
"""


def main():
    env = Env()
    env.read_env()

    SHEET_API_KEY = env.str("SHEET_API_KEY")
    SERP_API_KEY = env.str("SERP_API_KEY")
    SERP_API_URL = env.str("SERP_API_URL")

    logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument("-source-table", '--source-table', help="source table name")
    parser.add_argument("-results-table", '--results-table', help="results table name")
    argv, unknown = parser.parse_known_args()
    if argv.source_table and argv.results_table:
        source_table = argv.source_table
        results_table = argv.results_table
        logger.info(f"Extracting data from {source_table} to {results_table}")

        sheet_manager = SheetManager(SHEET_API_KEY)
        serp_manager = SerpApiSearcher(SERP_API_URL, SERP_API_KEY)
        sheet_manager.get_data(serp_manager)
    logger.error(f'Source table and Result table should be provided as arguments e.g.'
                 f' “--source-table "CA Test" —results-table "Data"”')
    sys.exit(0)


if __name__ == '__main__':
    main()
