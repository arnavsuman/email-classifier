import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from joblib import dump
import os

print("Import complete Starting trainig")

def train_model():
    df = pd.read_csv('combined_emails_with_natural_pii.csv')  

    print(" Splitting dataset into train and test")
    X_train, X_test, y_train, y_test = train_test_split(df['email'], df['type'], test_size=0.2, random_state=42)
    print(f" Training samples: {len(X_train)}, Test samples: {len(X_test)}")

    # Pipeline: TF-IDF + SVM
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', SVC(kernel='linear', probability=True))
    ])

    print("Training model")
    pipeline.fit(X_train, y_train)
    print("Model training complete.")

    os.makedirs("model_checkpoints", exist_ok=True)

    # Save model
    dump(pipeline, 'model_checkpoints/tfidf_svm_model.pkl')
    print("Model trained and saved to model_checkpoints/")

if __name__ == "__main__":
    train_model()
