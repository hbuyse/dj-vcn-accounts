=====
Usage
=====

To use Django VCN accounts in a project, add it to your `INSTALLED_APPS`:

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
