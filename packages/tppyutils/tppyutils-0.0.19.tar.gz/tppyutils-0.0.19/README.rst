tpPyUtils
============================================================

.. image:: https://img.shields.io/github/license/tpoveda/tpPyUtils.svg
    :target: https://github.com/tpoveda/tpPyUtils/blob/master/LICENSE

.. image:: https://travis-ci.com/tpoveda/tpPyUtils.svg?branch=master
    :target: https://travis-ci.com/tpoveda/tpPyUtils

Collection of Python modules to make your life easier when working with Python, specially for DCC tool development.

Installation
-------------------
Manual
~~~~~~~~~~~~~~~~~~~~~~
1. Clone/Download tpPyUtils anywhere in your PC (If you download the repo, you will need to extract the contents of the .zip file).
2. Copy **tpPyUtils** folder located inside **source** folder in a path added to **sys.path**

Automatic
~~~~~~~~~~~~~~~~~~~~~~
Automatic installation for tpPyUtils is not finished yet.

Usage
-------------------

Initialization Code
~~~~~~~~~~~~~~~~~~~~~~
tpPyUtils must be initialized before being used.

.. code-block:: python

    import tpPyUtils
    tpPyUtils.init()

Reloading
~~~~~~~~~~~~~~~~~~~~~~
For development purposes, you can enable reloading system, so  you can reload tpPyUtils sources without the necessity of restarting your Python session. Useful when working with DCCs

.. code-block:: python

    import tpPyUtils
    reload(tpPyUtils)
    tpPyUtils.init(True)


Enabling debug log
~~~~~~~~~~~~~~~~~~~~~~
By default, tpPyUtils logger only logs warning messages. To enable all log messages you can set TPPYUTILS_DEV environment variables to 'True'

.. code-block:: python

    import os
    os.environ['TPPYUTILS_DEV'] = 'True'
    import tpPyUtils
    tpPyUtils.init()


Deploying new version (only for devs)
-----------------------------------------

Update version
~~~~~~~~~~~~~~~~~~~~~~

Make sure **setup.cfg** file version field is updated

Installing libraries
~~~~~~~~~~~~~~~~~~~~~~
Make sure that you have installed the following packages:

* **wheel**

.. code-block:: console

    pip install wheel

* **twine**

.. code-block:: console

    pip install twine

* **setuptools**

.. code-block:: console

    pip install setuptools

Make sure to update setuptools to latest available version:

.. code-block:: console

    pip install setuptools --upgrade


Generate wheel
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    python setup.py sdist bdist_wheel

Validate wheel package generation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    twine check dist/*

Upload package to PyPi
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    twine upload dist/*
