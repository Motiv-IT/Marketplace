from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from db import model
from db.database import engine
from fastapi.responses import HTMLResponse
from router import advertisement
from router import category
from router.auth import router as auth_router
from router import chat

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(advertisement.router)
app.include_router(category.router)


app.include_router(chat.router)




# @app.get("/")
# def root():
#     return {"message": "Welcome to the API. Use /auth for registration, login, and logout."}

model.Base.metadata.create_all(engine)
