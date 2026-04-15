import unittest

from alg import (
    levenstein_matrix,
    levenstein_recursive,
    levenstein_cash,
    damerau_levenstein_matrix
)

class TestLevenshteinAlgorithms(unittest.TestCase):
    
    def tests_cases(self):
        self.test_cases = [
            ("", "", 0),
            ("test", "test", 0),
            ("test", "tests", 1),
            ("tests", "test", 1),
            ("cat", "bat", 1),
            ("abcdefg", "axcyf", 4),
            ("xyz", "abc", 3),
            ("", "xyz", 3),
            ("xyz", "", 3),
            ("m", "n", 1),
            ("sunday", "saturnday", 3),
            ("", "x", 1),
            ("12345", "34512", 4),
            ("remove", "moore", 4),
        ]
    
    def test_levenstein_matrix(self):
        self.tests_cases()
        for lhs, rhs, expected in self.test_cases:
            with self.subTest(lhs=lhs, rhs=rhs):
                self.assertEqual(levenstein_matrix(lhs, rhs), expected)
    
    def test_levenstein_recursive(self):
        self.tests_cases()
        for lhs, rhs, expected in self.test_cases:
            with self.subTest(lhs=lhs, rhs=rhs):
                self.assertEqual(levenstein_recursive(lhs, rhs), expected)
    
    def test_levenstein_cash(self):
        self.tests_cases()
        for lhs, rhs, expected in self.test_cases:
            with self.subTest(lhs=lhs, rhs=rhs):
                self.assertEqual(levenstein_cash(lhs, rhs), expected)
    
    def test_damerau_levenstein_matrix(self):
        self.tests_cases()
        for lhs, rhs, expected in self.test_cases:
            with self.subTest(lhs=lhs, rhs=rhs):
                self.assertEqual(damerau_levenstein_matrix(lhs, rhs), expected)

if __name__ == "__main__":
    unittest.main()
