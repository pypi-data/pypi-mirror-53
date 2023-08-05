ftw.autofeature automatically registers ZCML features.


Extras features
===============

The ``autofeature:extras`` directive automatically registers ZCML features for each
extra (``extras_requires``) of your package.
The feature for an extra is automatically provided when each dependency of the extra
is installed.


Example
-------

When having a setup.py like this:

.. code:: python

    from setuptools import setup, find_packages

    setup(name='my.package',
          version='1.0.0dev0',
          packages=find_packages(exclude=['ez_setup']),
          namespace_packages=['my'],
          install_requires=[
              'setuptools',
              'ftw.autofeature',
          ],

          extras_require={
              'tests': ['unittest2'],
              'foo': ['foo', 'foo-compat'],
              'bar': ['bar', 'bar-compat']})


you can let ``ftw.autofeature`` automatically declare features for your extras:

.. code:: XML

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:zcml="http://namespaces.zope.org/zcml"
        xmlns:autofeature="http://namespaces.zope.org/autofeature">

        <include package="ftw.autofeature" file="meta.zcml" />
        <autofeature:extras />

        <configure zcml:condition="have my.package:foo">
            <!-- foo things -->
        </configure>

        <configure zcml:condition="have my.package:bar">
            <!-- bar things -->
        </configure>

        <configure zcml:condition="have my.package:foo:bar">
            <!-- foo and bar things -->
        </configure>

    </configure>


The feature ``my.package:foo`` is only registered when the extras is installed.
When installing both, ``foo`` and ``bar``, multiple features are registered so that
it easy to combine extras with ``AND``:

- ``my.package:foo``
- ``my.package:foo:bar``
- ``my.package:bar``
- ``my.package:bar:foo``


Limitiation
-----------

We cannot really detect whether the extras was explictly used on installation time.
We therefore test whether each dependency in the extras is installed.
When each dependency is installed but not the extras explicitly, this will thus also
register the feature.


Dump feature
============

The ``autofeature:dump`` directive dumps the currently registered ZCML features
to the standard out.
Simply use the directive to dump the features at any point in the ZCML:


.. code:: XML

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:autofeature="http://namespaces.zope.org/autofeature">

        <include package="ftw.autofeature" file="meta.zcml" />
        <autofeature:dump />

    </configure>


Links
=====

- Github: https://github.com/4teamwork/ftw.autofeature
- Issues: https://github.com/4teamwork/ftw.autofeature/issues
- Pypi: http://pypi.python.org/pypi/ftw.autofeature
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.autofeature


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.autofeature`` is licensed under GNU General Public License, version 2.
