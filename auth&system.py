import json
import os
import random
import time
from datetime import datetime

USERS_FILE = "users.json"
OTP_STORAGE = {}

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def register_user(email, password):
    users = load_users()
    
    if email in users:
        return False, "Email already exists!"
    
    users[email] = {
        "password": password,
        "created_at": datetime.now().isoformat(),
        "premium": False
    }
    
    save_users(users)
    return True, "Account created successfully!"

def login_user(email, password):
    users = load_users()
    
    if email in users and users[email]["password"] == password:
        return True, users[email]
    
    return False, "Invalid credentials!"

def send_otp(email):
    """Demo OTP - just for testing"""
    otp = str(random.randint(100000, 999999))
    OTP_STORAGE[email] = {
        "otp": otp,
        "expiry": time.time() + 300  # 5 minutes expiry
    }
    print(f"📧 OTP for {email}: {otp}")  # Will show in terminal
    return otp

def verify_otp(email, otp):
    if email in OTP_STORAGE:
        stored_otp = OTP_STORAGE[email]
        if time.time() < stored_otp["expiry"] and stored_otp["otp"] == otp:
            return True
    return False

def reset_password(email, new_password):
    users = load_users()
    if email in users:
        users[email]["password"] = new_password
        save_users(users)
        return True
    return False

def update_premium(email):
    users = load_users()
    if email in users:
        users[email]["premium"] = True
        save_users(users)
        return True
    return False

def is_premium(email):
    users = load_users()
    if email in users:
        return users[email].get("premium", False)
    return False