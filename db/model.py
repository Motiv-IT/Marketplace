
from sqlalchemy import Column, Integer, String
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # Primary key, auto-increment
    email = Column(String, unique=True, index=True, nullable=False)  # User email
    hashed_password = Column(String, nullable=False)  # Hashed password storage
    name = Column(String, nullable=False)  # User's name
