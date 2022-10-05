import geopandas as gpd
from typing import Tuple, List

Extents = Tuple[float, float, float, float]
Point2D = Tuple[float, float]
BoundingBox = Tuple[Point2D, Point2D, Point2D, Point2D]


def extract_state_dataframe(
    countryGDF: gpd.geodataframe.GeoDataFrame, state_name: str
) -> gpd.geodataframe.GeoDataFrame:
    """Extracts the geodataframe for a given state from the gadm level 1 shapefile of a country

    Args:
        countryGDF (gpd.geodataframe.GeoDataFrame): GeoDataFrame of the gadm36 level 1 shapefile of a country
        state_name (str): Name of a state present in the country represented by countryGDF.

    Returns:
        gpd.geodataframe.GeoDataFrame: GeoDataFrame of the state as extracted from countryGDF
    """
    state_gdf: gpd.geodataframe.GeoDataFrame = countryGDF[
        countryGDF["NAME_1"] == state_name
    ]
    state_gdf = state_gdf[["NAME_1", "geometry"]]
    return state_gdf


def extract_district_dataframe(
    countryGDF: gpd.geodataframe.GeoDataFrame, district_name: str
) -> gpd.geodataframe.GeoDataFrame:
    """Extracts the geodataframe for a given district from the gadm level 2 shapefile of a country

    Args:
        countryGDF (gpd.geodataframe.GeoDataFrame): GeoDataFrame of the gadm36 level 2 shapefile of a country
        district_name (str): Name of a district present in the country represented by countryGDF.

    Returns:
        gpd.geodataframe.GeoDataFrame: GeoDataFrame of the state as extracted from countryGDF
    """
    district_gdf: gpd.geodataframe.GeoDataFrame = countryGDF[
        countryGDF["NAME_2"] == district_name
    ]
    district_gdf = district_gdf[["NAME_2", "geometry"]]
    return district_gdf


def region_extents(region_gdf: gpd.geodataframe.GeoDataFrame) -> Extents:
    """Computes the extents the bounding box of a given geo dataframe.

    Args:
        region_gdf (gpd.geodataframe.GeoDataFrame): Geo Dataframe of a region.

    Returns:
        Extents: Denotes the coordinates of the bounding box of the geo dataframe.
    """
    region_bbox = region_gdf.bounds
    w, s, e, n = (
        region_bbox.minx.values[0],
        region_bbox.miny.values[0],
        region_bbox.maxx.values[0],
        region_bbox.maxy.values[0],
    )
    return (w, s, e, n)


def compute_center_from_extents(state_extents: Extents):
    center = [
        (state_extents[1] + state_extents[3]) / 2.0,
        (state_extents[0] + state_extents[2]) / 2.0,
    ]
    return center


def get_region_bounding_box(region_extents: Extents) -> BoundingBox:
    left_down = (region_extents[0], region_extents[1])
    right_down = (region_extents[2], region_extents[1])
    right_up = (region_extents[2], region_extents[3])
    left_up = (region_extents[0], region_extents[3])
    return (left_down, right_down, right_up, left_up)
