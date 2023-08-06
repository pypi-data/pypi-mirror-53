# PEP8: Group imports
# 1) Standard library imports.
import logging
import os
import getpass
# import virtualenv
import venv
import subprocess
import sys
# 2) Related third party imports.
from menu import menu
# 3) Local application/library specific imports.
from py_guide import project_factory
from py_guide import get_pip


class ConsoleMenu:
    def __init__(self, cmdline_argument_parser, logger=None):
        self.log = logger
        self.cmdline_parser = cmdline_argument_parser

        self.menu_main = menu.Menu()
        title = "******************************************\n" \
                "\tPython Guide for Practicing Wizards\n" \
                "*******************************************"
        self.menu_main.title = title
        self.menu_main.set_options([
                                    ("Generate new project", self.new_project_generator),
                                    ("py_guide help", self.show_help),
                                    ("Exit", self.close_menu)
                                   ])

    def new_project_generator(self):
        """Collects some information, then generates a project using the best practices of this guide."""
        py = project_factory.PyProject(project_name="", logger=self.log)
        username = getpass.getuser()
        # Set the py author.  Showing as a default [name] if enter is hit with nothing else, you get the default value
        py.author = username
        py.author = menu.input("What name do you want to use for author, copyright holder? [{0}]".format(username))

        # new_name will be used if the current project_name exists
        new_name = None
        while new_name is None:
            py.project_name = menu.input("What is the name of your project?")

            try:
                new_name = py.project_name
                py.create()
            except FileExistsError as e:
                action = menu.input("Directory {0} already exists. (D)elete or (R)ename?".format(py.project_absolute_path))

                if action.upper() == "D":
                    try:
                        py.remove_directory()
                    except FileNotFoundError as e:
                        # the file was already removed.  Move on
                        pass

                    py.project_name = new_name
                else:
                    new_name = menu.input("What is the new name of your project?")
                    py.project_name = new_name

                py.create()

            self.log.info("Your project was created at {0}".format(py.find_project_base_directory()))

        venv_path = os.path.join(py.project_absolute_path, "venv")
        self.create_virtual_environment(venv_path=venv_path)

    def create_virtual_environment(self, venv_path):
        # Store the current environment so we an re-activate it
        sys_prefix = sys.prefix
        # Deactivate the current virtual environment
        self.log.info("Deactivating Python Virtual Environment ({0})".format(sys_prefix))
        os.system(os.path.join(sys.prefix, "Scripts", "deactivate"))

        sys.prefix = venv_path
        self.log.info("Creating Virtual environment...")
        venv.create(venv_path)
        self.log.info("Activating Python Virtual Environment ({0})".format(venv_path))
        os.system(os.path.join(venv_path, "Scripts", "activate"))
        self.log.info("Downloading pip installation file...")
        pip_stream = get_pip.GetPip(venv_path)
        pip_stream.get_pip()
        self.log.info("Installing pip ...")
        subprocess.call([os.path.join(venv_path, "scripts", "python"), os.path.join(venv_path, "get_pip.py")])
        pip_file = os.path.join(venv_path, "scripts", "pip")
        self.log.info("Installing requirements using pip...")
        requirements_file = os.path.join(venv_path, "..", "requirements.txt")
        subprocess.call([pip_file, "install", "-r", requirements_file])
        # Deactivate the virtual environment
        self.log.info("Deactivating Python Virtual Environment ({0})".format(venv_path))
        os.system(os.path.join(venv_path, "Scripts", "deactivate"))
        # Reactivate the current virtual environment
        self.log.info("Activating Python Virtual Environment ({0})".format(sys_prefix))
        os.system(os.path.join(sys_prefix, "Scripts", "activate"))
        # Restore previous values after creating new virtual environment and activating it
        sys.prefix = sys_prefix

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
