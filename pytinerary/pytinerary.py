"""
Pytinerary - Python library for generating itineraries from a given timetable.
@Author: Robert Topolowski
@Date: 23.08.2023
@Version: 1.0
@License: LGPL-2.1

Copyright (C) 2023 Robert Topolowski

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
USA
"""
from collections.abc import Iterable
from typing import Any, List, Callable

import datetime
import sys


class Connection(object):
    """
    Data format for holding individual connections.
    """

    def __init__(
        self,
        uid: str,
        dep_time: datetime.datetime | str,
        arr_time: datetime.datetime | str,
        dep_loc: str,
        arr_loc: str,
        datetime_format: str = "",
        other_data: dict = {},
    ) -> None:
        """
        Initialise the connection object.
        @param uid: Unique identifier of the connection.
        @param dep_time: Departure time of the connection.
        @param arr_time: Arrival time of the connection.
        @param dep_loc: Departure location identifier.
        @param arr_loc: Arrival location identifier.
        @param other_data: Other data present in the timetable for this
        connection (e.g. mode, operator, etconnection.)
        """
        self.__uid = uid
        self.__dep_time = self.__datetime_formatter(dep_time, datetime_format)
        self.__arr_time = self.__datetime_formatter(arr_time, datetime_format)
        if self.__arr_time <= self.__dep_time:
            raise ValueError("Arrival time must be after departure time")
        self.__dep_loc = dep_loc
        self.__arr_loc = arr_loc
        self.__other_data = other_data

    def __datetime_formatter(
        self, datetime_var, datetime_format: str = ""
    ) -> datetime.datetime:
        """
        Format a datetime object into a string.
        @param datetime: Datetime object to format.
        @param datetime_format: (Optional, default "") Format string to use.
        @return: Formatted datetime string.
        """
        if isinstance(datetime_var, datetime.datetime):
            return datetime_var
        else:
            if datetime_format == "":
                raise ValueError(
                    "Datetime format not provided, departure time not a datetime object"
                )
            else:
                return datetime.datetime.strptime(datetime_var, datetime_format)

    def __repr__(self) -> str:
        return f"Connection({self.__uid}, {self.__dep_loc} @ {self.__dep_time}, {self.__arr_loc} @ {self.__arr_time}, {self.__other_data})"

    def __str__(self) -> str:
        return f"Connection({self.__uid}, {self.__dep_loc} @ {self.__dep_time}, {self.__arr_loc} @ {self.__arr_time}, {self.__other_data})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Connection):
            return (
                self.__uid == other.get_uid()
                and self.__dep_time == other.get_dep_time()
                and self.__arr_time == other.get_arr_time()
                and self.__dep_loc == other.get_dep_loc()
                and self.__arr_loc == other.get_arr_loc()
                and self.__other_data == other.__other_data
            )
        else:
            raise TypeError("Cannot compare Connection with non-Connection")

    def __gt__(self, other) -> bool:
        if isinstance(other, Connection):
            return self.__dep_time > other.get_dep_time()
        else:
            raise TypeError("Cannot compare Connection with non-Connection")

    def __ge__(self, other) -> bool:
        if isinstance(other, Connection):
            return self.__dep_time >= other.get_dep_time()
        else:
            raise TypeError("Cannot compare Connection with non-Connection")

    def __lt__(self, other) -> bool:
        if isinstance(other, Connection):
            return self.__dep_time < other.get_dep_time()
        else:
            raise TypeError("Cannot compare Connection with non-Connection")

    def __le__(self, other) -> bool:
        if isinstance(other, Connection):
            return self.__dep_time <= other.get_dep_time()
        else:
            raise TypeError("Cannot compare Connection with non-Connection")

    def get_uid(self) -> str:
        """
        Get the unique identifier of the connection.
        @return: Unique identifier of the connection.
        """
        return self.__uid

    def get_dep_time(self) -> datetime.datetime:
        """
        Get the departure time of the connection.
        @return: Departure time of the connection.
        """
        return self.__dep_time

    def get_arr_time(self) -> datetime.datetime:
        """
        Get the arrival time of the connection.
        @return: Arrival time of the connection.
        """
        return self.__arr_time

    def get_dep_loc(self) -> str:
        """
        Get the departure location identifier.
        @return: Departure location identifier.
        """
        return self.__dep_loc

    def get_arr_loc(self) -> str:
        """
        Get the arrival location identifier.
        @return: Arrival location identifier.
        """
        return self.__arr_loc

    def __dict__(self) -> dict:
        return {
            "uid": self.__uid,
            "dep_time": self.__dep_time,
            "arr_time": self.__arr_time,
            "dep_loc": self.__dep_loc,
            "arr_loc": self.__arr_loc,
            **self.__other_data,
        }


