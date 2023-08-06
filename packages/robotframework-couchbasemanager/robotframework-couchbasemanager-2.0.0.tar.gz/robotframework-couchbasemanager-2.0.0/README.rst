RobotFramework Couchbase Manager Library
========================================

|Build Status|

Short Description
-----------------

`Robot Framework`_ library for managing Couchbase server, based on `Couchbase REST API`_.

Installation
------------

::

    pip install robotframework-couchbasemanager

Documentation
-------------

See keyword documentation for robotframework-couchbasemanager library in
folder ``docs``.

Example
-------
+-----------+------------------+
| Settings  |       Value      |
+===========+==================+
|  Library  | CouchbaseManager |
+-----------+------------------+
|  Library  |   Collections    |
+-----------+------------------+

+---------------+---------------------------------------+--------------+----------+---------------+-----------------+
|  Test cases   |                 Action                |   Argument   | Argument |    Argument   |    Argument     |
+===============+=======================================+==============+==========+===============+=================+
|  Simple Test  | CouchbaseManager.Connect To Couchbase | my_host_name |   8091   | administrator | alias=couchbase |
+---------------+---------------------------------------+--------------+----------+---------------+-----------------+
|               | ${overview}=                          | Overview     |          |               |                 |
+---------------+---------------------------------------+--------------+----------+---------------+-----------------+
|               | Log Dictionary                        | ${overview}  |          |               |                 |
+---------------+---------------------------------------+--------------+----------+---------------+-----------------+
|               | Close All Couchbase Connections       |              |          |               |                 |
+---------------+---------------------------------------+--------------+----------+---------------+-----------------+

License
-------

Apache License 2.0

.. _Robot Framework: http://www.robotframework.org
.. _Couchbase REST API: http://docs.couchbase.com/couchbase-manual-2.5/cb-rest-api/

.. |Build Status| image:: https://travis-ci.org/peterservice-rnd/robotframework-couchbasemanager.svg?branch=master
   :target: https://travis-ci.org/peterservice-rnd/robotframework-couchbasemanager