# -*- coding: utf-8 -*-
import collections
from watson.common import strings


class TagMixin(object):

    """Simple tag mixin used for all html tags.

    All keyword arguments that get passed to __init__ will be converted into
    attributes for the element.

    Attributes:
        attributes (dict): a dictionary of attributes associated with the tag.
    """
    attributes = None

    def __init__(self, **kwargs):
        self.attributes = collections.ChainMap(kwargs)

    def __str__(self):
        return self.render()

    def render(self):
        raise NotImplementedError('The render method has not been implemented')


def _value_check(value, keep_empty=False):
    return True if keep_empty else True if value else False


def flatten_attributes(attrs, keep_empty=False):
    """Flattens attributes into a single string of key=value pairs.

    Attributes are sorted alphabetically.
    """
    # value_check = lambda val: True if keep_empty else True if val else False
    return ' '.join(['{0}="{1}"'.format(
                    strings.hyphenate(name), value or '') for name, value
        in sorted(attrs.items()) if _value_check(value, keep_empty)])
