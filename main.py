from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from db import model
from db.database import engine
from fastapi.responses import HTMLResponse



#begin Nataliia
#Advertisement
from router import advertisement
from router import category
# end Nataliia

app = FastAPI()

@app.get('/')
def get_root():
    return 200

#begin Nataliia
#Advertisement 
app.include_router(advertisement.router)
app.include_router(category.router)

# end Nataliia


#begin Tina
from router import chat
app.include_router(chat.router)
#end Tina

model.Base.metadata.create_all(engine)   