from fastapi import HTTPException
from sqlalchemy.orm import Session
from db.model import Rating, Transaction
from schemas import RatingCreate
def create_rating(db: Session, rating: RatingCreate):
    transaction = db.query(Transaction).filter(Transaction.id == rating.transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    if not transaction.completed:
        raise HTTPException(status_code=400, detail="Transaction not completed")

    existing_rating = db.query(Rating).filter(
        Rating.transaction_id == rating.transaction_id,
        Rating.rater_id == rating.rater_id
    ).first()
    if existing_rating:
        raise HTTPException(status_code=400, detail="Rating already exists for this transaction")

    if rating.rater_id == transaction.buyer_id:
        ratee_id = transaction.seller_id
    elif rating.rater_id == transaction.seller_id:
        ratee_id = transaction.buyer_id
    else:
        raise HTTPException(status_code=403, detail="Rater is not involved in this transaction")

    new_rating = Rating(
        transaction_id=rating.transaction_id,
        rater_id=rating.rater_id,
        ratee_id=ratee_id,
        score=rating.score,
        comment=rating.comment
    )
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating

def get_ratings_for_user(db: Session, user_id: str):
    return db.query(Rating).filter(Rating.ratee_id == user_id).all()
