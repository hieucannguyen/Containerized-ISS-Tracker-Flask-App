from flask import Flask, request
from iss_tracker import get_data, find_closest_epoch, compute_speed, to_datetime, convert_to_lat_lon_alt, get_geolocation
import datetime

app = Flask(__name__)

@app.route("/comment", methods=["GET"])
def get_comment():
    try:
        data = get_data()['ndm']['oem']['body']['segment']['data']['COMMENT']
    except KeyError:
        return "ISS data unavailable right now. Try again later"
    return data

@app.route("/header", methods=["GET"])
def get_header():
    try:
        data = get_data()['ndm']['oem']['header']
    except KeyError:
        return "ISS data unavailable right now. Try again later"
    return data

@app.route("/metadata", methods=["GET"])
def get_metadata():
    try:
        data = get_data()['ndm']['oem']['body']['segment']['metadata']
    except KeyError:
        return "ISS data unavailable right now. Try again later"
    return data

@app.route("/epochs", methods=["GET"])
def get_epochs():
    """
        Route to return entire ISS dataset

        Query parameters:
            limit (int): limit amount of epochs
            offset (int): offset the epochs
    """
    try:
        data = get_data()['ndm']['oem']['body']['segment']['data']['stateVector']
    except KeyError:
        return "ISS data unavailable right now. Try again later"

    try:
        offset = int(request.args.get("offset", 0))
        if offset<0:
            raise ValueError
        limit = int(request.args.get("limit", len(data)-offset))
        if limit<0:
            raise ValueError
    except ValueError:
        return "Invalid limit or offset parameter; must be a positive integer."

    if limit or offset:
        result = []
        for i in range(limit):
            if offset+i>len(data)-1:
                return result
            result.append(data[offset + i])
        return result

    return data

@app.route("/epochs/<epoch>", methods=["GET"])
def get_specific_epoch(epoch):
    """
        Route to return a specific epoch in the ISS dataset

        Args:
            epoch (string): specific timestamp of the epoch
    """
    try:
        data = get_data()['ndm']['oem']['body']['segment']['data']['stateVector']
    except KeyError:
        return "ISS data unavailable right now. Try again later"
    for item in data:
        if item["EPOCH"] == epoch:
            return item

    return "Epoch not found."

@app.route("/epochs/<epoch>/speed", methods=["GET"])
def get_specific_epoch_speed(epoch):
    """
        Route to return a specific epoch's speed in the ISS dataset

        Args:
            epoch (string): specific timestamp of the epoch
    """
    try:
        data = get_data()['ndm']['oem']['body']['segment']['data']['stateVector']
    except KeyError:
        return "ISS data unavailable right now. Try again later"
    for item in data:
        if item["EPOCH"] == epoch:
            return {
                "EPOCH": item["EPOCH"],
                "Speed (km/s)": compute_speed(
                    float(item["X_DOT"]["#text"]),
                    float(item["Y_DOT"]["#text"]),
                    float(item["Z_DOT"]["#text"]),
                ),
            }

    return "Epoch not found."

@app.route("/epochs/<epoch>/location", methods=["GET"])
def get_specific_epoch_location(epoch):
    """
        Route to return a specific epoch's speed in the ISS dataset

        Args:
            epoch (string): specific timestamp of the epoch
    """
    try:
        data = get_data()['ndm']['oem']['body']['segment']['data']['stateVector']
    except KeyError:
        return "ISS data unavailable right now. Try again later"
    for item in data:
        if item["EPOCH"] == epoch:
            return {
                "EPOCH": item["EPOCH"],
                "Speed (km/s)": compute_speed(
                    float(item["X_DOT"]["#text"]),
                    float(item["Y_DOT"]["#text"]),
                    float(item["Z_DOT"]["#text"]),
                ),
            }

    return "Epoch not found."

@app.route("/now", methods=["GET"])
def get_current_epoch():
    """
        Route to return the closest epoch to the current time along with its speed in the ISS dataset

    """
    try:
        data = get_data()['ndm']['oem']['body']['segment']['data']['stateVector']
    except KeyError:
        return "ISS data unavailable right now. Try again later"
    current_epoch = find_closest_epoch(data)
    curr_speed = compute_speed(
        float(current_epoch["X_DOT"]["#text"]),
        float(current_epoch["Y_DOT"]["#text"]),
        float(current_epoch["Z_DOT"]["#text"]),
    )
    latitude, longitude, altitude = convert_to_lat_lon_alt(current_epoch)
    coodinates = f'{latitude}, {longitude}'
    location = get_geolocation(coodinates)
    return {
        "epoch_timestamp (GMT)": str(to_datetime(current_epoch)),
        "now_timestamp (GMT)": str(datetime.datetime.utcnow()),
        "speed (km/s)": curr_speed,
        "latitude": latitude,
        "longitude": longitude,
        "altitude": altitude,
        "geolocation": location
    }

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
