"""API to preprocess sentinel data.
    Parameters :
        start_date : Start date to get images (inclusive)
        end_date : Last date to get images (inclusive)
        polarization: The Sentinel-1 image polarization to select for processing.
            'VV' : selects the VV polarization
            'VH' : selects the VH polarization
            'VVVH' : selects both VV and VH polarization for processing.
            In our case the default will be 'VH' since that is what is required by this paper :
            (https://www.nature.com/articles/s41597-019-0036-3)
        orbit: Orbits to include (BOTH, ASCENDING or DESCENDING)
        state_name: State name to get the geometry from the country shapefile
        border_noise_correction: true or false options to apply additional Border noise correction (Optional)
        speckle_filtering: true or false options to apply speckle filtering (optional)
        speckle_filter:
            'BOX_CAR': Applies a boxcar filter on each individual image in the collection
        format: the output format for the processed collection is either `LINEAR` or `DB`.
        clip_to_region: true or false options to clip the output collection to the region of interest (optional)
        save_to_drive: true or false options to save the output collection to Google Drive (optional)
        output_path: the path to save the output collection to Google Drive (optional)

    Returns :
        An ee.ImageCollection with an analysis ready Sentinel 1 imagery with the specified
        polarization images and angle band.
"""

import contextlib
import json
import os
import urllib.error
import urllib.request
from types import SimpleNamespace
from typing import List

import ee
import geojson
import geojson.geometry
from src.lib.common.logger_factory import LoggerFactory

logger = LoggerFactory("preprocess_sentinel1").get_logger()

from dataclasses import dataclass


@dataclass
class Configuration:
    start_date: ee.Date
    end_date: ee.Date
    polarization_list: List[str]
    orbit: str
    clip_to_region: bool
    save_to_drive: bool
    write_to_csv: bool
    output_path: str
    sampling_factor: float


def create_configuration(config: SimpleNamespace) -> Configuration:
    start_date = ee.Date(config.start_date)
    end_date = ee.Date(config.end_date)
    polarization_list = config.polarization.replace(" ", "").split(",")
    orbit = config.orbit
    clip_to_region = config.clip_to_region
    save_to_drive = config.save_to_drive
    write_to_csv = config.write_to_csv
    output_path = config.output_path
    sampling_factor = config.sampling_factor
    return Configuration(
        start_date,
        end_date,
        polarization_list,
        orbit,
        clip_to_region,
        save_to_drive,
        write_to_csv,
        output_path,
        sampling_factor,
    )


def validate_configuration(config: Configuration):
    # Create output_path in case it doesn't exist
    os.makedirs(config.output_path, exist_ok=True)

    if config.orbit is None:
        config.orbit = "BOTH"

    polarization_band = ["HH", "HV", "VV", "VH"]
    valid_pol_list = all(item in polarization_band for item in config.polarization_list)
    if not valid_pol_list:
        raise ValueError(
            f"The polarization must be one of the following: {polarization_band}"
        )

    orbit_values = ["ASCENDING", "DESCENDING", "BOTH"]
    if config.orbit not in orbit_values:
        raise ValueError(f"The orbit must be one of the following: {orbit_values}")

    if config.sampling_factor < 0 or config.sampling_factor > 1:
        raise ValueError("The sampling factor has to lie between (0,1]")

    return config


def preprocess_sentinel_1(
    index: int, geometry: geojson.geometry.Polygon, config: SimpleNamespace
):
    # create configuration polygons
    configuration: Configuration = create_configuration(config)
    # validate configuration
    configuration = validate_configuration(config=configuration)
    poly_name = f"Polygon_{index}"
    output_dir = os.path.join(configuration.output_path, poly_name)
    os.makedirs(output_dir, exist_ok=True)

    if geometry.type == "Polygon":
        return _extracted_from_preprocess_sentinel_1_13(geometry, configuration, config, output_dir)


