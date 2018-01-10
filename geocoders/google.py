import urllib
import cgi
import os

class Google(object):
    def __init__(self, address):
        self.address = address

        # Google
        # https://developers.google.com/maps/documentation/geocoding/start
        self.google_app_url = "https://maps.googleapis.com/maps/api"
        self.google_app_url += "/geocode/json"

        self.google_api_key = ''

        try:
            self.google_api_key = cgi.escape(os.environ['GOOGLE_API_KEY'])
        except Exception as e:
            google_service_error = ("Error: Google API key not set in "
                                    "environment variables. Will attempt to use without, but "
                                    "rate limiting without an API key may result in inconsistent "
                                    "results.")

            print(google_service_error)

    def request_url(self, address):
        print("Geocode with Google: {address}".format(
            address=address))

        url = self.google_app_url
        url += "?address="

        # Google expects address attributes separated by ,.
        address_values = address.values()
        address_values = ','.join([str(attribute)
                                  for attribute in address_values])

        url += urllib.quote(address_values)

        if self.google_api_key:
            url += "&key="
            url += self.google_api_key

        return url

    def response(self, data):
        print("Response data: {data}".format(data=data))

        response = []

        if data['status'] == 'OVER_QUERY_LIMIT':
            error = { 'error': 'over_query_limit' }
            response.append(error.copy())
        elif data['status'] == 'OK':
            for result in data['results']:
                geometry_location = result['geometry']['location']
                lat_lng = {
                    "lat": geometry_location['lat'], "lng": geometry_location['lng']}

                response.append(lat_lng.copy())

        print(response)
        return response
