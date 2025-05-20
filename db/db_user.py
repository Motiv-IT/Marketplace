from schemas import UserBase
from db.model import DbUser
from sqlalchemy.orm import Session
from hash import hash_password

# create user
def create_user(db:Session, request: UserBase):
    new_user = DbUser(
        username = request.username,
        email = request.email,
        password = hash_password(request.password),
        address = request.address,
        phone = request.phone
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
