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
