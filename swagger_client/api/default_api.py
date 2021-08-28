# coding: utf-8

"""
    The Earth Observatory Natural Event Tracker ([EONET](https://eonet.sci.gsfc.nasa.gov/what-is-eonet))

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 3.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from swagger_client.api_client import ApiClient


class DefaultApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def categories_category_id_get(self, category_id, **kwargs):  # noqa: E501
        """Returns a json object of categories.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.categories_category_id_get(category_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str category_id: Filter the events by the Category. (required)
        :param str source: Filter the topically-constrained events by the Source. Multiple sources can be included in the parameter, comma separated, operates as a boolean OR.
        :param str status: Events that have ended are assigned a closed date and the existence of that date will allow you to filter for only-open or only-closed events. Omitting the status parameter will return only the currently open events.
        :param int limit: Limits the number of events returned.
        :param int days: Limit the number of prior days (including today) from which events will be returned.
        :param str start: Select a starting date for the events. To be used together with end parameter.
        :param str end: Select an ending date for the events. To be used together with start parameter for defining a range.
        :return: CategoryResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        if kwargs.get('async_req'):
            return self.categories_category_id_get_with_http_info(category_id, **kwargs)  # noqa: E501
        else:
            (data) = self.categories_category_id_get_with_http_info(category_id, **kwargs)  # noqa: E501
            return data

    def categories_category_id_get_with_http_info(self, category_id, **kwargs):  # noqa: E501
        """Returns a json object of categories.  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.categories_category_id_get_with_http_info(category_id, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param str category_id: Filter the events by the Category. (required)
        :param str source: Filter the topically-constrained events by the Source. Multiple sources can be included in the parameter, comma separated, operates as a boolean OR.
        :param str status: Events that have ended are assigned a closed date and the existence of that date will allow you to filter for only-open or only-closed events. Omitting the status parameter will return only the currently open events.
        :param int limit: Limits the number of events returned.
        :param int days: Limit the number of prior days (including today) from which events will be returned.
        :param str start: Select a starting date for the events. To be used together with end parameter.
        :param str end: Select an ending date for the events. To be used together with start parameter for defining a range.
        :return: CategoryResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['category_id', 'source', 'status', 'limit', 'days', 'start', 'end']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method categories_category_id_get" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'category_id' is set
        if ('category_id' not in params or
                params['category_id'] is None):
            raise ValueError("Missing the required parameter `category_id` when calling `categories_category_id_get`")  # noqa: E501

        collection_formats = {}

        path_params = {}
        if 'category_id' in params:
            path_params['categoryId'] = params['category_id']  # noqa: E501

        query_params = []
        if 'source' in params:
            query_params.append(('source', params['source']))  # noqa: E501
        if 'status' in params:
            query_params.append(('status', params['status']))  # noqa: E501
        if 'limit' in params:
            query_params.append(('limit', params['limit']))  # noqa: E501
        if 'days' in params:
            query_params.append(('days', params['days']))  # noqa: E501
        if 'start' in params:
            query_params.append(('start', params['start']))  # noqa: E501
        if 'end' in params:
            query_params.append(('end', params['end']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = []  # noqa: E501

        return self.api_client.call_api(
            '/categories/{categoryId}', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='CategoryResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)