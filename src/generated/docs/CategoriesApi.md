# swagger_client.CategoriesApi

All URIs are relative to *https://eonet.sci.gsfc.nasa.gov/api/v3*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_category_by_id**](CategoriesApi.md#get_category_by_id) | **GET** /categories/{categoryId} | Categories are the types of events by which individual events are cataloged

# **get_category_by_id**
> Category get_category_by_id(category_id)

Categories are the types of events by which individual events are cataloged

Returns a single category

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = swagger_client.CategoriesApi()
category_id = 789 # int | ID of category to return

try:
    # Categories are the types of events by which individual events are cataloged
    api_response = api_instance.get_category_by_id(category_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CategoriesApi->get_category_by_id: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **category_id** | **int**| ID of category to return | 

### Return type

[**Category**](Category.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

