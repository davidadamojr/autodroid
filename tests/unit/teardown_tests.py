import unittest
from mocks.driver import MockDriver

class TearDownTests(unittest.TestCase):
    def setUp(self):
        self.driver = MockDriver()

    def test_test(self):
        self.driver.quit()