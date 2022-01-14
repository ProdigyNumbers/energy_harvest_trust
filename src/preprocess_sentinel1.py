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
        geometry: The polygon of the region we will be looking at 
        border_noise_correction: true or false options to apply additional Border noise correction (Optional)
        speckle_filtering: true or false options to apply speckle filtering (optional)
        speckle_filter:
            'BOX_CAR': Applies a boxcar filter on each individual image in the collection

    Returns : 
        An ee.ImageCollection with an analysis ready Sentinel 1 imagery with the specified polarization images and 
        angle band.
"""
import ee
import json
from types import SimpleNamespace


def preprocess_sentinel1(parameters):
    return


def load_data(input_parameters: str):
    ee.Initialize()
    parameters = json.loads(
        input_parameters, object_hook=lambda d: SimpleNamespace(**d)
    )
    sentinel1_data = preprocess_sentinel1(parameters)
