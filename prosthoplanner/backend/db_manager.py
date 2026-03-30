import pymysql
import pymysql.cursors
from werkzeug.security import generate_password_hash, check_password_hash
import json

class DatabaseManager:
    def __init__(self):
        self.config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "database": "prosthoplanner",
            "charset": "utf8mb4",
            "cursorclass": pymysql.cursors.DictCursor
        }

    def get_connection(self):
        try:
            return pymysql.connect(**self.config)
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return None

    def ensure_schema_stability(self):
        """Self-healing logic to ensure all required columns exist"""
        conn = self.get_connection()
        if not conn: return
        try:
            with conn.cursor() as cursor:
                # Add is_verified if missing
                try:
                    cursor.execute("ALTER TABLE users ADD COLUMN is_verified TINYINT(1) DEFAULT 0")
                except: pass
                # Add otp_code if missing
                try:
                    cursor.execute("ALTER TABLE users ADD COLUMN otp_code VARCHAR(10)")
                except: pass
                # Add otp_expiry if missing
                try:
                    cursor.execute("ALTER TABLE users ADD COLUMN otp_expiry DATETIME")
                except: pass
                conn.commit()
        finally:
            conn.close()

    def create_user(self, full_name, email, mobile, password):
        conn = self.get_connection()
        if not conn: return False, "Database connection failed"
        try:
            with conn.cursor() as cursor:
                hashed_pw = generate_password_hash(password)
                sql = "INSERT INTO users (full_name, email, mobile_number, password_hash) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (full_name, email, mobile, hashed_pw))
                conn.commit()
                return True, "User created successfully"
        except Exception as e:
            return False, str(e)
        finally:
            conn.close()

    def authenticate_user(self, email, password):
        conn = self.get_connection()
        if not conn: return None
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM users WHERE email = %s"
                cursor.execute(sql, (email,))
                user = cursor.fetchone()
                if user and check_password_hash(user['password_hash'], password):
                    return user
                return None
        finally:
            conn.close()

    def save_otp(self, email, otp_code):
        conn = self.get_connection()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                # Set expiry to 10 mins from now
                sql = "UPDATE users SET otp_code = %s, otp_expiry = DATE_ADD(NOW(), INTERVAL 10 MINUTE) WHERE email = %s"
                cursor.execute(sql, (otp_code, email))
                conn.commit()
                return cursor.rowcount > 0
        finally:
            conn.close()

    def verify_user_otp(self, email, otp_code):
        conn = self.get_connection()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                sql = "SELECT id FROM users WHERE email = %s AND otp_code = %s AND otp_expiry > NOW()"
                cursor.execute(sql, (email, otp_code))
                if cursor.fetchone():
                    # Clear OTP and mark as verified
                    cursor.execute("UPDATE users SET is_verified = 1, otp_code = NULL WHERE email = %s", (email,))
                    conn.commit()
                    return True
                return False
        finally:
            conn.close()

    def reset_user_password(self, email, new_password):
        conn = self.get_connection()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                hashed_pw = generate_password_hash(new_password)
                sql = "UPDATE users SET password_hash = %s WHERE email = %s"
                cursor.execute(sql, (hashed_pw, email))
                conn.commit()
                return cursor.rowcount > 0
        finally:
            conn.close()

    def register_patient(self, data):
        conn = self.get_connection()
        if not conn: return None
        try:
            with conn.cursor() as cursor:
                # Insert basic info
                sql_patient = "INSERT INTO patients (patient_external_id, full_name, age, gender, mobile_number) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql_patient, (data.get('patient_id'), data.get('full_name'), data.get('age'), data.get('gender'), data.get('mobile_number')))
                patient_db_id = cursor.lastrowid
                
                # Insert medical history
                sql_history = """INSERT INTO medical_history (patient_id, is_diabetic, has_hypertension, has_thyroid, has_asthma, is_smoker, drinks_alcohol, allergies, medications) 
                                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql_history, (
                    patient_db_id,
                    data.get('is_diabetic', 0),
                    data.get('has_hypertension', 0),
                    data.get('has_thyroid', 0),
                    data.get('has_asthma', 0),
                    data.get('is_smoker', 0),
                    data.get('drinks_alcohol', 0),
                    data.get('allergies', ''),
                    data.get('medications', '')
                ))
                
                # Insert clinical exam
                sql_exam = """INSERT INTO clinical_examinations (patient_id, edentulous_area, kennedy_classification, tissue_condition, occlusion_type, clinical_notes)
                              VALUES (%s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql_exam, (
                    patient_db_id,
                    data.get('edentulous_area', ''),
                    data.get('kennedy_classification', ''),
                    data.get('tissue_condition', ''),
                    data.get('occlusion_type', ''),
                    data.get('clinical_notes', '')
                ))
                
                conn.commit()
                return patient_db_id
        except Exception as e:
            conn.rollback()
            print(f"DB Error: {e}")
            return None
        finally:
            conn.close()

    def save_suggestion(self, patient_id, plans):
        conn = self.get_connection()
        if not conn: return
        try:
            with conn.cursor() as cursor:
                sql = """INSERT INTO treatment_suggestions 
                         (patient_id, plan_a_treatment, plan_a_cost, plan_a_time, 
                          plan_b_treatment, plan_b_cost, plan_b_time, 
                          plan_c_treatment, plan_c_cost, plan_c_time) 
                         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (
                    patient_id,
                    plans['A']['treatment'], plans['A']['cost'], plans['A']['time'],
                    plans['B']['treatment'], plans['B']['cost'], plans['B']['time'],
                    plans['C']['treatment'], plans['C']['cost'], plans['C']['time']
                ))
                conn.commit()
        except Exception as e:
            print(f"Error saving plans: {e}")
        finally:
            conn.close()

    def save_image_metadata(self, patient_id, image_type, file_path, vision_analysis=None):
        conn = self.get_connection()
        if not conn: return False
        try:
            with conn.cursor() as cursor:
                vision_json = json.dumps(vision_analysis) if vision_analysis else None
                sql = "INSERT INTO patient_imaging (patient_id, image_type, file_path, vision_analysis_json) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (patient_id, image_type, file_path, vision_json))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving image metadata: {e}")
            return False
        finally:
            conn.close()

    def get_latest_vision_data(self, patient_id):
        conn = self.get_connection()
        if not conn: return {}
        try:
            with conn.cursor() as cursor:
                sql = "SELECT vision_analysis_json FROM patient_imaging WHERE patient_id = %s ORDER BY uploaded_at DESC LIMIT 1"
                cursor.execute(sql, (patient_id,))
                row = cursor.fetchone()
                if row and row['vision_analysis_json']:
                    return json.loads(row['vision_analysis_json'])
                return {}
        finally:
            conn.close()

    def update_plan_selection(self, patient_id, selection):
        conn = self.get_connection()
        if not conn: return
        try:
            with conn.cursor() as cursor:
                sql = "UPDATE treatment_suggestions SET selected_plan = %s WHERE patient_id = %s ORDER BY generated_at DESC LIMIT 1"
                cursor.execute(sql, (selection, patient_id))
                conn.commit()
        finally:
            conn.close()
    def get_all_patients(self):
        conn = self.get_connection()
        if not conn: return []
        try:
            with conn.cursor() as cursor:
                sql = """SELECT p.id, p.patient_external_id, p.full_name, p.gender, p.age,
                                ts.selected_plan, ts.generated_at
                         FROM patients p
                         LEFT JOIN treatment_suggestions ts ON p.id = ts.patient_id
                         ORDER BY p.id DESC"""
                cursor.execute(sql)
                return cursor.fetchall()
        finally:
            conn.close()
