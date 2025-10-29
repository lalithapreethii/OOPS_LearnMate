"""
Module for making predictions using the trained weakness classifier model.
Includes functions for loading model and making predictions with recommendations.
"""

import joblib
import numpy as np
import pandas as pd
from typing import Dict, List, Union
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeaknessPredictor:
    def __init__(self, model_path="../models"):
        """Initialize the predictor with model path"""
        self.model_path = Path(model_path)
        self.model = None
        self.scaler = None
        self.load_model()
        
    def load_model(self) -> bool:
        """Load the trained model and scaler"""
        try:
            self.model = joblib.load(self.model_path / 'weakness_classifier.pkl')
            self.scaler = joblib.load(self.model_path / 'scaler.pkl')
            logger.info("Model and scaler loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return False
    
    def get_recommendations(self, weakness_level: str, weak_topics: List[str]) -> List[str]:
        """Generate personalized recommendations based on weakness level and topics"""
        # This is a placeholder - implement your recommendation logic here
        recommendations = []
        
        if weakness_level == "weak":
            recommendations.extend([
                "Focus on fundamental concepts",
                "Schedule regular practice sessions",
                "Consider one-on-one tutoring"
            ])
        elif weakness_level == "moderate":
            recommendations.extend([
                "Review specific weak topics",
                "Practice with additional exercises",
                "Join study groups"
            ])
        else:  # strong
            recommendations.extend([
                "Challenge yourself with advanced problems",
                "Help peers with studying",
                "Explore related topics"
            ])
            
        # Add topic-specific recommendations
        for topic in weak_topics:
            recommendations.append(f"Review resources for: {topic}")
            
        return recommendations

    def predict_weakness(self, student_data: Dict[str, Union[float, int, str]]) -> Dict:
        """
        Predict weakness level for given student data
        
        Args:
            student_data: Dictionary containing student features
                Expected keys match the features used in training
                
        Returns:
            Dictionary containing:
                - weakness_level: predicted level
                - confidence: prediction probability
                - weak_topics: list of identified weak topics
                - recommendations: list of personalized recommendations
        """
        try:
            # Convert input dictionary to DataFrame
            input_df = pd.DataFrame([student_data])
            
            # Ensure all required features are present
            required_features = self.scaler.feature_names_in_
            missing_features = set(required_features) - set(input_df.columns)
            if missing_features:
                raise ValueError(f"Missing required features: {missing_features}")
            
            # Scale features
            X_scaled = self.scaler.transform(input_df[required_features])
            
            # Make prediction
            weakness_level = self.model.predict(X_scaled)[0]
            confidence = np.max(self.model.predict_proba(X_scaled)[0])
            
            # Identify weak topics (example logic - customize based on your needs)
            weak_topics = [
                feature for feature, value in student_data.items()
                if 'topic' in feature.lower() and value < 0.6
            ]
            
            # Get recommendations
            recommendations = self.get_recommendations(weakness_level, weak_topics)
            
            return {
                'weakness_level': weakness_level,
                'confidence': float(confidence),
                'weak_topics': weak_topics,
                'recommendations': recommendations
            }
            
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            return None

# Example usage
def example_usage():
    """Demonstrate usage of the WeaknessPredictor class"""
    
    # Sample student data
    sample_data = {
        'quiz_score': 75,
        'time_taken': 45,
        'attempts': 2,
        'topic_algebra': 0.65,
        'topic_calculus': 0.45,
        'topic_statistics': 0.80,
        'previous_performance': 0.70,
        'engagement_score': 0.85
    }
    
    # Create predictor instance
    predictor = WeaknessPredictor()
    
    # Make prediction
    result = predictor.predict_weakness(sample_data)
    
    if result:
        print("\nPrediction Results:")
        print(f"Weakness Level: {result['weakness_level']}")
        print(f"Confidence: {result['confidence']:.2%}")
        print("\nWeak Topics:")
        for topic in result['weak_topics']:
            print(f"- {topic}")
        print("\nRecommendations:")
        for rec in result['recommendations']:
            print(f"- {rec}")

if __name__ == "__main__":
    example_usage()