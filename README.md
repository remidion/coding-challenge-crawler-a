# Objective
 
Write a crawler for National Express that can extract:
* list of stops
* list of departures

## Step 1: get stops

This process is done once to create a mapping between National Express stops and existing stops, if possible.

From this [page](http://coach.nationalexpress.com/nxbooking/stop-finder), get the list of all bus stops including the
address, latitude and longitude.  The output should be stored in a `stops.json` file and the schema should be something
like this:

```json
[
  {
    "stop_name": "Dundee, Scotland",
    "stop_location":"Seagate Dundee, Seagate Bus Station, Tayside Scotland",
    "lat":56.46338,
    "long":-2.9657300000000077
  }
]
```

The step should be invoked like so

```sh
python run.py --extract stops --output stops.json
```

## Step 2: get departures

This process is done repeatedly to update our database of departure.  As an input, this function should accept an origin,
 destination and a range of dates for which departures will be returned.

1. Go to this [page](http://www.nationalexpress.com/)
1. Use the normal view or accessible view from the 'choose your journey' box to get a list of departures for each
origin-destination pair of stops obtained in step 1.
1. For each departure extract the following information:

* origin_stop
* destination_stop
* departure time
* arrival time
* duration
* adult one-way price

The output should be stored in departures.json

The step should be invoked like so

```sh
python run.py --extract departures --output departures.json --startdate 2013-11-13 --enddate 2013-11-20
```


# Non-functional requirements

* the code should be written in Python and compatible with Python 2.7.
* the code should be hosted on github, and the repo should be shared with Busbud
* the code should be written in a way that it can easily be extended to become a scheduled process that updates our
database of departure
* any packages required must be installable via `pip install -r requirements.txt`, see [pip](http://www.pip-installer.org/en/latest/)
