from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.model import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./marketpalce.db"  # Or your DB URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



Base.metadata.create_all(bind=engine)
