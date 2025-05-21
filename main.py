<<<<<<< HEAD
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from db import model
from db.database import engine
from fastapi.responses import HTMLResponse


=======
from fastapi import FastAPI
from db import model
from db.database import engine
>>>>>>> origin/Nataliia

#begin Nataliia
#Advertisement
from router import advertisement
<<<<<<< HEAD
from router import category
=======
>>>>>>> origin/Nataliia
# end Nataliia

app = FastAPI()

@app.get('/')
def get_root():
    return 200

#begin Nataliia
#Advertisement 
app.include_router(advertisement.router)
<<<<<<< HEAD
app.include_router(category.router)

# end Nataliia


#begin Tina
from router import chat
app.include_router(chat.router)
#end Tina

=======

# end Nataliia

>>>>>>> origin/Nataliia
model.Base.metadata.create_all(engine)   