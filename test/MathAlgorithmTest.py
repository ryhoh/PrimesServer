import unittest
import sys
sys.path.append('../src')

from MathAlgorithm import *


class MathAlgorithmTest(unittest.TestCase):

    """
    eratosthenes(end: int)
    [2, end) の区間内の素数をリストに詰める
    2以下の入力に対し空リストを返す
    """
    def test_eratosthenes(self):
        self.assertEqual([],                   eratosthenes(-1))
        self.assertEqual([],                   eratosthenes(0))
        self.assertEqual([],                   eratosthenes(1))
        self.assertEqual([],                   eratosthenes(2))
        self.assertEqual([2],                  eratosthenes(3))
        self.assertEqual([2, 3],               eratosthenes(4))
        self.assertEqual([2, 3],               eratosthenes(5))
        self.assertEqual([2, 3, 5, 7],         eratosthenes(8))
        self.assertEqual([2, 3, 5, 7],         eratosthenes(9))
        self.assertEqual([2, 3, 5, 7, 11, 13], eratosthenes(14))

    def test_eratosthenes_too_big(self):
        self.assertRaises(ValueError, eratosthenes, 10000001)

    def test_generate_primes_str(self):
        self.assertEqual("None",          generate_primes_str(-1))
        self.assertEqual("None",          generate_primes_str(0))
        self.assertEqual("None",          generate_primes_str(1))
        self.assertEqual("None",          generate_primes_str(2))
        self.assertEqual("2",             generate_primes_str(3))
        self.assertEqual("2 3",           generate_primes_str(4))
        self.assertEqual("2 3",           generate_primes_str(5))
        self.assertEqual("2 3 5 7",       generate_primes_str(8))
        self.assertEqual("2 3 5 7",       generate_primes_str(9))
        self.assertEqual("2 3 5 7 11 13", generate_primes_str(14))

    def test_generate_primes_str_too_big(self):
        self.assertRaises(ValueError, eratosthenes, 10000001)


if __name__ == '__main__':
    unittest.main()
