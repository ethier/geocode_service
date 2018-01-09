# Here response:
{"Response": {
    "MetaInfo": {"Timestamp": "2016-11-02T13:24:11.575+0000"},
    "View": [{
        "_type": "SearchResultsViewType",
        "ViewId": 0,
        "Result": [{
            "Relevance": 1,
            "MatchLevel": "houseNumber",
            "MatchQuality": {
                "City": 1,
                "Street": [0.9],
                "HouseNumber": 1
            },
            "MatchType": "pointAddress",
            "Location": {
                "LocationId": "NT_Opil2LPZVRLZjlWNLJQuWB_0ITN",
                "LocationType": "point",
                "DisplayPosition": {
                    "Latitude": 41.88432,
                    "Longitude": -87.6387699
                },
                "NavigationPosition": [{
                    "Latitude": 41.88449,
                    "Longitude": -87.6387699
                }],
                "MapView": {
                    "TopLeft": {
                        "Latitude": 41.8854442,
                        "Longitude": -87.6402799
                    },
                    "BottomRight": {
                        "Latitude": 41.8831958,
                        "Longitude": -87.6372599
                    }
                },
                "Address": {
                    "Label": "425 W Randolph St, Chicago, IL 60606, United States",
                    "Country": "USA",
                    "State": "IL",
                    "County": "Cook",
                    "City": "Chicago",
                    "District": "West Loop",
                    "Street": "W Randolph St",
                    "HouseNumber": "425",
                    "PostalCode": "60606",
                    "AdditionalData": [
                        {
                            "value": "United States",
                            "key": "CountryName"
                        },
                        {
                            "value": "Illinois",
                            "key": "StateName"
                        },
                        {
                            "value": "Cook",
                            "key": "CountyName"
                        },
                        {
                            "value": "N",
                            "key": "PostalCodeType"
                        }
                    ]
                }
            }
        }]
    }]
}}

# Google response:
{ "Response": {
    "results": [
        {
            "address_components": [
                {
                    "long_name": "2247",
                    "short_name": "2247",
                    "types": ["street_number"]
                },
                {
                    "long_name": "Rembrandt Road",
                    "short_name": "Rembrandt Rd",
                    "types": ["route"]
                },
                {
                    "long_name": "Whitehaven - Queensway Terrace North",
                    "short_name": "Whitehaven - Queensway Terrace North",
                    "types": ["neighborhood", "political"]
                },
                {
                    "long_name": "Ottawa",
                    "short_name": "Ottawa",
                    "types": ["locality", "political"]
                },
                {
                    "long_name": "Ottawa Division",
                    "short_name": "Ottawa Division",
                    "types": ["administrative_area_level_2", "political"]
                },
                {
                    "long_name": "Ontario",
                    "short_name": "ON",
                    "types": ["administrative_area_level_1", "political"]
                },
                {
                    "long_name": "Canada",
                    "short_name": "CA",
                    "types": ["country", "political"]
                },
                {
                    "long_name": "K2B 7P8",
                    "short_name": "K2B 7P8",
                    "types": ["postal_code"]
                }
            ],
            "formatted_address": "2247 Rembrandt Rd, Ottawa, ON K2B 7P8, Canada",
            "geometry": {
                "bounds": {
                    "northeast": {
                        "lat": 45.3630046,
                        "lng": -75.7701526
                    },
                    "southwest": {
                        "lat": 45.3628831,
                        "lng": -75.77036149999999
                    }
                },
                "location": {
                    "lat": 45.3629439,
                    "lng": -75.77025709999999
                },
                "location_type": "ROOFTOP",
                "viewport": {
                    "northeast": {
                        "lat": 45.3642928302915,
                        "lng": -75.7689080697085
                    },
                    "southwest": {
                        "lat": 45.3615948697085,
                        "lng": -75.77160603029151
                    }
                }
            },
            "partial_match": true,
            "place_id": "ChIJ1-3fj9EGzkwRAl5-P2frMUE",
            "types": ["premise"]
        }
    ],
    "status": "OK"
}}