# TODO Rename this here and in `preprocess_sentinel_1`
def _extracted_from_preprocess_sentinel_1_13(geometry, configuration, config, output_dir):
    polygon = ee.Geometry.Polygon(geometry.coordinates)
    # read more about the data collection here
    # https://developers.google.com/earth-engine/tutorials/community/sar-basics
    # get the Sentinel-1 data image collection
    sentinel1 = (
        ee.ImageCollection("COPERNICUS/S1_GRD")
        .filter(ee.Filter.eq("instrumentMode", "IW"))
        .filter(ee.Filter.eq("resolution_meters", 10))
        .filterDate(configuration.start_date, configuration.end_date)
        .filterBounds(polygon)
        # .select(["VH", "VV", "HH", "HV"])
    )

    # select orbit
    if configuration.orbit != "BOTH":
        sentinel1 = sentinel1.filter(
            ee.Filter.eq("orbitProperties_pass", configuration.orbit)
        )

    # select polarization
    # if configuration.polarization_list != [""]:
    #     sentinel1 = sentinel1.select(configuration.polarization_list)
    # if configuration.polarization == "VV":
    #     sentinel1 = sentinel1.select(["VV"])
    # elif configuration.polarization == "VH":
    #     sentinel1 = sentinel1.select(["VH"])
    # elif configuration.polarization == "VVVH":
    #     sentinel1 = sentinel1.select(["VV", "VH"])
    # elif configuration.polarization == "VVVHHH":
    #     sentinel1 = sentinel1.select(["VV", "VH", ])

    logger.info(f"Number of images in the collection: {sentinel1.size().getInfo()}")

    if configuration.clip_to_region:
        sentinel1 = sentinel1.map(lambda image: image.clip(geometry))

    if configuration.save_to_drive:
        size = sentinel1.size().getInfo()
        image_list = sentinel1.toList(size)
        for id in range(size):
            image = image_list.get(id)
            image = ee.Image(image)
            image_name = str(image.id().getInfo())
            description = image_name

            image = image.clip(geometry)
            if configuration.write_to_csv:
                # Add a layer to image with lat, lon.
                image_lat = image.addBands(image.pixelLonLat())
                # Extract a sample as csv
                csv_url = image_lat.sample(
                    region=sentinel1.geometry(),
                    dropNulls=True,
                    scale=10,
                    geometries=True,
                    factor=config.sampling_factor,
                ).getDownloadUrl()

                if not os.path.exists(
                    os.path.join(output_dir, f"{image_name}.csv")
                ):
                    with contextlib.suppress(urllib.error.HTTPError):
                        urllib.request.urlretrieve(
                            csv_url, os.path.join(output_dir, f"{image_name}.csv")
                        )

            image_path = image.getDownloadUrl(
                {
                    "scale": 10,
                    "region": sentinel1.geometry().getInfo(),
                    "crs": "EPSG:4326",
                    "description": description,
                    "format": "GEO_TIFF",
                    "maxPixels": 1e13,
                    "fileNamePrefix": image_name,
                }
            )

            if not os.path.exists(os.path.join(output_dir, f"{image_name}.tif")):
                with contextlib.suppress(urllib.error.HTTPError):
                    urllib.request.urlretrieve(
                        image_path, os.path.join(output_dir, f"{image_name}.tif")
                    )
            logger.info(f"Exporting image {image_name} to Local Drive")

    return sentinel1


