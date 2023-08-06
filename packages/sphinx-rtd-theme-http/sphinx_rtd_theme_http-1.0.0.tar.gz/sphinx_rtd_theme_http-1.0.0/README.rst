sphinx_rtd_theme_http
=====================

``sphinx_rtd_theme_http`` provides customisations on top of
`sphinx_rtd_theme <https://github.com/rtfd/sphinx_rtd_theme/>`_
to make it easier to view and navigate documentation written with the
`Sphinx HTTP domain <https://github.com/sphinx-contrib/httpdomain>`_.

.. image:: screenshot.gif
    :alt: Screenshot

Getting Started
---------------

The following steps will walk through how to add ``sphinx_rtd_theme_http``
to an existing Sphinx project.

For instructions on how to set up a Sphinx project,
see Sphinx's documentation on
`Getting Started <https://www.sphinx-doc.org/en/master/usage/quickstart.html>`_.

Installation
~~~~~~~~~~~~

The package can be installed though pip:

.. code-block:: bash

    pip install sphinx_rtd_theme_http

Next, add ``sphinx_rtd_theme_http`` to the list of extensions in your
Sphinx project's ``conf.py``.

.. code-block:: python

    extensions.append('sphinx_rtd_theme_http')

Versioning
----------

We use `SemVer <http://semver.org/>`_ for versioning.
For the versions available,
see the `tags on this repository <https://github.com/AWhetter/sphinx_rtd_theme_http/tags>`_.

License
-------

This project is licensed under the BSD-3-Clause license.
See the `LICENSE.rst <LICENSE.rst>`_ file for details.
