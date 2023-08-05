History
=======

1.5.7 (2019-09-27)
------------------

* Enable accidentially disabled --upgrade option.

1.5.6 (2019-09-18)
------------------

* Minor fixes to packaging and documentation.

Note: this version is broken and won't pass ``--upgrade`` option to ``pip-compile``.

1.5.4 (2019-09-16)
------------------

* Fixed MANIFEST to include features directory

Note: this version is broken and won't pass ``--upgrade`` option to ``pip-compile``.

1.5.3 (2019-09-14)
------------------

* Refactored features to separate modules.
* Allow passing verify options after verify command.
* Trim irrelevant entries from the traceback.

Note: this version is broken and won't install ``features`` directory.

1.5.2 (2019-09-12)
------------------

* Added option ``--allow-unsafe``. (thanks to @mozbhearsum #157).

1.5.1 (2019-08-08)
------------------

* Added option ``--use-cache``. (thanks to @kolotev #149).


1.5.0 (2019-08-06)
------------------

* Changed short option for ``--forbid-post`` from ``-P`` to ``-p``
  (as it conflicted with ``-P`` for ``--upgrade-package`` #147).


1.3.1 (2019-02-19)
------------------

* Re-removed workaround for future[s] packages in Python3

1.3.0 (2018-12-27)
------------------

* Introduced CLI v2 (disabled by default)


1.2.2 (2018-11-20)
------------------

* Removed workaround for future[s] packages in Python3 (no longer needed)

1.2.1 (2018-04-16)
-------------------

* Fixed Restructured text formatting (thanks to @yigor)
* Updated test dependencies (and hashes)

1.2.0 (2018-04-03)
-------------------

* Added --forbid-post option

1.1.12 (2018-02-23)
-------------------

* Added checks for conflicting package versions
* Added support for VCS dependencies
* Added --no-upgrade option

1.1.11 (2018-02-09)
-------------------

* Propagate --only-name option to references
* Fixed extension override options

1.1.10 (2018-02-09)
-------------------

* Added ``--generate-hashes`` option

1.1.9 (2018-02-08)
------------------

* Fixed directory override option
* Added --only-name option

1.1.8 (2018-01-25)
------------------

* Fixed comment justification

1.1.6 (2018-01-19)
------------------

* Added ``pip-compile-multi verify`` command

1.1.5 (2018-01-16)
------------------

* Omit future[s] packages for Python3

1.1.0 (2018-01-12)
------------------

* Added files discovery.

1.0.0 (2018-01-11)
------------------

* First release on PyPI.
