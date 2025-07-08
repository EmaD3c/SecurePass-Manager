import os
from cryptography.fernet import Fernet

fernet_key = os.getenv('FERNET_KEY')

if not fernet_key:
    raise RuntimeError("FERNET_KEY is missing. Please set it in your environment variables.")

try:
    fernet = Fernet(fernet_key.encode())
except Exception as e:
    raise RuntimeError(f"Invalid FERNET_KEY: {str(e)}")

def encrypt_password(password: str) -> str:
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(token: str) -> str:
    return fernet.decrypt(token.encode()).decode()
