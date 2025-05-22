
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base


# # SQLite URL for local file database
# SQLALCHEMY_DATABASE_URL = "sqlite:///./marketplace.db"

# # Create engine with SQLite, allow multiple threads
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

# # Session class to create database sessions
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Base class to create models from
# Base = declarative_base()

# # Dependency to get DB session (for FastAPI or other use)
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
 
 
SQLALCHEMY_DATABASE_URL = 'sqlite:///./marketplace.db'
 
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True )
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
#begin Nataliia
metadata = MetaData()
metadata.reflect(bind=engine)
#end Nataliia
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  
 