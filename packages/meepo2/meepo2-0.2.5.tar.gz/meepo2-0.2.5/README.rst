======
Meepo2
======

.. image:: http://img.shields.io/travis/huskar-org/meepo2/master.svg?style=flat
   :target: https://travis-ci.org/huskar-org/meepo2

.. image:: http://img.shields.io/pypi/v/meepo2.svg?style=flat
   :target: https://pypi.python.org/pypi/meepo2

.. image:: http://img.shields.io/pypi/dm/meepo2.svg?style=flat
   :target: https://pypi.python.org/pypi/meepo2

Meepo2 is event sourcing and event broadcasting for databases.

Documentation: https://meepo2.readthedocs.org/


Installation
============

:Requirements: **Python 2.x >= 2.7** or **Python 3.x >= 3.2** or **PyPy**

To install the latest released version of Meepo2::

    $ pip install meepo2


Features
========

Meepo2 can be used to do lots of things, including replication, eventsourcing,
cache refresh/invalidate, real-time analytics etc. The limit is all the tasks
should be row-based, since meepo2 only gives ``table_action`` -> ``pk``
style events.

* Row-based database replication.

* Replicate RDBMS to NoSQL and search engine.

* Event Sourcing.

* Logging and Auditing

* Realtime analytics


Usage
=====

Checkout `documentation`_ and `examples/`_.

.. _`documentation`: https://meepo2.readthedocs.org/en/latest/
.. _`examples/`: https://github.com/huskar-org/meepo2/tree/develop/examples
