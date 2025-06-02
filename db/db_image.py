import os
import shutil
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile, status
from db.model import DbAdvertisement, DbImage
from schemas import ImageOrderDisplay, ImageAllDisplay


# add images to advertisement
def add_image(id: int,image: UploadFile, db: Session, current_user_id: int):
    advertisement = db.query(DbAdvertisement).filter(DbAdvertisement.id == id).first()
    if not advertisement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'Advertisement with id {id} not found')
    if advertisement.user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail='No permission to modify this advertisement')

    max_order = (
        db.query(func.max(DbImage.order_id))
        .filter(DbImage.advertisement_id == id)
        .scalar()
    )
    if not max_order:
         max_order=0
    
    UPLOAD_DIR = "uploaded_images"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    image_path = os.path.join(UPLOAD_DIR, image.filename)

    # Save the file synchronously
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    image_record = DbImage(
        order_id=max_order+1,
        image_name=image.filename,
        image_path=image_path,
        image_type=image.content_type,
        advertisement_id=id
    )
    db.add(image_record)
    db.commit()
    db.refresh(image_record)

    return image_record

#show all images related to specific advertisement
def get_all_images(id:int,db:Session):
    advertisement=db.query(DbAdvertisement).filter(DbAdvertisement.id==id).first()
    if not advertisement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'Advertisement with id {id} not found')
    all_images =(db.query(DbImage)
                 .filter(DbImage.advertisement_id==id)
                 .order_by(DbImage.order_id.asc())
                 .all())
    
    for image in all_images:
            image.image_path=f"http://127.0.0.1:8000/images/{image.image_name}"

    return all_images


#changing order of images related to advertisement
def change_image_order(image_id:int,new_order:int,db:Session,current_user_id:int):
   
    image=db.query(DbImage).filter(DbImage.id==image_id).first()
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detal=f'Image with id {image_id} is not found')
   
    advertisement:DbAdvertisement=image.advertisement
    user_id=advertisement.user_id

    if user_id!=current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail='No permission to modify this advertisement')
    
    if image.order_id==new_order:
         raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, 
                            detail='The order is the same')
    
  
    max_order = (
        db.query(func.max(DbImage.order_id))
        .filter(DbImage.advertisement_id == advertisement.id)
        .scalar()
    )

    if new_order<=0 or new_order>max_order:
         raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, 
                            detail=f'The new order_id should be  greater than 0 and less than {max_order}')
    
    repl_image=db.query(DbImage).filter(DbImage.order_id==new_order).first()

    if repl_image:
        repl_image.order_id = image.order_id

    image.order_id = new_order

    db.commit()
    db.refresh(image)
    if repl_image:
        db.refresh(repl_image)

    all_images =(db.query(DbImage)
                 .filter(DbImage.advertisement_id==advertisement.id)
                 .order_by(DbImage.order_id.asc())
                 .all())
    
    for image in all_images:
            image.image_path=f"http://127.0.0.1:8000/images/{image.image_name}"

    return all_images


#delete one image from advertisement
def delete_image(image_id:int,db:Session,current_user_id:int):
  
    image=db.query(DbImage).filter(DbImage.id==image_id).first()
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detal=f'Image with id {image_id} not found')
   
    advertisement:DbAdvertisement=image.advertisement
    user_id=advertisement.user_id
   
    if user_id!=current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail='No permission to modify this advertisement')
    db.delete(image)
    db.commit()
    return {"message": f"Image with id {image_id} has been deleted"}