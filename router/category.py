from typing import List
from fastapi import  APIRouter
from fastapi import Depends
from sqlalchemy.orm.session import Session

from db import db_category
from db.database import get_db
from schemas import CategoryBase, CategoryDisplay

router=APIRouter(
    prefix='/cat',
    tags=["Category"]
)

@router.post('/create',response_model=CategoryDisplay)
def create_advertisement(request:CategoryBase,db:Session=Depends(get_db)):
    return  db_category.create_category(db,request)
   

@router.get('/all',response_model=List[CategoryDisplay])
def get_all(db:Session=Depends(get_db)):
    return db_category.get_all(db)