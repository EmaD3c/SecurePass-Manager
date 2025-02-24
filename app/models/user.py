import uuid
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
from app import bcrypt
from app import db
from sqlalchemy.orm import validates, relationship


class User(db.Model):
    """Represent an user."""

    __tablename__ = "users"

    uuid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=True, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

def update(self, data):
        """Update user."""
        if data["first_name"] is not None:
            self.is_valid_length("first_name", data["first_name"])

        if data["last_name"] is not None:
            self.is_valid_length("last_name", data["last_name"])

        if data["email"] is not None:
            valid_new_email = self.check_mail("email", data["email"])
            data["email"] = valid_new_email

        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()

def __repr__(self):
        """Represent formated values of attributes."""
        return f"<User uuid={self.uuid}, \
            name={self.first_name} {self.last_name}, \
            email={self.email}, is_admin={self.is_admin}, \
            "

@validates("first_name", "last_name")
def is_valid_length(self, key, field):
        """Check the length of the first_name or last_name."""
        if field is None or not (1 <= len(field) <= 50):
            raise ValueError(f"{field} must be between 1 and 50 characters.")
        return field

@validates("email")
def check_mail(self, key, email):
        """Check the validity of the mail."""
        if not email:
            raise ValueError("Email is required")

        try:
            validated_email = validate_email(email)
            email = validated_email.email
            return email
        except EmailNotValidError as e:
            raise ValueError(f"{str(e)}")

def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
