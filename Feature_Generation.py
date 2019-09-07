import pandas as pd
import random
from math import sin, cos, sqrt, atan2, radians
import sys


def calculate_distance_to_next_stop(train_data,bus_stop_data):
    # approximate radius of earth in km
    R = 6373.0
    min_distance=sys.maxsize
    for index,row in train_data.iterrows():
        lat1 = radians(row['Stop Latitude'])
        lon1 = radians(row['Stop Longitude'])
        lat2 = radians(bus_stop_data['Stop Latitude'])
        lon2 = radians(bus_stop_data['Stop Longitude'])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        if distance!=0 and distance<min_distance:
            min_distance=distance
    
    return min_distance

def calculate_distance_from_suburb_center(suburb_data,bus_stop_data):
    # approximate radius of earth in km
    R = 6373.0
    min_distance=sys.maxsize
    lat1 = radians(suburb_data['latitude'])
    lon1 = radians(suburb_data['longitude'])
    lat2 = radians(bus_stop_data['Stop Latitude'])
    lon2 = radians(bus_stop_data['Stop Longitude'])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    if distance!=0 and distance<min_distance:
        min_distance=distance
    
    return min_distance

def select_bus_stops(data):
    final_bus_stops=[]
    df=data.groupby(['Suburb'])
    for name,group in df:
        if len(group)>3:
            for i in range(0,3):
                final_bus_stops.append(list(group.iloc[i,:].values))


    final_df=pd.DataFrame(final_bus_stops,columns=['Stop ID','Stop Latitude','Stop Longitude','Stop Name','Suburb','Location'])
    return final_df


data=pd.read_csv('Bus_Stops.csv')
final_df=select_bus_stops(data)
print(final_df.head())
min_distance_stop=[]
for index,row in final_df.iterrows():
    min_distance_stop.append(calculate_distance_to_next_stop(data,row))

final_df['distance_next_stop']=pd.Series(min_distance_stop)
print(final_df.head())

suburb_desc=pd.read_csv('suburb_desc.csv')
print(suburb_desc['input_string'].values)
distance_from_suburb_center=list()
for index,row in final_df.iterrows():
    if row['Suburb'] in suburb_desc['input_string'].values:
        suburb_data=suburb_desc.loc[suburb_desc['input_string']==row['Suburb']]
        distance_from_suburb_center.append(calculate_distance_from_suburb_center(suburb_data,row))
    else:
        distance_from_suburb_center.append(0)

final_df['distance_suburb_center']=pd.Series(distance_from_suburb_center)
print(final_df.head())
final_df.to_csv('bus_stop_data.csv',encoding='utf-8')

