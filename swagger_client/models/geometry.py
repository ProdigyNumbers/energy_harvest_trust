# coding: utf-8

"""
    The Earth Observatory Natural Event Tracker ([EONET](https://eonet.sci.gsfc.nasa.gov/what-is-eonet))

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 3.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Geometry(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'magnitude_value': 'str',
        'magnitude_unit': 'str',
        '_date': 'str',
        'type': 'str',
        'coordinates': 'list[float]'
    }

    attribute_map = {
        'magnitude_value': 'magnitudeValue',
        'magnitude_unit': 'magnitudeUnit',
        '_date': 'date',
        'type': 'type',
        'coordinates': 'coordinates'
    }

    def __init__(self, magnitude_value=None, magnitude_unit=None, _date=None, type=None, coordinates=None):  # noqa: E501
        """Geometry - a model defined in Swagger"""  # noqa: E501
        self._magnitude_value = None
        self._magnitude_unit = None
        self.__date = None
        self._type = None
        self._coordinates = None
        self.discriminator = None
        if magnitude_value is not None:
            self.magnitude_value = magnitude_value
        if magnitude_unit is not None:
            self.magnitude_unit = magnitude_unit
        if _date is not None:
            self._date = _date
        if type is not None:
            self.type = type
        if coordinates is not None:
            self.coordinates = coordinates

    @property
    def magnitude_value(self):
        """Gets the magnitude_value of this Geometry.  # noqa: E501

        Information regarding the event magnitude is displayed if available.  # noqa: E501

        :return: The magnitude_value of this Geometry.  # noqa: E501
        :rtype: str
        """
        return self._magnitude_value

    @magnitude_value.setter
    def magnitude_value(self, magnitude_value):
        """Sets the magnitude_value of this Geometry.

        Information regarding the event magnitude is displayed if available.  # noqa: E501

        :param magnitude_value: The magnitude_value of this Geometry.  # noqa: E501
        :type: str
        """

        self._magnitude_value = magnitude_value

    @property
    def magnitude_unit(self):
        """Gets the magnitude_unit of this Geometry.  # noqa: E501

        Information regarding the event magnitude unit is displayed if available.  # noqa: E501

        :return: The magnitude_unit of this Geometry.  # noqa: E501
        :rtype: str
        """
        return self._magnitude_unit

    @magnitude_unit.setter
    def magnitude_unit(self, magnitude_unit):
        """Sets the magnitude_unit of this Geometry.

        Information regarding the event magnitude unit is displayed if available.  # noqa: E501

        :param magnitude_unit: The magnitude_unit of this Geometry.  # noqa: E501
        :type: str
        """

        self._magnitude_unit = magnitude_unit

    @property
    def _date(self):
        """Gets the _date of this Geometry.  # noqa: E501

        The date/time will most likely be 00:00Z unless the source provided a particular time.  # noqa: E501

        :return: The _date of this Geometry.  # noqa: E501
        :rtype: str
        """
        return self.__date

    @_date.setter
    def _date(self, _date):
        """Sets the _date of this Geometry.

        The date/time will most likely be 00:00Z unless the source provided a particular time.  # noqa: E501

        :param _date: The _date of this Geometry.  # noqa: E501
        :type: str
        """

        self.__date = _date

    @property
    def type(self):
        """Gets the type of this Geometry.  # noqa: E501


        :return: The type of this Geometry.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Geometry.


        :param type: The type of this Geometry.  # noqa: E501
        :type: str
        """
        allowed_values = ["Point", "Polygon"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def coordinates(self):
        """Gets the coordinates of this Geometry.  # noqa: E501


        :return: The coordinates of this Geometry.  # noqa: E501
        :rtype: list[float]
        """
        return self._coordinates

    @coordinates.setter
    def coordinates(self, coordinates):
        """Sets the coordinates of this Geometry.


        :param coordinates: The coordinates of this Geometry.  # noqa: E501
        :type: list[float]
        """

        self._coordinates = coordinates

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Geometry, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Geometry):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
