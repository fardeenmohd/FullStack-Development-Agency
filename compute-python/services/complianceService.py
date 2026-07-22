from typing import List, Dict
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Ensure necessary NLTK resources are downloaded
nltk.download('punkt')

class ComplianceService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.trade_data = self.load_trade_data()

    def load_trade_data(self) -> List[str]:
        # Placeholder for loading historical trade data
        return ["trade1", "trade2", "trade3"]

    def preprocess_text(self, text: str) -> str:
        # Simple preprocessing: tokenization and lowercasing
        tokens = nltk.word_tokenize(text)
        return ' '.join([token.lower() for token in tokens])

    def calculate_similarity_scores(self, lead_description: str) -> List[float]:
        preprocessed_lead = self.preprocess_text(lead_description)
        tfidf_matrix = self.vectorizer.fit_transform([preprocessed_lead] + self.trade_data)
        similarity_scores = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1:])
        return similarity_scores.flatten().tolist()

    def evaluate_compliance_risk(self, lead_description: str) -> Dict[str, float]:
        scores = self.calculate_similarity_scores(lead_description)
        risk_score = sum(scores) / len(scores)
        return {"risk_score": risk_score}

# Example usage
if __name__ == "__main__":
    compliance_service = ComplianceService()
    lead_description = "This is a sample lead description."
    result = compliance_service.evaluate_compliance_risk(lead_description)
    print(result)
