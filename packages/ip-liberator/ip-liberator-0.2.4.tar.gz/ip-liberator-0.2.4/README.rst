============
IP Liberator
============


.. image:: https://img.shields.io/pypi/v/ip-liberator.svg
        :target: https://pypi.python.org/pypi/ip-liberator

.. image:: https://img.shields.io/travis/wagnerluis1982/ip-liberator.svg
        :target: https://travis-ci.org/wagnerluis1982/ip-liberator

.. image:: https://readthedocs.org/projects/ip-liberator/badge/?version=latest
        :target: https://ip-liberator.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


A command line utility to update AWS Security Groups rules.


* Free software: GNU General Public License v3
* Documentation: https://ip-liberator.readthedocs.io.


Features
--------

* Update a list of security groups of your AWS account at once.
* Grant access to informed ports for your current IP address or an informed IP.
* Read profile files in JSON with all the information needed to contact.
* Fit for use as script (e.g. to update your dynamic IP regularly).

Installation
------------

.. code-block:: console

    $ pip install ip-liberator

Quickstart
----------

Consider a file ``/path/my-profile.json`` with the following content:

.. code-block:: json

    {
      "credentials": {
        "access_key": "<AWS_ACCESS_KEY>",
        "secret_key": "<AWS_SECRET_KEY>",
        "region_name": "<AWS REGION>"
      },
      "config": {
        "operator": "John",
        "services": [
          {
            "name": "FTP+SFTP",
            "port": "21-22"
          },
          {
            "name": "HTTPS",
            "port": "443"
          }
        ],
        "security_groups": [
          "sg-<GROUP_ID_1>",
          "sg-<GROUP_ID_2>"
        ]
      }
    }

Using the profile defined above will create or update two entries in the informed security groups:

- **John FTP+SFTP** granting access for the current IP the ports 21 and 22.
- **John HTTPS** granting access for the current IP the port 443.

To accomplish it, simply run:

.. code-block:: console

    $ ip-liberator --profile /path/my-profile.json
    Authorizing rules ['John FTP+SSH', 'John HTTPS'] to IP 192.30.253.112/32
    - sg-<GROUP_ID_1>
    - sg-<GROUP_ID_2>

Credits
-------

Authors
:::::::

* Wagner Macedo <wagnerluis1982@gmail.com> (maintainer)


=======
History
=======

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.1.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

0.2.4 (2019-10-10)
------------------

Added
+++++

- Improve script output showing version and a cool summary of settings.

Fixed
+++++

- When using a tag, the script was always reauthorizing even when IP was not changed,
  this version fixed this bad behavior.

0.2.3 (2019-09-20)
------------------

Fixed
+++++

- Fix tagged rule is retagged when authorizing or revoking

0.2.2 (2019-09-18)
------------------

This release marks a breaking change. Now the script "tags" recorded entries in
the security groups, e.g. ``[ip-liberator] SSH John`` instead of only ``SSH John``.
That helps to identify what IP Liberator added and what was added by hand.

By default, the tag is **ip-liberator**, but can be change through the new
option ``--tag``. If the user wants the previous behavior, i.e. without a tag,
he or she must pass the option ``--no-tag``.

Added
+++++

- Add option ``--operator`` to change the profile operator.
- Add short option ``-p`` for ``--profile``
- Add option ``--version`` to show current script version.

Changed
+++++++

- Add option ``--tag`` to identify entries added by the script.
- Migrate build system to Poetry

0.2.1 (2019-04-19)
------------------

- Fix documentation

0.2.0 (2019-04-19)
------------------

This release marks as the first to be published to PyPI.

No new functionality was added. The version was changed was to place a history mark.

- Added documentation.
- Added full coverage tests.
- Code refactoring.

0.1.1 (2018-10-16)
------------------

- Better console output.
- Added option ``--revoke-only``.
- Don't reauthorize if the IP address is already in the security group.
- Authorizing and revoking in batch to be more efficient.
- Bugfixes

0.1.0 (2018-09-27)
------------------

- Added option ``--my-ip`` to inform an IP address explicitly.
- Show in console the security groups being processed.
- Allow use as script by reading JSON as external config.
