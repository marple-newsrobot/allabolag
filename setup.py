# encoding:utf-8
from setuptools import setup

###
# Versioning
###
from datetime import date

name = "allabolag"

short_version = "0.8.0"
long_version = short_version

short_desc = """\
Scrape data from allabolag.se.\
"""
authors = u"Jens Finnäs, Newsworthy"
year = date.today().year
copyright = "%s, %s" % (year, authors)
email = "jens.finnas@gmail.com"

version = long_version

###
# Setup
###


def readme():
    """Import README for use as long_description."""
    with open("README.rst") as f:
        return f.read()


repo = "https://github.com/marple-newsrobot/allabolag"

setup(
    name=name,
    version=version,
    description=short_desc,
    long_description=readme(),
    long_description_content_type='text/x-rst',
    url=repo,
    author=authors,
    author_email=email,
    license="MIT",
    packages=[name],
    zip_safe=False,
    python_requires='>=2.7',
    install_requires=[
        "requests>=2.22.0",
        "beautifulsoup4>=4.7.1",
    ],
    include_package_data=True,
    download_url="{}/archive/{}.tar.gz".format(repo, version),
)
