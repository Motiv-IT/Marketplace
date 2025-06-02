from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional
import enum
from datetime import datetime

#---------user schemas----------

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str
    model_config = ConfigDict(from_attributes=True)

class UserOut(BaseModel):
    id: int
    username: str
    email: str   # <-- to fix the KeyError
    model_config = ConfigDict(from_attributes=True)

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
    model_config = ConfigDict(from_attributes=True)

class User(BaseModel):
    username: str
    email: str
    address: Optional[str] = None
    phone: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class Category(BaseModel):
    title: str   
    model_config = ConfigDict(from_attributes=True)

#---------user schemas----------

class UserBase(BaseModel):
    username: str
    email: str
    password: str
    address: Optional[str] = None
    phone: Optional[str] = None

class UserDisplay(BaseModel):
    username: str
    email: str
    advertisements: List[Advertisement]
    model_config = ConfigDict(from_attributes=True)

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
    model_config = ConfigDict(from_attributes=True)

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
    model_config = ConfigDict(from_attributes=True)
#end Nataliia

#----------category schemas----------

class CategoryBase(BaseModel):
    title: str   

class CategoryDisplay(BaseModel):
    title: str
    advertisements: List[Advertisement]  
    model_config = ConfigDict(from_attributes=True)

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
    model_config = ConfigDict(from_attributes=True)
    

#--------------- transactions Schemas ---------
#----------Tina sprint2-------------
class TransactionCreate(BaseModel):
    advertisement_id: int
    completed: bool                 
    model_config = ConfigDict(from_attributes=True)


class TransactionRead(BaseModel):
    id: int
    buyer_id: int
    seller_id: int
    advertisement_id: int
    completed: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)