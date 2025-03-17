from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from controllers.database_handler import Base
from sqlalchemy_serializer import SerializerMixin


class Password(Base, SerializerMixin):
    __tablename__ = 'passwords'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
