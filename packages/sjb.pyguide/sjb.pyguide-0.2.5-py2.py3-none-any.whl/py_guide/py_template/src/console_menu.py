# PEP8: Group imports
# 1) Standard library imports.
import logging
import os
import getpass
# import virtualenv
import venv
import pip
from pip._internal import main
import subprocess
import sys
# 2) Related third party imports.
from menu import menu
# 3) Local application/library specific imports.


class ConsoleMenu:
    def __init__(self, cmdline_argument_parser, logger=None):
        self.log = logger
        self.cmdline_parser = cmdline_argument_parser

        self.menu_main = menu.Menu()
        title = "******************************************\n" \
                "\t{{project_name}} Console\n" \
                "*******************************************"
        self.menu_main.title = title
        self.menu_main.set_options([
                                    ("{{project_name}} help", self.show_help),
                                    ("Exit", self.close_menu)
                                   ])

    def show_menu(self):
        self.menu_main.open()

    def close_menu(self):
        self.menu_main.close()

    def show_help(self):
        self.cmdline_parser.print_help()
        self.pause()

    @staticmethod
    def pause():
        print('\n')
        input("Press enter key to continue...")

    def make_directory(self, directory_name):
        if not os.path.exists(directory_name):
            try:
                os.mkdir(directory_name)
                self.log.info("Created directory {0}".format(directory_name))
            except OSError as e:
                self.log.error("Failed to create log directory {0} due to {1}.".format(directory_name, e.strerror))
                raise e

    @property
    def log(self):
        return self._log

    @log.setter
    def log(self, value):
        if value is not None:
            self._log = value
        else:
            self._log = logging.getLogger(__name__)
            self._log.warning("No logger provided. Initialised logger {0}".format(__name__))
