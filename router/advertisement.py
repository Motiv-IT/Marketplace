from typing import List
from fastapi import  APIRouter
from fastapi import Depends
from sqlalchemy.orm.session import Session

from db import db_advertisement
from db.database import get_db
from schemas import AdvertisementBase, AdvertisementDisplay, AdvertisementEditBase, AdvertisementStatusDisplay

router=APIRouter(
    prefix='/adv',
    tags=["advertisement"]
)
#creating one advertisement
@router.post('/create',response_model=AdvertisementDisplay)
def create_advertisement(request:AdvertisementBase,db:Session=Depends(get_db)):
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
def edit_advertisement(id:int,request:AdvertisementEditBase,db:Session=Depends(get_db)):
    return db_advertisement.edit_advertisement(id,request,db)

#deleting one advertisement
@router.delete('/{id}')
def delete_advertisement(id:int,db:Session=Depends(get_db)):
    return db_advertisement.delete_advertisement(id,db)

#updating status of one advertisement
@router.patch('/{id}/status',response_model=AdvertisementStatusDisplay)
def status_advertisement(id:int,request:AdvertisementStatusDisplay,db:Session=Depends(get_db)):
    return db_advertisement.status_advertisement(id,request,db)