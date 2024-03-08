# ISS-Tracker-Web-Application
This project uses real-time ISS trajectory data to build a containerized Flask app for users to interact with. Overall, the project aims to process the ISS trajectory data and allow users to easily retrieve the processed data using the API endpoints.

Must have [Docker](https://docs.docker.com/get-docker/) installed on your system.

## ISS Data Overview
The [ISS Trajectory Data website](https://spotthestation.nasa.gov/trajectory_data.cfm) provides access to data available in both plain text and XML formats. These datasets contain ISS state vectors spanning a 15-day period. State vectors include Cartesian vectors for position {X, Y, Z} and velocity {X_DOT, Y_DOT, Z_DOT}, along with timestamps (EPOCH), describing the complete state of the ISS relative to Earth, based on the J2000 reference frame.

## File Descriptions
~~~
Containerized-ISS-Tracker-Flask-App/
    ├── Dockerfile
    ├── docker-compose.yml
    ├── app.py
    ├── iss_tracker.py
    ├── test_iss_tracker.py
    ├── software_diagram.svg
    └── README.md
~~~

- [Dockerfile](Dockerfile) Dockerfile to generate a docker image of our application
- [docker-compose.yml](docker-compose.yml) docker-compose file to run the containerized Flask application
- [requirements.txt](requirements.txt) Required dependencies for the project
- [iss_tracker.py](iss_tracker.py) Scripts to process the ISS dataset
- [test_iss_tracker.py](test_iss_tracker.py) Unit tests for ISS data processing
- [app.py](app.py) Flask application for API endpoints

## Software Diagram
![image](software_diagram.svg)

*Software diagram of the Flask Application. Visualization of the containerized application using Docker and how to API endpoints interact between the code and web server.*

## Running the application using Docker
### Build the image
Navigate into the directory where our app, Dockerfile, and docker-compose.yml are located.

Run 
~~~
$ docker build -t username/iss_tracker_app:1.0 .
~~~

(Run-Flask-Application-Container)=
### Run Flask Application Container
Using the [docker-compose.yml](docker-compose.yml) file we can run it to start the Flask application container
~~~
$ docker-compose up -d
~~~
**Note:** -d starts the application in the background

Since we mapped to port 5000 in the [docker-compose.yml](docker-compose.yml) to interact with the Flask microservices we can use `curl localhost:5000/...`

To stop the container use
~~~
$ docker-compose down
~~~
## API Endpoints

### `/comment`
- METHOD: GET
- Return the ‘comment’ list object from ISS data which gives you a general summary of the ISS Trajectory data.

Example output using `$ curl localhost:5000/comment`:
~~~
[
  "Units are in kg and m^2",
  "MASS=459325.00",
  "DRAG_AREA=1487.80",
  "DRAG_COEFF=1.85",
  "SOLAR_RAD_AREA=0.00",
  "SOLAR_RAD_COEFF=0.00",
  "Orbits start at the ascending node epoch",
  "ISS first asc. node: EPOCH = 2024-03-04T12:26:27.616 $ ORBIT = 231 $ LAN(DEG) = 124.75313",
  "ISS last asc. node : EPOCH = 2024-03-19T11:33:05.982 $ ORBIT = 463 $ LAN(DEG) = 49.27177",
  "Begin sequence of events",
  "TRAJECTORY EVENT SUMMARY:",
  null,
  "|       EVENT        |       TIG        | ORB |   DV    |   HA    |   HP    |",
  "|                    |       GMT        |     |   M/S   |   KM    |   KM    |",
  "|                    |                  |     |  (F/S)  |  (NM)   |  (NM)   |",
  "=============================================================================",
  "Crew-8 Docking        065:08:00:00.000             0.0     422.5     412.8",
  "(0.0)   (228.1)   (222.9)",
  null,
  "Crew-7 Undock         071:15:00:00.000             0.0     423.8     410.2",
  "(0.0)   (228.9)   (221.5)",
  null,
  "GMT073 Reboost Preli  073:13:59:00.000             1.5     424.2     409.5",
  "(4.9)   (229.1)   (221.1)",
  null,
  "SpX-30 Launch         075:23:13:00.000             0.0     424.5     413.8",
  "(0.0)   (229.2)   (223.4)",
  null,
  "SpX-30 Docking        077:11:00:00.000             0.0     424.9     413.4",
  "(0.0)   (229.4)   (223.2)",
  null,
  "=============================================================================",
  "End sequence of events"
]
~~~
### `/header`
- METHOD: GET
- Return the ‘header’ list object from ISS data which gives you when the data was created and the organization that created it.

Example output using `$ curl localhost:5000/header`:
~~~
{
  "CREATION_DATE": "2024-064T19:05:34.727Z",
  "ORIGINATOR": "JSC"
}
~~~
### `/metadata`
- METHOD: GET
- Return the ‘metadata’ dict object from ISS data including its identification, position reference frame, temporal coverage, and the time system used for timestamping, with start and stop times in UTC format.

Example output using `$ curl localhost:5000/metadata`:
~~~
{
  "CENTER_NAME": "EARTH",
  "OBJECT_ID": "1998-067-A",
  "OBJECT_NAME": "ISS",
  "REF_FRAME": "EME2000",
  "START_TIME": "2024-064T12:00:00.000Z",
  "STOP_TIME": "2024-079T12:00:00.000Z",
  "TIME_SYSTEM": "UTC"
}
~~~
### `/epochs`
- METHOD: GET
- Returns the entire data set of epochs.

Example output using `$ curl localhost:5000/epochs`:
~~~
[
  {
    "EPOCH": "2024-052T12:00:00.000Z",
    ...
  },
  {
    "EPOCH": "2024-052T12:04:00.000Z",
    ...
  },
  ...
]
~~~
### `/epochs?limit=int&offset=int`
- METHOD: GET
- Returns a modified list of epochs based on query parameters.

Example output using `$ curl localhost:5000/epochs?limit=2&offset=1`:
~~~
[
  {
    "EPOCH": "2024-052T12:04:00.000Z",
    ...
  },
  {
    "EPOCH": "2024-052T12:08:00.000Z",
    ...
  },
]
~~~
### `/epochs/<epoch>`
- METHOD: GET
- Returns state vectors for a specific epoch from the data set.

Example output using `$ curl localhost:5000/epochs/2024-052T12:00:00.000Z`:
~~~
{
  "EPOCH": "2024-052T12:00:00.000Z",
  ...
}
~~~
### `/epochs/<epoch>/speed`
- METHOD: GET
- Returns instantaneous speed for a specific epoch in the data set.

Example output using `$ curl localhost:5000/epochs/2024-052T12:00:00.000Z/speed`:
~~~
{
  "EPOCH": "2024-052T12:00:00.000Z",
  "Speed (km/s)": 7.655330269344684
}
~~~
### `/epochs/<epoch>/location`
- METHOD: GET
- Returns latitude, longitude, altitude, and geolocation for a specific Epoch in the data set.

Example output using `$ curl localhost:5000/epochs/2024-075T23:01:00.000Z/location`:
~~~
{
  "EPOCH": "2024-075T23:01:00.000Z",
  "altitude": 426.69665337138576,
  "geolocation": "Wadh Tehsil, Khuzdar District, Qalat Division, Balochistan, 90151, Pakistan",
  "latitude": 27.42580375493891,
  "longitude": 66.80902239018769
}
~~~
### `/now`
- METHOD: GET
- Returns instantaneous speed, latitude, longitude, altitude, and geolocation for the Epoch that is nearest in time.

Example output `$ curl localhost:5000/now`:
~~~
{
  "altitude": 419.4847035370267,
  "epoch_timestamp (GMT)": "2024-03-06 04:52:00",
  "geolocation": "Eastland County, Texas, United States",
  "latitude": 32.411567298902774,
  "longitude": -98.51480751430176,
  "now_timestamp (GMT)": "2024-03-06 04:50:10.216243",
  "speed (km/s)": 7.665103951573263
}
~~~
## Run unit tests
Ensure the Flask service is running [](#Run-Flask-Application-Container)

Use pytest to run all unit tests
~~~
$ pytest
~~~
