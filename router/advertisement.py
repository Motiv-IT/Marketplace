from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import AdvertisementBase, AdvertisementDisplay, AdvertisementEditBase, AdvertisementStatusDisplay
from db import db_advertisement
from typing import List, Optional
from db.database import get_db
from typing import List
from sqlalchemy.orm.session import Session
from utils.security import oauth2_scheme

router = APIRouter(
    prefix='/advertisement',
    tags=['Advertisement']
)
#------- get list of searched ads by keyword------------
@router.get('/search/keyword', summary='Search Ads by keyword',
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

#creating one advertisement
@router.post('/create',response_model=AdvertisementDisplay)
def create_advertisement(request:AdvertisementBase,db:Session=Depends(get_db),token: str = Depends(oauth2_scheme)):
    return  db_advertisement.create_advertisement(db,request)
   
#selecting all advertisements
@router.get('/all',response_model=List[AdvertisementDisplay])
def get_all_advertisements(db:Session=Depends(get_db)):
    return db_advertisement.get_all_advertisements(db)

#selecting one advertisement
@router.get('/{id}',response_model=AdvertisementDisplay)
def get_one_advertisement(id:int,db:Session=Depends(get_db)):
    return db_advertisement.get_one_advertisement(id,db)

#editing  one advertisement
@router.patch('/{id}/edit',response_model=AdvertisementDisplay)
def edit_advertisement(id:int,request:AdvertisementEditBase,db:Session=Depends(get_db),token: str = Depends(oauth2_scheme)):
    return db_advertisement.edit_advertisement(id,request,db)

#deleting one advertisement
@router.delete('/{id}')
def delete_advertisement(id:int,db:Session=Depends(get_db),token: str = Depends(oauth2_scheme)):
    return db_advertisement.delete_advertisement(id,db)

#updating status of one advertisement
@router.patch('/{id}/status',response_model=AdvertisementStatusDisplay)
def status_advertisement(id:int,request:AdvertisementStatusDisplay,db:Session=Depends(get_db),token: str = Depends(oauth2_scheme)):
    return db_advertisement.status_advertisement(id,request,db)
