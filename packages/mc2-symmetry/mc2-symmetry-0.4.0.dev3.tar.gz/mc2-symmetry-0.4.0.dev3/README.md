symmetry
========

Cluster management tool for the MC2.

Build
-----

To create a virtual environment and install the requirements, run (by default it uses `python3.7`, you can change that
in the `Makefile` variable `VENV_BIN`)

    make venv
    

Build the Docker image for local use (may need `sudo`)

    make docker-build


Run Symmetry with Docker
------------------------

Populate `etc/nodes.ini` with the information from your cluster.
The application can then be started with

    make start


And point your browser to http://localhost:5000/ui/dashboard

Stop with

    make stop

Both commands use  `docker-compose` on `docker/symmetry/docker-compose.yml`, and may need `sudo`

Run Symmetry components manually
--------------------------------

### Prerequisites

Make sure the virtualenv is activated

    source .venv/bin/activate

Symmetry publishes and reads telemetry data to and from [redis](http://redis.io),
so you need a running redis instance first:

    redis-server

### Start the telemetry deamon

Start the telemetry daemon in the activated virtualenv via

    python -m symmetry.cli.telemd

`telemd` also takes various arguments to control runtime aspects (activate the `-h` flag).
For exampe, to disable power monitoring and probe nodes every 0.5 seconds, run

    python -m symmetry.cli.telemd --power-disable --agent-interval=.5

You can verify that the telemetry daemon sends data by suscribing to the topic
via the redis CLI:

    redis-cli psubscribe "telemetry:*"


### Start the cluster deamon

Start the cluster daemon (which controls the cluster state)

    python -m symmetry.cli.clusterd


### Websocket server

To start the websocket server for the dashboard:

    python -m symmetry.cli.websocket
    
The websocket is running on port ```8082``` and automatically connects to the local redis-server on `localhost:6379`.
Connect with ```ws://ip:8082/topic``` to receive all published messages for the given ```topic```. 
    

### Run the dashboard

Serve the app with gunicorn

    gunicorn -w 4 --preload -b 0.0.0.0:5000 \
        -c symmetry/webapp/gunicorn.conf.py \
        symmetry.webapp.wsgi:api

Point your browser to http://localhost:5000/ui/dashboard.

Using Symmetry
--------------

### Creating services

To create a new service in the cluster a `POST` request must be sent to the
`api/services/{service_id}` endpoint, with `service_id` being the new service.

The `POST` request has one optional 
([tar-exported docker image](https://docs.docker.com/engine/reference/commandline/save/)) and one mandatory (service 
description) body element.

The service description is structured this way:

```yaml
%YAML 1.2
---
id: #must be same id as in endpoint
maintainer: #the uploader of the service
name: #"Pretty" version of the name
version: #any version number
description: #simple description
image_tag: #if docker image uploaded then this tag must be provided by the image. otherwise it is pulled 
port: #the port which is exposed by the service
```  

After correct execution the answer should look somewhat like this:

```json
{
    "name": "Test Service",
    "version": "1.0.0",
    "desc": "This is a simple test_service",
    "maintainer": "silvio",
    "10.0.0.3": "1"
}
```


Other Client Scripts
--------------------

### Recording telemetry data

You can use the telemetry client `cli.telemc` to consume telemetry data in
various ways.

    # prints to system out
    python -m symmetry.cli.telemc

    # writes to a csv file
    python -m symmetry.cli.telemc --file /tmp/telemetry-results.csv

### Arduino Power Meter

To sample wattage from the arduino power monitor every 0.5 seconds call:

    python -m symmetry.cli.power --interval 0.5

This will write the data into the Redis instance like the telemetry daemon.
