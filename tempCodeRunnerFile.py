from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)  # allow frontend requests

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",        # change if needed
    password="12345678",    # change if needed
    database="SIH"
)
cursor = db.cursor()

# ------------------- USER AUTH -------------------

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    hashed_pw = generate_password_hash(password)

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_pw)
        )
        db.commit()
        return jsonify({"message": "Signup successful"}), 200
    except Exception as e:
        print("Database error:", e)
        return jsonify({"message": "Signup failed"}), 500


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    cursor.execute("SELECT id, password FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()

    if user and check_password_hash(user[1], password):
        return jsonify({"message": "Login successful", "user_id": user[0]}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


# ------------------- CROPS -------------------

@app.route('/crops', methods=['GET'])
def get_crops():
    cursor.execute("SELECT crop_id, crop_name FROM crops")
    crops = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
    return jsonify(crops)


# ------------------- DISTRICTS -------------------

@app.route('/districts', methods=['GET'])
def get_districts():
    cursor.execute("SELECT district_id, name FROM districts")
    districts = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
    return jsonify(districts)


@app.route('/subdistricts/<int:district_id>', methods=['GET'])
def get_subdistricts(district_id):
    cursor.execute(
        "SELECT subdistrict_id, name FROM subdistricts WHERE district_id=%s",
        (district_id,)
    )
    subdistricts = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
    return jsonify(subdistricts)


# ------------------- ADVISORIES -------------------

@app.route('/advisory', methods=['POST'])
def submit_advisory():
    data = request.get_json()
    crop_id = data.get("crop")
    district_id = data.get("district")
    subdistrict_id = data.get("subdistrict")
    severity = data.get("severity")

    if not crop_id or not district_id or not subdistrict_id or not severity:
        return jsonify({"message": "All fields are required"}), 400

    try:
        cursor.execute(
            "INSERT INTO advisories (crop_id, district_id, subdistrict_id, severity) VALUES (%s, %s, %s, %s)",
            (crop_id, district_id, subdistrict_id, severity)
        )
        db.commit()
        return jsonify({"message": "Advisory saved successfully"}), 200
    except Exception as e:
        print("Database error:", e)
        return jsonify({"message": "Failed to save advisory"}), 500


if __name__ == '__main__':
    app.run(debug=True)

 