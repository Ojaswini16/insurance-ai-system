import shap
import joblib
import numpy as np

MODEL_PATH = "model/fraud_model.pkl"

def explain_prediction(features):

    model = joblib.load(MODEL_PATH)

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(features)

    if isinstance(shap_values,list):
        importance=np.abs(shap_values[0][0])
    else:
        importance=np.abs(shap_values[0])

    names=[
    "AGE",
    "TENURE",
    "PREMIUM_AMOUNT",
    "CLAIM_AMOUNT",
    "FAMILY_MEMBERS",
    "RISK_SEGMENTATION"
    ]

    return dict(zip(names,importance.tolist()))