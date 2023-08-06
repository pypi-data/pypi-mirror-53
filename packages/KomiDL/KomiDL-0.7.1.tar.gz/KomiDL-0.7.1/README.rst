Description
===========

KomiDL (コミDL) is a command-line program that can download images and series
from web galleries.

Inspired by youtube-dl, KomiDL is able to download
images from any supported website URL. It also supports tag extraction and
can export files downloaded to formats such as archives (zip, tar, gztar,
bztar) or PDF.

Custom extractors can be written by implementing the abstract Extractor class
and registering it to extractors.py.

As the program is currently in early stages of development, bugs are likely
to occur. Use the program at your own risk.

Dependencies
============

* python 3.7+
* requests
* BeautifulSoup
* Pillow
* aiohttp
* aiofiles

Installation
============

As the program is currently in early stages of development, it is
recommended that you download and install the latest version from the git
repository's MASTER branch to get all the lastest features and bug fixes.

Installation from pip
---------------------

``
pip install komidl
``

Installation from source
------------------------

Clone the repository, then install using setup.py.

``
git clone http://gitlab.com/dnsheng/komidl.git
cd ./komidl
python3 setup.py install
``

Usage
=====

Get help by running:

``
komidl -h
``

Testing
=======

Go to the folder containing setup.py and run the following command:

``
python setup.py test
``

License
=======

Copyright (c) 2019 DNSheng

Licensed under the GNU GPLv3 license.

See LICENSE for the full details.
