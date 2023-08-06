=======================================================
Clout: Command Line Object Utility Tool
=======================================================

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        |
    * - package
      - | |version|
        | |wheel|
        | |supported-versions|
        | |supported-implementations|
        | |commits-since|

.. |docs| image:: https://img.shields.io/readthedocs/clout
    :target: https://clout.readthedocs.org
    :alt: Documentation Status


.. |travis| image:: https://img.shields.io/travis/com/python-clout/clout
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/python-clout/clout

.. |version| image:: https://img.shields.io/pypi/v/clout.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/pypi/clout

.. |commits-since| image:: https://img.shields.io/github/commits-since/python-clout/clout/v0.1.8.svg
    :alt: Commits since latest release
    :target: https://github.com/python-clout/clout/compare/v0.1.8...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/clout.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/pypi/clout

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/clout.svg
    :alt: Supported versions
    :target: https://pypi.org/pypi/clout

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/clout.svg
    :alt: Supported implementations
    :target: https://pypi.org/pypi/clout


.. end-badges



..
    start-usage


Convert dataclasses into a command-line interface.

Quickstart
---------------


To install, use

.. code-block:: bash

    pip install clout


Define some dataclasses and convert them into a command-line interface.


.. code-block:: python

    import attr
    import click

    import clout


    @attr.dataclass
    class DB:
        host: str
        port: int


    @attr.dataclass
    class Config:
        db: DB
        dry_run: bool


    cli = clout.Command(type=Config)

    print(cli.build())


.. code-block:: bash

    $ myapp config --dry-run db --host example.com --port 9999
    Config(db=DB(host='example.com', port=9999), dry_run=True)


..
    end-usage

See the full docs for more information: https://clout.readthedocs.io/
