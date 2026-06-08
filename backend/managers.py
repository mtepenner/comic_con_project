# managers.py
import os
import json
import hashlib
from config import AUTH_FILE, BANK_FILE

# ==========================================
# Data Managers (Auth & Banking)
# ==========================================
class AuthManager:
    @staticmethod
    def get_users():
        if not os.path.exists(AUTH_FILE):
            return {}
        with open(AUTH_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def save_users(users):
        with open(AUTH_FILE, "w") as f:
            json.dump(users, f, indent=4)

    @staticmethod
    def create_account(first_name, username, password, role):
        users = AuthManager.get_users()
        if username in users:
            return False, "ERR: USER_ALREADY_EXISTS"
        
        salt = os.urandom(16) 
        hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        
        users[username] = {
            "first_name": first_name,
            "role": role,
            "salt": salt.hex(),
            "hash": hash_obj.hex()
        }
        AuthManager.save_users(users)
        return True, "SYS: ACCOUNT_ALLOCATED_SUCCESSFULLY"

    @staticmethod
    def verify_login(username, password):
        users = AuthManager.get_users()
        if username not in users:
            return False, None, None
        
        user_data = users[username]
        salt = bytes.fromhex(user_data["salt"])
        stored_hash = user_data["hash"]
        
        hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        
        if hash_obj.hex() == stored_hash:
            return True, user_data["first_name"], user_data["role"]
        return False, None, None

class BankManager:
    @staticmethod
    def get_bank_info():
        if not os.path.exists(BANK_FILE):
            return None
        with open(BANK_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def save_bank_info(bank_name, account_num, routing_num):
        data = {
            "bank_name": bank_name,
            "account_number": account_num,
            "routing_number": routing_num
        }
        with open(BANK_FILE, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def remove_bank_info():
        if os.path.exists(BANK_FILE):
            os.remove(BANK_FILE)
