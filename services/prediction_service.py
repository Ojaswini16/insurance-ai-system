import numpy as np
import joblib

MODEL_PATH = "model/fraud_model.pkl"

def predict_claim(data):

    model = joblib.load(MODEL_PATH)

    features = np.array([[

        data["age"],
        data["tenure"],
        data["premium_amount"],
        data["claim_amount"],
        data["family_members"],
        data["risk_segmentation"]

    ]])

    prob = model.predict_proba(features)[0][1]

    risk_score = round(prob*100,2)

    prediction = model.predict(features)[0]

    if risk_score < 30:
        level="LOW"
    elif risk_score < 60:
        level="MEDIUM"
    else:
        level="HIGH"

    decision = "Fraud Risk Detected" if prediction==1 else "Valid Claim"

    return prediction,risk_score,decision,features,level