import unittest
from src.cache import Cache

class CacheTests(unittest.TestCase):
    def test_round_trip(self):
        cache = Cache()
        cache.put("example", "saved")
        self.assertEqual(cache.get("example"), "saved")

    def test_missing(self):
        self.assertIsNone(Cache().get("absent"))
