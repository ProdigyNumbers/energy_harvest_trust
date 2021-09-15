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

class Event(object):
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
        'id': 'str',
        'title': 'str',
        'description': 'str',
        'link': 'str',
        'closed': 'str',
        'categories': 'list[OneOfEventCategoriesItems]',
        'sources': 'list[OneOfEventSourcesItems]',
        'geometry': 'list[OneOfEventGeometryItems]'
    }

    attribute_map = {
        'id': 'id',
        'title': 'title',
        'description': 'description',
        'link': 'link',
        'closed': 'closed',
        'categories': 'categories',
        'sources': 'sources',
        'geometry': 'geometry'
    }

    def __init__(self, id=None, title=None, description=None, link=None, closed=None, categories=None, sources=None, geometry=None):  # noqa: E501
        """Event - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._title = None
        self._description = None
        self._link = None
        self._closed = None
        self._categories = None
        self._sources = None
        self._geometry = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if link is not None:
            self.link = link
        if closed is not None:
            self.closed = closed
        if categories is not None:
            self.categories = categories
        if sources is not None:
            self.sources = sources
        if geometry is not None:
            self.geometry = geometry

    @property
    def id(self):
        """Gets the id of this Event.  # noqa: E501

        Unique id for this event.  # noqa: E501

        :return: The id of this Event.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Event.

        Unique id for this event.  # noqa: E501

        :param id: The id of this Event.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def title(self):
        """Gets the title of this Event.  # noqa: E501

        The title of the event.  # noqa: E501

        :return: The title of this Event.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this Event.

        The title of the event.  # noqa: E501

        :param title: The title of this Event.  # noqa: E501
        :type: str
        """

        self._title = title

    @property
    def description(self):
        """Gets the description of this Event.  # noqa: E501

        Optional longer description of the event. Most likely only a sentence or two.  # noqa: E501

        :return: The description of this Event.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this Event.

        Optional longer description of the event. Most likely only a sentence or two.  # noqa: E501

        :param description: The description of this Event.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def link(self):
        """Gets the link of this Event.  # noqa: E501

        The full link to the API endpoint for this specific event.  # noqa: E501

        :return: The link of this Event.  # noqa: E501
        :rtype: str
        """
        return self._link

    @link.setter
    def link(self, link):
        """Sets the link of this Event.

        The full link to the API endpoint for this specific event.  # noqa: E501

        :param link: The link of this Event.  # noqa: E501
        :type: str
        """

        self._link = link

    @property
    def closed(self):
        """Gets the closed of this Event.  # noqa: E501

        An event is deemed “closed” when it has ended. The closed field will include a date/time when the event has ended. Depending upon the nature of the event, the closed value may or may not accurately represent the absolute ending of the event. If the event is open, this will show “null”.  # noqa: E501

        :return: The closed of this Event.  # noqa: E501
        :rtype: str
        """
        return self._closed

    @closed.setter
    def closed(self, closed):
        """Sets the closed of this Event.

        An event is deemed “closed” when it has ended. The closed field will include a date/time when the event has ended. Depending upon the nature of the event, the closed value may or may not accurately represent the absolute ending of the event. If the event is open, this will show “null”.  # noqa: E501

        :param closed: The closed of this Event.  # noqa: E501
        :type: str
        """

        self._closed = closed

    @property
    def categories(self):
        """Gets the categories of this Event.  # noqa: E501

        One or more categories assigned to the event.  # noqa: E501

        :return: The categories of this Event.  # noqa: E501
        :rtype: list[OneOfEventCategoriesItems]
        """
        return self._categories

    @categories.setter
    def categories(self, categories):
        """Sets the categories of this Event.

        One or more categories assigned to the event.  # noqa: E501

        :param categories: The categories of this Event.  # noqa: E501
        :type: list[OneOfEventCategoriesItems]
        """

        self._categories = categories

    @property
    def sources(self):
        """Gets the sources of this Event.  # noqa: E501

        One or more sources that refer to more information about the event.  # noqa: E501

        :return: The sources of this Event.  # noqa: E501
        :rtype: list[OneOfEventSourcesItems]
        """
        return self._sources

    @sources.setter
    def sources(self, sources):
        """Sets the sources of this Event.

        One or more sources that refer to more information about the event.  # noqa: E501

        :param sources: The sources of this Event.  # noqa: E501
        :type: list[OneOfEventSourcesItems]
        """

        self._sources = sources

    @property
    def geometry(self):
        """Gets the geometry of this Event.  # noqa: E501

        One or more event geometries are the pairing of a specific date/time with a location. Information regarding the event magnitude, if available, is displayed here.  # noqa: E501

        :return: The geometry of this Event.  # noqa: E501
        :rtype: list[OneOfEventGeometryItems]
        """
        return self._geometry

    @geometry.setter
    def geometry(self, geometry):
        """Sets the geometry of this Event.

        One or more event geometries are the pairing of a specific date/time with a location. Information regarding the event magnitude, if available, is displayed here.  # noqa: E501

        :param geometry: The geometry of this Event.  # noqa: E501
        :type: list[OneOfEventGeometryItems]
        """

        self._geometry = geometry

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
        if issubclass(Event, dict):
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
        if not isinstance(other, Event):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
