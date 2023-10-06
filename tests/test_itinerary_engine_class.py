from unittest import TestCase

import pytinerary

import datetime
import json


class ItineraryEngineTestCases(TestCase):
    def setUp(self):
        self.timetable = pytinerary.Timetable()
        self.schema = pytinerary.TimetableSchema(
            "uid", "dep_time", "arr_time", "location", "%Y-%m-%d %H:%M:%S", "locations"
        )
        with open("./tests/helper_files/timetable.json", encoding="utf-8") as data_file:
            self.data = json.loads(data_file.read())
        self.timetable.parse_list(self.data, self.schema)
        self.locations = {
            "A": pytinerary.Location("A", "Location A", 0),
            "B": pytinerary.Location("B", "Location B", 0),
            "C": pytinerary.Location("C", "Location C", 0),
        }
        self.engine = pytinerary.ItineraryEngine(self.timetable, self.locations)

    def test_correct_itinerary_returned(self):
        route = self.engine.generate_itinerary(
            self.locations["A"],
            self.locations["C"],
            datetime.datetime(2023, 9, 1, 0, 0, 0),
        )
        self.assertEqual(
            route,
            [
                pytinerary.Connection(
                    "2",
                    "2023-09-01 00:10:00",
                    "2023-09-01 00:15:00",
                    "A",
                    "C",
                    "%Y-%m-%d %H:%M:%S",
                )
            ],
        )

    def test_correct_itinerary_by_arrive_time_returned(self):
        route = self.engine.generate_itinerary(
            self.locations["B"],
            self.locations["C"],
            datetime.datetime(2023, 9, 1, 0, 30, 0),
            arrive_by=True,
        )
        self.assertEqual(
            route,
            [
                pytinerary.Connection(
                    "4",
                    "2023-09-01 00:22:00",
                    "2023-09-01 00:30:00",
                    "B",
                    "C",
                    "%Y-%m-%d %H:%M:%S",
                ),
            ],
        )

    def test_impossible_journey_returns_empty_list(self):
        route = self.engine.generate_itinerary(
            self.locations["C"],
            self.locations["A"],
            datetime.datetime(2023, 9, 1, 0, 0, 0),
        )
        self.assertEqual(route, [])

    def test_string_origin_id_is_valid(self):
        route = self.engine.generate_itinerary(
            "A",
            self.locations["C"],
            datetime.datetime(2023, 9, 1, 0, 0, 0),
        )
        self.assertEqual(
            route,
            [
                pytinerary.Connection(
                    "2",
                    "2023-09-01 00:10:00",
                    "2023-09-01 00:15:00",
                    "A",
                    "C",
                    "%Y-%m-%d %H:%M:%S",
                )
            ],
        )

    def test_non_existent_origin_raises_exception(self):
        other_locations = {
            "A": pytinerary.Location("A", "Location A", 0),
            "B": pytinerary.Location("B", "Location B", 0),
            "C": pytinerary.Location("C", "Location C", 0),
            "D": pytinerary.Location("D", "Location D", 0),
        }
        with self.assertRaises(ValueError):
            self.engine.generate_itinerary(
                other_locations["D"],
                self.locations["C"],
                datetime.datetime(2023, 9, 1, 0, 0, 0),
            )

    def test_non_existent_origin_string_raises_exception(self):
        with self.assertRaises(ValueError):
            self.engine.generate_itinerary(
                "D",
                self.locations["C"],
                datetime.datetime(2023, 9, 1, 0, 0, 0),
            )

    def test_string_destination_id_is_valid(self):
        route = self.engine.generate_itinerary(
            self.locations["A"],
            "C",
            datetime.datetime(2023, 9, 1, 0, 0, 0),
        )
        self.assertEqual(
            route,
            [
                pytinerary.Connection(
                    "2",
                    "2023-09-01 00:10:00",
                    "2023-09-01 00:15:00",
                    "A",
                    "C",
                    "%Y-%m-%d %H:%M:%S",
                )
            ],
        )

    def test_non_existent_destination_raises_exception(self):
        other_locations = {
            "A": pytinerary.Location("A", "Location A", 0),
            "B": pytinerary.Location("B", "Location B", 0),
            "C": pytinerary.Location("C", "Location C", 0),
            "D": pytinerary.Location("D", "Location D", 0),
        }
        with self.assertRaises(ValueError):
            self.engine.generate_itinerary(
                self.locations["A"],
                other_locations["D"],
                datetime.datetime(2023, 9, 1, 0, 0, 0),
            )

    def test_non_existent_destination_string_raises_exception(self):
        with self.assertRaises(ValueError):
            self.engine.generate_itinerary(
                self.locations["C"],
                "D",
                datetime.datetime(2023, 9, 1, 0, 0, 0),
            )

    def test_invalid_datetime_raises_exception(self):
        with self.assertRaises(TypeError):
            self.engine.generate_itinerary(
                self.locations["A"],
                self.locations["C"],
                "Hello",  # type: ignore
            )

    def test_invalid_time_type_raises_exception(self):
        with self.assertRaises(TypeError):
            self.engine.generate_itinerary(
                self.locations["A"],
                self.locations["C"],
                datetime.datetime(2023, 9, 1, 0, 0, 0),
                123,  # type: ignore
            )

    def test_connections_merged(self):
        route = self.engine.generate_itinerary(
            self.locations["A"],
            self.locations["C"],
            datetime.datetime(2023, 9, 1, 0, 30, 0),
            merge_connections=True,
        )
        self.assertEqual(
            route,
            [
                pytinerary.Connection(
                    "5",
                    "2023-09-01 00:31:00",
                    "2023-09-01 01:00:00",
                    "A",
                    "C",
                    "%Y-%m-%d %H:%M:%S",
                )
            ],
        )
