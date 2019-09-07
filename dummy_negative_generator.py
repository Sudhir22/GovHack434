import pandas as pd
import requests
import time
import json
import sys
from math import sin, cos, sqrt, atan2, radians
from apiclient import discovery

# ------------------ CONFIGURATION -------------------------------

API_KEY = 'AIzaSyCtXVrgFImIZ_psK2XDkc0ilPJLWzOt5Wo'
R = 6373.0

# ----------------------------------------------------------------


def get_suburb(lat, lng):
    sub = ''
    geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}'.format(lat, lng)
    if API_KEY is not None:
        geocode_url = geocode_url + "&key={}".format(API_KEY)
    results = requests.get(geocode_url)
    results = results.json()
    sub = results['results'][0]['address_components'][2]['short_name']
    return sub


def get_distance_next_stop(lat1, lng1, lat2, lng2):
    min_distance = sys.maxsize
    dlat = lat2 - lat1
    dlon = lng2 - lng1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    if distance != 0 and distance < min_distance:
        min_distance = distance
    return min_distance


def get_distance_suburb_centre(lat1, lng1, lat2, lng2):
    min_distance = sys.maxsize
    dlat = lat2 - lat1
    dlon = lng2 - lng1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    if distance != 0 and distance < min_distance:
        min_distance = distance
    return min_distance


# Test to get suburb information
test_lat = -35.2713868
test_lng = 149.1292744

y = get_suburb(test_lat, test_lng)
print(y)



