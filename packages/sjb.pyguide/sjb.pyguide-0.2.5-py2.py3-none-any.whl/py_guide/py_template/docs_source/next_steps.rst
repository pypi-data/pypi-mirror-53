===================================================
Next Steps
===================================================

The goal of this project is to help a Python package start with all the
pieces that are normally left for later. This will ensure you build software
that can be installed, documented,and maintained over time.

##########################
PyCharm and Build
##########################

Open this new project up in Pycharm.
Look at the Run Configurations (drop down with "play button" [#f1]_)

Build Setup Wheel
=======================

Locate the Run configuration by this name and run it.  You will get a /dist folder created in your file
structure and a wheel file (whl extension) is built.  This can then be uploaded to test PyPi.

Build Sphinx Docs
=======================

Locate the Run configuration by this name and run it. You will get html files built in the /docs folder.
Visit that folder and open index.html in a browser and check it out.

############################
Install your project
############################

You already have a project that you can install.  That's the whole point
of this thing.

Assumptions

* You understand we are showing windows here; everyone else does linux
* There's a Python installation such as C:\Python37
* We want to install this application to C:\apps\{{project_name}}

.. rubric:: Footnotes
.. [#f1] Like on a VCR
