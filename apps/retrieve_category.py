import swagger_client
from swagger_client.api.default_api import DefaultApi
from swagger_client.models import CategoryResponse


def main():
    api = DefaultApi()
    # Example 1: Obtain wildfire response object
    wildfire_response: CategoryResponse = api.categories_category_id_get("wildfires")
    # Example 2: Obtain wildfire response object from a specific source
    wildfire_response_source: CategoryResponse = api.categories_category_id_get(
        "wildfires", source="InciWeb"
    )
    # Example 3:
    print(wildfire_response)
    print(wildfire_response_source._description)


if __name__ == "__main__":
    main()
