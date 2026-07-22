import unittest
from fastapi.testclient import TestClient
from leadConversionModel import LeadConversionModel

class TestLeadConversionModel(unittest.TestCase):
    def setUp(self):
        self.model = LeadConversionModel()
        self.client = TestClient()

    def test_train_model(self):
        # Mock the data loading and processing
        mock_data = pd.DataFrame({
            'feature1': [1, 2, 3, 4],
            'feature2': [5, 6, 7, 8],
            'conversion': [0, 1, 0, 1]
        })
        
        # Save the mock data to a temporary CSV file
        temp_csv_path = "temp_data.csv"
        mock_data.to_csv(temp_csv_path, index=False)
        
        # Train the model using the temporary CSV file
        self.model.train(temp_csv_path)
        
        # Clean up the temporary CSV file
        import os
        os.remove(temp_csv_path)
        
        # Check if the model is trained (model should have a non-empty feature_importances_ attribute)
        self.assertTrue(hasattr(self.model.model, 'feature_importances_'))

    def test_predict_model(self):
        # Mock the data loading and processing
        mock_data = pd.DataFrame({
            'feature1': [1, 2, 3, 4],
            'feature2': [5, 6, 7, 8]
        })
        
        # Save the mock data to a temporary CSV file
        temp_csv_path = "temp_data.csv"
        mock_data.to_csv(temp_csv_path, index=False)
        
        # Train the model using the temporary CSV file
        self.model.train(temp_csv_path)
        
        # Clean up the temporary CSV file
        import os
        os.remove(temp_csv_path)
        
        # Predict a conversion for a new set of features
        prediction = self.model.predict({'feature1': 5, 'feature2': 9})
        
        # Check if the prediction is either 0 or 1 (binary classification)
        self.assertIn(prediction, [0, 1])

if __name__ == '__main__':
    unittest.main()
