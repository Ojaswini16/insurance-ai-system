import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


DATASET_PATH = "dataset/insurance_data.csv"
MODEL_PATH = "model/fraud_model.pkl"


def train_model():

    print("Loading dataset...")

    df = pd.read_csv(DATASET_PATH)

    print("Dataset loaded")

    # Create fraud label
    df["fraud"] = np.where(
        df["CLAIM_AMOUNT"] > df["PREMIUM_AMOUNT"] * 5,
        1,
        0
    )

    X = df.drop("fraud", axis=1)
    y = df["fraud"]

    print("Training model...")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=200)

    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    acc = accuracy_score(y_test, preds)

    joblib.dump(model, MODEL_PATH)

    print("Model trained successfully")
    print("Accuracy:", acc)
    print("Model saved at:", MODEL_PATH)


if __name__ == "__main__":
    train_model()