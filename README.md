## Synopsis

This is a simple web socket listener implemented in Python (2.7) that takes a formatted GET request, with
address attributes, and geocodes it with Here or, failing that, Google.

## Installation

```git clone git@github.com:ethier/geocode_service.git```

It only relies on standard Python libraries (2.7) so if this version is installed, nothing else should be required. 2.7 is the default on Mac OSX High Sierra.

Once cloned, the service can be run via:

```python geocode_service.py --help```

A port and host can be specified via (with defaults):

    --port 8080
    --host <machine name>

## API Reference

When issuing a request to the service, the following address attributes are valid in the query string:

* address1
* address2
* city
* state
* zip
* country_code

Example: <url>?address1=123 Example Dr.&city=Example&state=EG&country_code=CA

The geocoding service will attempt to geocode anything that is passed in and will return an array of latitude/longitude results for the geocoded address.

    [
        {
            "lat": 45.3922778,
            "lng": -75.7529818
        }
    ]

In the event of an error, it will be single object response with an error key/value indicating the problem.

    [
        "error": "over_query_limit"
    ]

The service relies on both the [Here](https://developer.here.com/documentation/geocoder/topics/quick-start-geocode.html) and [Google](https://developers.google.com/maps/documentation/geocoding/start) geocoding services.

It will attempt to use Here first, provided that the HERE_APP_ID and HERE_APP_CODE environment variables are set. Without them, this service will not work, and it will fallback to Google.

For Google, a GOOGLE_API_KEY is recommended. Google rate limits requests without an application key, and results will be inconsistent without it.

## Tests

TODO
