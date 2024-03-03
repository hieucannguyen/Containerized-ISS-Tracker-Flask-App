# Containerized-ISS-Tracker-Flask-App
This project uses real time ISS trajectory data to build a containerized Flask app for users to interact with.

**Will finish by 3/5**

Must have [Docker](https://docs.docker.com/get-docker/) installed on your system.

## ISS Data Overview
The [ISS Trajectory Data website](https://spotthestation.nasa.gov/trajectory_data.cfm) provides access to data available in both plain text and XML formats. These datasets contain ISS state vectors spanning a 15-day period. State vectors include Cartesian vectors for position {X, Y, Z} and velocity {X_DOT, Y_DOT, Z_DOT}, along with timestamps (EPOCH), describing the complete state of the ISS relative to Earth, based on the J2000 reference frame.

## File Descriptions
~~~
Containerized-ISS-Tracker-Flask-App
 ┣ app.py
 ┣ docker-compose.yml
 ┣ Dockerfile
 ┣ iss_tracker.py
 ┣ README.md
 ┣ requirements.txt
 ┣ software_diagram.svg
 ┗ test_iss_tracker.py
~~~

- [Dockerfile](Dockerfile) Dockerfile to generate docker image of our application
- [docker-compose.yml](docker-compose.yml) docker-compose file to run the containerized Flask application
- [requirements.txt](requirements.txt) required dependencies for the project
- [iss_tracker.py](iss_tracker.py) Script to process the ISS dataset
- [test_iss_tracker.py](test_iss_tracker.py) Unit tests for ISS data processing
- [app.py](app.py) Flask application for API endpoints

## Software Diagram
![image](software_diagram.svg)

*Software diagram of the Flask Application. Visualization of the application workflow using Docker and how to API endpoints interact between the code and web server.*

## Docker: Build the image
Navigate into the directory where our app, Dockerfile, and docker-compose.yml are located.

Run 
~~~
$ docker build -t username/iss_tracker_app:1.0 .
~~~

## Docker: Run Flask Application Container
Using the [docker-compose.yml](docker-compose.yml) file we can run it to start the Flask application container
~~~
$ docker-compose up -d
~~~
**Note:** -d starts the application in the background

Since we mapped to port 5000 in the [docker-compose.yml](docker-compose.yml) to interact with the Flask microservices we can use `curl`

To stop the container use
~~~
$ docker-compose down
~~~
## API Endpoints

### `/epochs`
- METHOD: GET
- Returns the entire data set of epochs.

Example output `$ curl localhost:5000/epochs`:
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
### `/now`
- METHOD: GET
- Returns state vectors and instantaneous speed for the epoch that is nearest in time.

Example output `$ curl localhost:5000/now`:
~~~
{
  "EPOCH": "2024-057T19:38:32.672Z",
  "Speed (km/s)": 7.66218133024622,
  ...
}
~~~
## Run unit tests
In the working directory run
~~~
$ pytest
~~~
