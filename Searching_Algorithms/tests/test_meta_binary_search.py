import unittest
from meta_binary_search import meta_binary_search

class TestMetaBinarySearch(unittest.TestCase):

    def test_element_found(self):
        arr = [1, 3, 5, 7, 9, 11, 13]
        self.assertEqual(meta_binary_search(arr, 9), 4)

    def test_element_not_found(self):
        arr = [10, 20, 30, 40, 50]
        self.assertEqual(meta_binary_search(arr, 25), -1)

    def test_first_element(self):
        arr = [2, 4, 6, 8, 10]
        self.assertEqual(meta_binary_search(arr, 2), 0)

    def test_last_element(self):
        arr = [5, 10, 15, 20, 25]
        self.assertEqual(meta_binary_search(arr, 25), 4)

    def test_empty_array(self):
        arr = []
        self.assertEqual(meta_binary_search(arr, 10), -1)


if __name__ == "__main__":
    unittest.main()
