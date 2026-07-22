import unittest
from lead_conversion_model import LeadConversionModel

class TestLeadConversionModel(unittest.TestCase):

    def setUp(self):
        self.model = LeadConversionModel()
        self.model.train()

    def test_train_model(self):
        # Verify that the model is trained after calling train method
        self.assertTrue(hasattr(self.model, 'is_trained'))
        self.assertTrue(self.model.is_trained)

    def test_predict_accuracy(self):
        # Test prediction accuracy on a sample input
        sample_input = {
            'age': 30,
            'income': 50000,
            'education_level': 'Bachelor',
            'previous_conversions': 2
        }
        expected_output = True  # Assuming the model predicts conversion for this input
        prediction = self.model.predict(sample_input)
        self.assertEqual(prediction, expected_output)

if __name__ == '__main__':
    unittest.main()
