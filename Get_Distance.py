import pandas as pd
import requests
import time
import json
import sys
from math import sin, cos, sqrt, atan2, radians
from apiclient import discovery

# ------------------ CONFIGURATION -------------------------------
# Put credential keys in the string format
API_KEY = None
R = 6373.0

# ----------------------------------------------------------------

busstop_data_path = './Data/Bus_Stops.csv'
busstop_df = pd.read_csv(busstop_data_path)

suburb_data_path = './Data/suburb_desc.csv'
suburb_df = pd.read_csv(suburb_data_path)


def get_suburb(lat, lng):
    sub = ''
    geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}'.format(lat, lng)
    if API_KEY is not None:
        geocode_url = geocode_url + "&key={}".format(API_KEY)
    results = requests.get(geocode_url)
    results = results.json()
    sub = results['results'][0]['address_components'][2]['short_name']
    return sub


def get_distance_next_stop(lat, lng, busstop_df):
    min_distance = sys.maxsize
    for index, row in busstop_df.iterrows():
        lat = radians(lat)
        lng = radians(lng)
        lat1 = radians(row['Stop Latitude'])
        lng1 = radians(row['Stop Longitude'])

        dlat = lat1 - lat
        dlon = lng1 - lng

        a = sin(dlat / 2) ** 2 + cos(lat) * cos(lat1) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        if distance != 0 and distance < min_distance:
            min_distance = distance
            
    return min_distance


def get_distance_suburb_centre(lat, lng):
    min_distance = sys.maxsize

    dlat = lat - lat
    dlon = lng - lng
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    if distance != 0 and distance < min_distance:
        min_distance = distance
    return min_distance


# Test to get suburb information
# test_lat = -35.418312
# test_lng = 149.11557
#
# y = get_distance_next_stop(test_lat, test_lng,busstop_df)
# print(busstop_df.head())
# print(y)




