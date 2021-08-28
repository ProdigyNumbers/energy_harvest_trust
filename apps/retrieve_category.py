import swagger_client
from swagger_client.api.default_api import DefaultApi
from swagger_client.models import CategoryResponse


def main():
    api = DefaultApi()
    wildfire_response: CategoryResponse = api.categories_category_id_get("wildfires")

    print(wildfire_response)


if __name__ == "__main__":
    main()
