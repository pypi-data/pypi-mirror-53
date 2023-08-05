# coding=utf-8
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2019

"""
Overview
++++++++

Provides functions to add Streams operators acting as communication endpoints for your Streams application.


Sample
++++++

A simple example of a Streams application that provides an endpoint for json injection::

    from streamsx.topology.topology import *
    from streamsx.topology.context import submit
    import streamsx.endpoint as endpoint

    topo = Topology()

    s1 = endpoint.inject(topo)
    s1.print()

    # Use for IBM Streams including IBM Cloud Pak for Data
    submit ('DISTRIBUTED', topo)


"""

__version__='0.3.0'

__all__ = ['download_toolkit', 'inject', 'view_tuples']
from streamsx.endpoint._endpoint import download_toolkit, inject, view_tuples

