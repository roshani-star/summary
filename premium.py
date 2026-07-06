import json
import os

PREMIUM_FILE = "premium_users.json"

def activate_premium(username):
    users = {}
    if os.path.exists(PREMIUM_FILE):
        with open(PREMIUM_FILE, 'r') as f:
            users = json.load(f)
    
    users[username] = True
    
    with open(PREMIUM_FILE, 'w') as f:
        json.dump(users, f)
    
    return True

def is_premium(username):
    if not os.path.exists(PREMIUM_FILE):
        return False
    
    with open(PREMIUM_FILE, 'r') as f:
        users = json.load(f)
    
    return users.get(username, False)