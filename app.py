from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import os
import sqlite3

from services.prediction_service import predict_claim
from services.explain_service import explain_prediction
from services.chatbot_service import chatbot_response
from services.document_verifier import verify_document
from services.insurance_recommender import recommend_insurance
from database import init_db, save_claim

app = Flask(__name__)

init_db()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ── Home ──────────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html")


# ── Predict (Manual Form) ─────────────────────────────────────────────────────
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = {
            "age":              int(request.form["age"]),
            "tenure":           int(request.form["tenure"]),
            "premium_amount":   float(request.form["premium_amount"]),
            "claim_amount":     float(request.form["claim_amount"]),
            "family_members":   int(request.form["family_members"]),
            "risk_segmentation": int(request.form["risk_segmentation"]),
        }
    except (KeyError, ValueError) as e:
        return render_template("index.html", error=f"Invalid input: {e}"), 400

    pred, score, decision, features, level = predict_claim(data)
    raw_explanation = explain_prediction(features)
    recommendation  = recommend_insurance(data)
    save_claim(data, score, decision)

    # Normalize SHAP / list values → plain Python floats so Jinja2 can do math
    explanation = {}
    if raw_explanation:
        for k, v in raw_explanation.items():
            try:
                # SHAP returns arrays/lists like [0.125, 0.125]; take first element
                scalar = float(v[0]) if hasattr(v, '__iter__') and not isinstance(v, str) else float(v)
                explanation[k] = abs(scalar)          # use absolute importance
            except (TypeError, IndexError, ValueError):
                explanation[k] = 0.0

    return render_template(
        "result.html",
        score=score,
        decision=decision,
        level=level,
        explanation=explanation,
        recommendation=recommendation,
        # Pass original inputs so result page can display them
        age=data["age"],
        tenure=data["tenure"],
        premium=data["premium_amount"],
        claim_amount=data["claim_amount"],
        family=data["family_members"],
        risk=data["risk_segmentation"],
    )


# ── Upload CSV (Bulk Analysis) ────────────────────────────────────────────────
@app.route("/upload_csv", methods=["POST"])
def upload_csv():
    if "file" not in request.files or request.files["file"].filename == "":
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    try:
        df = pd.read_csv(file)
    except Exception as e:
        return jsonify({"error": f"Could not parse CSV: {e}"}), 400

    required_cols = {"AGE", "TENURE", "PREMIUM_AMOUNT", "CLAIM_AMOUNT",
                     "NO_OF_FAMILY_MEMBERS", "RISK_SEGMENTATION"}
    missing = required_cols - set(df.columns)
    if missing:
        return jsonify({"error": f"Missing columns: {missing}"}), 400

    results = []
    for _, row in df.iterrows():
        data = {
            "age":               row["AGE"],
            "tenure":            row["TENURE"],
            "premium_amount":    row["PREMIUM_AMOUNT"],
            "claim_amount":      row["CLAIM_AMOUNT"],
            "family_members":    row["NO_OF_FAMILY_MEMBERS"],
            "risk_segmentation": row["RISK_SEGMENTATION"],
        }
        pred, score, decision, _, level = predict_claim(data)
        results.append({"risk_score": score, "decision": decision, "level": level})

    return jsonify(results)


# ── Chatbot ───────────────────────────────────────────────────────────────────
@app.route("/chatbot", methods=["POST"])
def chatbot():
    body = request.get_json(silent=True)
    if not body or "message" not in body:
        return jsonify({"error": "No message provided"}), 400

    reply = chatbot_response(body["message"])
    return jsonify({"reply": reply})


# ── Document Verification ─────────────────────────────────────────────────────
@app.route("/verify_document", methods=["POST"])
def verify_doc():
    if "file" not in request.files or request.files["file"].filename == "":
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    result = verify_document(path)
    return jsonify({"verification": result})


# ── History ───────────────────────────────────────────────────────────────────
@app.route("/history")
def history():
    conn = sqlite3.connect("claims.db")
    conn.row_factory = sqlite3.Row          # rows behave like dicts
    cursor = conn.execute("SELECT * FROM history ORDER BY id DESC")
    columns = [desc[0].lower() for desc in cursor.description]
    rows_raw = cursor.fetchall()
    conn.close()

    # Convert to plain dicts so Jinja2 can access by name safely
    rows = [dict(zip(columns, tuple(r))) for r in rows_raw]

    return render_template("history.html", rows=rows, columns=columns)


# ── Debug: inspect DB schema (remove in production) ──────────────────────────
@app.route("/db_schema")
def db_schema():
    conn = sqlite3.connect("claims.db")
    info = conn.execute("PRAGMA table_info(history)").fetchall()
    conn.close()
    return jsonify([{"cid": r[0], "name": r[1], "type": r[2]} for r in info])


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)