# -*- coding: UTF-8 -*-
"""
This module provides a class for storing properties of points (and therefore also for lines). Properties for points are
the same as logs, except there is only one value, not a list of values. They are both derived from the AbstractLogClass.

.. todo:: - reformat docstrings, espacially of setter and getter functions
          - check exception types
"""

import sqlalchemy as sq

from enum import Enum
from GeologicalToolbox.AbstractLog import AbstractLogClass
from GeologicalToolbox.DBHandler import Base, AbstractDBObject


class PropertyTypes(Enum):
    INT = 0,
    FLOAT = 1,
    STRING = 2


class Property(Base, AbstractLogClass):
    """
    This class represents logging information for wells
    """
    # define db table name and columns
    __tablename__ = 'properties'

    id = sq.Column(sq.INTEGER, sq.Sequence('properties_id_seq'), primary_key=True)
    point_id = sq.Column(sq.INTEGER, sq.ForeignKey('geopoints.id'), default=-1)
    prop_value = sq.Column(sq.TEXT, default="")
    prop_type = sq.Column(sq.VARCHAR(20), default="string")

    def __init__(self, *args, **kwargs):
        # type: (*object, **object) -> None
        """
        Initialise the class

        :param args: parameters for AbstractLogClass initialisation
        :type args: List()

        :param kwargs: parameters for AbstractLogClass initialisation
        :type kwargs: Dict()
        """
        AbstractLogClass.__init__(self, *args, **kwargs)

    def __repr__(self):
        text = "<Property(value={})>\n".format(self.value)
        text += AbstractLogClass.__repr__(self)
        return text

    def __str__(self):
        text = "{} [{}]: {} - ".format(self.property_name, self.property_unit, self.value)
        text += AbstractDBObject.__str__(self)
        return text

    def __convert_value(self, value):
        """
        converts the property value from type string to the specified type
        :return: converted property value
        """

        if self.property_type == PropertyTypes.STRING:
            return value
        try:
            if self.property_type == PropertyTypes.INT:
                return int(value)
            if self.property_type == PropertyTypes.FLOAT:
                return float(value)
        except ValueError:
            return None

    def __check_value(self, value):
        # type: (any) -> bool
        """
        Test, if the value can be converted to the specified format
        :param value: value to test
        :return: True, if it can be converted, else False
        """
        return self.__convert_value(value) is not None

    @property
    def property_type(self):
        # type: () -> PropertyTypes
        """
        Returns the type of the value
        :return: Returns the type of the value
        """
        return PropertyTypes[self.prop_type]

    @property_type.setter
    def property_type(self, value):
        # type: (PropertyTypes) -> None
        """
        Sets a new type for the property
        :return: nothing
        :raises ValueError: if type is not available in PropertyTypes
        """
        if not isinstance(value, PropertyTypes):
            raise ValueError("{} is not in PropertyTypes".format(value))
        self.prop_type = value.name

    @property
    def property_value(self):
        # type: () -> str
        """
        Returns the value of the property

        :return: Returns the value of the property
        """
        return self.__convert_value(self.prop_value)

    @property_value.setter
    def property_value(self, value):
        # type: (any) -> None
        """
        Sets a new value for the property

        :param value: new value
        :type value: float

        :return: Nothing
        :raises ValueError: Raises ValueError if prop_value cannot be converted to the specified property_type
        """
        if self.__check_value(str(value)):
            self.prop_value = str(value)
        else:
            raise ValueError("Cannot convert property values [{}] to specified type {}".
                             format(value, self.property_type.name))
