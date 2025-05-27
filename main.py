from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from db import model
from db.database import engine, Base
from fastapi.responses import HTMLResponse
from router import advertisement
from router import category
from router.rating import router as rating_router   #sayed main -----
from router.auth import router as auth_router
from router import chat

app = FastAPI()
Base.metadata.create_all(bind=engine)  # Create tables on startup

app.include_router(auth_router, prefix="/auth", tags=["Registration"])
app.include_router(advertisement.router)
app.include_router(category.router)
app.include_router(chat.router)
app.include_router(rating_router)













