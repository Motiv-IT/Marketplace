from fastapi import FastAPI
from db import model
from db.database import engine

#begin Nataliia
#Advertisement
from router import advertisement
# end Nataliia

app = FastAPI()

@app.get('/')
def get_root():
    return 200

#begin Nataliia
#Advertisement 
app.include_router(advertisement.router)

# end Nataliia

model.Base.metadata.create_all(engine)   