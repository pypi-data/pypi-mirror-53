Django Find Replace
===================

A Django_ management command which will replace all instances of a string throughout a database
with another - useful for bulk content changes.

.. _Django: https://www.djangoproject.com/

Installation
------------

Using pip_:

.. _pip: https://pip.pypa.io/

.. code-block:: console

    $ pip install django-findreplace

Edit your Django project's settings module, and add the application to ``INSTALLED_APPS``:

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        "findreplace",
        # ...
    ]

Usage
-----

To replace all instances of *foo* with *bar*:

.. code-block:: console

    $ ./manage.py findreplace foo bar

To use this command without being asked for confirmation:

.. code-block:: console

    $ ./manage.py findreplace --noinput foo bar
