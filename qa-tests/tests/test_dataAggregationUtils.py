import unittest

class TestDataAggregationUtils(unittest.TestCase):

    def test_aggregateData(self):
        self.assertEqual(aggregateData([]), 0)
        self.assertEqual(aggregateData([5]), 5)
        self.assertEqual(aggregateData([1, 2, 3, 4, 5]), 15)
        self.assertEqual(aggregateData([-1, -2, -3, -4, -5]), -15)
        self.assertEqual(aggregateData([1, -2, 3, -4, 5]), 3)

    def test_processData(self):
        self.assertEqual(processData([]), [])
        self.assertEqual(processData([5]), [5])
        self.assertEqual(processData([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])
        self.assertEqual(processData([-1, -2, -3, -4, -5]), [-1, -2, -3, -4, -5])
        self.assertEqual(processData([1, -2, 3, -4, 5]), [1, -2, 3, -4, 5])

if __name__ == '__main__':
    unittest.main()
