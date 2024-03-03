import pytest
import math
from iss_tracker import (
        time_range,
        find_closest_epoch,
        average_speed,
        compute_speed
)

def test_time_range():
        # Test case where start and end are same
        start = "2024-047T12:08:00.000Z"
        end = "2024-047T12:08:00.000Z"
        expected_start = "02/16/2024"
        expected_end = "02/16/2024"
        expected_range = 0
        start_date, end_date, range_val = time_range(start, end)
        assert start_date == expected_start
        assert end_date == expected_end
        assert range_val == expected_range

        # Test case where start and end are different
        start = "2024-047T12:08:00.000Z"
        end = "2024-057T12:08:00.000Z"
        expected_start = "02/16/2024"
        expected_end = "02/26/2024"
        expected_range = 10
        start_date, end_date, range_val = time_range(start, end)
        assert start_date == expected_start
        assert end_date == expected_end
        assert range_val == expected_range

def test_find_closest_epoch():
        data = [
            {'EPOCH': '2024-047T12:08:00.000Z'},
            {'EPOCH': '2024-147T12:08:00.000Z'},
            {'EPOCH': '2024-247T12:08:00.000Z'}
        ]
        closest_epoch = find_closest_epoch(data)
        
        # Check if the result is a dictionary
        assert isinstance(closest_epoch, dict)

        # AS OF 02/19/2024
        assert closest_epoch['EPOCH'] == '2024-047T12:08:00.000Z'

def test_average_speed():
        data = [
            {'X_DOT': {'#text': '1'}, 'Y_DOT': {'#text': '1'}, 'Z_DOT': {'#text': '1'}},
            {'X_DOT': {'#text': '2'}, 'Y_DOT': {'#text': '2'}, 'Z_DOT': {'#text': '2'}},
            {'X_DOT': {'#text': '3'}, 'Y_DOT': {'#text': '3'}, 'Z_DOT': {'#text': '3'}}
        ]
        expected_average_speed = math.sqrt(1**2 + 1**2 + 1**2) + math.sqrt(2**2 + 2**2 + 2**2) + math.sqrt(3**2 + 3**2 + 3**2)
        expected_average_speed /= len(data)
        
        # Calculate the average speed using the function
        avg_speed = average_speed(data)

        # Check if the average speed is calculated correctly
        assert avg_speed == expected_average_speed

def test_compute_speed():

        expected_speed = math.sqrt(1**2 + 2**2 + 3**2)
        
        # Calculate the speed using the function
        speed = compute_speed(1, 2, 3)

        # Check if the speed is calculated correctly
        assert expected_speed == speed
