
from fastapi import FastAPI
from db.database import engine
from db import model
from router.auth import router as auth_router



app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def root():
    return {"message": "Welcome to the API. Use /auth for registration, login, and logout."}

model.Base.metadata.create_all(engine)
