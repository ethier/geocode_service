# https://gist.github.com/joncardasis/cc67cfb160fa61a0457d6951eff2aeae

import socket
import signal  # Allow socket destruction on Ctrl+C
import sys
import time
import threading
import argparse
import urlparse
import cgi
import re
import os
import json
import urllib
import urllib2
import collections
import textwrap

class GeocodingService(object):
    def __init__(self, host, port):
        if not host:
            self.host = socket.gethostname().split('.')[0]
        else:
            self.host = host

        self.port = port

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

            print(here_service_error)

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

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            print("Starting server on {host}:{port}".format(
                host=self.host, port=self.port))
            self.socket.bind((self.host, self.port))
            print("Server started on port {port}.".format(port=self.port))

        except Exception as e:
            print("Error: Could not bind to port {port}".format(
                port=self.port))
            self.shutdown()
            sys.exit(1)

        self._listen()

    def shutdown(self):
        try:
            print("Shutting down server")
            self.socket.shutdown(socket.SHUT_RDWR)

        except Exception as e:
            pass

    def _generate_headers(self, response_code):
        header = ''

        if response_code == 200:
            header += 'HTTP/1.1 200 OK\n'
        elif response_code == 404:
            header += 'HTTP/1.1 404 Not Found\n'

        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += 'Date: {now}\n'.format(now=time_now)
        header += 'Server: Geocode address service\n'
        header += 'Content-Type: application/json\n'
        header += 'Connection: close\n\n'

        return header

    def _listen(self):
        self.socket.listen(5)
        while True:
            (client, address) = self.socket.accept()
            client.settimeout(60)
            print("Recieved connection from {addr}".format(addr=address))
            threading.Thread(target=self._handle_client,
                             args=(client, address)).start()

    def _handle_client(self, client, address):
        PACKET_SIZE = 1024

        while True:
            print("CLIENT", client)
            data = client.recv(PACKET_SIZE).decode()

            if not data:
                break

            data_split = data.split(' ')
            request_method = data_split[0]

            if not request_method == "GET":
                print("Unknown HTTP request method: {method}".format(
                    method=request_method))
            else:
                print("Successful method used: {method}".format(
                    method=request_method))

                print("Method: {m}".format(m=request_method))
                print("Request Body: {b}".format(b=data))
                print("Data {data}".format(data=data_split))

                address = self._address(data_split[1])

                response_data = self._geocode_address(address)

                # Make HTTP error code specific to the success of the encoding.
                response_header = self._generate_headers(200)

                response = response_header.encode()

                response += json.dumps(response_data)

                client.send(response)
                client.close()
                break

    def _valid_address_keys(self):
        return ['address1', 'address2', 'city', 'state',
                'zip', 'country_code']

    def _clean_address_data(self, query_string_data):
        parsed_qs = urlparse.parse_qs(query_string_data)

        print("Parsed QS: {parsed_qs}".format(parsed_qs=parsed_qs))

        valid_address_keys = self._valid_address_keys()

        clean_address = {}

        for key, value in parsed_qs.iteritems():
            key = re.sub(r'/\?', '', key)
            key = cgi.escape(key)
            value = [cgi.escape(item) for item in value][0]

            print("Key {key}".format(key=key))
            print("Value {value}".format(value=value))

            if key in valid_address_keys:
                clean_address[key] = value

        return clean_address

    def _address(self, query_string_data):
        print("Query sting data: {query_string_data}".format(
            query_string_data=query_string_data))

        clean_address = self._clean_address_data(query_string_data)

        valid_address_keys = self._valid_address_keys()
        clean_address_keys = clean_address.keys()

        # Ensure address attribute order.
        address = collections.OrderedDict()

        for key in valid_address_keys:
            if key in clean_address_keys:
                address[key] = clean_address[key]

        return address

    def _geocode_address(self, address):
        print("Address to geocode: {address}".format(address=address))

        geocoded_address = {}

        try:
            geocoded_address = self._here(address)
        except Exception as e:
            print("Here failed. Trying Google. Exception: {e}".format(e=e))
            geocoded_address = self._google(address)

        return geocoded_address

    def _here(self, address):
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
        address_values = ' '.join([str(attribute) for attribute in address_values])

        # Here expects address attributes separated by +.
        address_values = re.sub(r' ', '+', address_values)

        url += urllib.quote(address_values)

        response = self._geocode_request(url)

        print("Response: {response}".format(response=response))

        lat_lngs = []

        for response_result in response['results']['View']['Result']:
            geometry_location = response_result['Location']['NavigationPosition']
            lat_lngs.append(
                {lat: geometry_location['Latitude'], lng: geometry_location['Longitude']})
        print(lat_lngs)
        return lat_lngs

        return response

    def _google(self, address):
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

        response = self._geocode_request(url)

        print("Response: {response}".format(response=response))

        lat_lngs = []

        for response_result in response['results']:
            geometry_location = response_result['geometry']['location']
            lat_lngs.append(
                {lat: geometry_location['lat'], lng: geometry_location['lng']})
        print(lat_lngs)
        return lat_lngs

    def _geocode_request(self, url):
        print("Geocode request URL: {url}".format(url=url))

        request = urllib2.urlopen(url)
        response = request.read()

        return response


epilog = textwrap.dedent('''\
            Geocode address service

            This service will take a GET request of an address.
            It will attempt to Geocode the address with Here first, then Google.

            Valid address query string parameters are:
            ['address1', 'address2', 'city', 'state', 'zip', 'country_code']

            Example: <url>?address1=123 Example Dr.&city=Example&state=EG&...

            Here:
            HERE_APP_ID/HERE_APP_CODE are required as enviroment variables.

            Google:
            Optionally specify a GOOGLE_APP_KEY to avoid rate limiting.''')

parser = argparse.ArgumentParser(description='Geocode address service',
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=epilog)

parser.add_argument("--port", type=int, default=8080, required=False,
    help="The port for the service to listen on.")
parser.add_argument("--host", type=str, default="", required=False,
    help="The host for the service to listen on.")

args = parser.parse_args()

if args.port > 1000:
    geocoding_service = GeocodingService(host=args.host, port=args.port)
    geocoding_service.start()
else:
    print("Port should be above 1000, you specified {args.port}".format(
        method=args.port))
