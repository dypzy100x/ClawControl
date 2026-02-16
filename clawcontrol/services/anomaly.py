"""Anomaly Detection - ML-based threat detection"""
from sklearn.ensemble import IsolationForest
import numpy as np

class AnomalyDetector:
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.trained = False
        self.feature_history = []
    
    def train(self, features_list: list):
        if len(features_list) < 10:
            return False
        X = np.array(features_list)
        self.model.fit(X)
        self.trained = True
        return True
    
    def detect(self, features: list) -> dict:
        if not self.trained:
            return {"anomaly": False, "score": 0.5}
        
        X = np.array([features])
        prediction = self.model.predict(X)
        score = self.model.score_samples(X)[0]
        
        return {
            "anomaly": prediction[0] == -1,
            "score": float(score),
            "confidence": abs(float(score))
        }

anomaly_detector = AnomalyDetector()
