import urlparse
import collections
import re
import cgi

class AddressCleaner(object):
    def __init__(self, query_string_data):
        self.query_string_data = query_string_data

    def clean(self):
        query_string_data = self.query_string_data

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
