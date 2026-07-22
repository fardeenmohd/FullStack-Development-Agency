import unittest
from lead_scoring_service import LeadScoringService

class TestLeadScoringService(unittest.TestCase):

    def setUp(self):
        self.service = LeadScoringService()

    def test_calculate_score_basic(self):
        self._test_calculate_score({
            'age': 30,
            'income': 50000,
            'education_level': 'Bachelor',
            'credit_score': 700
        }, 85)

    def test_calculate_score_edge_cases(self):
        self._test_calculate_score({
            'age': 16,
            'income': 20000,
            'education_level': 'High School',
            'credit_score': 300
        }, 45)

    def test_calculate_score_high_income(self):
        self._test_calculate_score({
            'age': 45,
            'income': 200000,
            'education_level': 'Master',
            'credit_score': 850
        }, 95)

    def test_calculate_score_low_income(self):
        self._test_calculate_score({
            'age': 35,
            'income': 10000,
            'education_level': 'High School',
            'credit_score': 600
        }, 70)

    def test_calculate_score_low_credit_score(self):
        self._test_calculate_score({
            'age': 30,
            'income': 50000,
            'education_level': 'Bachelor',
            'credit_score': 400
        }, 60)

    def test_calculate_score_high_credit_score(self):
        self._test_calculate_score({
            'age': 30,
            'income': 50000,
            'education_level': 'Bachelor',
            'credit_score': 900
        }, 90)

    def test_calculate_score_invalid_age(self):
        self._test_calculate_score_with_exception({
            'age': -5,
            'income': 50000,
            'education_level': 'Bachelor',
            'credit_score': 700
        }, ValueError)

    def test_calculate_score_invalid_income(self):
        self._test_calculate_score_with_exception({
            'age': 30,
            'income': -10000,
            'education_level': 'Bachelor',
            'credit_score': 700
        }, ValueError)

    def test_calculate_score_invalid_credit_score(self):
        self._test_calculate_score_with_exception({
            'age': 30,
            'income': 50000,
            'education_level': 'Bachelor',
            'credit_score': -100
        }, ValueError)

    def _test_calculate_score(self, lead_data, expected_score):
        self.assertEqual(self.service.calculate_score(lead_data), expected_score)

    def _test_calculate_score_with_exception(self, lead_data, exception_type):
        with self.assertRaises(exception_type):
            self.service.calculate_score(lead_data)

if __name__ == '__main__':
    unittest.main()
