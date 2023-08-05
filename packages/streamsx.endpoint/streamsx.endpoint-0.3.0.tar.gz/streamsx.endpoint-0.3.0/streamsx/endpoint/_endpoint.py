# coding=utf-8
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2019

import datetime
from tempfile import gettempdir
import streamsx.spl.op
import streamsx.spl.types
from streamsx.topology.schema import CommonSchema, StreamSchema
from streamsx.spl.types import rstring

from streamsx.toolkits import download_toolkit

_TOOLKIT_NAME = 'com.ibm.streamsx.inetserver'



def download_toolkit(url=None, target_dir=None):
    r"""Downloads the latest Inetserver toolkit from GitHub.

    Example for updating the Inetserver toolkit for your topology with the latest toolkit from GitHub::

        import streamsx.endpoint as endpoint
        # download toolkit from GitHub
        toolkit_location = endpoint.download_toolkit()
        # add the toolkit to topology
        streamsx.spl.toolkit.add_toolkit(topology, toolkit_location)

    Example for updating the topology with a specific version of the toolkit using a URL::

        import streamsx.endpoint as endpoint
        url410 = 'https://github.com/IBMStreams/streamsx.inetserver/releases/download/v4.1.0/streamsx.inetserver-4.1.0-9c07b97-20190905-1147.tgz'
        toolkit_location = endpoint.download_toolkit(url=url410)
        streamsx.spl.toolkit.add_toolkit(topology, toolkit_location)

    Args:
        url(str): Link to toolkit archive (\*.tgz) to be downloaded. Use this parameter to 
            download a specific version of the toolkit.
        target_dir(str): the directory where the toolkit is unpacked to. If a relative path is given,
            the path is appended to the system temporary directory, for example to /tmp on Unix/Linux systems.
            If target_dir is ``None`` a location relative to the system temporary directory is chosen.

    Returns:
        str: the location of the downloaded toolkit

    .. note:: This function requires an outgoing Internet connection
    """
    _toolkit_location = streamsx.toolkits.download_toolkit (toolkit_name=_TOOLKIT_NAME, url=url, target_dir=target_dir)
    return _toolkit_location


def inject(topology, port=0, schema=CommonSchema.Json, name=None):
    """Receives HTTP POST requests.

    Embeds a Jetty web server to allow HTTP/HTTPS POST requests with the following mime types to be submitted as tuple on the output stream:

    .. csv-table::
        :header: schema, content-type

        CommonSchema.Json, application/json
        CommonSchema.XML, application/xml
        CommonSchema.String, application/x-www-form-urlencoded
        StreamSchema, application/x-www-form-urlencoded

    Args:
        topology: The Streams topology.
        port: Port number for the embedded Jetty HTTP server. If the port is set to 0, the jetty server uses a free tcp port, and the metric serverPort delivers the actual value. 
        schema: Schema for returned Stream, default is ``CommonSchema.Json``
        name(str): Source name in the Streams context, defaults to a generated name.

    Returns:
        Output Stream with schema defined in ``schema`` parameter (default ``CommonSchema.Json``).
    """

    if schema is CommonSchema.Json:
        kind = 'com.ibm.streamsx.inet.rest::HTTPJSONInjection'   
    elif schema is CommonSchema.XML:
        kind = 'com.ibm.streamsx.inet.rest::HTTPXMLInjection'
    elif (schema is CommonSchema.String) or (isinstance(schema, StreamSchema)):
        kind = 'com.ibm.streamsx.inet.rest::HTTPTupleInjection'
    else:
        raise ValueError(schema)

    _op = _HTTPInjection(topology, kind=kind, port=port, schema=schema, name=name)
    return _op.outputs[0]


def view_tuples(stream, port=0, name=None):
    """REST HTTP/HTTPS API to view tuples from windowed input ports.

    Embeds a Jetty web server to provide HTTP REST access to the collection of tuples in the input port window at the time of the last eviction for tumbling windows, or last trigger for sliding windows.

    Example with a sliding window::

        import streamsx.endpoint as endpoint
        s = topo.source([{'a': 'Hello'}, {'a': 'World'}, {'a': '!'}]).as_json()
        endpoint.view_tuples(s.last(3).trigger(1))

    Args:
        stream(Stream): Windowed stream of tuples that will be viewable using a HTTP GET request. 
        port: Port number for the embedded Jetty HTTP server. If the port is set to 0, the jetty server uses a free tcp port, and the metric serverPort delivers the actual value. 
        name(str): Source name in the Streams context, defaults to a generated name.

    Returns:
        streamsx.topology.topology.Sink: Stream termination.
    """
    _op = _HTTPTupleView(stream, port=port, name=name)
    return streamsx.topology.topology.Sink(_op)



class _HTTPInjection(streamsx.spl.op.Source):

    def __init__(self, topology, kind, schema=None, certificateAlias=None, context=None, contextResourceBase=None, keyPassword=None, keyStore=None, keyStorePassword=None, port=None, trustStore=None, trustStorePassword=None, vmArg=None, name=None):
        topology = topology
        params = dict()
        if vmArg is not None:
            params['vmArg'] = vmArg
        if certificateAlias is not None:
            params['certificateAlias'] = certificateAlias 
        if context is not None:
            params['context'] = context
        if contextResourceBase is not None:
            params['contextResourceBase'] = contextResourceBase
        if keyPassword is not None:
            params['keyPassword'] = keyPassword
        if keyStore is not None:
            params['keyStore'] = keyStore
        if keyStorePassword is not None:
            params['keyStorePassword'] = keyStorePassword
        if port is not None:
            params['port'] = port
        if trustStore is not None:
            params['trustStore'] = trustStore
        if trustStorePassword is not None:
            params['trustStorePassword'] = trustStorePassword

        super(_HTTPInjection, self).__init__(topology,kind,schema,params,name)


class _HTTPTupleView(streamsx.spl.op.Sink):

    def __init__(self, stream, certificateAlias=None, context=None, contextResourceBase=None, forceEmpty=None, headers=None, host=None, keyPassword=None, keyStore=None, keyStorePassword=None, namedPartitionQuery=None, partitionBy=None, partitionKey=None, port=None, trustStore=None, trustStorePassword=None, vmArg=None, name=None):
        topology = stream.topology
        kind="com.ibm.streamsx.inet.rest::HTTPTupleView"
        params = dict()
        if vmArg is not None:
            params['vmArg'] = vmArg
        if certificateAlias is not None:
            params['certificateAlias'] = certificateAlias
        if context is not None:
            params['context'] = context
        if contextResourceBase is not None:
            params['contextResourceBase'] = contextResourceBase
        if forceEmpty is not None:
            params['forceEmpty'] = forceEmpty
        if headers is not None:
            params['headers'] = headers
        if host is not None:
            params['host'] = host
        if keyPassword is not None:
            params['keyPassword'] = keyPassword
        if keyStore is not None:
            params['keyStore'] = keyStore
        if keyStorePassword is not None:
            params['keyStorePassword'] = keyStorePassword
        if namedPartitionQuery is not None:
            params['namedPartitionQuery'] = namedPartitionQuery
        if partitionBy is not None:
            params['partitionBy'] = partitionBy
        if partitionKey is not None:
            params['partitionKey'] = partitionKey
        if port is not None:
            params['port'] = port
        if trustStore is not None:
            params['trustStore'] = trustStore
        if trustStorePassword is not None:
            params['trustStorePassword'] = trustStorePassword

        super(_HTTPTupleView, self).__init__(kind,stream,params,name)

