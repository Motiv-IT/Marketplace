from sqlalchemy.orm import Session
from db.model import DbAdvertisement
from fastapi import HTTPException
from typing import Optional
from schemas import AdvertisementBase
#----------get all ads which sorted by recency first and rating secondly-------
def get_all_advertisements():
    pass
#---------- get ads based on search by keabord-------------
def get_searched_advertisements(db: Session, keyword: str):
    ads = db.query(DbAdvertisement).filter(
        DbAdvertisement.title.ilike(f"%{keyword}%") |
        DbAdvertisement.content.ilike(f"%{keyword}%")
    ).order_by(DbAdvertisement.created_at.desc()).all()

    if not ads:
         raise HTTPException(status_code=404, detail="No advertisements found with that keyword.")
    return ads
    
#----------- get ads based on filter on category------------
def get_category_filtered_advertisements(db: Session, category_id: int):
    ads = db.query(DbAdvertisement)\
        .filter(DbAdvertisement.category_id == category_id)\
        .order_by(DbAdvertisement.created_at.desc())\
        .all()
    if not ads:
        raise HTTPException(status_code=404, detail="No advertisements found in this category.")
    return ads

#----------- get ads based on recency--------------    
def get_sorted_advertisements(db: Session):
    return db.query(DbAdvertisement).order_by(DbAdvertisement.created_at.desc()).all()

#-----------get ads by combining search by keyword and filtering by category and sorting by recency--------
def get_filtered_advertisements(db: Session, keyword: Optional[str] = None, category_id: Optional[int] = None):
    query = db.query(DbAdvertisement)

    if keyword :
        query = query.filter(
            (DbAdvertisement.title.ilike(f"%{keyword}%"))|
            (DbAdvertisement.content.ilike(f"%{keyword}%"))             
        )
    if category_id:
        query = query.filter(DbAdvertisement.category_id == category_id)  
    ads = query.order_by(DbAdvertisement.created_at.desc()).all()  

    if not ads:
         raise HTTPException(status_code=404, detail="No advertisements found.")
    return ads  