class ConnectionList(object):
    """
    A memory-efficient way of storing a list of connections.
    """

    def __init__(self, connection_list: list | None = None) -> None:
        """
        Initialise the ConnectionList object.
        """
        if connection_list == None:
            self.__connection_list = []
        else:
            self.__connection_list = connection_list

    def __check_type(self, connection: Connection) -> None:
        """
        Check that the connection is of type Connection.
        @param connection: Connection to check.
        """
        if isinstance(connection, Connection) != True:
            raise TypeError("Connection must be of type Connection")

    def __len__(self) -> int:
        return len(self.__connection_list)

    def __getitem__(self, index: int) -> Connection:
        return self.__connection_list[index]

    def __setitem__(self, index: int, connection: Connection) -> None:
        if isinstance(connection, Connection) != True:
            raise TypeError("Connection must be of type Connection")
        self.__connection_list[index] = connection

    def __delitem__(self, index: int) -> None:
        del self.__connection_list[index]

    def __iter__(self):
        return self.__connection_list.__iter__()

    def __reversed__(self) -> Iterable:
        return reversed(self.__connection_list)

    def __contains__(self, connection: Connection, /) -> bool:
        return connection in self.__connection_list

    def __repr__(self) -> str:
        return f"ConnectionList({self.__connection_list})"

    def __str__(self) -> str:
        return f"ConnectionList({self.__connection_list})"

    def append(self, connection: Connection) -> None:
        """
        Append a connection to the end of the list.
        @param connection: Connection to append.
        """
        self.__check_type(connection)
        self.__connection_list.append(connection)

    def insert(self, index: int, connection: Connection) -> None:
        """
        Insert a connection at a given index.
        @param index: Index to insert the connection at.
        @param connection: Connection to insert.
        """
        self.__check_type(connection)
        self.__connection_list.insert(index, connection)

    def pop(self, index: int = -1) -> Connection:
        """
        Remove and return the connection at a given index.
        @param index: (Optional, default -1) Index to remove the connection at.
        @return: The connection at the given index.
        """
        return self.__connection_list.pop(index)

    def remove(self, connection: Connection) -> None:
        """
        Remove the first occurrence of a connection from the list.
        @param connection: Connection to remove.
        """
        self.__check_type(connection)
        self.__connection_list.remove(connection)

    def clear(self) -> None:
        """
        Remove all connections from the list.
        """
        self.__connection_list.clear()

    def index(self, connection: Connection, start: int = 0, end: int = -1) -> int:
        """
        Return the index of the first occurrence of a connection in the list.
        @param connection: Connection to find the index of.
        @param start: (Optional, default 0) Index to start searching from.
        @param end: (Optional, default -1) Index to stop searching at.
        @return: Index of the first occurrence of the connection.
        """
        self.__check_type(connection)
        return self.__connection_list.index(connection, start, end)

    def sort(self, key: Callable, reverse: bool = False) -> None:
        """
        Sort the list in place.
        @param key: (Optional, default None) Key to sort by.
        @param reverse: (Optional, default False) Whether to sort in reverse.
        """
        self.__connection_list.sort(key=key, reverse=reverse)


