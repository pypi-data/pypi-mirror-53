========================
django-language-fields
========================

Language and Region Fields for Django apps. Includes all language choices from the IANA Language Subtag Registry.

Included is:

* ``LanguageField``, a model field
* ``RegionField``, a model field

Installation
============

::

    pip install django-language-fields


Basic usage
===========

Add ``languages`` to the list of the installed apps in
your ``settings.py`` file::

    INSTALLED_APPS = [
        ...
        'languages',
        ...
    ]

Then, you can use it like any regular model field::

    from languages.fields import LanguageField, RegionField

    class MyModel(models.Model):
        ..
        language = LanguageField()
        ..

    class MyModel(models.Model):
        ..
        region = RegionField()
        ..

Internally, LanguageField and RegionField are based upon ``CharField`` and by default
represented as strings.

As with ``CharField``'s, it is discouraged to use ``null=True`` use ``blank=True`` if you want to make it a non-required field.
