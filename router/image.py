from typing import List
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from router.auth import get_current_user
from db import db_image
from db.database import get_db
from sqlalchemy.orm.session import Session
from schemas import  ImageAllDisplay, ImageOneDisplay


router = APIRouter(
    prefix='/advertisements',
    tags=['Images']
)


# add images to advertisement
@router.post('/{advertisement_id}/add_images',response_model=ImageOneDisplay)
def add_image(advertisement_id:int,image: UploadFile = File(None),db:Session=Depends(get_db), user_id: int = Depends(get_current_user)):
    return  db_image.add_image(advertisement_id,image,db,user_id)

#show images related to advertisement
@router.get('/{advertisement_id}/show_images',response_model=List[ImageAllDisplay])
def get_all_images(advertisement_id:int,db:Session=Depends(get_db)):
    return db_image.get_all_images(advertisement_id,db)

#changing order of images related to advertisement
@router.patch('/change_order/{image_id}',response_model=List[ImageAllDisplay])
def change_image_order(image_id:int,new_order:int,db:Session=Depends(get_db),user_id:int=Depends(get_current_user)):
    return db_image.change_image_order(image_id,new_order,db,user_id)

#delete one image related to advertisement
@router.delete('/delete_image/{image_id}')
def delete_image(image_id:int,db:Session=Depends(get_db),user_id:int=Depends(get_current_user)):
    return db_image.delete_image(image_id,db,user_id)