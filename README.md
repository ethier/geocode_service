## Synopsis

This is a simple web socket listener implemented in Python (2.7) that takes a formatted GET request, with
address attributes, and geocodes it with Here or, failing that, Google.

Once cloned, the service can be run via:

```python service.py --help```

A port and host can be specified via (with defaults):
```--port 8080```
```--host <machine name>```

It expects environment variables to configure the Here service, or set a Google API key.

Details on what they should be are specified in the service help.

## Installation

```git clone git@github.com:ethier/geocode_service.git```

It only relies on standard Python libraries (2.7) so if this version is installed, nothing else should be required. 2.7 is the default on Mac OSX High Sierra.

## API Reference

The following address attributes are valid in the query string:
['address1', 'address2', 'city', 'state', 'zip', 'country_code']

Example: <url>?address1=123 Example Dr.&city=Example&state=EG&...

## Tests

TODO
