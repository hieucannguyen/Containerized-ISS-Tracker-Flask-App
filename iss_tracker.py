#!/usr/bin/env python3

import requests
import xmltodict
import datetime
import math
from typing import List

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
    response = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')
    iss_data = xmltodict.parse(response.content)
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

def find_closest_epoch(data: List[dict]) -> dict:
    """
        Finds the closest epoch to the current date time

        Args:
            data (List[dict]): iss data set

        Returns:
            closest_epoch (dict): dictionary of the closest epoch
    """

    # initialize current datetime
    now = datetime.datetime.now()
    # set first epoch as closest
    closest_date = datetime.datetime(int(data[0]['EPOCH'][0:4]), 1, 1) + datetime.timedelta(int(data[0]['EPOCH'][5:8]) - 1, \
                                    hours=int(data[0]['EPOCH'][9:11]), \
                                    minutes=int(data[0]['EPOCH'][12:14]), \
                                    seconds=float(data[0]['EPOCH'][15:21]))
    
    closest_time_difference = abs((now - closest_date).total_seconds()) # time difference in seconds
    closest_epoch = data[0]

    # loop through every epoch to find the closest one to current date time
    for epoch in data:
        new_date = datetime.datetime(int(epoch['EPOCH'][0:4]), 1, 1) + datetime.timedelta(int(epoch['EPOCH'][5:8]) - 1, \
                                        hours=int(epoch['EPOCH'][9:11]), \
                                        minutes=int(epoch['EPOCH'][12:14]),\
                                        seconds=float(epoch['EPOCH'][15:21]))
        
        new_time_difference = abs((now - new_date).total_seconds())
        if new_time_difference < 0:
            logging.warning('negative time, NOT wanted')

        if new_time_difference < closest_time_difference:
            closest_date = new_date
            closest_time_difference = new_time_difference
            logging.debug(f'Closest date: {closest_date}, time-diff: {closest_time_difference}s')
            closest_epoch = epoch

    return closest_epoch
    
def average_speed(data: List[dict]) -> float:
    """
        Compute average speed of iss

        Args:
            data (List[dict]): iss data set

        Returns:
            average_speed (float): average speed of the iss
    """

    total_speed = 0
    for epoch in data:
        # speed formula
        total_speed += math.sqrt((float(epoch['X_DOT']['#text']))**2 + \
                                 (float(epoch['Y_DOT']['#text']))**2 + \
                                 (float(epoch['Z_DOT']['#text']))**2)
        
    return total_speed/len(data)

def current_speed(data):
    closest_epoch = find_closest_epoch(data)
    logging.debug(f'Closest epoch: {closest_epoch}')
    return math.sqrt((float(closest_epoch['X_DOT']['#text']))**2 + \
                     (float(closest_epoch['Y_DOT']['#text']))**2 + \
                     (float(closest_epoch['Z_DOT']['#text']))**2)

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

def main():
    response = requests.get(url='https://nasa-public-data.s3.amazonaws.com/iss-coords/current/ISS_OEM/ISS.OEM_J2K_EPH.xml')

    iss_data = xmltodict.parse(response.content)
    iss_data = iss_data['ndm']['oem']['body']['segment']['data']['stateVector']

    start_date, end_date, range = time_range(iss_data[0]['EPOCH'], iss_data[len(iss_data)-1]['EPOCH'])

    print('ISS SUMMARY\n')
    print('DATE RANGE:')
    print(f'\t- {start_date} - {end_date}: {range} days\n')

    print('CURRENT STATUS')
    closest_epoch = find_closest_epoch(iss_data)
    closest_time = datetime.datetime(int(closest_epoch['EPOCH'][0:4]), 1, 1) + datetime.timedelta(int(closest_epoch['EPOCH'][5:8]) - 1, \
                                        hours=int(closest_epoch['EPOCH'][9:11]), \
                                        minutes=int(closest_epoch['EPOCH'][12:14]),\
                                        seconds=float(closest_epoch['EPOCH'][15:21]))
    curr_position = closest_epoch['X']['#text'] + ', '  + closest_epoch['Y']['#text'] + ', ' + closest_epoch['Z']['#text']
    curr_speed = closest_epoch['X_DOT']['#text'] + ', '  + closest_epoch['Y_DOT']['#text'] + ', ' + closest_epoch['Z_DOT']['#text']
    print(f'\t- Date/Time: {closest_time}')
    print(f'\t- Coordinates: ({curr_position}) km')
    print(f'\t- Velocity vector: ({curr_speed}) km/s')
    print(f'\t- Speed: {current_speed(iss_data)} km/s\n')

    print(f'AVERAGE SPEED: {average_speed(iss_data)} km/s')

if __name__ == '__main__':
    main()
