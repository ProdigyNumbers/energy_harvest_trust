import argparse
import logging
import os
import src.preprocess_sentinel1 as ps1


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
