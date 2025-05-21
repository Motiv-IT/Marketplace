from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import db_advertisement
from schemas import AdvertisementDisplay, AdvertisementBase
from typing import List, Optional
from db.database import get_db

router = APIRouter(
    prefix='/advertisement',
    tags=['advertisement']
)
#------- get list of searched ads by keyword------------
@router.get('/search', summary='Search Ads by keyword',
            description='this API call enables user to search by keybords', response_model=List[AdvertisementDisplay])
def get_searched_advertisements(search: str, db: Session = Depends(get_db)):
    return db_advertisement.get_searched_advertisements(db, search)

#--------get list of serached ads by category-----------
@router.get('/search/category', summary='Search Ads by Category',
            description='this API call enables user to filter by category',
            response_model=List[AdvertisementDisplay])
def get_filtered_advertisements(category_id: int, db: Session = Depends(get_db)):
    return db_advertisement.get_category_filtered_advertisements(db, category_id )

#--------- get list of sorted by date of creation ads----------
@router.get('/sorted_by_date', response_model=List[AdvertisementDisplay])
def get_sorted_advertisements(db: Session = Depends(get_db)):
    return db_advertisement.get_sorted_advertisements(db)

#----------get list of combined filtered ads------------------
@router.get('/search/category-keyword', summary='Search Ads by Keyword + Category',
            description='this API call enables user to serach by keyword and filter by category',
            response_model=List[AdvertisementDisplay])
def get_filtered_advertisements(search: Optional[str] = None, category_id: Optional[int] = None, db: Session = Depends(get_db)):
    return db_advertisement.get_filtered_advertisements(db, search, category_id)

