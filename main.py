from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from db import model
from db.database import engine
from fastapi.responses import HTMLResponse
from router import advertisement
from router import category

app = FastAPI()

app.include_router(advertisement.router)
app.include_router(category.router)

from router import chat
app.include_router(chat.router)

model.Base.metadata.create_all(engine) 
