from unittest import TestCase

import pytinerary


class LocationTestCases(TestCase):
    def setUp(self):
        self.location = pytinerary.Location("A", "Location A", 0)

    def test_correct_name_returned(self):
        name = self.location.get_location_name()
        self.assertEqual(name, "Location A")

    def test_correct_id_returned(self):
        id = self.location.get_location_id()
        self.assertEqual(id, "A")

    def test_correct_mct_returned(self):
        mct = self.location.get_minimum_connection_time()
        self.assertEqual(mct, 0)

    def test_str_returned(self):
        returned_str = str(self.location)
        self.assertEqual(returned_str, "Location(A, Location A, 0)")

    def test_repr_returned(self):
        returned_repr = repr(self.location)
        self.assertEqual(returned_repr, "Location(A, Location A, 0)")
