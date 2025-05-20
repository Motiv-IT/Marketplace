from fastapi import APIRouter, Depends
from schemas import UserDisplay, UserBase
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_user


router = APIRouter(
    prefix='/user',
    tags=['user']
)
@router.post('/', summary='create new user' , response_model=UserDisplay)
def create_ads(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)