import unittest
from ternary_search import ternary_search

class TestTernarySearch(unittest.TestCase):

    def test_element_found(self):
        arr = [1, 3, 5, 7, 9, 11, 13]
        self.assertEqual(ternary_search(arr, 7), 3)

    def test_element_not_found(self):
        arr = [2, 4, 6, 8, 10]
        self.assertEqual(ternary_search(arr, 5), -1)

    def test_first_element(self):
        arr = [1, 2, 3, 4, 5]
        self.assertEqual(ternary_search(arr, 1), 0)

    def test_last_element(self):
        arr = [1, 2, 3, 4, 5]
        self.assertEqual(ternary_search(arr, 5), 4)

    def test_empty_array(self):
        arr = []
        self.assertEqual(ternary_search(arr, 10), -1)


if __name__ == "__main__":
    unittest.main()
