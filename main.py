from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from db import model
from db.database import engine
from fastapi.responses import HTMLResponse
from router import advertisement, category, image, chat
from router.auth import router as auth_router


app = FastAPI()
app.mount("/images", StaticFiles(directory="uploaded_images"), name="images")

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(advertisement.router)
app.include_router(image.router)
app.include_router(category.router)


app.include_router(chat.router)




model.Base.metadata.create_all(engine)
