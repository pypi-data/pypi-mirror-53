# PEP8: Group imports
# 1) Standard library imports.
import os
import sys
import argparse
import pkg_resources
from pkg_resources import DistributionNotFound
# 2) Related third party imports.
from backports import configparser2
# 3) Local application/library specific imports.
from {{ project_name }}.console_menu import ConsoleMenu
from {{ project_name }} import logging_trees


global log
log = logging_trees.LoggerOfTrees()


def main(args=None):
    """As a best practice, main() will be the entry point for this package.  We will define a pattern of how we
        take information passed to main (arguments) and send them to methods to handle them (route).  First we will
        define an argument parser.  We put it in it's own method to keep the main method clean.  Next we'll use
        a route_arguments() method, which in turn will handle further routing delegation via other methods, as a way
        to handle command line parameters.

        If you want to add an argument

        * Define the argument in the parser_build() method
        * Create a route_action_[description] method following the existing pattern
        * Call that method within route_arguments() for the correct condition


        Note:
            Using the main() will help creating deployment packages using setup.py, wheel, and wanting
            creation of any entry point in the scripts directory of the virtual environment

        When an argument is parsed it should be routed to a handler action method.
    """

    parser = parser_build()
    route_arguments(parser)

    return 0


def parser_build():
    """This method builds the argument parser to handle values passed in from the command line.  Centralized in this
    method for readability.

    The Argument parser allows standard patterns for parsing.  For instance you do not have to program -h, or --help
    to explain how the command line is used.  The argument parser will build this from the arguments, and descriptions
    provided for those arguments, when building the parser object.
    """

    module_description = "{{ project_name }} is a best practices based Python package that does cool stuff"
    # Create an instance of a parser specific to this module
    parser = argparse.ArgumentParser(description=module_description)

    # Now tell the parser what arguments we expect
    argument_name = '--show_menu'
    multiple_argument_actions = "?"
    argument_action = "store_true"  # If you pass this argument, by default it is true
    argument_type = bool
    argument_help = "When this parameter is provided the flag is set to true.  When true a console menu " \
                    "will be shown."
    # The type on this argument is implied by the action being store_true.  Adding it will cause an error
    #   https://stackoverflow.com/a/33574535
    parser.add_argument(argument_name,
                        action=argument_action,
                        help=argument_help)

    argument_name = '--version'
    argument_action = "store_true"  # If you pass this argument, by default it is true
    argument_type = bool
    argument_help = "When this parameter is provided the version information will be displayed. "
    parser.add_argument(argument_name,
                        action=argument_action,
                        help=argument_help)

    return parser


def route_arguments(cmdline_parser):
    """This method will use the arguments parsed from the command line to route different pieces of functionality
    in the module"""

    # Grab arguments off command line, sys.argv[1:], and parse them
    args = cmdline_parser.parse_args()

    if args.version:
        route_action_version()

    if args.show_menu:
        route_action_show_menu(cmdline_parser=cmdline_parser)

    if not args.show_menu and not args.version:
        # If nothing was passed in, print the help usage
        cmdline_parser.print_help()


def route_action_show_menu(cmdline_parser):
    """If ``--show_menu`` is passed as part of calling this module, this method will be triggered by routing, and
    a console menu will be shown."""
    menu = ConsoleMenu(cmdline_argument_parser=cmdline_parser, logger=log)
    menu.show_menu()


def route_action_version():
    """Will display the version of the current package."""
    # if you see a cfg file, then we are in development mode
    ini_file_name = os.path.join(os.getcwd(), "..", "project.cfg")
    if os.path.exists(ini_file_name):
        ini_file = configparser2.ConfigParser()
        ini_file.read(ini_file_name)

        __version__ = "{0}.dev, build {1}. Non production DEVELOPMENT code." \
            .format(ini_file["distribution"]["version"], ini_file["distribution"]["build_number"])
    else:
        try:
            __version__ = pkg_resources.get_distribution('{{ project_name }}').version
        except DistributionNotFound as e:
            __version__ = "unknown"

    print("Version {0}".format(__version__))


if __name__ == "__main__":
    """The __name__ == \"__main__\" construct ensures this package is only executed when the {{ project_name }} 
    module is specifically called.  One example of when this is important is using Sphinx, when the module 
    is imported or scanned by the Sphinx engine.
    
    https://docs.python.org/3/library/__main__.html"""

    # Using ``sys.exit(status)``  to exit Python cleanly. https://docs.python.org/2/library/sys.html#sys.exit
    sys.exit(main())
