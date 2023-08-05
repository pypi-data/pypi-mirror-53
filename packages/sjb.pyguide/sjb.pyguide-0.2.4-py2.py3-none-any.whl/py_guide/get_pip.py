# PEP8: Group imports
# 1) Standard library imports.
import os
# 2) Related third party imports.
import requests
# 3) Local application/library specific imports.


class GetPip(object):
    def __init__(self, venv_path):
        self.url = "https://bootstrap.pypa.io/get-pip.py"
        self.venv_path = venv_path

    def get_pip(self):
        stream = requests.get(self.url)

        try:
            pip_file = open(os.path.join(self.venv_path, "get_pip.py"), "w")
            pip_file.write(stream.text)
        finally:
            pip_file.close()

    @property
    def venv_path(self):
        return self._venv_path

    @venv_path.setter
    def venv_path(self, value):
        self._venv_path = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value
