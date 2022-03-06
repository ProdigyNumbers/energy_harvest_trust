import argparse
from pathlib import Path

from src.logger_factory import LoggerFactory
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.preprocess_sentinel1 import load_config, load_data

logger = LoggerFactory('retrieve_images').get_logger()


# import sys


"""
Command line interface for retrieving Sentinel-1 images and saving them to Google Drive.
Before running this script, you need to have a Google account and a Google Drive account.
Followed by the following steps:
`$ earthengine authenticate`
`$ python apps/retrieve_images.py --input_poly_file ./data/input/paddy/polygons/polygon0.json --config ./data/input/config/config.json`
"""

parser = argparse.ArgumentParser(description="Retrieve images given a json file")
parser.add_argument(
    "--input_poly_file", type=str, help="File containing the input polygon"
)
parser.add_argument(
    "--config", action='append', help='Configuration file to drive algorithm.')

args = parser.parse_args()

if args.config is not None:
    config_file = args.config[0]
    config = load_config(config_file)
       
    if args.input_poly_file is not None:
        input_poly_file = args.input_poly_file
        input_poly_file = Path(input_poly_file)
        if input_poly_file.is_file():
            logger.info(f"Reading input parameters from {input_poly_file}")
            load_data(str(input_poly_file), config)
        else:
            raise Exception(f"File {input_poly_file} does not exist")

# # Check if the file exists
# if os.path.exists(args.input_poly_file):
#     logger.info(f"Reading input parameters from {}".format(args.input_parameters_file))
#     ps1.load_data(args.input_parameters_file)

# else:
#     raise Exception("File {} does not exist".format(args.input_parameters_file))
