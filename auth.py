# auth.py

import json
import os
import bcrypt

USER_FILE = "users.json"

def load_users():
    """Loads the users from the JSON file."""
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_users(users):
    """Saves the users to the JSON file."""
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    """Hashes a password using bcrypt."""
    # bcrypt requires bytes, so we encode the string to utf-8
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password, hashed):
    """Checks if a password matches the hashed version."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_user(username, password):
    """Creates a new user if the username doesn't already exist."""
    users = load_users()
    if username in users:
        return False  # Username already taken
    users[username] = hash_password(password)
    save_users(users)
    return True

def authenticate_user(username, password):
    """Verifies a user's login credentials."""
    users = load_users()
    if username not in users:
        return False
    return verify_password(password, users[username])