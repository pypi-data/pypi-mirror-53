linenotipy
==========

|PyPI| |License: MIT| |codecov| |Build Status| |PyPI - Python Version|

linenotipy is a python client library for line notify api on Python 3.5
and above.

Installation
------------

::

    $ pip install linenotipy

Usage
-----

.. code:: python

    #
    # basic
    #
    from linenotipy import Line

    line = Line(token='XXXXXXXXXX')
    line.post(message="Hello, world.")

    #
    # image
    #
    from linenotipy import Line

    line = Line(token='XXXXXXXXXX')
    line.post(message="Hello, image.", imageFile="test.png")

    #
    # stamp
    #
    from linenotipy import Line

    line = Line(token='XXXXXXXXXX')
    line.post(message="Hello, stamp.", stickerPackageId=3, stickerId=180)

sticker
`documentation <https://devdocs.line.me/files/sticker_list.pdf>`__

Getting started
---------------

For help getting started with LINE Notify API, view our online
`documentation <https://notify-bot.line.me/doc/en/>`__.

Contributing
------------

1. Fork it
2. Create your feature branch (``git checkout -b my-new-feature``)
3. Commit your changes (``git commit -am 'Add some feature'``)
4. Push to the branch (``git push origin my-new-feature``)
5. Create new Pull Request

.. |PyPI| image:: https://img.shields.io/pypi/v/linenotipy
   :target: https://pypi.org/project/linenotipy/
.. |License: MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
.. |codecov| image:: https://codecov.io/gh/10mohi6/line-notify-python/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/10mohi6/line-notify-python
.. |Build Status| image:: https://travis-ci.com/10mohi6/line-notify-python.svg?branch=master
   :target: https://travis-ci.com/10mohi6/line-notify-python
.. |PyPI - Python Version| image:: https://img.shields.io/pypi/pyversions/linenotipy
   :target: https://pypi.org/project/linenotipy/
