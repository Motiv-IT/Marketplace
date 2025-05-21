from fastapi import FastAPI
from db import model
from db.database import engine
from router import advertisement

app = FastAPI()

app.include_router(advertisement.router)

model.Base.metadata.create_all(engine)