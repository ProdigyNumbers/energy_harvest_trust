import argparse
import json
import os
import pathlib
from pathlib import Path
from typing import List, Tuple
import sys

sys.path.append(".")

import geojson
from src.logger_factory import LoggerFactory

logger = LoggerFactory("txt2geojson").get_logger()


def get_all_txt_files(input_data_dir: str) -> List[pathlib.Path]:
    return list(Path(input_data_dir).rglob("*.txt"))


def write_text_to_geojson(
    list_of_txt_files: List[pathlib.Path], output_dir: str, output_filename: str
):
    polygons = []
    for file in list_of_txt_files:
        poly_list: List[Tuple] = []
        with open(file, "r") as io:
            data = json.load(io)
        first_lat = data[0]["latitude"]
        first_lon = data[0]["longitude"]
        for elem in data:
            lat = elem["latitude"]
            lon = elem["longitude"]
            poly_list.append((lat, lon))
        poly_list.append((first_lat, first_lon))
        polygon = geojson.Polygon([poly_list])
        polygons.append(polygon)
    polygon_collection = geojson.GeometryCollection(polygons)

    # write the polygon_collection geojson to a file in output directory
    if not pathlib.Path(output_dir).exists():
        pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    output_file_path = f"{output_dir}/{output_filename}"
    with open(output_file_path, "w+") as out:
        geojson.dump(polygon_collection, out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Retrieve all txt files from a folder and convert them in a  \
                geojson file of a geometry collection."
    )
    parser.add_argument(
        "--input_data_dir",
        type=str,
        help="Directory containing input data as text files.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        help="Directory to which the geojson file will be written to.",
    )
    parser.add_argument(
        "--output_filename",
        type=str,
        help="Name of geojson file to which output will be written to.",
    )
    args = parser.parse_args()

    if args.input_data_dir is not None:
        txt_files_list: List[pathlib.Path] = get_all_txt_files(args.input_data_dir)
        write_text_to_geojson(txt_files_list, args.output_dir, args.output_filename)
