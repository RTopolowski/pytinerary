from unittest import TestCase

import pytinerary


class TimetableSchemaTestCases(TestCase):
    def setUp(self):
        self.connection = pytinerary.TimetableSchema(
            "uid", "dep_time", "arr_time", "dep_loc", "%Y-%m-%dT%H:%M:%S", "locations"
        )

    def test_correct_uid_key_returned(self):
        uid = self.connection.get_uid_key()
        self.assertEqual(uid, "uid")

    def test_correct_dep_time_key_returned(self):
        dep_time = self.connection.get_dep_time_key()
        self.assertEqual(dep_time, "dep_time")

    def test_correct_arr_time_key_returned(self):
        arr_time = self.connection.get_arr_time_key()
        self.assertEqual(arr_time, "arr_time")

    def test_correct_loc_key_returned(self):
        dep_loc = self.connection.get_loc_key()
        self.assertEqual(dep_loc, "dep_loc")

    def test_correct_list_key_returned(self):
        list_key = self.connection.get_list_key()
        self.assertEqual(list_key, "locations")

    def test_correct_keys_returned(self):
        keys = self.connection.get_keys()
        self.assertEqual(keys, ["uid", "dep_time", "arr_time", "dep_loc", "locations"])

    def test_correct_datetime_format_returned(self):
        datetime_format = self.connection.get_datetime_format()
        self.assertEqual(datetime_format, "%Y-%m-%dT%H:%M:%S")
