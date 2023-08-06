========================
Utils for url shortener
========================

Included is:

* ``URLParser``

Installation
============

::

    pip install smm_utils

=============
Usage
=============

::

    from us_utils import URLParser

    parser = URLParser(url)

    print(parser.scheme)
    print(parser.username)
    print(parser.password)
    print(parser.subdomain)
    print(parser.path)
    print(parser.uri)
    print(parser.uri_dict)

