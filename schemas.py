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

#----for CHANGING STATUS-------#
class StatusChangeAdvertisementEnum(str, enum.Enum):
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
    status: StatusChangeAdvertisementEnum
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
    
#-----------images---------------#
class ImageOrderDisplay(BaseModel):
    id:int
    new_order_id:int

class ImageAllDisplay(BaseModel):
    id:int
    order_id:int
    image_name:str
    image_path: str
    class Config():
        orm_mode = True

class ImageOneDisplay(BaseModel):
    id:int
    order_id:int
    image_name:str
    image_path: str
    advertisement:Advertisement
  
    class Config():
        orm_mode = True



class Image(BaseModel):
    order_id:int
    image_name:str
class AdvertisementOneDisplay(BaseModel):
    title: str
    content: str
    price: float
    status: StatusAdvertisementEnum
    created_at: datetime
    user: User
    category: Category
    images:List[Image]
    class Config():
        orm_mode = True 

class AdvertisementShortDisplay(BaseModel):
    title: str
    price: float
    status: StatusAdvertisementEnum
    created_at: datetime
    category:CategoryBase
    class Config():
        orm_mode = True 

AdvertisementOneDisplay.model_rebuild()


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
