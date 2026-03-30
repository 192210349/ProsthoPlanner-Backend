from flask import Blueprint, request, jsonify
from backend.db_manager import DatabaseManager
from backend.ai_engine import AIEngine

patient_routes = Blueprint('patient_routes', __name__)
db = DatabaseManager()
ai = AIEngine()

@patient_routes.route('/register-patient', methods=['POST'])
def register_patient():
    """Initial patient record creation"""
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    patient_id = db.register_patient(data)
    if patient_id:
        return jsonify({"status": "success", "patient_db_id": patient_id}), 201
    else:
        return jsonify({"error": "Failed to register patient"}), 500

@patient_routes.route('/ai-analysis', methods=['POST'])
def ai_analysis():
    """Returns preliminary vision insights for a case"""
    data = request.json
    patient_id = data.get('patient_db_id')
    if not patient_id:
        return jsonify({"error": "patient_db_id required"}), 400
        
    vision_data = db.get_latest_vision_data(patient_id)
    return jsonify({
        "status": "success",
        "vision_insights": vision_data,
        "message": "Preliminary analysis complete"
    }), 200

@patient_routes.route('/suggest-treatment', methods=['POST'])
def suggest_treatment():
    """Full AI treatment suggestion flow"""
    data = request.json
    # If data has patient_db_id, use it. Otherwise register.
    patient_id = data.get('patient_db_id')
    if not patient_id:
        patient_id = db.register_patient(data)
    
    if not patient_id:
        return jsonify({"error": "Failed to identify/register patient"}), 500
    
    vision_data = db.get_latest_vision_data(patient_id)
    plans = ai.suggest(data, vision_data=vision_data)
    
    if not plans:
        return jsonify({"error": "AI Engine could not generate plans"}), 500
    
    db.save_suggestion(patient_id, plans)
    return jsonify({
        "status": "success", 
        "patient_db_id": patient_id, 
        "plans": plans
    }), 200

@patient_routes.route('/select-plan', methods=['POST'])
def select_plan():
    data = request.json
    db.update_plan_selection(data.get('patient_db_id'), data.get('selection'))
    return jsonify({"status": "success"}), 200

@patient_routes.route('/patients', methods=['GET'])
def list_patients():
    patients = db.get_all_patients()
    return jsonify({"status": "success", "patients": patients}), 200
