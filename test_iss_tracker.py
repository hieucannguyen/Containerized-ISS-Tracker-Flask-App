import pytest
import math
import datetime
from iss_tracker import (
        find_closest_epoch,
        compute_speed,
        convert_to_lat_lon_alt,
        to_datetime,
        get_geolocation
)

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


def test_compute_speed():

        expected_speed = math.sqrt(1**2 + 2**2 + 3**2)
        
        # Calculate the speed using the function
        speed = compute_speed(1, 2, 3)

        # Check if the speed is calculated correctly
        assert expected_speed == speed

def test_convert_to_lat_lon_alt():
    # Example epoch data
    epoch = {
        "EPOCH": "2024-075T23:01:00.000Z",
        "X": {"#text": "1000"},
        "Y": {"#text": "1000"},
        "Z": {"#text": "1000"}
    }

    # Expected output
    expected_lat = 35.264389682754654
    expected_lon = -101.25
    expected_alt = math.sqrt(3*(1000**2)) - 6371.0088

    # Call the function
    lat, lon, alt = convert_to_lat_lon_alt(epoch)
    assert expected_lat == lat
    assert expected_lon ==  lon
    assert expected_alt == alt

def test_to_datetime():
    # Example epoch data
    epoch = {
        "EPOCH": "2024-075T23:01:00.000Z"
    }

    # Expected output
    expected_datetime = datetime.datetime(2024, 3, 15, 23, 1, 0)

    # Call the function
    result_datetime = to_datetime(epoch)

    assert result_datetime == expected_datetime

def test_get_geolocation():
    # Example coordinates
    coordinates = "40.73061, -73.935242"

    result_location = get_geolocation(coordinates)
    print(result_location)
    assert result_location == "New York, USA"