from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pandas as pd
import numpy as np

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


def get_suburb(lat, lng):
    sub = ''
    geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}'.format(lat, lng)
    if API_KEY is not None:
        geocode_url = geocode_url + "&key={}".format(API_KEY)
    results = requests.get(geocode_url)
    results = results.json()
    sub = results['results'][0]['address_components'][2]['short_name']
    return sub


def calculate_distance_to_next_stop(train_data, bus_stop_data):
    # approximate radius of earth in km
    R = 6373.0
    min_distance = sys.maxsize
    for index, row in train_data.iterrows():
        lat1 = radians(row['Stop Latitude'])
        lon1 = radians(row['Stop Longitude'])
        lat2 = radians(bus_stop_data['Stop Latitude'])
        lon2 = radians(bus_stop_data['Stop Longitude'])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        if distance != 0 and distance < min_distance:
            min_distance = distance

    return min_distance


def calculate_distance_from_suburb_center(suburb_data, bus_stop_data):
    # approximate radius of earth in km
    R = 6373.0
    min_distance = sys.maxsize
    lat1 = radians(suburb_data['latitude'])
    lon1 = radians(suburb_data['longitude'])
    lat2 = radians(bus_stop_data['Stop Latitude'])
    lon2 = radians(bus_stop_data['Stop Longitude'])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    if distance != 0 and distance < min_distance:
        min_distance = distance

    return min_distance


file_path = '../Data/bus_stop_data.csv'
df = pd.read_csv(file_path)

print(df.loc[1, :])
print(df.loc[318, :])
busstop_data_path = '../Data/Bus_Stops.csv'
busstop_df = pd.read_csv(busstop_data_path)

dist_next_stop = []

for index, row in df.iterrows():
    dist_next_stop.append(calculate_distance_to_next_stop(df, row))
print(dist_next_stop[0])

df['distance_next_stop'] = pd.Series(dist_next_stop)
print(df.loc[1, :])
print(df.loc[318, :])

suburb_data_path = '../Data/suburb_desc.csv'
suburb_desc = pd.read_csv(suburb_data_path)

dist_suburb_center = []
for index, row in df.iterrows():
    if row['Suburb'] in suburb_desc['input_string'].values:
        suburb_data = suburb_desc.loc[suburb_desc['input_string'] == row['Suburb']]
        dist_suburb_center.append(calculate_distance_from_suburb_center(suburb_data,row))
    else:
        dist_suburb_center.append(0)

df['distance_suburb_center'] = pd.Series(dist_suburb_center)
print(df.loc[1, :])
print(df.loc[318, :])
# df.to_csv('../Data/bus_stop_data_v2.csv' , encoding='utf-8')


