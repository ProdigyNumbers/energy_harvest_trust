import os

print(os.getcwd())


from swagger_client.api.categories_api import CategoriesApi


api = CategoriesApi()
api.get_category_by_id(1)