class TimetableSchema(object):
    """
    Class for storing the details necessary to convert a timetable from a
    dictionary to a ConnectionList of Connections.
    """

    def __init__(
        self,
        uid_key: str,
        dep_time_key: str,
        arr_time_key: str,
        loc_key: str,
        datetime_format: str = "",
        list_key: str = "",
    ) -> None:
        """
        Create a timetable schema to be used by parse_dict.
        @param uid_key: Key in the dictionary for the unique identifier of a
        given service.
        @param dep_time_key: Key in the dictionary for the departure time of the
        connection.
        @param arr_time_key: Key in the dictionary for the arrival time of the
        connection.
        @param list_key: (Optional, default empty) Key in the dictionary for the
        list of stops on a given service (i.e. a list of arrival and departure
        times). If this is not provided, it will be assumed that the list of
        stops is the root of each service (i.e. the timetable is a list of lists)
        """
        self.__uid_key = uid_key
        self.__dep_time_key = dep_time_key
        self.__arr_time_key = arr_time_key
        self.__loc_key = loc_key
        self.__datetime_format = datetime_format
        self.__list_key = list_key

    def get_uid_key(self) -> str:
        """
        Get the key for the unique identifier.
        @return: Key for the unique identifier.
        """
        return self.__uid_key

    def get_dep_time_key(self) -> str:
        """
        Get the key for the departure time.
        @return: Key for the departure time.
        """
        return self.__dep_time_key

    def get_arr_time_key(self) -> str:
        """
        Get the key for the arrival time.
        @return: Key for the arrival time.
        """
        return self.__arr_time_key

    def get_loc_key(self) -> str:
        """
        Get the key for the departure location identifier.
        @return: Key for the departure location identifier.
        """
        return self.__loc_key

    def get_list_key(self) -> str:
        """
        Get the key for the list of stops.
        @return: Key for the list of stops.
        """
        return self.__list_key

    def get_keys(self) -> list:
        """
        Get all keys in the schema.
        @return: List of keys in the schema.
        """
        return [
            self.__uid_key,
            self.__dep_time_key,
            self.__arr_time_key,
            self.__loc_key,
            self.__list_key,
        ]

    def get_datetime_format(self) -> str:
        """
        Get the datetime format.
        @return: Datetime format.
        """
        return self.__datetime_format


class Timetable(object):
    """
    Class for storing a timetable, which is defined as a list of services.
    """

    def __init__(self, connection_list: ConnectionList | None = None) -> None:
        """
        Initialise a Timetable object with an optional ConnectionList.
        @param connection_list: (Optional, default None) A ConnectionList
        """
        if connection_list == None:
            self.__connection_list = ConnectionList()
        else:
            self.__connection_list = connection_list

    def __parse_service(self, service: dict | list, schema: TimetableSchema) -> None:
        """
        Parse a service from a dict.
        @param service: A dict of stops.
        @param schema: A TimetableSchema object describing the structure of the
        timetable.
        """
        uid = ""
        datetime_format = schema.get_datetime_format()
        if schema.get_list_key() != "" and type(service) == dict:
            try:
                uid = service[schema.get_uid_key()]
            except KeyError:
                raise KeyError("Unique identifier not found")
            stops = service[schema.get_list_key()]
        else:
            stops = service
        dep_time = []
        dep_loc = []
        for stop in stops:
            if schema.get_list_key() == "" or type(service) == list:
                try:
                    uid = stop[schema.get_uid_key()]
                except KeyError:
                    raise KeyError("Unique identifier not found")
            other_data = {
                key: stop[key] for key in stop if key not in schema.get_keys()
            }
            if schema.get_dep_time_key() in stop or schema.get_arr_time_key() in stop:
                if dep_time != None:
                    if (
                        schema.get_arr_time_key() in stop
                        and schema.get_dep_time_key() in stop
                    ):
                        # Normal stop
                        arr_time = stop[schema.get_arr_time_key()]
                        arr_loc = stop[schema.get_loc_key()]
                        self.__create_connections(
                            uid,
                            dep_time,
                            arr_time,
                            dep_loc,
                            arr_loc,
                            datetime_format,
                            other_data,
                        )
                        dep_time = [stop[schema.get_dep_time_key()]]
                        dep_loc = [stop[schema.get_loc_key()]]
                    elif (
                        schema.get_arr_time_key() in stop
                        and schema.get_dep_time_key() not in stop
                    ):
                        # Set down stop only
                        arr_time = stop[schema.get_arr_time_key()]
                        arr_loc = stop[schema.get_loc_key()]
                        self.__create_connections(
                            uid,
                            dep_time,
                            arr_time,
                            dep_loc,
                            arr_loc,
                            datetime_format,
                            other_data,
                        )
                    elif (
                        schema.get_arr_time_key() not in stop
                        and schema.get_dep_time_key() in stop
                    ):
                        # Pick up stop only
                        dep_time.append(stop[schema.get_dep_time_key()])
                        dep_loc.append(stop[schema.get_loc_key()])

    def __create_connections(
        self,
        uid: str,
        dep_times: List[datetime.datetime],
        arr_time: datetime.datetime,
        dep_locs: List[str],
        arr_loc: str,
        datetime_format: str = "",
        other_data: dict = {},
    ) -> None:
        """
        Create connections from a list of departure times and an arrival time.
        Arrival time is not a list as there is no use case for it.
        @param uid: Unique identifier of the service.
        @param dep_times: List of departure times.
        @param arr_time: Arrival time.
        @param other_data: Other data present in the timetable for this
        connection (e.g. mode, operator, etconnection.)
        """
        for i in range(len(dep_times)):
            self.__connection_list.append(
                Connection(
                    uid,
                    dep_times[i],
                    arr_time,
                    dep_locs[i],
                    arr_loc,
                    datetime_format,
                    other_data,
                )
            )

    def parse_list(self, timetable: list, schema: TimetableSchema) -> None:
        """
        Parse a timetable from a list.
        @param timetable: A list of services.
        @param schema: A TimetableSchema object describing the structure of the
        timetable.
        """
        for service in timetable:
            self.__parse_service(service, schema)
        # DEBUG
        # print(self.__connection_list)

    def stats(self) -> dict:
        """
        Return statistics about the timetable
        @return: A list of statistics about the timetable
        """
        return {
            "connection_list_length": len(self.__connection_list),
            "timetable_memory_size": sys.getsizeof(self),
        }

    def get_connections(self) -> ConnectionList:
        """
        Get the connection list.
        @return: The connection list.
        """
        return self.__connection_list


