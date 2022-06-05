import argparse
import os
from pathlib import Path
import sys

sys.path.append('.')

from src.logger_factory import LoggerFactory
from src.preprocess_sentinel1 import load_config, load_data_collection

logger = LoggerFactory("batch_retrieve_images").get_logger()

"""
Command line interface for batch retrieving Sentinel-1 images and saving them to Local Drive.
Before running this script, you need to have a Google account and a Google Drive account.
Followed by the following steps:
`$ earthengine authenticate`
`$ python apps/batch_retrieve_images.py --input_data_dir ./data/input/only_fields/onlyFields.geojson --config \
   ./data/input/only_fields/config/config.json`
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Retrieve images given a geojson file and config file."
    )
    parser.add_argument(
        "--input_data_dir", type=str, help="Directory containing the input data."
    )
    parser.add_argument(
        "--config", action="append", help="Configuration file to drive algorithm."
    )

    args = parser.parse_args()

    if args.config is not None:
        config_file = args.config[0]
        config = load_config(config_file)

        if args.input_data_dir is not None:
            input_data_dir = args.input_data_dir
            input_data_dir = Path(input_data_dir)
            if input_data_dir.is_file():
                logger.info(f"Reading input parameters from file {input_data_dir}")
                print(str(input_data_dir))
                print('-----------')
                print(config)
                print('***********+')
                load_data_collection(str(input_data_dir), config)
            else:
                raise IOError(f"Directory {input_data_dir} does not exist")
