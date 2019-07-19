# encoding: utf-8
"""
Provides a count of the directories and files in a given dataset
"""
__author__ = 'Richard Smith'
__date__ = '17 Jul 2019'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from .registery import CommandRegistry
import hashlib


@CommandRegistry.register
class DatasetCount(object):
    command_name = 'datasetcount'

    @classmethod
    def dir_query(cls, path):

        depth = len(path.split('/'))

        return {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match_phrase_prefix": {
                                "archive_path": path
                            }
                        }
                    ],
                    "filter": {
                        "range": {
                            "depth": {
                                "gte": depth
                            }
                        }
                    }
                }
            }
        }

    @classmethod
    def fbi_query(cls, path):

        return {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match_phrase_prefix": {
                                "info.directory.analyzed": path
                            }
                        }
                    ],
                    "filter": {
                        "term": {
                            "info.is_link": "false"
                        }
                    }
                }
            }
        }

    @classmethod
    def help(cls, cmdcls):
        """
        This will be run when help <command_name> is called.
        This method should print help information.
        :param cmdcls: The command line class running the command (likely un-used)
        """
        print ('''
            Count the directories and files in the index under a particular path

            Usage:
            ------

            datasetcount <path>
            ''')

    @classmethod
    def run_command(cls, cmdcls, line):
        """
        This will be run when the command is called.
        :param cmdcls: The command line class running the command
        :param line: String of the arguments supplied to the command
        """

        es = cmdcls.es

        dir_hash = hashlib.sha1(line).hexdigest()

        try:
            dir = es.get(index='ceda-dirs', id=dir_hash)
        except elasticsearch.exceptions.NotFoundError:
            print('Directory does not exist in index: {}'.format(line))
            return

        path = dir['_source']['archive_path']

        dir_count = es.count(index='ceda-dirs', body=cls.dir_query(path))['count']
        file_count = es.count(index='ceda-fbi', body=cls.fbi_query(path))['count']

        print(
            'Directories: {} Files: {}'.format(
                dir_count,
                file_count
            )
        )
