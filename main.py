from fastapi import FastAPI
from db import model
from db.database import engine

app = FastAPI()

@app.get('/')
def get_root():
    return 200

model.Base.metadata.create_all(engine)   