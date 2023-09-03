from unittest import TestCase

import pytinerary

import datetime


class ConnectionTestCases(TestCase):
    def setUp(self):
        self.connection = pytinerary.Connection(
            "1",
            datetime.datetime(2023, 8, 24, 12, 0),
            datetime.datetime(2023, 8, 24, 12, 30),
            "A",
            "B",
            other_data={"mode": "Train", "operator": "DB"},
        )

    def test_correct_uid_returned(self):
        uid = self.connection.get_uid()
        self.assertEqual(uid, "1")

    def test_correct_dep_time_returned(self):
        dep_time = self.connection.get_dep_time()
        self.assertEqual(dep_time, datetime.datetime(2023, 8, 24, 12, 0))

    def test_correct_arr_time_returned(self):
        arr_time = self.connection.get_arr_time()
        self.assertEqual(arr_time, datetime.datetime(2023, 8, 24, 12, 30))

    def test_correct_dep_loc_returned(self):
        dep_loc = self.connection.get_dep_loc()
        self.assertEqual(dep_loc, "A")

    def test_correct_arr_loc_returned(self):
        arr_loc = self.connection.get_arr_loc()
        self.assertEqual(arr_loc, "B")

    def test_correct_dict_returned(self):
        returned_dict = self.connection.__dict__()
        self.assertEqual(
            returned_dict,
            {
                "uid": "1",
                "dep_time": datetime.datetime(2023, 8, 24, 12, 0),
                "arr_time": datetime.datetime(2023, 8, 24, 12, 30),
                "dep_loc": "A",
                "arr_loc": "B",
                "mode": "Train",
                "operator": "DB",
            },
        )

    def test_correct_str_returned(self):
        returned_str = str(self.connection)
        self.assertEqual(
            returned_str,
            "Connection(1, A @ 2023-08-24 12:00:00, B @ 2023-08-24 12:30:00, {'mode': 'Train', 'operator': 'DB'})",
        )

    def test_correct_repr_returned(self):
        returned_str = self.connection.__repr__()
        self.assertEqual(
            returned_str,
            "Connection(1, A @ 2023-08-24 12:00:00, B @ 2023-08-24 12:30:00, {'mode': 'Train', 'operator': 'DB'})",
        )

    def test_arr_time_must_be_after_dep_time(self):
        with self.assertRaises(ValueError):
            pytinerary.Connection(
                "1",
                datetime.datetime(2023, 8, 24, 12, 30),
                datetime.datetime(2023, 8, 24, 12, 0),
                "A",
                "B",
                other_data={"mode": "Train", "operator": "DB"},
            )

    def test_datetime_format(self):
        second_connection = pytinerary.Connection(
            "2",
            "2023-08-24T13:00:00",
            "2023-08-24T13:30:00",
            "A",
            "B",
            datetime_format="%Y-%m-%dT%H:%M:%S",
            other_data={"mode": "Train", "operator": "DB"},
        )
        self.assertEqual(
            str(second_connection),
            "Connection(2, A @ 2023-08-24 13:00:00, B @ 2023-08-24 13:30:00, {'mode': 'Train', 'operator': 'DB'})",
        )

    def test_datetime_format_must_be_provided_for_strings(self):
        with self.assertRaises(ValueError):
            pytinerary.Connection(
                "2",
                "2023-08-24T13:00:00",
                "2023-08-24T13:30:00",
                "A",
                "B",
                other_data={"mode": "Train", "operator": "DB"},
            )

    def test_eq(self):
        second_connection = pytinerary.Connection(
            "1",
            datetime.datetime(2023, 8, 24, 12, 0),
            datetime.datetime(2023, 8, 24, 12, 30),
            "A",
            "B",
            other_data={"mode": "Train", "operator": "DB"},
        )
        self.assertEqual(self.connection, second_connection)

    def test_neq(self):
        second_connection = pytinerary.Connection(
            "2",
            datetime.datetime(2023, 8, 24, 12, 0),
            datetime.datetime(2023, 8, 24, 12, 30),
            "A",
            "B",
            other_data={"mode": "Train", "operator": "DB"},
        )
        self.assertNotEqual(self.connection, second_connection)

    def test_eq_with_non_connection(self):
        with self.assertRaises(TypeError):
            self.assertNotEqual("string", self.connection)

    def test_lt(self):
        second_connection = pytinerary.Connection(
            "2",
            datetime.datetime(2023, 8, 24, 12, 10),
            datetime.datetime(2023, 8, 24, 12, 30),
            "A",
            "B",
            other_data={"mode": "Train", "operator": "DB"},
        )
        self.assertLess(self.connection, second_connection)

    def test_lt_with_non_connection(self):
        with self.assertRaises(TypeError):
            self.assertLess("string", self.connection)

    def test_le(self):
        second_connection = pytinerary.Connection(
            "2",
            datetime.datetime(2023, 8, 24, 12, 10),
            datetime.datetime(2023, 8, 24, 12, 30),
            "A",
            "B",
            other_data={"mode": "Train", "operator": "DB"},
        )
        self.assertLessEqual(self.connection, second_connection)

    def test_le_with_non_connection(self):
        with self.assertRaises(TypeError):
            self.assertLessEqual("string", self.connection)

    def test_gt(self):
        second_connection = pytinerary.Connection(
            "2",
            datetime.datetime(2023, 8, 24, 12, 10),
            datetime.datetime(2023, 8, 24, 12, 30),
            "A",
            "B",
            other_data={"mode": "Train", "operator": "DB"},
        )
        self.assertGreater(second_connection, self.connection)

    def test_gt_with_non_connection(self):
        with self.assertRaises(TypeError):
            self.assertGreater("string", self.connection)

    def test_ge(self):
        second_connection = pytinerary.Connection(
            "2",
            datetime.datetime(2023, 8, 24, 12, 10),
            datetime.datetime(2023, 8, 24, 12, 30),
            "A",
            "B",
            other_data={"mode": "Train", "operator": "DB"},
        )
        self.assertGreaterEqual(second_connection, self.connection)

    def test_ge_with_non_connection(self):
        with self.assertRaises(TypeError):
            self.assertGreaterEqual("string", self.connection)
