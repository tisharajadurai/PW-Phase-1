# from flask import Flask, request, jsonify, session
# from flask_cors import CORS
# import random
# import json
# from datetime import datetime
# from typing import Dict, Any
# import os
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# app.secret_key = "YOUR_SECRET_KEY_123"   # Change this later
# CORS(app, supports_credentials=True)

# # ---------------------------------------------------------------
# # Helper: mock SHAP explanation
# # ---------------------------------------------------------------
# def shap_mock() -> list[Dict[str, Any]]:
#     feats = [
#         "Attention Variability", "Reaction Time", "AQ-10 Score",
#         "Task Accuracy", "Impulsivity Index", "Consistency"
#     ]
#     shap_data = []
#     for f in feats:
#         impact = round(random.uniform(-1, 1), 2)
#         shap_data.append({
#             "feature": f,
#             "impact": impact,
#             "direction": "Increased" if impact > 0 else "Decreased",
#             "value": round(random.uniform(0, 1), 2)
#         })
#     shap_data.sort(key=lambda x: abs(x["impact"]), reverse=True)
#     return shap_data


# # ---------------------------------------------------------------
# # Home route
# # ---------------------------------------------------------------
# @app.route('/')
# def home():
#     return jsonify({"message": "Backend running"})


# # ---------------------------------------------------------------
# # Login system (JSON Storage)
# # ---------------------------------------------------------------
# USERS_FILE = "users.json"


# def read_users():
#     if not os.path.exists(USERS_FILE):
#         return {}
#     try:
#         with open(USERS_FILE, "r") as f:
#             return json.load(f)
#     except:
#         return {}


# def write_users(data):
#     with open(USERS_FILE, "w") as f:
#         json.dump(data, f, indent=4)


# # ------------------- REGISTER -------------------
# @app.route('/api/register', methods=['POST'])
# def register_user():
#     data = request.json
#     username = data.get("username")
#     password = data.get("password")

#     if not username or not password:
#         return jsonify({"error": "Missing fields"}), 400

#     users = read_users()

#     if username in users:
#         return jsonify({"error": "Username already exists"}), 400

#     # 🔐 Password hashing
#     hashed_pw = generate_password_hash(password)

#     users[username] = {
#         "password": hashed_pw
#     }

#     write_users(users)

#     return jsonify({"status": "registered"}), 200


# # ------------------- LOGIN -------------------
# @app.route('/api/login', methods=['POST'])
# def login_user():
#     data = request.json
#     username = data.get("username")
#     password = data.get("password")

#     users = read_users()

#     if username not in users:
#         return jsonify({"error": "User not found"}), 404

#     hashed_pw = users[username]["password"]

#     # 🔐 Secure password check
#     if not check_password_hash(hashed_pw, password):
#         return jsonify({"error": "Invalid password"}), 400

#     # Save login in session
#     session["username"] = username

#     return jsonify({"status": "login_success", "username": username}), 200


# # ------------------- LOGOUT -------------------
# @app.route('/api/logout', methods=['POST'])
# def logout():
#     session.pop("username", None)
#     return jsonify({"status": "logged_out"}), 200


# # ------------------- CHECK LOGIN -------------------
# @app.route('/api/check_login', methods=['GET'])
# def check_login():
#     if "username" in session:
#         return jsonify({"logged_in": True, "username": session["username"]}), 200
#     return jsonify({"logged_in": False}), 200


# # ---------------------------------------------------------------
# # Assessment (Prediction)
# # ---------------------------------------------------------------
# @app.route('/api/assess', methods=['POST'])
# def assess():
#     try:
#         data = request.get_json()

#         name = data.get("name", "")
#         age = data.get("age", 0)
#         gender = data.get("gender", "")
#         relation = data.get("relation", "")
#         aq10_answers: Dict[int, int] = data.get("aq10_answers", {})
#         cpt_data: Dict[str, Any] = data.get("cpt_data", {})

#         scoring_key = [1, 0, 0, 0, 0, 0, 1, 1, 0, 1]
#         aq10_score = 0
#         for i in range(10):
#             raw = aq10_answers.get(i, 0)
#             aq10_score += 1 if raw == scoring_key[i] else 0

#         cpt_accuracy = cpt_data.get("accuracy", 0)
#         cpt_avg_rt = cpt_data.get("avg_reaction_time", 0)
#         cpt_errors = cpt_data.get("errors", 0)
#         cpt_missed = cpt_data.get("missed", 0)
#         cpt_correct = cpt_data.get("correct", 0)
#         cpt_total_x = cpt_data.get("total_x", 0)

#         adhd_prob = round(random.uniform(0.1, 0.95), 2)
#         asd_prob = round(random.uniform(0.1, 0.95), 2)

