# -*- coding: utf-8 -*-
"""This file will create an instance of a new project with default settings"""
# PEP8: Group imports
# 1) Standard library imports.
import os
import shutil
from datetime import datetime
import errno
# 2) Related third party imports.
from backports import configparser2
from jinja2 import Environment, PackageLoader, select_autoescape
# 3) Local application/library specific imports.
from py_guide import logging_trees as logging


class PyProject(object):
    def __init__(self, logger=None, project_name="python_project"):
        self._project_name = project_name
        self.log = logger
        self.author = ""
        self.name = u'Python Guide for Practicing Wizards'
        self.description = u'A Python Project'

    def create(self):
        """Create a template project on disk from the information in the object    """
        self.create_project_directories(self.project_name)
        self.create_core_files()

    def create_core_files(self):
        """Creates standard files for all projects following this Python guide.  As a pattern this method will call
        another method to create the file.  In that method it will handle the data needed for that file, as well as
        calling another method to write the file.

        Note:
            The environment parameter for each sub-method will give it the context of loading templates with
            py_template sub-package as the root.  In contrast, when you write a file, it will be written relative
            to the project root.
        """
        env = Environment(
            loader=PackageLoader('py_guide', 'py_template'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        # The following methods will handle determining template and providing data to it while creating files

        # Files in the root of the project (not the source code directory)
        self.create_license(environment=env)
        self.create_requirements(environment=env)
        self.create_gitignore(environment=env)
        self.create_docs_source(environment=env)
        self.create_dist_pypi(environment=env)
        self.create_jrepl(environment=env)
        self.create_project_config(environment=env)
        self.create_setup(environment=env)
        self.create_readme(environment=env)

        # Files in the source folder; named the same as the project per PEP
        self.create_init(environment=env, directory=self.project_name)
        self.create_main(environment=env)
        self.create_console_menu(environment=env)
        self.create_logging(environment=env)

        # PyCharm files
        self.create_run_configurations(environment=env)

    def create_console_menu(self, environment=None):
        console_t = environment.get_template('src/console_menu.py')
        console_d = {u'project_name': self.project_name}
        destination = os.path.join(self.project_name, "console_menu.py")
        self.write_file(destination, console_t, console_d)

    def create_dist_pypi(self, environment=None):
        """Creates the distribute to PyPi bat files for Windows machines.

        Args:
            environment(Jinja2.environment): Context for the template engine Jinja2
        """
        dist_t = environment.get_template('dist_pypi.bat')
        dist_config_t = environment.get_template('dist_pypi_config.default')
        self.write_file('dist_pypi.bat', dist_t)
        self.write_file('dist_pypi.config.bat', dist_config_t)

    def create_docs_source(self, environment=None):
        """Creates the Sphinx configuration file in the docs_source directory

        Args:
            environment(Jinja2.environment): Context for the template engine Jinja2
        """
        # Data for the Sphinx Conf template
        conf_d = {u'project_name': self.project_name}
        conf_t = environment.get_template('docs_source/conf.py')
        self.write_file(os.path.join('docs_source', 'conf.py'), conf_t, conf_d)
        # Index file for documentation
        conf_t = environment.get_template('docs_source/index.rst')
        self.write_file(os.path.join('docs_source', 'index.rst'), conf_t, conf_d)
        # Readme file in documentation which draws in the readme.rst from the project root
        conf_t = environment.get_template('docs_source/readme.rst')
        self.write_file(os.path.join('docs_source', 'readme.rst'), conf_t)
        # Next step file
        next_t = environment.get_template('docs_source/next_steps.rst')
        self.write_file(os.path.join('docs_source', 'next_steps.rst'), next_t)

    def create_gitignore(self, environment=None):
        """Creates the GIT Ignore file.  This list excludes things in the project that should not be checked into
        source control.

        Args:
            environment(Jinja2.environment): Context for the template engine Jinja2
        """
        git_t = environment.get_template('.gitignore')
        self.write_file(".gitignore", git_t)

    def create_init(self, environment=None, directory=None):
        """Creates a Python __init__ file.   As this file can be used multiple times within packages and sub-packages,
        we will allow for a directory parameter on where it should be written.

        Args:
            environment(Jinja2.environment): Context for the template engine Jinja2
            directory(str): A string that can be treated like a PathLike object
        """
        init_t = environment.get_template('src/__init__.py')
        if directory is None:
            # Write to the default directory
            self.write_file("__init__.py", init_t)
        else:
            self.write_file("{0}".format(os.path.join(directory, "__init__.py")), init_t)

    def create_jrepl(self, environment=None):
        """jrepl.bat or jreplace is a batch script that will update another file.  On a windows box it can be used
        to update the project.cfg file with builds.
         """
        jrepl_t = environment.get_template('jrepl.bat')
        self.write_file('jrepl.bat', jrepl_t)

    def create_license(self, environment=None):
        """Creates the LICENSE file for the project.

        Args:
            environment(Jinja2.environment): Context for the template engine Jinja2
        """
        # Data for the license template as a Python dictionary
        license_d = {u'year': u'{0}'.format(str(datetime.now().year)),
                     u'copyright_holder': u'{0}'.format(self.author)}

        license_t = environment.get_template('LICENSE-MIT')

        self.write_file("LICENSE", license_t, license_d)

    def create_logging(self, environment=None):
        log_t = environment.get_template('src/logging_trees.py')
        self.write_file(os.path.join(self.project_name, "logging_trees.py"), log_t)

    def create_main(self, environment=None):
        """Method creates the __main__ file for the project.  As part of our best practices standard the __main__ is
        important for creating a standard handling of arguments with argparse, a standard way to route those arguments
        to methods to implement them, and a standard way to create entry points.  Entry points enable an installed
        application to have a Scripts/ directory start command.  For instance, when this project is installed, there
        is a venv/scripts/py_guide command that can be executed."""
        main_d = {u'project_name': self.project_name}
        main_t = environment.get_template('src/__main__.py')
        destination = os.path.join(self.project_name, "__main__.py")
        self.write_file(destination, main_t, main_d)

    def create_project_config(self, environment=None):
        """Creates the LICENSE file for the project.

        Args:
            environment(Jinja2.environment): Context for the template engine Jinja2
        """
        name = u'Python Guide for Practicing Wizards'
        project_d = {u'name': name,
                     u'name-nospace': name.strip(),
                     u'author': self.author,
                     u'description': u'Python project generator for best practices',
                     u'license': u'MIT'}
        project_t = environment.get_template('project.cfg', project_d)
        self.write_file('project.cfg', project_t, project_d)

    def create_project_directories(self, project_name):
        if project_name is None:
            project_name = self.project_name

        directory = os.path.join(self.find_project_base_directory(), project_name)
        self.make_directory(directory)
        project_name_root = directory
        # .idea project folder for PyCharm IDE
        directory = os.path.join(project_name_root, ".idea")
        self.make_directory(directory)
        directory = os.path.join(project_name_root, ".idea", "runConfigurations")
        self.make_directory(directory)
        # build directory will be created for Sphinx
        directory = os.path.join(project_name_root, "build")
        self.make_directory(directory)
        # dist [distribution] folder created by setuptools
        directory = os.path.join(project_name_root, "dist")
        self.make_directory(directory)
        # documentation html directory; the has been generated end result
        directory = os.path.join(project_name_root, "docs")
        self.make_directory(directory)
        # documentation source directory, for the projects documentation
        directory = os.path.join(project_name_root, "docs_source")
        self.make_directory(directory)
        # documentation source directory, _static is required by Sphinx
        directory = os.path.join(project_name_root, "docs_source", "_static")
        self.make_directory(directory)
        # documentation source directory, for the code documentation
        directory = os.path.join(project_name_root, "docs_source", "code")
        self.make_directory(directory)
        # source code directory [should reference use same name PEP here]
        directory = os.path.join(project_name_root, project_name)
        self.make_directory(directory)
        # virtual environment
        directory = os.path.join(project_name_root, "venv")
        self.make_directory(directory)

    def create_readme(self, environment=None):
        """This method will create a README.rst file.  We use rst so that it will be displayed in Rich Text when
        using systems like github.

        Note:
            I have recently discovered that if you use BitBucket Server (installed, not cloud) they will not render
            rst files.   May need to consider changing the README.rst to README.md in that circumstance.
        """
        readme_d = {u'project_name': self.project_name}
        readme_t = environment.get_template('README.rst')
        self.write_file('README.rst', readme_t, readme_d)

    def create_requirements(self, environment=None):
        """Creates the requirements.txt file.  This file is used by Python to update a projects virtual environment
        with the packages needed to run the project.  Initialized with core packages that are needed for all projects
        like pip, setuptools and wheel, and packages needed to follow good practices like documentation,  such as
        sphinx.

        Args:
            environment(jinja2.Environment): Context for the template engine Jinja2.
                https://jinja.palletsprojects.com/en/2.10.x/api/#jinja2.Environment
        """
        requirements_t = environment.get_template('requirements.txt')
        self.write_file(file_name="requirements.txt", template=requirements_t)

    def create_run_configurations(self, environment=None):
        """This method creates files that allow for building of the project.  Originally conceived to create the
        PyCharm .idea/runConfigurations xml files. I'm a big fan of PyCharm and recommend that if you are writing
        Python get the community edition.  When you're good enough to know why it's worth it, by a pro license.

        TODO:
            Extend this project to have a run.py or build.py or some structure like that which will allow build
            without PyCharm

        """
        # Jinja expects paths to template files to be / even on Windows
        template_file = '.idea/runConfigurations/Build_setup_wheel.xml'
        run_t = environment.get_template(template_file)
        run_d = {u'project_name': self.project_name}
        self.write_file(os.path.join(r'.idea', 'runConfigurations', 'Build_setup_wheel.xml'), run_t, run_d)

        template_file = '.idea/runConfigurations/Build_Sphinx_docs.xml'
        run_t = environment.get_template(template_file)
        self.write_file(os.path.join(r'.idea', 'runConfigurations', 'Build_Sphinx_docs.xml'), run_t, run_d)

    def create_setup(self, environment=None):
        """Creates the setup.py file for the project used with building the wheel file, deployed via pip"""
        setup_d = {u'name_nospace': self.name.strip(' '),
                   u'license': u'MIT',
                   u'project_name': self.project_name}

        setup_t = environment.get_template('setup.py')
        self.write_file('setup.py', setup_t, setup_d)

    def find_project_base_directory(self):
        """Determines a directory for creating the new project.  First check to see if there is a PycharmProjects
        directory in use.  If so use it.  If not then just use the user directory."""
        # Do they use PyCharm?
        project_dir = r"{0}\{1}".format(os.path.expanduser("~"), "PycharmProjects")
        if os.path.exists(project_dir):
            self.project_directory = project_dir
        else:
            project_dir = r"{0}".format(os.path.expanduser("~"))
            self.project_directory = project_dir

        # We could also find a path relative to this file
        # directory_file = os.path.dirname(__file__)
        # Relative to this file could be the py_guide root
        # py_guide_root = os.path.join(directory_file, "..")

        return self.project_directory

    def make_directory(self, directory_path=None):
        """Creates a directory for the project.  Handles errors and logging"""
        try:
            os.mkdir(directory_path)
            self.log.info("Created directory {0}".format(directory_path))
        except FileExistsError as e:
            self.log.info("Directory {0} already exists.".format(directory_path))
            raise e
        except OSError as e:
            self.log.error(r"Failed to created directory {0}.\n\rError indicates {1}".format(directory_path,
                                                                                             e.strerror))
            raise e

    def remove_directory(self):
        """Primarily created for when make_directory experiences a FileExistsError, this method will delete an
        existing project folder.  It takes the name we pass (or wnated to create) and finds it in the project directory
        path.  This allows the calling user interface to not have to understand the full path to the directory."""
        directory = os.path.join(self.find_project_base_directory(), self.project_name)
        try:
            shutil.rmtree(directory)
            self.log.info("Removed directory {0}".format(directory))
        except OSError as e:
            if e.errno == 145:
                self.log.error("[WinError 145] The directory is not empty.  Could it be open in another "
                               "application? Error Message: {0}".format(e.strerror))

    def write_file(self, file_name=None, template=None, template_data={}):
        """Wrapper method for successive file creation.  Assumes all files want to be written
        relative to the project root.

        Args:
            file_name(str): Name of the file to write
            template(jinja2.Template): The jinja2 template to be written
            template_data(dictionary): Key/Value pairs of data for the jinja2 template
        """
        absolute_file_name = os.path.join(self.project_absolute_path, file_name)
        try:
            with open(absolute_file_name, 'w') as file:
                file.write(template.render(template_data))
                self.log.info("Created file {0}".format(absolute_file_name))
        except EnvironmentError as e:
            self.log.error(e.strerror)

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value

    @property
    def project_name(self):
        return self._project_name

    @project_name.setter
    def project_name(self, value):
        self._project_name = value

    @property
    def project_directory(self):
        return self._project_directory

    @project_directory.setter
    def project_directory(self, value):
        self._project_directory = value

    @property
    def project_absolute_path(self):
        """The abspath() of this file.  The absolute path will be the full file on path on disk for the operating
        system you are on."""
        return os.path.abspath(os.path.join(self.project_directory, self.project_name))

    @property
    def log(self):
        return self._log

    @log.setter
    def log(self, value):
        if value is None:
            self._log = logging.LoggerOfTrees()
        else:
            self._log = value

    @property
    def name(self):
        """This is the name of the project and the root of the directory structure."""
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value
