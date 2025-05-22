# Import the necessary SQLAlchemy classes to define database columns and types
from sqlalchemy import Column, Integer, String

# Import the Base class from your database module (used to define database models)
from db.database import Base

# Define a User model that maps to the "users" table in the database
class User(Base):
    __tablename__ = "users"  # This tells SQLAlchemy to name the table "users"

    # Define the columns in the table:

    # A unique ID for each user — this is the primary key and will auto-increment
    id = Column(Integer, primary_key=True, index=True)

    # The user's email address — must be unique and cannot be empty
    email = Column(String, unique=True, index=True, nullable=False)

    # The user's password, stored in a hashed format — cannot be empty
    hashed_password = Column(String, nullable=False)

    # The user's full name — cannot be empty
    name = Column(String, nullable=False)
