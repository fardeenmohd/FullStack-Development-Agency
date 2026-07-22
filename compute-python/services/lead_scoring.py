from typing import List, Dict
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class LeadScoringService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.alert_criteria = {}

    def train_model(self, leads: List[Dict[str, str]]):
        # Extract text data from leads and vectorize it
        texts = [lead['description'] for lead in leads]
        self.X = self.vectorizer.fit_transform(texts)

    def update_alert_criteria(self, criteria: Dict[str, float]):
        self.alert_criteria = criteria

    def evaluate_leads(self, new_leads: List[Dict[str, str]]) -> List[bool]:
        # Extract text data from new leads and vectorize it
        texts = [lead['description'] for lead in new_leads]
        X_new = self.vectorizer.transform(texts)
        
        # Calculate cosine similarity between new leads and trained model
        similarities = cosine_similarity(X_new, self.X)
        
        # Evaluate based on alert criteria
        evaluations = []
        for sim_row in similarities:
            score = sum(sim * weight for sim, weight in zip(sim_row, self.alert_criteria.values()))
            evaluations.append(score >= max(self.alert_criteria.values()))
        
        return evaluations

# Example usage:
# lead_service = LeadScoringService()
# leads = [{'description': 'High demand for solar panels'}, {'description': 'Low interest in electric vehicles'}]
# lead_service.train_model(leads)
# alert_criteria = {'high_demand': 0.8, 'low_interest': 0.5}
# lead_service.update_alert_criteria(alert_criteria)
# new_leads = [{'description': 'High demand for solar panels'}, {'description': 'Moderate interest in electric vehicles'}]
# evaluations = lead_service.evaluate_leads(new_leads)
# print(evaluations)
