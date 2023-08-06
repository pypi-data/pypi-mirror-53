
.. image:: https://img.shields.io/pypi/v/cdumay-http-client.svg
   :target: https://pypi.python.org/pypi/cdumay-http-client/
   :alt: Latest Version

.. image:: https://travis-ci.org/cdumay/cdumay-http-client.svg?branch=master
   :target: https://travis-ci.org/cdumay/cdumay-http-client
   :alt: Latest version


.. image:: https://readthedocs.org/projects/cdumay-http-client/badge/?version=latest
   :target: http://cdumay-http-client.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://img.shields.io/badge/license-BSD3-blue.svg
    :target: https://github.com/cdumay/cdumay-http-client/blob/master/LICENSE

cdumay-http-client
==================

This library is a basic HTTP client for NON-REST api with exception formatting.


Quickstart
----------

First, install cdumay-rest-client using
`pip <https://pip.pypa.io/en/stable/>`_:

    $ pip install cdumay-http-client

Next, add a `HttpClient` instance to your code:

.. code-block:: python

    from cdumay_http_client.client import HttpClient

    client = HttpClient(server="http://warp.myhost.com/api/v0")
    print(client.do_request(method="POST", path="/exec", data=[...]))

Exception
---------

You can use `marshmallow <https://marshmallow.readthedocs.io/en/latest>`_
to serialize exceptions:

.. code-block:: python

    import json, sys
    from cdumay_http_client.client import HttpClient
    from cdumay_http_client.exceptions import HTTPException, HTTPExceptionValidator

    try:
        client = HttpClient(server="http://warp.myhost.com/api/v0")
        data = client.do_request(method="GET", path="/me")
    except HTTPException as exc:
        data = HTTPExceptionValidator().dump(exc).data

    json.dump(data, sys.stdout, sort_keys=True, indent=4, separators=(',', ': '))

Result:

.. code-block:: python

    {
        "code": 404,
        "extra": {},
        "message": "Not Found"
    }

License
-------

Licensed under `BSD 3-Clause License <./LICENSE>`_ or https://opensource.org/licenses/BSD-3-Clause.