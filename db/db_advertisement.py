from sqlalchemy.orm import Session, joinedload
from sqlalchemy.orm.session import Session
from sqlalchemy import func
from typing import Optional
from fastapi import HTTPException, status
from db.database import get_db
from db.model import DbAdvertisement, DbCategory, DbUser, DbRating, DbTransaction
from schemas import (
    AdvertisementBase,
    AdvertisementEditBase,
    AdvertisementStatusDisplay,
)
from db.model import ScoreTypeEnum


# -----------search for desired ads by searching on keyword and filtering by category_id--------
# -----------------------the result is sorted by recency and rating------------------------------
def get_filtered_advertisements(
    db: Session, keyword: Optional[str] = None, category_id: Optional[int] = None
):
    subquery = (
        db.query(
            DbAdvertisement.user_id.label("seller_id"),
            func.avg(DbRating.score).label("avg_seller_score"),
        )
        .join(DbTransaction, DbTransaction.advertisement_id == DbAdvertisement.id)
        .join(DbRating, DbRating.transaction_id == DbTransaction.id)
        .where(DbRating.score_type == ScoreTypeEnum.SELLER_SCORE)
        .group_by(DbAdvertisement.user_id)
        .subquery()
    )
    query = db.query(DbAdvertisement, subquery.c.avg_seller_score).outerjoin(
        subquery, DbAdvertisement.user_id == subquery.c.seller_id
    )
    if keyword:
        query = query.filter(
            DbAdvertisement.title.ilike(f"%{keyword}%")
            | DbAdvertisement.content.ilike(f"%{keyword}%")
        )

    if category_id:
        query = query.filter(DbAdvertisement.category_id == category_id)

    ads = query.order_by(
        DbAdvertisement.created_at.desc(),
        subquery.c.avg_seller_score.desc().nullslast(),
    ).all()

    return [
        {"advertisement": ad, "average_rating": avg_score or 0} for ad, avg_score in ads
    ]


# creating one advertisement
def create_advertisement(db: Session, request: AdvertisementBase):
    user = db.query(DbUser).filter(DbUser.id == request.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {request.user_id} not found",
        )

    category = db.query(DbCategory).filter(DbCategory.id == request.category_id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {request.category_id} not found",
        )

    if request.price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Price must be more than 0"
        )

    new_adv = DbAdvertisement(
        title=request.title,
        content=request.content,
        price=request.price,
        status=request.status,
        created_at=request.created_at,
        user_id=request.user_id,
        category_id=request.category_id,
    )
    db.add(new_adv)
    db.commit()
    db.refresh(new_adv)
    return new_adv


# selecting all advertisements which are ranked by recency and user rating
def get_all_advertisements(db: Session):
    subquery = (
        db.query(
            DbAdvertisement.user_id.label("seller_id"),
            func.avg(DbRating.score).label("avg_seller_score"),
        )
        .join(DbTransaction, DbTransaction.advertisement_id == DbAdvertisement.id)
        .join(DbRating, DbRating.transaction_id == DbTransaction.id)
        .where(DbRating.score_type == ScoreTypeEnum.SELLER_SCORE)
        .group_by(DbAdvertisement.user_id)
        .subquery()
    )

    # Main query to get ads and join with avg score per seller
    ads = (
        db.query(DbAdvertisement, subquery.c.avg_seller_score)
        .outerjoin(subquery, DbAdvertisement.user_id == subquery.c.seller_id)
        .order_by(
            DbAdvertisement.created_at.desc(),
            subquery.c.avg_seller_score.desc().nullslast(),
        )
        .all()
    )

    return [{"advertisement": ad, "average_rating": avg_score} for ad, avg_score in ads]


# selecting one  advertisement
def get_one_advertisement(id: int, db: Session):
    subquery = (
        db.query(
            DbAdvertisement.user_id.label("seller_id"),
            func.avg(DbRating.score).label("avg_seller_score"),
        )
        .join(DbTransaction, DbTransaction.advertisement_id == DbAdvertisement.id)
        .join(DbRating, DbRating.transaction_id == DbTransaction.id)
        .where(DbRating.score_type == ScoreTypeEnum.SELLER_SCORE)
        .group_by(DbAdvertisement.user_id)
        .subquery()
    )
    result = (
        db.query(DbAdvertisement, subquery.c.avg_seller_score)
        .outerjoin(subquery, DbAdvertisement.user_id == subquery.c.seller_id)
        .filter(DbAdvertisement.id == id)
        .first()
    )
    if not result:
        raise HTTPException(status_code=404, detail="Ads not found")
    ad, avg_score = result
    return {"advertisement": ad, "average_rating": avg_score or 0}


# editing one advertisement
def edit_advertisement(id: int, request: AdvertisementEditBase, db: Session):
    advertisement = db.query(DbAdvertisement).filter(DbAdvertisement.id == id).first()
    if not advertisement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Advertisement with id {id} does not exist",
        )

    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if getattr(advertisement, key) != value:
            if key == "category_id":
                category = (
                    db.query(DbCategory)
                    .filter(DbCategory.id == request.category_id)
                    .first()
                )
                if not category:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Category with id {request.category_id} not found",
                    )
            if key == "price":
                if value <= 0:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Price should be more than 0",
                    )
            setattr(advertisement, key, value)
    db.commit()
    db.refresh(advertisement)
    return advertisement


# deleting one advertisement
def delete_advertisement(id: int, db: Session):
    advertisement = db.query(DbAdvertisement).filter(DbAdvertisement.id == id).first()
    if not advertisement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Advertisement with id {id} does not exist",
        )
    db.delete(advertisement)
    db.commit()
    return {"message": f"Advertisement with id {id} has been deleted"}


# updating status of one advertisement
def status_advertisement(id: int, request: AdvertisementStatusDisplay, db: Session):
    advertisement = db.query(DbAdvertisement).filter(DbAdvertisement.id == id).first()
    if not advertisement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Advertisement with id {id} does not exist",
        )
    advertisement.status = request.status
    db.commit()
    db.refresh(advertisement)
    return advertisement