#         response = {
#             "adhd": {
#                 "prediction": "Positive" if adhd_prob > 0.5 else "Negative",
#                 "probability": adhd_prob,
#                 "confidence": round(random.uniform(0.4, 0.9), 2),
#                 "shap_explanation": shap_mock()
#             },
#             "asd": {
#                 "prediction": "Positive" if asd_prob > 0.5 else "Negative",
#                 "probability": asd_prob,
#                 "confidence": round(random.uniform(0.4, 0.9), 2),
#                 "shap_explanation": shap_mock()
#             },
#             "raw_features": {
#                 "name": name,
#                 "age": age,
#                 "gender": gender,
#                 "relation": relation,
#                 "aq10_score": aq10_score,
#                 "cpt_accuracy": round(cpt_accuracy, 2),
#                 "cpt_avg_rt": round(cpt_avg_rt, 0),
#                 "cpt_errors": cpt_errors,
#                 "cpt_missed": cpt_missed,
#                 "cpt_correct": cpt_correct,
#                 "cpt_total_x": cpt_total_x
#             }
#         }

#         return jsonify(response)

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# # ---------------------------------------------------------------
# # Save Assessment
# # ---------------------------------------------------------------
# @app.route('/api/save_assessment', methods=['POST'])
# def save_assessment():
#     try:
#         payload = request.json
#         payload["saved_at"] = datetime.utcnow().isoformat() + "Z"

#         with open("assessments.json", "a", encoding="utf-8") as f:
#             json.dump(payload, f)
#             f.write("\n")

#         return jsonify({"status": "saved"}), 200

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500


# # ---------------------------------------------------------------
# # History
# # ---------------------------------------------------------------
# @app.route('/api/get_history', methods=['GET'])
# def get_history():
#     if not os.path.exists("assessments.json"):
#         return jsonify([])

#     records = []
#     with open("assessments.json", "r", encoding="utf-8") as f:
#         for line in f:
#             try:
#                 records.append(json.loads(line))
#             except:
#                 pass

#     return jsonify(records)


# # ---------------------------------------------------------------
# # Run
# # ---------------------------------------------------------------
# if __name__ == '__main__':
#     print("Backend running at http://localhost:5000")
#     app.run(host="0.0.0.0", port=5000, debug=True)



# main.py
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import random
import json
from datetime import datetime
from typing import Dict, Any
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super_secret_key_change_in_production_2025"
CORS(app, supports_credentials=True)  # Allows cookies from frontend

USERS_FILE = "users.json"
ASSESSMENTS_FILE = "assessments.json"

# ------------------- Helper Functions -------------------
def read_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def write_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def shap_mock():
    feats = ["Attention Variability", "Reaction Time", "AQ-10 Score", "Task Accuracy", "Impulsivity Index", "Consistency"]
    data = []
    for f in feats:
        impact = round(random.uniform(-1, 1), 2)
        data.append({"feature": f, "impact": impact, "direction": "Increased" if impact > 0 else "Decreased", "value": round(random.uniform(0, 1), 2)})
    data.sort(key=lambda x: abs(x["impact"]), reverse=True)
    return data

# ------------------- Routes -------------------
@app.route('/')
def home():
    return jsonify({"message": "ADHD & ASD Classifier Backend Running", "status": "OK"})

# Register
@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    users = read_users()
    if username in users:
        return jsonify({"error": "Username already exists"}), 400

    users[username] = {"password": generate_password_hash(password)}
    write_users(users)
    return jsonify({"status": "registered", "username": username}), 200

# Login
@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    users = read_users()
    if username not in users or not check_password_hash(users[username]["password"], password):
        return jsonify({"error": "Invalid username or password"}), 401

    session["username"] = username
    return jsonify({"status": "login_success", "username": username}), 200

# Logout
@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop("username", None)
    return jsonify({"status": "logged_out"}), 200

# Check Login Status
@app.route('/api/check_login', methods=['GET'])
def check_login():
    if "username" in session:
        return jsonify({"logged_in": True, "username": session["username"]}), 200
    return jsonify({"logged_in": False}), 200

# Assessment Prediction
@app.route('/api/assess', methods=['POST'])
def assess():
    try:
        data = request.get_json()
        aq10_answers = data.get("aq10_answers", {})
        cpt_data = data.get("cpt_data", {})

        scoring_key = [1, 0, 0, 0, 0, 0, 1, 1, 0, 1]
        aq10_score = sum(1 for i in range(10) if aq10_answers.get(i, 0) == scoring_key[i])

        adhd_prob = round(random.uniform(0.1, 0.95), 2)
        asd_prob = round(random.uniform(0.1, 0.95), 2)

        return jsonify({
            "adhd": {"prediction": "Positive" if adhd_prob > 0.5 else "Negative", "probability": adhd_prob, "shap_explanation": shap_mock()},
            "asd": {"prediction": "Positive" if asd_prob > 0.5 else "Negative", "probability": asd_prob, "shap_explanation": shap_mock()},
            "raw_features": {"aq10_score": aq10_score, **cpt_data}
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Save Assessment
@app.route('/api/save_assessment', methods=['POST'])
def save_assessment():
    payload = request.json
    payload["saved_at"] = datetime.utcnow().isoformat() + "Z"
    payload["username"] = session.get("username", "guest")

    with open(ASSESSMENTS_FILE, "a", encoding="utf-8") as f:
        json.dump(payload, f)
        f.write("\n")
    return jsonify({"status": "saved"}), 200

# Get History
@app.route('/api/get_history', methods=['GET'])
def get_history():
    if not os.path.exists(ASSESSMENTS_FILE):
        return jsonify([])
    records = []
    with open(ASSESSMENTS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return jsonify(records)

if __name__ == '__main__':
    print("Backend running at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)