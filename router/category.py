from fastapi import APIRouter, Depends
from schemas import CategoryDisplay, CategoryBase
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_category


router = APIRouter(
    prefix='/category',
    tags=['category']
)
@router.post('/', summary='create new Category', response_model=CategoryDisplay)
def create_ads(request: CategoryBase, db: Session = Depends(get_db)):
    return db_category.create_category(db, request)