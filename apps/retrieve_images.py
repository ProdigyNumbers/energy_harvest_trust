import argparse
import logging
import os
import src.preprocess_sentinel1 as ps1

"""
Command line interface for retrieving Sentinel-1 images and saving them to Google Drive.
Before running this script, you need to have a Google account and a Google Drive account.
Followed by the following steps:
`$ earthengine authenticate`
``
"""


parser = argparse.ArgumentParser(description="Retrieve images given a json file")
parser.add_argument(
    "input_parameters_file", type=str, help="File containing the input parameters"
)
args = parser.parse_args()

# Check if the file exists
if os.path.exists(args.input_parameters_file):
    logging.info("Reading input parameters from {}".format(args.input_parameters_file))
    ps1.load_data(args.input_parameters_file)

else:
    raise Exception("File {} does not exist".format(args.input_parameters_file))
