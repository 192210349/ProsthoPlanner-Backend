from flask import Blueprint, jsonify

simulation_routes = Blueprint('simulation_routes', __name__)

@simulation_routes.route('/simulation/status', methods=['GET'])
def simulation_status():
    return jsonify({"status": "ready", "message": "Simulation engine is operational"}), 200
