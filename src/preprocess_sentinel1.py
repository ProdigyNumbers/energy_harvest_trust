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
import ee
import json
from types import SimpleNamespace
import logging
import geopandas as gpd
import urllib


def preprocess_sentinel1(parameters: SimpleNamespace):

    # extract parameters
    start_date = ee.Date(parameters.start_date)
    end_date = ee.Date(parameters.end_date)
    polarization = parameters.polarization
    orbit = parameters.orbit
    if parameters.geometry.type == "Polygon":
        geometry = ee.Geometry.Polygon(parameters.geometry.coordinates)
    # border_noise_correction = parameters.border_noise_correction
    # speckle_filtering = parameters.speckle_filtering
    # speckle_filter = parameters.speckle_filter
    # format = parameters.format
    clip_to_region = parameters.clip_to_region
    save_to_drive = parameters.save_to_drive
    write_to_csv = parameters.write_to_csv
    output_path = parameters.output_path

    # check the validity of the parameters
    # if speckle_filter is None:
    #     speckle_filter = 'BOX_CAR'
    # if format is None:
    #     format = 'DB'
    if orbit is None:
        orbit = "BOTH"

    polarization_band = ["VV", "VH", "VVVH"]
    if polarization not in polarization_band:
        raise ValueError(
            "The polarization must be one of the following: {}".format(
                polarization_band
            )
        )

    orbit_values = ["ASCENDING", "DESCENDING", "BOTH"]
    if orbit not in orbit_values:
        raise ValueError(
            "The orbit must be one of the following: {}".format(orbit_values)
        )

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
        .filterDate(start_date, end_date)
        .filterBounds(geometry)
        .select(["VH"])
    )

    # select orbit
    if orbit != "BOTH":
        sentinel1 = sentinel1.filter(ee.Filter.eq("orbitProperties_pass", orbit))

    # select polarization
    if polarization == "VV":
        sentinel1 = sentinel1.select(["VV"])
    elif polarization == "VH":
        sentinel1 = sentinel1.select(["VH"])
    elif polarization == "VVVH":
        sentinel1 = sentinel1.select(["VV", "VH"])

    logging.info(
        "Number of images in the collection: {}".format(sentinel1.size().getInfo())
    )

    if clip_to_region:
        sentinel1 = sentinel1.map(lambda image: image.clip(geometry))

    if save_to_drive:
        size = sentinel1.size().getInfo()
        image_list = sentinel1.toList(size)
        for id in range(0, size):
            image = image_list.get(id)
            image = ee.Image(image)
            image_name = str(image.id().getInfo())
            description = image_name

            image = image.clip(geometry)
            if write_to_csv:
                # Add a layer to image with lat, lon.
                image_lat = image.addBands(image.pixelLonLat())
                # Extract a sample as csv
                csv_url = image_lat.sample(
                    region=sentinel1.geometry(),
                    dropNulls=True,
                    scale=10,
                    geometries=True,
                ).getDownloadUrl()
                urllib.request.urlretrieve(
                    csv_url, output_path + "/" + image_name + ".csv"
                )

            image_path = image.getDownloadUrl(
                {
                    "scale": 10,
                    "region": sentinel1.geometry().getInfo(),
                    "crs": "EPSG:4326",
                    "description": description,
                    "fileFormat": "GeoTIFF",
                    "maxPixels": 1e13,
                    "fileNamePrefix": image_name,
                }
            )
            urllib.request.urlretrieve(
                image_path, output_path + "/" + image_name + ".tif"
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
            logging.info("Exporting image {} to Local Drive".format(image_name))
    return sentinel1


def load_data(input_parameters: str):
    ee.Initialize()
    # parameters = json.loads(
    #     input_parameters, object_hook=lambda d: SimpleNamespace(**d)
    # )
    with open(input_parameters, "r") as f:
        parameters = json.load(f)
        f.seek(0)
        parameters = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
        sentinel1_data = preprocess_sentinel1(parameters)
