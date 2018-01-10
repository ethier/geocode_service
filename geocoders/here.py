import re
import urllib
import cgi
import os

class Here(object):
    def __init__(self, address):
        self.address = address

        # Here:
        # https://developer.here.com/documentation/geocoder/topics/quick-start-geocode.html
        self.here_app_url = "https://geocoder.cit.api.here.com/6.2"
        self.here_app_url += "/geocode.json"

        self.here_app_id = ''
        self.here_app_code = ''

        try:
            self.here_app_id = cgi.escape(os.environ['HERE_APP_ID'])
            self.here_app_code = cgi.escape(os.environ['HERE_APP_CODE'])
        except Exception as e:
            here_service_error = ("Error: Could not enable Here service, "
                                  "no HERE_APP_ID/HERE_APP_CODE set in environment.")

            raise RuntimeError(here_service_error)

    def request_url(self, address):
        print("Geocode with Here: {address}".format(address=address))

        url = self.here_app_url

        if self.here_app_id:
            url += "?app_id="
            url += self.here_app_id

        if self.here_app_code:
            url += "&app_code="
            url += self.here_app_code

        url += "&searchtext="

        address_values = address.values()
        address_values = ' '.join([str(attribute)
                                  for attribute in address_values])

        # Here expects address attributes separated by +.
        address_values = re.sub(r' ', '+', address_values)

        url += urllib.quote(address_values)

        return url

    def response(self, data):
        print("Response data: {data}".format(data=data))

        response = []

        for result in data['results']['View']['Result']:
            geometry_location = result['Location']['NavigationPosition']
            lat_lng = { "lat": geometry_location['Latitude'],
                        "lng": geometry_location['Longitude'] }

            response.append(lat_lng.copy())

        print(response)
        return response
