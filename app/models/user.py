from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import bcrypt
from models.password import generate_password_hash

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(String(60), primary_key=True)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, email, password):
        self.email = email
        self.password = self.generate_password_hash(password)
