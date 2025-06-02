from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from schemas import RatingCreate, RatingOut
import crud

router = APIRouter(prefix="/ratings", tags=["Ratings"])

@router.post("/", response_model=RatingOut)
def rate_user(rating: RatingCreate, db: Session = Depends(get_db)):
    return crud.create_rating(db, rating)

@router.get("/user/{user_id}", response_model=List[RatingOut])
def get_user_ratings(user_id: str, db: Session = Depends(get_db)):
    return crud.get_ratings_for_user(db, user_id)
