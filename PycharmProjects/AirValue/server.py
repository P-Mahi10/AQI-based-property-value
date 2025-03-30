from flask import Flask, jsonify, request
from flask_cors import CORS
from data import data  # Import properties from data.py
import pandas as pd

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Allow frontend

# Ensure each property has an integer ID
for i, p in enumerate(data):
    p["id"] = i + 1  # Assigning sequential IDs if missing

# API to get all properties
@app.route('/properties', methods=['GET'])
def get_properties():
    return jsonify(data)

# API to search properties by name or location
@app.route('/search', methods=['GET'])
def search_properties():
    query = request.args.get('query', '').strip().lower()
    if not query:
        return jsonify([])
    filtered_properties = [p for p in data if query in p.get("name", "").lower() or query in p.get("location", "").lower()]
    return jsonify(filtered_properties)

# ✅ NEW API: Get details for a specific property by ID
@app.route('/property/<int:property_id>', methods=['GET'])
def get_property_details(property_id):
    property_item = next((p for p in data if p.get("id") == property_id), None)

    if property_item is None:
        return jsonify({"error": "Property not found"}), 404

    return jsonify(property_item)  # Send full property data

# Load the CSV file
csv_file = "properties_final.csv"  # Update if needed
df = pd.read_csv("properties_final.csv")


@app.route("/area-health-data", methods=["GET"])
def get_area_health_data():
    try:
        df = pd.read_csv("properties_aggregated.csv")  # Change to your actual CSV file name
        data = df.to_dict(orient="records")  # Convert DataFrame to list of dicts
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
