from pydantic import BaseModel, EmailStr
from typing import List, Optional
import enum
from datetime import datetime



#---------user schemas----------

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str
    class Config:
        orm_mode = True


#______________  i add this below new code to now to counter my erroor in my test______sayed 
class UserOut(BaseModel):
    id: int
    username: str
    email: str   # <-- i add this line to fix the KeyError

    class Config:
        orm_mode = True

#___________ its first line of code before using test______
# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str

# class UserOut(BaseModel):
#     id: int
#     username: str
#     class Config:
#         orm_mode = True

#----------advertisement schemas------------
class StatusAdvertisementEnum(str, enum.Enum):
    OPEN = "OPEN"
    SOLD = "SOLD"
    RESERVED = "RESERVED"


class Advertisement(BaseModel):
    title: str
    content: str
    price: float
    status: StatusAdvertisementEnum
    class Config():
        orm_mode = True

class User(BaseModel):
    username: str
    email: str
    address: Optional[str] = None
    phone: Optional[str] = None
    class Config():
        orm_mode = True 

class Category(BaseModel):
    title: str   
    class Config():
        orm_mode = True 


#---------user schemas----------
class UserBase(BaseModel):
    username: str
    email: str
    password: str
    address: Optional[str] = None
    phone: Optional[str] = None


class UserDisplay(BaseModel):
    username: str
    email:str
    advertisements: List[Advertisement]
    class Config():
        orm_mode = True 


#----------advertisement schemas------------
class AdvertisementBase(BaseModel):
    title: str
    content: str
    price: float
    status: StatusAdvertisementEnum
    created_at: datetime
    user_id: int
    category_id: int
    
class AdvertisementDisplay(BaseModel):
    title: str
    content: str
    price: float
    status: StatusAdvertisementEnum
    created_at: datetime
    user: User
    category: Category
    class Config():
        orm_mode = True 

#begin Nataliia
#for editing  - not possible to change user_id and created_at
class AdvertisementEditBase(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    price: Optional[float] = None
    status: Optional[StatusAdvertisementEnum] = None
    category_id: Optional[int] = None

#for updating status
class AdvertisementStatusDisplay(BaseModel):
    status: StatusAdvertisementEnum
    class Config():
        orm_mode = True 
#end Nataliia
#----------category schemas----------
class CategoryBase(BaseModel):
    title: str   

class CategoryDisplay(BaseModel):
    title: str
    advertisements: List[Advertisement]  
    class Config():
        orm_mode = True  


AdvertisementDisplay.model_rebuild()
CategoryDisplay.model_rebuild()        
    


#--------------- Rating user and user Schemas ---------
#----------Sayed sprint2-------------

class RatingCreate(BaseModel):
    transaction_id: str
    rater_id: str
    score: int
    comment: Optional[str] = None

class RatingOut(BaseModel):
    id: str
    transaction_id: str
    rater_id: str
    ratee_id: str
    score: int
    comment: Optional[str]

    class Config:
        orm_mode = True
