# coding: utf-8

"""
    The Earth Observatory Natural Event Tracker ([EONET](https://eonet.sci.gsfc.nasa.gov/what-is-eonet))

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 3.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import swagger_client
from swagger_client.models.category import Category  # noqa: E501
from swagger_client.rest import ApiException


class TestCategory(unittest.TestCase):
    """Category unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCategory(self):
        """Test Category"""
        # FIXME: construct object with mandatory attributes with example values
        # model = swagger_client.models.category.Category()  # noqa: E501
        model = swagger_client.models.category.Category(1)


if __name__ == "__main__":
    unittest.main()
