import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

class LeadConversionModel:
    def __init__(self):
        self.model = RandomForestClassifier()

    def train(self, data_path):
        # Load the dataset
        data = pd.read_csv(data_path)
        
        # Separate features and target variable
        X = data.drop('conversion', axis=1)
        y = data['conversion']
        
        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train the model
        self.model.fit(X_train, y_train)
        
        # Evaluate the model
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Model Accuracy: {accuracy:.2f}")

    def predict(self, features):
        return self.model.predict([features])[0]

# Example usage:
# model = LeadConversionModel()
# model.train('path_to_your_data.csv')
# prediction = model.predict({'feature1': value1, 'feature2': value2})
# print(f"Predicted Conversion: {prediction}")
