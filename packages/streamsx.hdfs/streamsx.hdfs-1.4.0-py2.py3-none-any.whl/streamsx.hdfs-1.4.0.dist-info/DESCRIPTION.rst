Overview
========

Provides functions to access files on HDFS. For example, connect to IBM Analytics Engine on IBM Cloud.

This package exposes the `com.ibm.streamsx.hdfs <https://ibmstreams.github.io/streamsx.hdfs/>`_ toolkit as Python methods for use with Streaming Analytics service on
IBM Cloud and IBM Streams including IBM Cloud Pak for Data.

* `Streaming Analytics service <https://console.ng.bluemix.net/catalog/services/streaming-analytics>`_
* `IBM Streams developer community <https://developer.ibm.com/streamsdev/>`_
* `IBM Analytics Engine <https://www.ibm.com/cloud/analytics-engine>`_


Sample
======

A simple hello world example of a Streams application writing string messages to
a file to HDFS. Scan for created file on HDFS and read the content::

    from streamsx.topology.topology import *
    from streamsx.topology.schema import CommonSchema, StreamSchema
    from streamsx.topology.context import submit
    import streamsx.hdfs as hdfs

    credentials = json.load(credentials_analytics_engine_service)

    topo = Topology('HDFSHelloWorld')

    to_hdfs = topo.source(['Hello', 'World!'])
    to_hdfs = to_hdfs.as_string()

    # Write a stream to HDFS
    hdfs.write(to_hdfs, credentials=credentials, file='/sample/hw.txt')

    scanned = hdfs.scan(topo, credentials=credentials, directory='/sample', init_delay=10)

    # read text file line by line
    r = hdfs.read(scanned, credentials=credentials)

    # print each line (tuple)
    r.print()

    submit('STREAMING_ANALYTICS_SERVICE', topo)
    # Use for IBM Streams including IBM Cloud Pak for Data
    # submit ('DISTRIBUTED', topo)


Documentation
=============

* `streamsx.hdfs package documentation <http://streamsxhdfs.readthedocs.io/>`_


