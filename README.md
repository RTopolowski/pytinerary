# Pytinerary

!!! WORK IN PROGRESS !!!

A simple and fast timetable-based journey planner module.

## Overview

The primary function is to take a given timetable, process it into an iterable list of connections, and then generate itineraries based on a given set of criteria, such as departure or arrival time, via/avoid locations, mode preference/avoidance etc. The primary use case for this module is for public transport journey planners, but there are probably other uses to which this could be applied - this is a Python implementation of the [Connection Scan Algorithm](https://i11www.iti.kit.edu/extra/publications/dpsw-isftr-13.pdf).

## Requirements

The only requirement as of now is to use a supported version of Python, which at present is 3.10 and above. **3.9 and below are not supported** and will return a TypeError due to the way in which type definitions are handled.

## Example

The below example is a minimum set up example to get it working. Docstrings are provided for function/class parameters. "uid" is the unique identifier for a service.

```python
import datetime
import pytinerary

# This would be where you import your timetable - you'll probably be accessing it from a database rather than storing it here, but for the purposes of this example the timetable is a simple list.
timetable_data = [
    {
        "uid": "1",
        "locations": [
            {
                "dep_time": "2023-09-01 00:01:00",
                "location": "A"
            },
            {
                "arr_time": "2023-09-01 00:10:00",
                "dep_time": "2023-09-01 00:11:00",
                "location": "B"
            },
            {
                "arr_time": "2023-09-01 00:20:00",
                "location": "C"
            }
        ]
    },
    {
        "uid": "2",
        "locations": [
            {
                "dep_time": "2023-09-01 00:10:00",
                "location": "A"
            },
            {
                "arr_time": "2023-09-01 00:15:00",
                "location": "C"
            }
        ]
    },
    {
        "uid": "3",
        "locations": [
            {
                "dep_time": "2023-09-01 00:05:00",
                "location": "A"
            },
            {
                "arr_time": "2023-09-01 00:14:00",
                "location": "B"
            }
        ]
    },
    {
        "uid": "4",
        "locations": [
            {
                "dep_time": "2023-09-01 00:22:00",
                "location": "B"
            },
            {
                "arr_time": "2023-09-01 00:30:00",
                "location": "C"
            }
        ]
    }
]

# A list of stations is also needed.
locations = {
    "A": pytinerary.Location("A", "Location A", 0),
    "B": pytinerary.Location("B", "Location B", 0),
    "C": pytinerary.Location("C", "Location C", 0),
}

timetable = pytinerary.Timetable()
schema = pytinerary.TimetableSchema(
    "uid", "dep_time", "arr_time", "location", "%Y-%m-%d %H:%M:%S", "locations"
)
timetable.parse_list(timetable_data, schema)

# Now that the timetable is loaded in the data format necessary, create an instance of the ItineraryEngine and start generating itineraries!
journey_planner = pytinerary.ItineraryEngine(timetable, locations)

# Simplest itinerary - generate one route based on a departure location, arrival location and departure time.
# This route should suggest a direct itinerary using the service with the UID "2".
itinerary_one = journey_planner.generate_itinerary(self.locations["A"], self.locations["C"], datetime.datetime(2023, 9, 1, 0, 0))
```

## Documentation

Most (if not all) functions and classes have docstrings provided. "Full" documentation is not yet available.

## License

This repository is licensed under the GNU Lesser General Public License v2.1 (GNU LGPLv2.1)
