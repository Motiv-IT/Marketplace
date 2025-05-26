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
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(advertisement.router)
app.include_router(category.router)
#------Sayed sprint2------
Base.metadata.create_all(bind=engine)  # Create tables on startup

app = FastAPI(title="User Rating System")

app.include_router(rating_router)
#------syed ----end

app.include_router(chat.router)

@app.get("/")
def root():
    return {"message": "User Rating System for Marketplace!"}
