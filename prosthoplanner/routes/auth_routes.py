from flask import Blueprint, request, jsonify
from backend.db_manager import DatabaseManager
from backend.utils.otp_manager import OTPManager

auth_routes = Blueprint('auth_routes', __name__)
db = DatabaseManager()
otp_mgr = OTPManager()

# Ensure schema is up to date on start
db.ensure_schema_stability()

@auth_routes.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400
        
    full_name = data.get("full_name")
    email = data.get("email")
    mobile = data.get("mobile_number")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    if not all([full_name, email, mobile, password]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400
        
    if password != confirm_password:
        return jsonify({"status": "error", "message": "Passwords do not match"}), 400

    success, message = db.create_user(full_name, email, mobile, password)
    if success:
        # Generate OTP for verification
        otp = otp_mgr.generate_otp()
        db.save_otp(email, otp)
        otp_mgr.send_otp(email, otp)
        return jsonify({
            "status": "success", 
            "message": "Signup initiated. OTP sent to email.",
            "email": email,
            "otp": otp
        }), 201
    else:
        return jsonify({"status": "error", "message": message}), 400

@auth_routes.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    email = data.get('email')
    otp = data.get('otp')
    
    if not email or not otp:
        return jsonify({"status": "error", "message": "Email and OTP required"}), 400
        
    if db.verify_user_otp(email, otp):
        return jsonify({"status": "success", "message": "Account verified successfully"}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid or expired OTP"}), 400

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"status": "error", "message": "Email and password required"}), 400
        
    user = db.authenticate_user(email, password)
    if user:
        if not user.get('is_verified'):
            return jsonify({"status": "error", "message": "Account not verified", "requires_otp": True}), 403
            
        user.pop('password_hash', None) # Security
        user.pop('otp_code', None)
        return jsonify({"status": "success", "user": user}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid email or password"}), 401

@auth_routes.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')
    
    if not email:
        return jsonify({"status": "error", "message": "Email required"}), 400
        
    # Check if user exists (simple implementation by trying to save OTP)
    otp = otp_mgr.generate_otp()
    if db.save_otp(email, otp):
        otp_mgr.send_otp(email, otp) # Console mock
        return jsonify({"status": "success", "message": "Password reset OTP sent", "email": email, "otp": otp}), 200
    else:
        return jsonify({"status": "error", "message": "Email not found"}), 404

@auth_routes.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get('email')
    otp = data.get('otp')
    new_password = data.get('new_password')
    
    if not all([email, otp, new_password]):
        return jsonify({"status": "error", "message": "Missing fields"}), 400
        
    # First verify OTP (this also clears it)
    if db.verify_user_otp(email, otp):
        if db.reset_user_password(email, new_password):
            return jsonify({"status": "success", "message": "Password updated successfully"}), 200
        else:
            return jsonify({"status": "error", "message": "Failed to update password"}), 500
    else:
        return jsonify({"status": "error", "message": "Invalid or expired OTP"}), 400

@auth_routes.route('/resend-otp', methods=['POST'])
def resend_otp():
    data = request.json
    email = data.get('email')
    if not email:
        return jsonify({"status": "error", "message": "Email required"}), 400
        
    otp = otp_mgr.generate_otp()
    if db.save_otp(email, otp):
        otp_mgr.send_otp(email, otp)
        return jsonify({"status": "success", "message": "New OTP sent", "otp": otp}), 200
    else:
        return jsonify({"status": "error", "message": "User not found"}), 404
