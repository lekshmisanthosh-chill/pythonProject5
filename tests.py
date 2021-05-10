from covid_visualizer.utils import mondayize
from unittest import TestCase


class TestDummy(TestCase):
    def test_random(self):
        self.assertEqual(mondayize("2020-01-01"), 2)
