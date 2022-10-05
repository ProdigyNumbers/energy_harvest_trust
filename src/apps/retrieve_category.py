from swagger_client.api.default_api import DefaultApi
from swagger_client.models.category_response import CategoryResponse


def main():
    api = DefaultApi()
    # # Example 1: Obtain wildfire response object
    # wildfire_response: CategoryResponse = api.categories_category_id_get("wildfires")
    # # Example 2: Obtain wildfire response object from a specific source
    # wildfire_response_source: CategoryResponse = api.categories_category_id_get(
    #     "wildfires", source="InciWeb"
    # )

    # # Example 3: Obtain wildfire response from a specific source in a specific date range
    # wildfire_response_range: CategoryResponse = api.categories_category_id_get(
    #     "wildfires", source="InciWeb,EO", start="2020-09-01", end="2020-09-30"
    # )

    # Example 4: Read data/sources.json and create a string of all the ids

    src = "ABFIRE,BCWILDFIRE,CALFIRE,InciWeb,MBFIRE,PDC"
    event_response: CategoryResponse = api.events_get(
        source=src,
        category="wildfires",
        status="all",
        start="2020-01-01",
        end="2020-12-31",
        bbox="74.919357,32.026057,76.196246,29.869031",
    )  # type: ignore
    print(event_response._events)


if __name__ == "__main__":
    main()
