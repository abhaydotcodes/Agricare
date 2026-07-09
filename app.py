from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import os

from mysql.connector import Error

# ------------------- FLASK APP -------------------
app = Flask(__name__)
CORS(app)  # allow frontend requests

# ------------------- HELPER FUNCTION -------------------
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("MYSQLHOST"),
            user=os.getenv("MYSQLUSER"),
            password=os.getenv("MYSQLPASSWORD"),
            database=os.getenv("MYSQLDATABASE"),
            port=int(os.getenv("MYSQLPORT", 3306))
        )
        return conn
    except Error as e:
        print("Error connecting to MySQL:", e)
        return None

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

    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_pw)
        )
        conn.commit()
        return jsonify({"message": "Signup successful"}), 200
    except mysql.connector.IntegrityError:
        return jsonify({"message": "Email already exists"}), 400
    except Exception as e:
        print("Database error:", e)
        return jsonify({"message": "Signup failed"}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, password FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        if user and check_password_hash(user['password'], password):
            return jsonify({"message": "Login successful", "user_id": user['id']}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        print("Database error:", e)
        return jsonify({"message": "Login failed"}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# ------------------- CROPS -------------------
@app.route('/crops', methods=['GET'])
def get_crops():
    conn = get_db_connection()
    if not conn:
        return jsonify([])

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT crop_id, crop_name FROM crops ORDER BY crop_name")
        crops = cursor.fetchall()
        return jsonify(crops)
    except Exception as e:
        print("Database error:", e)
        return jsonify([])
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# ------------------- DISTRICTS -------------------
@app.route('/districts', methods=['GET'])
def get_districts():
    conn = get_db_connection()
    if not conn:
        return jsonify([])

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT district_id, name FROM districts ORDER BY name")
        districts = cursor.fetchall()
        return jsonify(districts)
    except Exception as e:
        print("Database error:", e)
        return jsonify([])
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/subdistricts/<int:district_id>', methods=['GET'])
def get_subdistricts(district_id):
    conn = get_db_connection()
    if not conn:
        return jsonify([])

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT subdistrict_id, name FROM subdistricts WHERE district_id=%s ORDER BY name",
            (district_id,)
        )
        subdistricts = cursor.fetchall()
        return jsonify(subdistricts)
    except Exception as e:
        print("Database error:", e)
        return jsonify([])
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# ------------------- SOILS -------------------
@app.route('/soils', methods=['GET'])
def get_soils():
    conn = get_db_connection()
    if not conn:
        return jsonify([])

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT soil_id, soil_name FROM soils ORDER BY soil_name")
        soils = cursor.fetchall()
        return jsonify(soils)
    except Exception as e:
        print("Database error:", e)
        return jsonify([])
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# ------------------- FIELD ADVISORY -------------------
@app.route('/field-advisory', methods=['POST'])
def field_advisory():
    data = request.get_json()
    district = data.get("district")
    subdistrict = data.get("subdistrict")
    soil = data.get("soil")

    if not district or not subdistrict or not soil:
        return jsonify({"message": "Please select district, subdistrict, and soil"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT c.crop_name
            FROM crops c
            JOIN crop_suitability cs ON c.crop_id = cs.crop_id
            WHERE cs.district_id=%s AND cs.subdistrict_id=%s AND cs.soil_id=%s
            ORDER BY c.crop_name
        """
        cursor.execute(query, (district, subdistrict, soil))
        crops = [row['crop_name'] for row in cursor.fetchall()]
        return jsonify({"suggested_crops": crops})
    except Exception as e:
        print("Database error:", e)
        return jsonify({"message": "Failed to fetch crop suggestions"}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# ------------------- ADVISORIES -------------------
@app.route('/advisory', methods=['POST'])
def submit_advisory():
    data = request.get_json()
    crop_id = data.get("crop")
    district_id = data.get("district")
    subdistrict_id = data.get("subdistrict")
    soil_id = data.get("soil")
    severity = data.get("severity")

    if not crop_id or not district_id or not subdistrict_id or not soil_id or not severity:
        return jsonify({"message": "All fields are required"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO advisories (crop_id, district_id, subdistrict_id, soil_id, severity) VALUES (%s, %s, %s, %s, %s)",
            (crop_id, district_id, subdistrict_id, soil_id, severity)
        )
        conn.commit()
        return jsonify({"message": "Advisory saved successfully"}), 200
    except Exception as e:
        print("Database error:", e)
        return jsonify({"message": "Failed to save advisory"}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# ------------------- FETCH ADVISORY TEXT -------------------
@app.route('/get-advisory', methods=['POST'])
def get_advisory():
    """
    Fetch advisory text from crop_advisories table
    Request JSON: { "crop": 1, "severity": "Low" }
    """
    data = request.get_json()
    crop_id = data.get("crop")
    severity = data.get("severity")

    if not crop_id or not severity:
        return jsonify({"message": "Crop ID and severity are required"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT advisory_text FROM crop_advisories WHERE crop_id=%s AND severity=%s",
            (crop_id, severity)
        )
        result = cursor.fetchone()
        if result:
            return jsonify({"message": "Advisory found", "advisory": result["advisory_text"]}), 200
        else:
            return jsonify({"message": "No advisory available for this crop and severity"}), 404
    except Exception as e:
        print("Database error:", e)
        return jsonify({"message": "Failed to fetch advisory"}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# ------------------- CONTACT FORM -------------------
@app.route('/submit', methods=['POST'])
def submit_contact():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not name or not email or not message:
        return jsonify({"message": "All fields are required"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"message": "Database connection failed"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO contact_messages (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message)
        )
        conn.commit()
        return jsonify({"message": "Message received successfully"}), 200
    except Exception as e:
        print("Database error:", e)
        return jsonify({"message": "Failed to save message"}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# ------------------- CROP PRICE TRENDS -------------------
@app.route('/crop-price-trends', methods=['POST'])
def crop_price_trends():
    """
    Request JSON: { "crops": ["Wheat", "Rice"] }
    Response: month-wise prices for these crops
    """
    data = request.get_json()
    selected_crops = data.get("crops", [])

    if not selected_crops:
        return jsonify({"message": "No crops selected"}), 400

    # Approximate prices dataset
    price_data = {
        "Wheat": [2600,2580,2550,2620,2650,2680,2650,2620,2600,2580,2550,2580],
        "Rice": [3200,3180,3150,3170,3190,3220,3250,3270,3250,3220,3200,3180],
        "Maize": [2000,2020,2050,2080,2100,2150,2200,2180,2150,2100,2050,2020],
        "Cotton": [7800,7850,7900,7950,8000,8050,8100,8150,8100,8050,8000,7950],
        "Sugarcane": [2850,2900,2950,3000,3050,3100,3150,3120,3100,3050,3000,2950],
        "Barley": [950,940,930,920,910,900,890,880,870,860,850,840],
        "Mustard": [2100,2200,2300,2350,2400,2450,2500,2480,2450,2400,2350,2300],
        "Potato": [1300,1250,1200,1150,1100,1050,1100,1150,1200,1250,1300,1350],
        "Soybeans": [5000,5050,5100,5150,5200,5250,5300,5350,5300,5250,5200,5150],
        "Cabbage": [1500,1480,1450,1420,1400,1380,1400,1420,1450,1480,1500,1520],
        "Tomato": [1800,2000,2200,2300,2400,2350,2300,2250,2200,2100,2000,1900],
        "Onion": [1700,1650,1600,1550,1500,1480,1500,1520,1550,1600,1650,1700],
        "Chillies": [4500,4550,4600,4650,4700,4750,4800,4750,4700,4650,4600,4550],
        "Pulses": [5700,5750,5800,5850,5900,5950,6000,6050,6000,5950,5900,5850]
    }

    # Filter only selected crops
    result = {crop: price_data[crop] for crop in selected_crops if crop in price_data}

    return jsonify({"months": ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"], 
                    "prices": result})


# ------------------- HELPER FUNCTION -------------------
@app.route("/test-db")
def test_db():
    conn = get_db_connection()
    if conn:
        return "✅ Connected to MySQL!"
    else:
        return "❌ DB connection failed", 500


@app.route("/test-crops")
def test_crops():
    conn = get_db_connection()
    if not conn:
        return "❌ DB connection failed"
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM crops")
        count = cursor.fetchone()[0]
        return f"✅ Connected! Crops count: {count}"
    except Exception as e:
        return f"❌ DB error: {e}"
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# ------------------- CHATBOT -------------------
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    query = data.get("query", "")

    if not query:
        return jsonify({"answer": "⚠️ Please enter a query"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",   # or another model like gpt-3.5-turbo
            messages=[{"role": "user", "content": query}]
        )
        answer = response.choices[0].message.content
    except Exception as e:
        print("Chatbot error:", e)
        answer = "❌ Chatbot is temporarily unavailable"

    return jsonify({"answer": answer}), 200


# ------------------- RUN APP -------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)

