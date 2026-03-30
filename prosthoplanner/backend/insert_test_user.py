import sys
import os

# Set unbuffered output
sys.stdout.reconfigure(line_buffering=True)

try:
    print("--- DEBUG: Starting insert_test_user.py ---")
    sys.stdout.flush()
    
    from db_manager import DatabaseManager
    print("--- DEBUG: DatabaseManager imported successfully ---")
    
    print("--- DEBUG: Initializing DatabaseManager... ---")
    db = DatabaseManager()
    
    email = "prakashkonisetty04@gmail.com"
    password = "123456"
    full_name = "Dr. Prakash Konisetty"
    mobile = "9876543210"
    
    print(f"--- DEBUG: Attempting to create user: {email} ---")
    success, message = db.create_user(full_name, email, mobile, password)
    
    if success:
        print("SUCCESS: User created successfully.")
    else:
        print(f"FAILED: {message}")
        if "Duplicate entry" in message:
            print("INFO: User already exists.")
        else:
            sys.exit(1)

except Exception as e:
    print(f"FATAL ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    print("--- DEBUG: Script finished ---")
