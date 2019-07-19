# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '18 Jul 2019'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from elasticsearch import Elasticsearch

class ElasticsearchConnection(object):

    @classmethod
    def get_connection(cls):
        if getattr(cls, 'es', None):
            return cls.es

        cls.es = Elasticsearch(["https://jasmin-es1.ceda.ac.uk"])
        return cls.es