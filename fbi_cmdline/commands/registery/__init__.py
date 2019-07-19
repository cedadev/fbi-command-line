# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '18 Jul 2019'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

class CommandRegistry(object):
    registry = []

    @classmethod
    def register(cls, obj):
        cls.registry.append('.'.join([obj.__module__, obj.__name__]))
        return obj

    def __iter__(self):
        for x in self.registry:
            yield x

