from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import bcrypt

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(String(60), primary_key=True)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, email, password):
        self.email = email
        self.password = self._hash_password(password)

    def _hash_password(self, password):
        """Hash le mot de passe avant de l'enregistrer dans la base de données."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """Vérifie si le mot de passe fourni correspond à celui stocké dans la base de données."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
