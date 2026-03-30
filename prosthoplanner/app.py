from flask import Flask, jsonify
from flask_cors import CORS

from routes.auth_routes import auth_routes
from routes.patient_routes import patient_routes
from routes.imaging_routes import imaging_routes
from routes.simulation_routes import simulation_routes
from backend.db_manager import DatabaseManager

app = Flask(__name__)
CORS(app)

# Initialize DB schema
db = DatabaseManager()
db.ensure_schema_stability()

app.register_blueprint(auth_routes, url_prefix='/api')
app.register_blueprint(patient_routes, url_prefix='/api')
app.register_blueprint(imaging_routes, url_prefix='/api')
app.register_blueprint(simulation_routes, url_prefix='/api')

@app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "ok", "message": "Backend is live on port 8076"}), 200

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "ProsthoPlanner Unified Backend is running"}), 200

if __name__ == "__main__":
    print("--- UNIFIED SERVER STARTUP ---")
    print("Starting ProsthoPlanner Backend on port 8076...")
    app.run(host='0.0.0.0', port=8076, debug=True)