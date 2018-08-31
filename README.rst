=============================
Django VCN accounts
=============================

.. image:: https://badge.fury.io/py/dj-vcn-accounts.svg
    :target: https://badge.fury.io/py/dj-vcn-accounts

.. image:: https://travis-ci.org/hbuyse/dj-vcn-accounts.svg?branch=master
    :target: https://travis-ci.org/hbuyse/dj-vcn-accounts

.. image:: https://codecov.io/gh/hbuyse/dj-vcn-accounts/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/hbuyse/dj-vcn-accounts

VCN accounts

Documentation
-------------

The full documentation is at https://dj-vcn-accounts.readthedocs.io.

Quickstart
----------

Install Django VCN accounts::

    pip install dj-vcn-accounts

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'dj_vcn_accounts.apps.DjVcnAccountsConfig',
        ...
    )

Add Django VCN accounts's URL patterns:

.. code-block:: python

    from dj_vcn_accounts import urls as dj_vcn_accounts_urls


    urlpatterns = [
        ...
        url(r'^', include(dj_vcn_accounts_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
