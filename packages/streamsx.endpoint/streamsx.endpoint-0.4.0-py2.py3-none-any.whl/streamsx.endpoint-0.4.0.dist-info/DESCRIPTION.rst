Overview
========

Provides functions to add Streams operators acting as communication endpoints for your Streams application.

This package exposes the `com.ibm.streamsx.inetserver <https://ibmstreams.github.io/streamsx.inetserver/>`_ toolkit as Python methods for use with IBM Streams including IBM Cloud Pak for Data.

* `IBM Streams developer community <https://developer.ibm.com/streamsdev/>`_


Sample
======

A simple example of a Streams application that provides an endpoint for json injection::

    from streamsx.topology.topology import *
    from streamsx.topology.context import submit
    import streamsx.endpoint as endpoint

    topo = Topology()

    s1 = endpoint.inject(topo)
    s1.print()

    submit ('DISTRIBUTED', topo)


Documentation
=============

* `streamsx.endpoint package documentation <http://streamsxendpoint.readthedocs.io>`_


