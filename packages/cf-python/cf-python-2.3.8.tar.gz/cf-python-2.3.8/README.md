As of 1st October 2019, the v3.0.0 (Python 3 only) cf-python repository has moved to https://github.com/NCAS-CMS/cf-python
==========================================================================================================================

Python 2 versions of cf-python will remain, and be supported, here.
===================================================================

----------------------------------------------------------------------


CF Python
=========

The cf python package implements the CF data model for the reading,
writing and processing of data and metadata.

----------------------------------------------------------------------

Home page (v2)
==============

[**cf-python v2**](http://cfpython.bitbucket.io)

----------------------------------------------------------------------

Documentation (v2)
==================

* [**Online documentation for the latest stable v2
  release**](http://cfpython.bitbucket.io/docs/latest/ "cf-python v2
  documentation")

* Online documentation for previous releases: [**cf-python documention
  archive**](https://ncas-cms.github.io/cf-python/releases.html)

* [**Change log**](https://ncas-cms.github.io/cf-python/Changelog.html)

----------------------------------------------------------------------

Dependencies (v2)
=================

* **Required:** A
  [**GNU/Linux**](http://www.gnu.org/gnu/linux-and-gnu.html) or [**Mac
  OS**](http://en.wikipedia.org/wiki/Mac_OS) operating system.

* **Required:** A [**python**](http://www.python.org) version 2.7.
 
* **Required:** The [**python psutil
  package**](https://pypi.python.org/pypi/psutil) at version 0.6.0 or
  newer (the latest version is recommended).

* **Required:** The [**python numpy
  package**](https://pypi.python.org/pypi/numpy) at version 1.8 or
  newer.

* **Required:** The [**python matplotlib
  package**](https://pypi.python.org/pypi/matplotlib) at version 1.4.2
  or newer.

* **Required:** The [**python scipy
  package**](https://pypi.python.org/pypi/scipy) at version 0.14.0 or
  newer.

* **Required:** The [**python netCDF4
  package**](https://pypi.python.org/pypi/netCDF4) at version 1.2.1 or
  newer. This package requires the
  [**netCDF**](http://www.unidata.ucar.edu/software/netcdf),
  [**HDF5**](http://www.hdfgroup.org/HDF5) and
  [**zlib**](ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4)
  libraries.

* **Required:** The [**UNIDATA Udunits-2
  library**](http://www.unidata.ucar.edu/software/udunits). This is a
  C library which provides support for units of physical
  quantities. If The Udunits-2 shared library file
  (``libudunits2.so.0`` on GNU/Linux or ``libudunits2.0.dylibfile`` on
  Mac OS) is in a non-standard location then its path should be added
  to the ``LD_LIBRARY_PATH`` environment variable. It may also be
  necessary to specify the location of the ``udunits2.xml`` file in
  the ``UDUNITS2_XML_PATH`` environment variable (although the default
  location is usually correct).

* **Optional:** For regridding to work, the [**ESMF
  package**](https://www.earthsystemcog.org/projects/esmf) at version
  7.0.0 or newer is required. If this package is not installed then
  regridding will not work, but all other cf-python functionality will
  be unaffected. ESMF may be installed via
  [**conda**](http://conda.pydata.org/docs) (see below) or from source
  (see the file [**ESMF.md**](ESMF.md) for instructions).

* **Optional:** The [**cf-plot
  package**](https://pypi.python.org/pypi/cf-plot) does not currently
  work for versions 2.x of cf. This will be resolved soon.

----------------------------------------------------------------------

Installation (v2)
=================

* To install by [**conda**](http://conda.pydata.org/docs):

        conda install -c ncas -c conda-forge cf-python udunits2=2.2.20

    These two commands will install cf-python, all of its required
    dependencies and the two optional packages cf-plot (for
    visualisation) and ESMF (for regridding). To install cf-python and
    all of its required dependencies alone:

        conda install -c ncas -c conda-forge cf-python cf-plot udunits2=2.2.20

    To update cf-python, cf-plot and ESMF to the latest versions::

        conda install -c ncas -c conda-forge cf-python cf-plot udunits2=2.2.20
        conda install -c conda-forge mpich esmpy
	
* To install the **latest** version from
  [**PyPI**](https://pypi.python.org/pypi/cf-python):

        pip install cf-python

* To install from source:

   Download the cf package from
   `<https://pypi.python.org/pypi/cf-python>`_
   
   Unpack the library (replacing <version> with the approrpriate release,
   e.g. ``2.3.5``):
   
      $ tar zxvf cf-python-<version>.tar.gz
      $ cd cf-python-<version>
   
   To install the cf package to a central location:
   
      $ python setup.py install
   
   To install the cf package locally to the user in the default location
   (often within ``~/.local``):
   
      $ python setup.py install --user
   
   To install the cf package in the <directory> of your choice::

      $ python setup.py install --home=<directory>

----------------------------------------------------------------------

Tests (v2)
==========

The test scripts are in the ``test`` directory. To run all tests:

    python test/run_tests.py


----------------------------------------------------------------------

Command line utilities (v2)
===========================

The ``cfdump`` tool generates text representations on standard output
of the CF fields contained in the input files. 

The ``cfa`` tool creates and writes to disk the CF fields contained in
the input files.

During the installation described above, these scripts will be copied
automatically to a location given by the ``PATH`` environment
variable.

For usage instructions, use the ``-h`` option to display the manual
pages:

    cfdump -h
    cfa -h

----------------------------------------------------------------------

Code license
============

[**MIT License**](http://opensource.org/licenses/mit-license.php)

  * Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without
    restriction, including without limitation the rights to use, copy,
    modify, merge, publish, distribute, sublicense, and/or sell copies
    of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

  * The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

  * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
