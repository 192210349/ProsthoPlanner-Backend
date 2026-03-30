from flask import Blueprint, request, jsonify
from backend.db_manager import DatabaseManager
import os

imaging_routes = Blueprint('imaging_routes', __name__)
db = DatabaseManager()

@imaging_routes.route('/upload-imaging', methods=['POST'])
def upload_imaging():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
        
    file = request.files['file']
    patient_id = request.form.get('patient_db_id')
    image_type = request.form.get('image_type') 
    
    if not patient_id or not image_type:
        return jsonify({"error": "Missing patient_db_id or image_type"}), 400
        
    # Simulated Vision Analysis
    vision_results = {}
    if image_type == 'OPG':
        vision_results = {"missing_teeth": [18, 28, 38, 48], "bone_loss_detected": True}
    elif image_type == 'CBCT':
        vision_results = {"bone_density": "Type II", "nerve_proximity": "3.5mm"}
    
    # Storage
    upload_dir = os.path.join("backend", "uploads", f"patient_{patient_id}")
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    file_path = os.path.join(upload_dir, file.filename)
    file.save(file_path)
    
    db.save_image_metadata(patient_id, image_type, file_path, vision_results)
    
    return jsonify({"status": "success", "vision_insights": vision_results}), 201
