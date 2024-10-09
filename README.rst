This is a scraper for collecting data from allabolag.se. It has no formal relationship with the site.

It is written and maintained for `Newsworthy <https://www.newsworthy.se/en/>`_, but could possibly come in handy for other people as well.


Installing
----------

.. code-block:: bash

  pip install allabolag


Example usage
-------------

.. code-block:: python3

  from allabolag import Company

  company = Company("559071-2807")

  # show all available data about the company in a raw...
  print(company.raw_data)

  # ...or cleaned format
  print(company.data)

And you can iterate the list of recent liquidations.

.. code-block:: python3

  from allabolag import iter_liquidated_companies

  for company in iter_liquidated_companies(until="2019-06-01"):
    print(company)

Use AWS API Gateway to rotate IP addresses

.. code-block:: python3

  from allabolag import AWSGatewayRequestClient
  request_client = AWSGatewayRequestClient()
  company = Company("559071-2807", request_client=request_client)

  for company in iter_liquidated_companies(until="2019-06-01",request_client=request_client):
    print(company)


Developing
----------

To run tests:

.. code-block:: python3

  python3 -m pytest

Deployment
----------

To deploy a new version to PyPi:

1. Update Changelog below.
2. Update version in `setup.py`
3. Build: `python3 setup.py sdist bdist_wheel`
4. Upload: `python3 -m twine upload dist/allabolag-X.Y.X*`

...assuming you have Twine installed (`pip install twine`) and configured.

Changelog
---------

- 0.8.0
  - Handle Koncernredovisning
  - Make RequestClient Python 3.8 compatible

- 0.7.1
  - Update request client to use inited client, rather than class

- 0.7.0
  - Add AWSGatewayRequestClient to enable request through rotating IP with AWS API Gateway

- 0.6.1
  - Bug fix: Actually use header in requests.

- 0.6.0
  - Add headers to request
  - Minor dependency updates
  - Use logger for debugging

- 0.5.1
  - Fix return type for `Company.liquidation`

- 0.5.0
  - Add `Company.liquidation`

- 0.4.1
  - Remove debug output
  - Don't crash when we reach the end of a list

- 0.4.0
  - Add option to start from page N
  - Add custom exception for missing company

- 0.3.1
  - Add cache for company data

- 0.3.0
  - Add `Company.remarks` (a list of remarks, e.g. “Konkurs”)

- 0.2.1
  - Make `iter_list()` more generic, by accepting the while url fragment

- 0.2.0
  - Add `iter_list()` function

- 0.1.7

  - Bug fix: Add encoding for Python 2.7 

- 0.1.6

  - Fixes bug when company has remark about Svensk Handels Varningslistan

- 0.1.5

  - Make Python 2.7 compatible.

- 0.1.4

  - Updating _iter_liquidate_companies to handle rebuilt site.

- 0.1.3

  - Bug fixes

- 0.1.0

  - First version
