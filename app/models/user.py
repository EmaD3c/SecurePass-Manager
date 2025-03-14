from sqlalchemy import Column, String, DateTime, Integer
from controllers.database_handler import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
