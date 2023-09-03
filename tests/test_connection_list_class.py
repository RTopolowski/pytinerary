from unittest import TestCase

import pytinerary


class ConnectionListTestCases(TestCase):
    def setUp(self):
        self.connection_list = pytinerary.ConnectionList(
            connection_list=[
                pytinerary.Connection(
                    "1",
                    "2023-09-01 00:01:00",
                    "2023-09-01 00:10:00",
                    "A",
                    "B",
                    "%Y-%m-%d %H:%M:%S",
                ),
                pytinerary.Connection(
                    "1",
                    "2023-09-01 00:11:00",
                    "2023-09-01 00:20:00",
                    "B",
                    "C",
                    "%Y-%m-%d %H:%M:%S",
                ),
                pytinerary.Connection(
                    "2",
                    "2023-09-01 00:10:00",
                    "2023-09-01 00:15:00",
                    "A",
                    "C",
                    "%Y-%m-%d %H:%M:%S",
                ),
                pytinerary.Connection(
                    "3",
                    "2023-09-01 00:05:00",
                    "2023-09-01 00:14:00",
                    "A",
                    "B",
                    "%Y-%m-%d %H:%M:%S",
                ),
                pytinerary.Connection(
                    "4",
                    "2023-09-01 00:22:00",
                    "2023-09-01 00:30:00",
                    "B",
                    "C",
                    "%Y-%m-%d %H:%M:%S",
                ),
            ]
        )

    def test_correct_length_returned(self):
        self.assertEqual(len(self.connection_list), 5)

    def test_get_by_index(self):
        fetched_connection = self.connection_list[2]
        self.assertEqual(
            str(fetched_connection),
            "Connection(2, A @ 2023-09-01 00:10:00, C @ 2023-09-01 00:15:00, {})",
        )

    def test_get_by_index_out_of_bounds(self):
        with self.assertRaises(IndexError):
            self.connection_list[5]

    def test_set_item(self):
        new_connection = pytinerary.Connection(
            "5",
            "2023-09-01 00:32:00",
            "2023-09-01 00:40:00",
            "C",
            "D",
            "%Y-%m-%d %H:%M:%S",
        )
        self.connection_list[2] = new_connection
        self.assertEqual(
            str(self.connection_list[2]),
            "Connection(5, C @ 2023-09-01 00:32:00, D @ 2023-09-01 00:40:00, {})",
        )

    def test_set_item_out_of_bounds(self):
        new_connection = pytinerary.Connection(
            "5",
            "2023-09-01 00:32:00",
            "2023-09-01 00:40:00",
            "C",
            "D",
            "%Y-%m-%d %H:%M:%S",
        )
        with self.assertRaises(IndexError):
            self.connection_list[5] = new_connection

    def test_set_item_wrong_type(self):
        with self.assertRaises(TypeError):
            self.connection_list[2] = "wrong type"  # type: ignore

    def test_del_item(self):
        del self.connection_list[2]
        self.assertEqual(
            str(self.connection_list[2]),
            "Connection(3, A @ 2023-09-01 00:05:00, B @ 2023-09-01 00:14:00, {})",
        )

    def test_del_item_out_of_bounds(self):
        with self.assertRaises(IndexError):
            del self.connection_list[5]

    def test_iter(self):
        for connection in self.connection_list:
            self.assertIsInstance(connection, pytinerary.Connection)
            self.assertIn(connection, self.connection_list)

    def test_reversed_iter(self):
        for connection in reversed(self.connection_list):
            self.assertIsInstance(connection, pytinerary.Connection)
            self.assertIn(connection, self.connection_list)

    def test_contains(self):
        self.assertIn(
            pytinerary.Connection(
                "1",
                "2023-09-01 00:01:00",
                "2023-09-01 00:10:00",
                "A",
                "B",
                "%Y-%m-%d %H:%M:%S",
            ),
            self.connection_list,
        )

    def test_not_contains(self):
        self.assertNotIn(
            pytinerary.Connection(
                "1",
                "2023-09-01 00:01:00",
                "2023-09-01 00:10:00",
                "A",
                "C",
                "%Y-%m-%d %H:%M:%S",
            ),
            self.connection_list,
        )

    def test_index(self):
        index = self.connection_list.index(
            pytinerary.Connection(
                "1",
                "2023-09-01 00:01:00",
                "2023-09-01 00:10:00",
                "A",
                "B",
                "%Y-%m-%d %H:%M:%S",
            )
        )
        self.assertEqual(index, 0)

    def test_index_not_found(self):
        with self.assertRaises(ValueError):
            self.connection_list.index(
                pytinerary.Connection(
                    "1",
                    "2023-09-01 00:01:00",
                    "2023-09-01 00:10:00",
                    "A",
                    "C",
                    "%Y-%m-%d %H:%M:%S",
                )
            )

    def test_repr(self):
        self.assertEqual(
            repr(self.connection_list),
            "ConnectionList([Connection(1, A @ 2023-09-01 00:01:00, B @ 2023-09-01 00:10:00, {}), Connection(1, B @ 2023-09-01 00:11:00, C @ 2023-09-01 00:20:00, {}), Connection(2, A @ 2023-09-01 00:10:00, C @ 2023-09-01 00:15:00, {}), Connection(3, A @ 2023-09-01 00:05:00, B @ 2023-09-01 00:14:00, {}), Connection(4, B @ 2023-09-01 00:22:00, C @ 2023-09-01 00:30:00, {})])",
        )

    def test_str(self):
        self.assertEqual(
            str(self.connection_list),
            "ConnectionList([Connection(1, A @ 2023-09-01 00:01:00, B @ 2023-09-01 00:10:00, {}), Connection(1, B @ 2023-09-01 00:11:00, C @ 2023-09-01 00:20:00, {}), Connection(2, A @ 2023-09-01 00:10:00, C @ 2023-09-01 00:15:00, {}), Connection(3, A @ 2023-09-01 00:05:00, B @ 2023-09-01 00:14:00, {}), Connection(4, B @ 2023-09-01 00:22:00, C @ 2023-09-01 00:30:00, {})])",
        )

    def test_append(self):
        self.connection_list.append(
            pytinerary.Connection(
                "5",
                "2023-09-01 00:32:00",
                "2023-09-01 00:40:00",
                "C",
                "D",
                "%Y-%m-%d %H:%M:%S",
            )
        )
        self.assertEqual(
            str(self.connection_list[5]),
            "Connection(5, C @ 2023-09-01 00:32:00, D @ 2023-09-01 00:40:00, {})",
        )

    def test_append_wrong_type(self):
        with self.assertRaises(TypeError):
            self.connection_list.append("wrong type")  # type: ignore

    def test_insert(self):
        self.connection_list.insert(
            2,
            pytinerary.Connection(
                "5",
                "2023-09-01 00:32:00",
                "2023-09-01 00:40:00",
                "C",
                "D",
                "%Y-%m-%d %H:%M:%S",
            ),
        )
        self.assertEqual(
            str(self.connection_list[2]),
            "Connection(5, C @ 2023-09-01 00:32:00, D @ 2023-09-01 00:40:00, {})",
        )

    def test_insert_wrong_type(self):
        with self.assertRaises(TypeError):
            self.connection_list.insert(2, "wrong type")  # type: ignore

    def test_sort_by_dep_time(self):
        self.connection_list.sort(pytinerary.Connection.get_dep_time)
        self.assertEqual(
            str(self.connection_list),
            "ConnectionList([Connection(1, A @ 2023-09-01 00:01:00, B @ 2023-09-01 00:10:00, {}), Connection(3, A @ 2023-09-01 00:05:00, B @ 2023-09-01 00:14:00, {}), Connection(2, A @ 2023-09-01 00:10:00, C @ 2023-09-01 00:15:00, {}), Connection(1, B @ 2023-09-01 00:11:00, C @ 2023-09-01 00:20:00, {}), Connection(4, B @ 2023-09-01 00:22:00, C @ 2023-09-01 00:30:00, {})])",
        )

    def test_sort_by_arr_time(self):
        self.connection_list.sort(pytinerary.Connection.get_arr_time)
        self.assertEqual(
            str(self.connection_list),
            "ConnectionList([Connection(1, A @ 2023-09-01 00:01:00, B @ 2023-09-01 00:10:00, {}), Connection(3, A @ 2023-09-01 00:05:00, B @ 2023-09-01 00:14:00, {}), Connection(2, A @ 2023-09-01 00:10:00, C @ 2023-09-01 00:15:00, {}), Connection(1, B @ 2023-09-01 00:11:00, C @ 2023-09-01 00:20:00, {}), Connection(4, B @ 2023-09-01 00:22:00, C @ 2023-09-01 00:30:00, {})])",
        )

    def test_pop(self):
        self.assertEqual(
            str(self.connection_list.pop(2)),
            "Connection(2, A @ 2023-09-01 00:10:00, C @ 2023-09-01 00:15:00, {})",
        )
        self.assertEqual(
            str(self.connection_list),
            "ConnectionList([Connection(1, A @ 2023-09-01 00:01:00, B @ 2023-09-01 00:10:00, {}), Connection(1, B @ 2023-09-01 00:11:00, C @ 2023-09-01 00:20:00, {}), Connection(3, A @ 2023-09-01 00:05:00, B @ 2023-09-01 00:14:00, {}), Connection(4, B @ 2023-09-01 00:22:00, C @ 2023-09-01 00:30:00, {})])",
        )

    def test_pop_out_of_bounds(self):
        with self.assertRaises(IndexError):
            self.connection_list.pop(5)

    def test_pop_empty_list(self):
        empty_list = pytinerary.ConnectionList([])
        with self.assertRaises(IndexError):
            empty_list.pop(0)

    def test_clear(self):
        self.connection_list.clear()
        self.assertEqual(
            str(self.connection_list),
            "ConnectionList([])",
        )

    def test_clear_empty_list(self):
        empty_list = pytinerary.ConnectionList([])
        empty_list.clear()
        self.assertEqual(
            str(empty_list),
            "ConnectionList([])",
        )

    def test_remove(self):
        self.connection_list.remove(
            pytinerary.Connection(
                "1",
                "2023-09-01 00:01:00",
                "2023-09-01 00:10:00",
                "A",
                "B",
                "%Y-%m-%d %H:%M:%S",
            )
        )
        self.assertEqual(
            str(self.connection_list),
            "ConnectionList([Connection(1, B @ 2023-09-01 00:11:00, C @ 2023-09-01 00:20:00, {}), Connection(2, A @ 2023-09-01 00:10:00, C @ 2023-09-01 00:15:00, {}), Connection(3, A @ 2023-09-01 00:05:00, B @ 2023-09-01 00:14:00, {}), Connection(4, B @ 2023-09-01 00:22:00, C @ 2023-09-01 00:30:00, {})])",
        )

    def test_remove_not_found(self):
        with self.assertRaises(ValueError):
            self.connection_list.remove(
                pytinerary.Connection(
                    "1",
                    "2023-09-01 00:01:00",
                    "2023-09-01 00:10:00",
                    "A",
                    "C",
                    "%Y-%m-%d %H:%M:%S",
                )
            )

    def test_remove_empty_list(self):
        empty_list = pytinerary.ConnectionList([])
        with self.assertRaises(ValueError):
            empty_list.remove(
                pytinerary.Connection(
                    "1",
                    "2023-09-01 00:01:00",
                    "2023-09-01 00:10:00",
                    "A",
                    "B",
                    "%Y-%m-%d %H:%M:%S",
                )
            )
