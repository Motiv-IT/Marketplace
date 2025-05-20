from pydantic import BaseModel
from typing import List, Optional
import enum
from datetime import datetime

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
    content: Optional[str] = None    
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

#----------category schemas----------
class CategoryBase(BaseModel):
    title: str
    content: Optional[str] = None   

class CategoryDisplay(BaseModel):
    title: str
    advertisements: List[Advertisement]  
    class Config():
        orm_mode = True  

AdvertisementDisplay.model_rebuild()
CategoryDisplay.model_rebuild()        
     


