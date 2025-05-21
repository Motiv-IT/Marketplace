from fastapi import HTTPException,status
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.model import DbAdvertisement, DbCategory, DbUser
from schemas import AdvertisementBase, AdvertisementEditBase, AdvertisementStatusDisplay, StatusAdvertisementEnum
from sqlalchemy.orm import joinedload

#creating one advertisement
def create_advertisement(db:Session,request:AdvertisementBase):
    user = db.query(DbUser).filter(DbUser.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id {request.user_id} not found")

    category = db.query(DbCategory).filter(DbCategory.id == request.category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with id {request.category_id} not found")
    
    if request.price <=0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Price should be more than 0")
    
    new_adv=DbAdvertisement(
        title=request.title,
        content=request.content,
        price=request.price,
        status=request.status,
        created_at=request.created_at,
        user_id=request.user_id,
        category_id=request.category_id

    )
    db.add(new_adv)
    db.commit()
    db.refresh(new_adv)
    return new_adv

#selecting all advertisements
def get_all_advertisements(db:Session):
    return db.query(DbAdvertisement).all()

#selecting one  advertisement
def get_one_advertisement(id:int,db:Session):
    advertisement=db.query(DbAdvertisement).filter(DbAdvertisement.id==id).first()
    if not advertisement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'Advertisement with id {id} does not exist')
    return advertisement


#editing one advertisement
def edit_advertisement(id:int,request:AdvertisementEditBase,db:Session):
    advertisement=db.query(DbAdvertisement).filter(DbAdvertisement.id==id).first()
    if not advertisement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'Advertisement with id {id} does not exist')
    
    category = db.query(DbCategory).filter(DbCategory.id == request.category_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Category with id {request.category_id} not found")
    
    if request.price <=0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Price should be more than 0")
    
    advertisement.title=request.title
    advertisement.content=request.content
    advertisement.price=request.price
    advertisement.status=request.status
    advertisement.category_id=request.category_id
    db.commit()
    db.refresh(advertisement)
    return advertisement

#deleting one advertisement
def delete_advertisement(id:int,db:Session):
    advertisement=db.query(DbAdvertisement).filter(DbAdvertisement.id==id).first()
    if not advertisement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'Advertisement with id {id} does not exist')
    db.delete(advertisement)
    db.commit()
    return {"message": f"Advertisement with id {id} has been deleted"}

#updating status of one advertisement
def status_advertisement(id:int,request:AdvertisementStatusDisplay,db:Session):
    advertisement=db.query(DbAdvertisement).filter(DbAdvertisement.id==id).first()
    if not advertisement:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f'Advertisement with id {id} does not exist')
    advertisement.status=request.status
    db.commit()
    db.refresh(advertisement)
    return advertisement