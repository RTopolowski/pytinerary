from unittest import TestCase

import pytinerary

import json


class TimetableTestCases(TestCase):
    def setUp(self):
        self.timetable = pytinerary.Timetable()
        self.schema = pytinerary.TimetableSchema(
            "uid", "dep_time", "arr_time", "location", "%Y-%m-%d %H:%M:%S", "locations"
        )
        with open("./tests/helper_files/timetable.json", encoding="utf-8") as data_file:
            self.data = json.loads(data_file.read())
        self.timetable.parse_list(self.data, self.schema)

    def test_correct_connection_list_returned(self):
        connections = self.timetable.get_connections()
        self.assertEqual(
            str(connections),
            "ConnectionList([Connection(1, A @ 2023-09-01 00:01:00, B @ 2023-09-01 00:10:00, {}), Connection(1, B @ 2023-09-01 00:11:00, C @ 2023-09-01 00:20:00, {}), Connection(2, A @ 2023-09-01 00:10:00, C @ 2023-09-01 00:15:00, {}), Connection(3, A @ 2023-09-01 00:05:00, B @ 2023-09-01 00:14:00, {}), Connection(4, B @ 2023-09-01 00:22:00, C @ 2023-09-01 00:30:00, {}), Connection(5, A @ 2023-09-01 00:31:00, B @ 2023-09-01 00:40:00, {}), Connection(5, B @ 2023-09-01 00:41:00, C @ 2023-09-01 01:00:00, {})])",
        )

    def test_correct_statistics_returned(self):
        stats = self.timetable.stats()
        self.assertEqual(stats["connection_list_length"], 7)

    def test_no_locations_key(self):
        second_timetable = pytinerary.Timetable()
        second_schema = pytinerary.TimetableSchema(
            "uid", "dep_time", "arr_time", "location", "%Y-%m-%d %H:%M:%S"
        )
        with open(
            "./tests/helper_files/timetable_locations_only.json", encoding="utf-8"
        ) as data_file:
            second_data = json.loads(data_file.read())
        second_timetable.parse_list(second_data, second_schema)
        stats = second_timetable.stats()
        self.assertEqual(stats["connection_list_length"], 5)

    def test_no_uid_raises_exception(self):
        second_timetable = pytinerary.Timetable()
        second_schema = pytinerary.TimetableSchema(
            "uid", "dep_time", "arr_time", "location", "%Y-%m-%d %H:%M:%S", "locations"
        )
        with open(
            "./tests/helper_files/timetable_no_uid.json", encoding="utf-8"
        ) as data_file:
            second_data = json.loads(data_file.read())
        with self.assertRaises(KeyError):
            second_timetable.parse_list(second_data, second_schema)

    def test_no_uid_without_locations_key_raises_exception(self):
        second_timetable = pytinerary.Timetable()
        second_schema = pytinerary.TimetableSchema(
            "uid", "dep_time", "arr_time", "location", "%Y-%m-%d %H:%M:%S"
        )
        with open(
            "./tests/helper_files/timetable_locations_only_no_uid.json",
            encoding="utf-8",
        ) as data_file:
            second_data = json.loads(data_file.read())
        with self.assertRaises(KeyError):
            second_timetable.parse_list(second_data, second_schema)

    def test_init_with_connection_list(self):
        connection_list = self.timetable.get_connections()
        second_timetable = pytinerary.Timetable(connection_list)
        stats = second_timetable.stats()
        self.assertEqual(stats["connection_list_length"], 7)
