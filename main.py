
from fastapi import FastAPI
from db.database import engine
import db.model
from routers.auth import router as auth_router

db.model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def root():
    return {"message": "Welcome to the API. Use /auth endpoints for registration, login, and logout."}