class Location(object):
    """
    Class for storing location information
    """

    def __init__(
        self, location_id: str, location_name: str, minimum_connection_time: int = 0
    ) -> None:
        """
        Initialise a Location object.
        @param location_id: Location identifier.
        @param location_name: Location name.
        @param minimum_connection_time: Minimum connection time between services
        at this location.
        """
        self.__location_id = location_id
        self.__location_name = location_name
        self.__mct = minimum_connection_time

    def __repr__(self) -> str:
        return f"Location({self.__location_id}, {self.__location_name}, {self.__mct})"

    def __str__(self) -> str:
        return f"Location({self.__location_id}, {self.__location_name}, {self.__mct})"

    def get_location_id(self) -> str:
        """
        Get the location identifier.
        @return: Location identifier.
        """
        return self.__location_id

    def get_location_name(self) -> str:
        """
        Get the location name.
        @return: Location name.
        """
        return self.__location_name

    def get_minimum_connection_time(self) -> int:
        """
        Get the minimum connection time.
        @return: Minimum connection time.
        """
        return self.__mct


class ItineraryEngine(object):
    """
    Class for processing timetables for the generation of itineraries.
    """

    def __init__(self, timetable: Timetable, locations: dict[str, Location]) -> None:
        """
        Initialise the ItineraryEngine object.
        @param timetable: A Timetable object.
        @param stations: A list of station identifiers.
        """
        self.__timetable = timetable
        self.__locations = locations
        self.__in_connection = {k: -1 for k in self.__locations.keys()}
        self.__earliest_arrival = {
            k: datetime.datetime.max for k in self.__locations.keys()
        }

    def __merge_connections(self, connections: list) -> list:
        """
        Merge connections where possible.
        @param connections: List of connections to merge.
        @return: List of merged connections.
        """
        merged_connections = []
        for connection in connections:
            if len(merged_connections) == 0:
                merged_connections.append(connection)
            else:
                if (
                    merged_connections[-1].get_arr_loc() == connection.get_dep_loc()
                    and merged_connections[-1].get_uid() == connection.get_uid()
                ):
                    merged_connections[-1] = Connection(
                        merged_connections[-1].get_uid(),
                        merged_connections[-1].get_dep_time(),
                        connection.get_arr_time(),
                        merged_connections[-1].get_dep_loc(),
                        connection.get_arr_loc(),
                    )
                else:
                    merged_connections.append(connection)
        return merged_connections

    def generate_itinerary(
        self,
        origin: Location | str,
        destination: Location | str,
        planned_time: datetime.datetime,
        arrive_by: bool = False,
        merge_connections: bool = False,
    ) -> list | None:
        """
        Generate an itinerary based on the initialised timetable and parameters provided.
        @param origin: Origin location.
        @param destination: Destination location.
        @param planned_time: Planned departure/arrival time.
        @param time_type: True if planned_time is a departure time, False if planned_time is an arrival time.
        """
        if isinstance(origin, Location) != True:
            if origin not in self.__locations.keys():
                raise ValueError("Origin location does not exist")
            else:
                origin = self.__locations[str(origin)]
        elif (
            isinstance(origin, Location)
            and origin.get_location_id() not in self.__locations.keys()
        ):
            raise ValueError("Origin location does not exist")
        if isinstance(destination, Location) != True:
            if destination not in self.__locations.keys():
                raise ValueError("Destination location does not exist")
            else:
                destination = self.__locations[str(destination)]
        elif (
            isinstance(destination, Location)
            and destination.get_location_id() not in self.__locations.keys()
        ):
            raise ValueError("Destination location does not exist")
        if isinstance(planned_time, datetime.datetime) != True:
            raise TypeError("Planned time must be a datetime object")
        if arrive_by not in [True, False]:
            raise TypeError("Time type must be a boolean")

        earliest = datetime.datetime.max

        if arrive_by == False:
            self.__earliest_arrival = {
                key: datetime.datetime.max for key in self.__locations.keys()
            }
            self.__earliest_arrival[origin.get_location_id()] = planned_time  # type: ignore
            self.__timetable.get_connections().sort(key=lambda x: x.get_dep_time())
        else:
            self.__earliest_arrival = {
                key: datetime.datetime.min for key in self.__locations.keys()
            }
            self.__earliest_arrival[destination.get_location_id()] = planned_time  # type: ignore
            self.__timetable.get_connections().sort(key=lambda x: x.get_arr_time())

        for index, connection in enumerate(self.__timetable.get_connections()):
            mct = 0
            if (
                self.__timetable.get_connections()[
                    self.__in_connection[connection.get_arr_loc()]
                ].get_uid()
                != connection.get_uid()
            ):
                mct = self.__locations[
                    connection.get_arr_loc()
                ].get_minimum_connection_time()

            if (
                arrive_by == False
                and connection.get_dep_time()
                >= self.__earliest_arrival[connection.get_dep_loc()]
                + datetime.timedelta(minutes=mct)
                and connection.get_arr_time()
                < self.__earliest_arrival[connection.get_arr_loc()]
            ):
                self.__earliest_arrival[
                    connection.get_arr_loc()
                ] = connection.get_arr_time()
                self.__in_connection[connection.get_arr_loc()] = index

                if connection.get_arr_loc() == origin.get_location_id():  # type: ignore
                    earliest = min(earliest, connection.get_arr_time())
            elif (
                arrive_by
                and connection.get_arr_time()
                <= self.__earliest_arrival[connection.get_arr_loc()]
                + datetime.timedelta(minutes=mct)
                and connection.get_dep_time()
                > self.__earliest_arrival[connection.get_dep_loc()]
            ):
                self.__earliest_arrival[
                    connection.get_dep_loc()
                ] = connection.get_dep_time()
                self.__in_connection[connection.get_dep_loc()] = index

                if connection.get_dep_loc() == destination.get_location_id():  # type: ignore
                    earliest = min(earliest, connection.get_dep_time())
            elif connection.get_arr_time() > earliest:
                # No point in searching anymore
                break

        final_route = []

        if arrive_by == False:
            if self.__in_connection[destination.get_location_id()] == -1:  # type: ignore
                return []
            else:
                route = []

                last_connection_index = self.__in_connection[destination.get_location_id()]  # type: ignore

                while last_connection_index != -1:
                    connection = self.__timetable.get_connections()[
                        last_connection_index
                    ]
                    route.append(connection)
                    last_connection_index = self.__in_connection[
                        connection.get_dep_loc()
                    ]

                corrected_route = list(reversed(route))
                final_route = corrected_route
        else:
            if self.__in_connection[origin.get_location_id()] == -1:  # type: ignore
                return []
            else:
                route = []

                last_connection_index = self.__in_connection[origin.get_location_id()]  # type: ignore

                while last_connection_index != -1:
                    connection = self.__timetable.get_connections()[
                        last_connection_index
                    ]
                    route.append(connection)
                    last_connection_index = self.__in_connection[
                        connection.get_arr_loc()
                    ]

                final_route = route

        if merge_connections:
            return self.__merge_connections(final_route)
        else:
            return final_route
