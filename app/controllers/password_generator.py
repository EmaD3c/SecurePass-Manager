from flask import Flask, request, jsonify, render_template
import secrets
import string

app = Flask(__name__)

def generate_secure_password(length, use_upper, use_lower, use_digits, use_special):
    length = int(length)
    if length < 8 or length > 16:
        raise ValueError("Invalid length (8-16 characters).")

    character_pool = ''
    if use_upper:
        character_pool += string.ascii_uppercase
    if use_lower:
        character_pool += string.ascii_lowercase
    if use_digits:
        character_pool += string.digits
    if use_special:
        character_pool += "!@#$%^&*()_+-=[]{}|;:,.<>/?"

    if not character_pool:
        raise ValueError("No character type selected.")

    password = []
    if use_upper:
        password.append(secrets.choice(string.ascii_uppercase))
    if use_lower:
        password.append(secrets.choice(string.ascii_lowercase))
    if use_digits:
        password.append(secrets.choice(string.digits))
    if use_special:
        password.append(secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>/?"))

    while len(password) < length:
        password.append(secrets.choice(character_pool))

    secrets.SystemRandom().shuffle(password)
    return ''.join(password)
