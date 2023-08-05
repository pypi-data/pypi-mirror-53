# coding: utf-8

"""
Copyright (c) 2019 Aspose.Cells Cloud
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
"""


from pprint import pformat
from six import iteritems
import re


class IconSet(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
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
        'reverse': 'bool',
        'cf_icons': 'list[ConditionalFormattingIcon]',
        'cfvos': 'list[ConditionalFormattingValue]',
        'icon_set_type': 'str',
        'is_custom': 'bool',
        'show_value': 'bool'
    }

    attribute_map = {
        'reverse': 'Reverse',
        'cf_icons': 'CfIcons',
        'cfvos': 'Cfvos',
        'icon_set_type': 'IconSetType',
        'is_custom': 'IsCustom',
        'show_value': 'ShowValue'
    }
    
    @staticmethod
    def get_swagger_types():
        return IconSet.swagger_types
    
    @staticmethod
    def get_attribute_map():
        return IconSet.attribute_map
    
    def get_from_container(self, attr):
        if attr in self.container:
            return self.container[attr]
        return None

    def __init__(self, reverse=None, cf_icons=None, cfvos=None, icon_set_type=None, is_custom=None, show_value=None, **kw):
        """
        Associative dict for storing property values
        """
        self.container = {}
		    
        """
        IconSet - a model defined in Swagger
        """

        self.container['reverse'] = None
        self.container['cf_icons'] = None
        self.container['cfvos'] = None
        self.container['icon_set_type'] = None
        self.container['is_custom'] = None
        self.container['show_value'] = None

        if reverse is not None:
          self.reverse = reverse
        if cf_icons is not None:
          self.cf_icons = cf_icons
        if cfvos is not None:
          self.cfvos = cfvos
        if icon_set_type is not None:
          self.icon_set_type = icon_set_type
        if is_custom is not None:
          self.is_custom = is_custom
        if show_value is not None:
          self.show_value = show_value

    @property
    def reverse(self):
        """
        Gets the reverse of this IconSet.
        Get or set the flag indicating whether to reverses the default order of the   icons in this icon set.  Default value is false.             

        :return: The reverse of this IconSet.
        :rtype: bool
        """
        return self.container['reverse']

    @reverse.setter
    def reverse(self, reverse):
        """
        Sets the reverse of this IconSet.
        Get or set the flag indicating whether to reverses the default order of the   icons in this icon set.  Default value is false.             

        :param reverse: The reverse of this IconSet.
        :type: bool
        """

        self.container['reverse'] = reverse

    @property
    def cf_icons(self):
        """
        Gets the cf_icons of this IconSet.
        Get theAspose.Cells.ConditionalFormattingIcon from the collection

        :return: The cf_icons of this IconSet.
        :rtype: list[ConditionalFormattingIcon]
        """
        return self.container['cf_icons']

    @cf_icons.setter
    def cf_icons(self, cf_icons):
        """
        Sets the cf_icons of this IconSet.
        Get theAspose.Cells.ConditionalFormattingIcon from the collection

        :param cf_icons: The cf_icons of this IconSet.
        :type: list[ConditionalFormattingIcon]
        """

        self.container['cf_icons'] = cf_icons

    @property
    def cfvos(self):
        """
        Gets the cfvos of this IconSet.
        Get the CFValueObjects instance.

        :return: The cfvos of this IconSet.
        :rtype: list[ConditionalFormattingValue]
        """
        return self.container['cfvos']

    @cfvos.setter
    def cfvos(self, cfvos):
        """
        Sets the cfvos of this IconSet.
        Get the CFValueObjects instance.

        :param cfvos: The cfvos of this IconSet.
        :type: list[ConditionalFormattingValue]
        """

        self.container['cfvos'] = cfvos

    @property
    def icon_set_type(self):
        """
        Gets the icon_set_type of this IconSet.
        Get or Set the icon set type to display.  Setting the type will auto check    if the current Cfvos's count is accord with the new type. If not accord,    old Cfvos will be cleaned and default Cfvos will be added.             

        :return: The icon_set_type of this IconSet.
        :rtype: str
        """
        return self.container['icon_set_type']

    @icon_set_type.setter
    def icon_set_type(self, icon_set_type):
        """
        Sets the icon_set_type of this IconSet.
        Get or Set the icon set type to display.  Setting the type will auto check    if the current Cfvos's count is accord with the new type. If not accord,    old Cfvos will be cleaned and default Cfvos will be added.             

        :param icon_set_type: The icon_set_type of this IconSet.
        :type: str
        """

        self.container['icon_set_type'] = icon_set_type

    @property
    def is_custom(self):
        """
        Gets the is_custom of this IconSet.
        Indicates whether the icon set is custom.  Default value is false.

        :return: The is_custom of this IconSet.
        :rtype: bool
        """
        return self.container['is_custom']

    @is_custom.setter
    def is_custom(self, is_custom):
        """
        Sets the is_custom of this IconSet.
        Indicates whether the icon set is custom.  Default value is false.

        :param is_custom: The is_custom of this IconSet.
        :type: bool
        """

        self.container['is_custom'] = is_custom

    @property
    def show_value(self):
        """
        Gets the show_value of this IconSet.
        Get or set the flag indicating whether to show the values of the cells on    which this icon set is applied.  Default value is true.             

        :return: The show_value of this IconSet.
        :rtype: bool
        """
        return self.container['show_value']

    @show_value.setter
    def show_value(self, show_value):
        """
        Sets the show_value of this IconSet.
        Get or set the flag indicating whether to show the values of the cells on    which this icon set is applied.  Default value is true.             

        :param show_value: The show_value of this IconSet.
        :type: bool
        """

        self.container['show_value'] = show_value

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.get_swagger_types()):
            value = self.get_from_container(attr)
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

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, IconSet):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
