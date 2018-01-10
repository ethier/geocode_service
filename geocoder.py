from geocoders.google import Google
from geocoders.here import Here

import os
import urllib2
import json

class Geocoder(object):
    def __init__(self, address):
        self.address = address

        print("Address to geocode: {address}".format(address=self.address))

        self.geocoder = None

        try:
            self.geocoder = Here(address=address)
        except Exception as e:
            print("Here failed. Trying Google. Exception: {e}".format(e=e))
            self.geocoder = Google(address=address)

    def request(self):
        if not self.geocoder:
            raise RuntimeError('No geocoder instantiated correctly.')

        url = self.geocoder.request_url(address=self.address)

        print("Geocode request URL: {url}".format(url=url))

        response = urllib2.urlopen(url)
        data = json.load(response)

        geocoder_response = self.geocoder.response(data=data)

        return geocoder_response
