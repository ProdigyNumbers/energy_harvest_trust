from dataclasses import dataclass
from pathlib import Path
from typing import List

import pandas
from pandas import DataFrame, concat, read_csv

# Uses of different polarizations:
# HH polarization shows good capability in monitoring surface soil properties
# VV polarization is better for observing information of vertical vegetation structure,
# the cross polarizations (HV and VH) are good for capturing information of total canopy volume and plant biomass

"""_summary_

This code preprocesses all the downloaded csv files given a path and type of field
- It filters only the columns belonging to 'VV', 'VH', 'HH' and 'HV' polarisations and latitude and longitude
  and date.
- It combines all the csv's in the given path to one single csv with required path
_type_: _description_
"""


def concatenate_all_csv_files(path: Path, field_type: str) -> DataFrame:
    # read all csv files from a folder
    csv_files = path.rglob('*.csv')
    cols = ['VV', 'VH', 'HH', 'HV', 'latitude', 'longitude']
    df_list: List[DataFrame] = []
    for file in csv_files:
        str_file = str(file)
        if field_type in str_file.lower():
            try:
                df: DataFrame = read_csv(file)
                # extract columns: "VV", "VH", "HH", "HV", "lat", "lon"
                df_filter = df[df.columns[df.columns.isin(cols)]]
                date = (file.name)[17:25]
                df_filter["date"] = date
                df_filter["field_type"] = field_type
                df_list.append(df_filter)
            except pandas.errors.EmptyDataError:
                print(f"{file} is empty and won't be read.")
    if not df_list:
        raise ValueError(f"{field_type} unknown")
    return concat(df_list)


# @click.command()
# @click.option('--path', help='path to all csv files', type=Path)
# @click.option('--field_type', help='path to all csv files with field_type in path', type=str)
# @click.option('--output_dir', help='path to where the output is written to', type=Path)
def preprocess_csv(path: Path, field_type: str, output_dir: Path):
    df = concatenate_all_csv_files(path, field_type)
    # write the combined DataFrame to file
    output_file = Path(output_dir) / f"{field_type}_fields.csv"
    df.to_csv(output_file, index=False)

if __name__ == "__main__":

    absolute_path = Path().absolute()
    path = absolute_path / "data" / "output"
    print(type(path), path)
    output_dir = absolute_path / "data" / "output_clean"
    print(type(output_dir), output_dir)
    # preprocess all paddy fields and put in one file
    preprocess_csv(path, "paddy", output_dir)
    # preprocess all cotton fields and put in one file
    preprocess_csv(path, "cotton", output_dir)
    # preprocess play ground etc
    preprocess_csv(path, "play_ground", output_dir)
    # preprocess trees
    preprocess_csv(path, "tree", output_dir)
