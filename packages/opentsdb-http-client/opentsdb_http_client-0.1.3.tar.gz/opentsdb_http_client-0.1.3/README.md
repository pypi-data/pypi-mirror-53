# **opentsdb_http_client**

This library supports sending metrics using the opentsdb http protocal to opentsdb http endpoint. A 'Client' from the library should be instantiated once in an application, and then that instance should be used to send each new metric for indexing or putting. A Client is a specific http connection consisting of a set of connection settings.

## Client parameters:

> **host** = The host you will be sending data too, i.e. 'my-host.my.url'. Do not put the http:// in front.

> **port** = The port you will connect to on that host.

> **test_api** = The api end_point for testing if a service is up, i.e. '/api/health'. Assumes a 200 return code on success.

> **put_api** = The api end_point for a put request to the service, i.e. '/api/put'. Assumes a 200 or 204 return code on success.

> **qsize**[100000] = The size of your queue used to buffer messages to be sent from the worker thread.

> **host_tag**[True] = If True, sets a tag of host='current-hostname' automatically on each metric being sent.

> **mps**[0] = metrics per second you will allow. Every time the worker thread sends a metric it will sleep 1/mps before continueing. If it is 0, the worker thread will send metrics as fast as possible.

> **check_host**[True] = If True, the client will test the test_api endpoint on instantiation to see if the host is reachable.

> **test_mode**[False] = If True, the worker thread will not actually send any metrics to the host

## Available Clients:

> OpenTSDBClient - connects to host at port 4242 with put_api '/api/put'

## Usage:

First instantiate a client somewhere in the application:

```
from opentsdb_http_client import http_client

opentsdb_client = http_client.OpenTSDBClient('my-optsdb-instance.my.url')
```

Then add code throughout your application to send metrics. You may want to wrap the metrics sending code in a function which automatically adds a set of default tag key-value pairs for that application
Adding an optional 'async' parameter to sending the data will determine if the data is sent to opentsdb asynchronously (default)
or synchronously. Specificy async=True on sends that you want to happen immediately, like when the application will close
immediately after or you are trying to wrap threaded objects with metrics (like celery tasks).


```
opentsdb_client.put('test_metrics_namespace.metric_1', 24.5, tag1='tag1_value', tag2='tag2_value', ...)
```


This library is based off of pots (https://github.com/orionvm/potsdb) and should be considered to have its same license: GPL 2.0