def preprocess_sentinel1(parameters: SimpleNamespace, config: SimpleNamespace):

    geometry = ee.Geometry.Polygon()
    # extract configuration parameters
    configuration: Configuration = create_configuration(config)
    configuration = validate_configuration(configuration)
    if parameters.geometry.type == "Polygon":
        geometry = ee.Geometry.Polygon(parameters.geometry.coordinates)
    # border_noise_correction = parameters.border_noise_correction
    # speckle_filtering = parameters.speckle_filtering
    # speckle_filter = parameters.speckle_filter
    # format = parameters.format

    # check the validity of the parameters
    # if speckle_filter is None:
    #     speckle_filter = 'BOX_CAR'
    # if format is None:
    #     format = 'DB'

    # format_values = ['LINEAR', 'DB']
    # if format not in format_values:
    #     raise ValueError('The format must be one of the following: {}'.format(format_values))

    # format_speckle_filter = ['BOX_CAR']
    # if speckle_filter not in format_speckle_filter:
    #     raise ValueError('The speckle filter must be one of the following: {}'.format(format_speckle_filter))

    # read more about the data collection here https://developers.google.com/earth-engine/tutorials/community/sar-basics
    # get the Sentinel-1 data image collection
    sentinel1 = (
        ee.ImageCollection("COPERNICUS/S1_GRD")
        .filter(ee.Filter.eq("instrumentMode", "IW"))
        .filter(ee.Filter.eq("resolution_meters", 10))
        .filter(ee.Filter.listContains("transmitterReceiverPolarisation", "VH"))
        .filter(ee.Filter.listContains("transmitterReceiverPolarisation", "VV"))
        .filterDate(configuration.start_date, configuration.end_date)
        .filterBounds(geometry)
        .select(["VH", "VV"])
    )

    # select orbit
    if configuration.orbit != "BOTH":
        sentinel1 = sentinel1.filter(
            ee.Filter.eq("orbitProperties_pass", configuration.orbit)
        )

    # select polarization
    # if configuration.polarization_list != [""]:
    #     sentinel1 = sentinel1.select(configuration.polarization_list)
    # if configuration.polarization == "VV":
    #     sentinel1 = sentinel1.select(["VV"])
    # elif configuration.polarization == "VH":
    #     sentinel1 = sentinel1.select(["VH"])
    # elif configuration.polarization == "VVVH":
    #     sentinel1 = sentinel1.select(["VV", "VH"])

    logger.info(f"Number of images in the collection: {sentinel1.size().getInfo()}")

    if configuration.clip_to_region:
        sentinel1 = sentinel1.map(lambda image: image.clip(geometry))

    if configuration.save_to_drive:
        size = sentinel1.size().getInfo()
        image_list = sentinel1.toList(size)
        for id in range(size):
            image = image_list.get(id)
            image = ee.Image(image)
            image_name = str(image.id().getInfo())
            description = image_name

            image = image.clip(geometry)
            if configuration.write_to_csv:
                # Add a layer to image with lat, lon.
                image_lat = image.addBands(image.pixelLonLat())
                # Extract a sample as csv
                csv_url = image_lat.sample(
                    region=sentinel1.geometry(),
                    dropNulls=True,
                    scale=10,
                    geometries=True,
                ).getDownloadUrl()

                if not os.path.exists(
                    os.path.join(
                        csv_url, configuration.output_path, f"{image_name}.csv"
                    )
                ):

                    with contextlib.suppress(urllib.error.HTTPError):
                        urllib.request.urlretrieve(
                            os.path.join(
                                csv_url, configuration.output_path, f"{image_name}.csv"
                            )
                        )

            image_path = image.getDownloadUrl(
                {
                    "scale": 10,
                    "region": sentinel1.geometry().getInfo(),
                    "crs": "EPSG:4326",
                    "description": description,
                    "format": "GEO_TIFF",
                    "maxPixels": 1e13,
                    "fileNamePrefix": image_name,
                }
            )
            if not os.path.exists(
                os.path.join(image_path, configuration.output_path, f"{image_name}.tif")
            ):
                with contextlib.suppress(urllib.error.HTTPError):
                    urllib.request.urlretrieve(
                        os.path.join(
                            image_path, configuration.output_path, f"{image_name}.tif"
                        )
                    )

            # task = ee.batch.Export.image.toDrive(
            #     image=image.clip(geometry),
            #     description=description,
            #     folder="DSSG",
            #     fileNamePrefix=image_name,
            #     region=sentinel1.geometry(),
            #     scale=10,
            #     crs="EPSG:4326",
            #     maxPixels=1e13,
            # )

            # task.start()
            # logging.info("Exporting image {} to {}".format(image_name, output_path))
            logger.info(f"Exporting image {image_name} to Local Drive")
    return sentinel1


def load_data_collection(input_collections_file: str, config: SimpleNamespace):
    ee.Initialize()
    with open(input_collections_file, "r") as f:
        geometries = geojson.load(f)
    for index, geometry in enumerate(geometries["geometries"]):
        sentinel1 = preprocess_sentinel_1(index, geometry=geometry, config=config)


def load_data(input_parameters: str, config: SimpleNamespace):
    ee.Initialize()
    # parameters = json.loads(
    #     input_parameters, object_hook=lambda d: SimpleNamespace(**d)
    # )
    with open(input_parameters, "r") as f:
        parameters = json.load(f)
        f.seek(0)
        parameters = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
        sentinel1_data = preprocess_sentinel1(parameters, config)


def load_config(config_file: str):
    with open(config_file, "r") as f:
        config = json.load(f)
        f.seek(0)
        config = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
    return config
