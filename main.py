from fastapi import FastAPI
from db import model
from db.database import engine
from router import advertisement, user, category

app = FastAPI()

app.include_router(advertisement.router)
app.include_router(user.router)
app.include_router(category.router)

model.Base.metadata.create_all(engine)