from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score

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


file_path = '../Data/data.csv'
df = pd.read_csv(file_path)
cols = list(['Stop Latitude','Stop Longitude','num_bus_stop', 'population_density', 'distance_next_stop',
             'distance_suburb_center', 'Label'])
df = pd.DataFrame(df,
                  columns=cols)

scaler = StandardScaler()


def scaleCols(df, cols_to_scale):
    """
    idea from
    https://stackoverflow.com/questions/24645153/pandas-dataframe-columns-scaling-with-sklearn/36475297
    params: df: Pandas dataframe, list of pandas columns to transform
    return: dataframe with normalised value for each column.
    """
    for col in cols_to_scale:
        df[col] = scaler.fit_transform(df[col].values.reshape(-1,1))
    return df


np.random.seed(3)


df_normalised = scaleCols(df, cols[2:7])
df_normalised = shuffle(df_normalised)

msk = np.random.rand(len(df_normalised)) < 0.7  # split train and test set
train_data = df_normalised[msk]
test_data = df_normalised[~msk]

n_features = train_data.shape[1] - 1

train_input = train_data.iloc[:, 2:n_features]
train_target = train_data.iloc[:, n_features]
test_input = test_data.iloc[:, 2:n_features]
test_target = test_data.iloc[:, n_features]

# print(train_input.shape)
# print(train_target.shape)

lr = LogisticRegression(solver='lbfgs')

lr.fit(train_input, train_target)

test_predict = lr.predict(test_input)

acc = accuracy_score(test_target, test_predict)

print('---------- Model Performance ----------')
print('accuracy:{}'.format(acc))

print('---------- Bus Stop Detail ----------')
print(test_data.iloc[0, :])
print('---------- Should we build a bus stop according to the model? ----------')
print(test_predict[0])






