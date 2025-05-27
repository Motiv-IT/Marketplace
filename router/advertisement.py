from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import (
    AdvertisementBase,
    AdvertisementDisplay,
    AdvertisementEditBase,
    AdvertisementStatusDisplay,
    AdvertisementWithRating,
)
from db import db_advertisement
from typing import List, Optional
from db.database import get_db
from typing import List
from sqlalchemy.orm.session import Session
from utils.security import oauth2_scheme

router = APIRouter(prefix="/advertisement", tags=["Advertisement"])


# ----------search for desired ads by searching on keyword and filtering by category_id------------------
@router.get(
    "/search",
    summary="Search Ads by Keyword + Category",
    description="this API call enables user to serach by keyword and filter by category",
    response_model=List[AdvertisementWithRating],
)
def get_filtered_advertisements(
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    return db_advertisement.get_filtered_advertisements(db, search, category_id)


# creating one advertisement
@router.post("/create", response_model=AdvertisementDisplay)
def create_advertisement(
    request: AdvertisementBase,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    return db_advertisement.create_advertisement(db, request)


# selecting all advertisements
@router.get("/all", response_model=List[AdvertisementWithRating])
def get_all_advertisements(db: Session = Depends(get_db)):
    return db_advertisement.get_all_advertisements(db)


# selecting one advertisement
@router.get("/{id}", response_model=AdvertisementWithRating)
def get_one_advertisement(id: int, db: Session = Depends(get_db)):
    return db_advertisement.get_one_advertisement(id, db)


# editing  one advertisement
@router.patch("/{id}/edit", response_model=AdvertisementDisplay)
def edit_advertisement(
    id: int,
    request: AdvertisementEditBase,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    return db_advertisement.edit_advertisement(id, request, db)


# deleting one advertisement
@router.delete("/{id}")
def delete_advertisement(
    id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    return db_advertisement.delete_advertisement(id, db)


# updating status of one advertisement
@router.patch("/{id}/status", response_model=AdvertisementStatusDisplay)
def status_advertisement(
    id: int,
    request: AdvertisementStatusDisplay,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    return db_advertisement.status_advertisement(id, request, db)
