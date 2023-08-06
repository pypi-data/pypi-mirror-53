tpDccLib
============================================================

.. image:: https://img.shields.io/github/license/tpoveda/tpDccLib.svg
    :target: https://github.com/tpoveda/tpPyUtils/blob/master/LICENSE

.. image:: https://travis-ci.com/tpoveda/tpDccLib.svg?branch=master
    :target: https://travis-ci.com/tpoveda/tpDccLib

Collection of Python modules to write DCC tools in a DCC agnostic way.

When working with specific DCCs, tpDccLib will auto import proper modules and will use
DCC specific implementations.

Installation
-------------------
Manual
~~~~~~~~~~~~~~~~~~~~~~
1. Clone/Download tpDccLib anywhere in your PC (If you download the repo, you will need to extract
the contents of the .zip file).
2. Copy **tpDccLib** folder located inside **source** folder in a path added to **sys.path**

Automatic
~~~~~~~~~~~~~~~~~~~~~~
Automatic installation for tpDccLib is not finished yet.

DCC Implementations
-------------------
At this moment following DCCs are supported:

* **3ds Max**: https://github.com/tpoveda/tpMaxLib
* **Maya**: https://github.com/tpoveda/tpMayaLib
* **Houdini**: https://github.com/tpoveda/tpHoudiniLib
* **Nuke**: https://github.com/tpoveda/tpNukeLib
* **Blender**: *Work in Progress*

During tpDccLib initialization, if DCC specific implementation package is found in sys.path, tpDccLib
will automatically detect it and will import it.

Usage
-------------------
Initialization Code
~~~~~~~~~~~~~~~~~~~~~~
tpDccLib must be initialized before being used.

.. code-block:: python

    import tpDccLib
    tpDccLib.init()


Reloading
~~~~~~~~~~~~~~~~~~~~~~
For development purposes, you can enable reloading system, so 
you can reload tpDccLib sources without the necessity of restarting
your Python session. Useful when working with DCCs.

.. code-block:: python

    import tpDccLib
    reload(tpDccLib)
    tpDccLib.init(True)


Enabling debug log
~~~~~~~~~~~~~~~~~~~~~~
By default, tpDccLib logger only logs warning messages. To enable all log messages
you can set TPDCCLIB_DEV environment variables to 'True'

.. code-block:: python

    import os

    os.environ['TPDCCLIB_DEV'] = 'True'
    import tpDccLib
    tpDccLib.init()


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
