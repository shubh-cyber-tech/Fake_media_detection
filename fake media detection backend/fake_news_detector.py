import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import re
import string
import pickle
import os

class FakeNewsDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.model = SGDClassifier(
            loss="hinge",
            penalty=None,
            learning_rate="pa1",
            eta0=1.0,
            max_iter=50,
            random_state=42
        )
        self.is_trained = False
        
    def preprocess_text(self, text):
        """Clean and preprocess text data"""
        if pd.isna(text):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def load_dataset(self, fake_csv_path='Fake.csv', true_csv_path='True.csv'):
        """Load the Fake.csv and True.csv files"""
        print("Loading dataset...")
        
        try:
            # Load fake news
            fake_df = pd.read_csv(fake_csv_path)
            fake_df['label'] = 0  # 0 for fake
            
            # Load true news
            true_df = pd.read_csv(true_csv_path)
            true_df['label'] = 1  # 1 for true
            
            # Combine datasets
            df = pd.concat([fake_df, true_df], ignore_index=True)
            
            # Combine title and text for better prediction
            df['content'] = df['title'] + ' ' + df['text']
            
            print(f"✓ Loaded {len(fake_df)} fake news articles")
            print(f"✓ Loaded {len(true_df)} true news articles")
            print(f"✓ Total: {len(df)} articles")
            
            return df
            
        except FileNotFoundError as e:
            print("Error: Could not find CSV files.")
            print(e)
            return None
    
    def train(self, fake_csv_path='Fake.csv', true_csv_path='True.csv'):
        """Train the fake news detector on the dataset"""
        df = self.load_dataset(fake_csv_path, true_csv_path)
        
        if df is None:
            return False
        
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        print("\nPreprocessing text...")
        df['processed_content'] = df['content'].apply(self.preprocess_text)
        
        X_train, X_test, y_train, y_test = train_test_split(
            df['processed_content'],
            df['label'],
            test_size=0.2,
            random_state=42
        )
        
        print("\nTraining model...")
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        X_test_tfidf = self.vectorizer.transform(X_test)
        
        self.model.fit(X_train_tfidf, y_train)
        
        predictions = self.model.predict(X_test_tfidf)
        accuracy = accuracy_score(y_test, predictions)
        
        print("\n" + "="*60)
        print("MODEL TRAINING COMPLETED!")
        print("="*60)
        print(f"Training Accuracy: {accuracy:.2%}")
        print("\nClassification Report:")
        print(classification_report(y_test, predictions,
                                    target_names=['Fake News', 'True News']))
        
        self.is_trained = True
        return True
    
    def predict(self, article_text):
        """Predict if a news article is fake or true"""
        if not self.is_trained:
            return {'error': 'Model not trained yet.'}
        
        processed_text = self.preprocess_text(article_text)
        X = self.vectorizer.transform([processed_text])
        
        prediction = self.model.predict(X)[0]
        decision = self.model.decision_function(X)[0]
        confidence = min(abs(decision) * 20, 99)
        
        return {
    'prediction': 'TRUE NEWS' if int(prediction) == 1 else 'FAKE NEWS',
    'confidence': f"{confidence:.1f}%",
    'label': int(prediction)   # ✅ convert numpy int64 → Python int
}

    
    def save_model(self, filename='fake_news_model.pkl'):
        if not self.is_trained:
            print("No trained model to save.")
            return False
        
        with open(filename, 'wb') as f:
            pickle.dump({
                'vectorizer': self.vectorizer,
                'model': self.model
            }, f)
        
        print(f"✓ Model saved to {filename}")
        return True
    
    def load_model(self, filename='fake_news_model.pkl'):
        try:
            with open(filename, 'rb') as f:
                data = pickle.load(f)

            if 'vectorizer' not in data or 'model' not in data:
                raise ValueError("Invalid model file structure")

            self.vectorizer = data['vectorizer']
            self.model = data['model']
            self.is_trained = True

            print(f"✓ Model loaded from {filename}")
            return True

        except Exception as e:
            print("❌ Error loading model:", e)
            self.is_trained = False
            return False



def main():
    print("="*60)
    print("FAKE NEWS DETECTOR")
    print("="*60)
    
    detector = FakeNewsDetector()
    
    print("\n[1] Training the model...")
    if detector.train():
        detector.save_model()
    else:
        print("Training failed.")
        return


if __name__ == "__main__":
    main()
