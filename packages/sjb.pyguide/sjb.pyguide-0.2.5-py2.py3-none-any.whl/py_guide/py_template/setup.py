# Original guidance from http://go.chriswarrick.com/entry_points
# Also thanks to http://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/creation.html
# https://setuptools.readthedocs.io/en/latest/setuptools.html

# PEP8: Group imports
# 1) Standard library imports.
from datetime import datetime
from packaging import version
# 2) Related third party imports.
from backports import configparser2
from setuptools import setup, find_packages
# 3) Local application/library specific imports.


def find_and_list_packages():
    """This wrapper adds the display of packages found by setuptools.find_packages() during the build process.  This
    is useful when troubleshooting issues, such as when creating package_data entries for setup.py
    """
    packages = find_packages()

    print("Packages found during build:\r\n\t{0}".format(packages))

    return packages


def version_builder(write_new_version=True, ini_file=None):
    """This method determines the next version number.  The assumption is the version numbering scheme is semantic
    and stored in the project.cfg file.   This method will read the latest version, update it here in setup, and then
    update build information in the cfg file.

    Args:
        write_new_version: (bool) - If true will update the project.cfg file with the new version number
        ini_file: (configparser2.ConfigParser) - the configuration file we want to update build meta data in.
    """
    now = datetime.now()

    # read the Semantic Version.  To update it, go changein the file
    semantic_version = ini_file["distribution"]["version"]
    # Build an ISO timestamp of when the build was done
    military_time = int(str(now.hour) + "{:02d}".format(now.minute))
    build_timestamp = "{0}.{1}.{2}.{3}".format(str(now.year), str(now.month), str(now.day), str(military_time))
    build_number = int(ini_file["distribution"]["build_number"])
    build_number += 1

    # Update the some version information in the cfg file
    if write_new_version:
        # Timestamp and build number will increment each time, independent of version updating
        ini_file["distribution"]["build_number"] = str(build_number)
        ini_file["distribution"]["build_timestamp"] = build_timestamp

        # Write the file to disk using all the values of the object in memory
        with open('project.cfg', 'w') as ini_disk_file:
            ini_file.write(ini_disk_file)

    return semantic_version


if __name__ == "__main__":
    """As we have customized this file for version numbering, listing packages, etc., wrap the definition of 
    setup in the if name = main check.  Necessary for importing into Sphinx for documentation"""
    ini_file_name = "project.cfg"
    ini_file = configparser2.ConfigParser()
    ini_file.read(ini_file_name)

    setup(author=ini_file["project"]["author"],
          author_email='you@your-domain.com',
          classifiers=[
              # Trove classifiers
              # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
              'Development Status :: 4 - Beta',
              'Intended Audience :: Developers',
              'License :: OSI Approved :: MIT License',
              'Natural Language :: English',
              'Operating System :: OS Independent',
              'Programming Language :: Python',
              'Programming Language :: Python :: 2.7',
              'Programming Language :: Python :: 3',
              'Programming Language :: Python :: 3.3',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3.6',
              # https://www.geeksforgeeks.org/difference-various-implementations-python/
              'Programming Language :: Python :: Implementation :: CPython',
              # Need to test to see if this will run on PyPy.  That'd be cool.
              # 'Programming Language :: Python :: Implementation :: PyPy',
              'Topic :: Software Development'
          ],
          description='Python Project & Coding Standards for Practicing Wizards',
          entry_points={
            'console_scripts': ['{{ project_name }} = {{ project_name }}.__main__:main']
          },
          install_requires=[
              'configparser2==4.0.0',
              'Menu==3.1.0'
          ],
          license='{{ license }}',
          # newline separates Description: header in PKG-INFO from readme content
          long_description='\n' + open('README.rst').read(),
          long_description_content_type='text/x-rst',
          # setuptools will change an underscore (_) to a dash (-), in name, so doing it here explicitly
          # PEP 8: Python packages should also have short, all-lowercase names, although the use of
          #        underscores is discouraged.
          name='{{project_name}}',
          packages=find_and_list_packages(),
          project_urls={
            "Bug Tracker": "https://github.com/username/{{ project_name }}/issues/",
            "Documentation": "https://username.github.io/{{ project_name }}/",
            "Source Code": "https://github.com/username/{{ project_name }}/",
          },
          url="https://github.com/username/{{ project_name }}",
          version=version_builder(write_new_version=True, ini_file=ini_file),
          )
