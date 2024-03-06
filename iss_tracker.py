#!/usr/bin/env python3

import requests
import xmltodict
import datetime
import math
from typing import List
import math
from geopy.geocoders import Nominatim

# add logging
import argparse
import logging
import socket

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--loglevel', type=str, required=False, default='WARNING',
                    help='set log level to DEBUG, INFO, WARNING, ERROR, or CRITICAL')
args = parser.parse_args()

format_str=f'[%(asctime)s {socket.gethostname()}] %(filename)s:%(funcName)s:%(lineno)s - %(levelname)s: %(message)s'
logging.basicConfig(level=args.loglevel, format=format_str)

def get_data() -> List[dict]:
    """
        Returns ISS Trajectory dataset

        Returns:
            ISS Trajectory dataset
    """
    try:
        response = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
        iss_data = xmltodict.parse(response.content)
    except:
        return "ISS data is unavailable right now. Try again later."
    return iss_data

def time_range(start: str, end: str):
    """
        Given two date times from iss data, format it and compute range between dates

        Args:
            start (string): first time entry
            end (string): last time entry

        Returns:
            start (string): formatted start date
            end (string): formatted end date
            range (int): amount of days from start to end
    """

    # use slicing to extract date time numbers to datetime format
    range = int(end[5:8]) - int(start[5:8])
    start = datetime.datetime(int(start[0:4]), 1, 1) + datetime.timedelta(int(start[5:8]) - 1)
    end = datetime.datetime(int(end[0:4]), 1, 1) + datetime.timedelta(int(end[5:8]) - 1)

    return start.strftime('%m/%d/%Y'), end.strftime('%m/%d/%Y'), range

def to_datetime(epoch: dict):
    return datetime.datetime(int(epoch['EPOCH'][0:4]), 1, 1) + datetime.timedelta(int(epoch['EPOCH'][5:8]) - 1, \
                                        hours=int(epoch['EPOCH'][9:11]), \
                                        minutes=int(epoch['EPOCH'][12:14]),\
                                        seconds=float(epoch['EPOCH'][15:21]))

def find_closest_epoch(data: List[dict]) -> dict:
    """
        Finds the closest epoch to the current date time

        Args:
            data (List[dict]): iss data set

        Returns:
            closest_epoch (dict): dictionary of the closest epoch
    """

    # initialize current datetime
    now = datetime.datetime.utcnow()
    # set first epoch as closest
    closest_date = to_datetime(data[0])
    closest_time_difference = abs((now - closest_date).total_seconds()) # time difference in seconds
    closest_epoch = data[0]

    # loop through every epoch to find the closest one to current date time
    for epoch in data:
        new_date = to_datetime(epoch)
        
        new_time_difference = abs((now - new_date).total_seconds())
        if new_time_difference < 0:
            logging.warning('negative time, NOT wanted')

        if new_time_difference < closest_time_difference:
            closest_date = new_date
            closest_time_difference = new_time_difference
            logging.debug(f'Closest date: {closest_date}, time-diff: {closest_time_difference}s')
            closest_epoch = epoch

    return closest_epoch

def compute_speed(x: float, y: float, z: float) -> float:
    """
        Computes instantaneous speed

        Args:
            x (float): x component of velocity vector
            y (float): y component of velocity vector
            z (float): z component of velocity vector

        Returns:
            instantaneous speed
    """
    return math.sqrt(x**2 + y**2 + z**2)

def convert_to_lat_lon_alt(epoch: dict):
    date = to_datetime(epoch)
    x = float(epoch["X"]["#text"])
    y = float(epoch["Y"]["#text"])
    z = float(epoch["Z"]["#text"])
    lat = math.degrees(math.atan2(z, math.sqrt(x**2 + y**2)))
    alt = math.sqrt(x**2 + y**2 + z**2) - 6371.0088 
    lon = math.degrees(math.atan2(y, x)) - ((date.hour-12)+(date.minute/60))*(360/24) + 19
    if lon > 180: 
        lon = -180 + (lon - 180)
    if lon < -180: 
        lon = 180 + (lon + 180)
    return lat, lon, alt

def get_geolocation(coordinates: str):
    geolocator = Nominatim(user_agent="iss_tracker_app")
    location = geolocator.reverse(coordinates, zoom=15, language='en')
    if location is None:
        return "Over the ocean"
    return location
