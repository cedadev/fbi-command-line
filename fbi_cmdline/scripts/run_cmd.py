# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '17 Jul 2019'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from cmd import Cmd
import fbi_cmdline.commands as commands
import sys
import readline
import types
from fbi_cmdline.elasticsearch import ElasticsearchConnection


def getobj(loadstring):

    mod,_, cls = loadstring.rpartition('.')
    module = __import__(mod, fromlist=[cls])

    return getattr(module, cls)


class FbiCmdline(Cmd, object):
    """
    Command Processor for fbi command line tool
    """
    prompt = 'FBI cmd> '

    es = ElasticsearchConnection.get_connection()

    def emptyline(self):
        return None

    def do_quit(self, line):
        return True

    def help_quit(self):
        print('Quit')

    do_q = do_quit
    help_q = help_quit


def main():

    # Attach all registered commands
    for command in commands.REGISTRY:
        command_class = getobj(command)

        # Attach the do method
        setattr(
            FbiCmdline,
            'do_{}'.format(command_class.command_name),
            types.MethodType(command_class.run_command, FbiCmdline)
        )

        # Attach the help method
        setattr(
            FbiCmdline,
            'help_{}'.format(command_class.command_name),
            types.MethodType(command_class.help, FbiCmdline)
        )

    cmd = FbiCmdline()

    if len(sys.argv) > 1:
        cmd.onecmd(' '.join(sys.argv[1:]))
        sys.exit()
    else:
        cmd.cmdloop()


if __name__ == '__main__':
    main()
