# Web service initializer / headers / listen and client handler inspired by:
# https://gist.github.com/joncardasis/cc67cfb160fa61a0457d6951eff2aeae

from address_cleaner import AddressCleaner
from geocoder import Geocoder

import socket
import signal  # Allow socket destruction on Ctrl+C
import sys
import time
import threading
import argparse
import json
import textwrap

class GeocodeService(object):
    def __init__(self, host, port):
        if not host:
            self.host = socket.gethostname().split('.')[0]
        else:
            self.host = host

        self.port = port

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
            print("Received connection from {addr}".format(addr=address))
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

                address_cleaner = AddressCleaner(query_string_data=data_split[1])
                address = address_cleaner.clean()

                geocoder = Geocoder(address=address)
                geocode_response = geocoder.request()

                http_code = 200

                if 'error' in geocode_response[0]:
                    http_code = 403

                response_header = self._generate_headers(http_code)

                response = response_header.encode()

                response += json.dumps(geocode_response)

                client.send(response)
                client.close()
                break

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
    geocoder_service = GeocodeService(host=args.host, port=args.port)
    geocoder_service.start()
else:
    print("Port should be above 1000, you specified {args.port}".format(
        method=args.port))
