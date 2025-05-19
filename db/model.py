from db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

class StatusAdvertisementEnum(Enum):
    OPEN = 'open',
    SOLD = 'sold',
    RESERVED = 'reserved' 

class DbUser (Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    address = Column(String)
    phone = Column(String)
    advertisements = relationship('DbAdvertisement', back_populates='user')


class DbAdvertisement(Base):
    __tablename__ = 'advertisement'
    id = Column(Integer, primary_key=True, index=True)    
    tille = Column(String)
    content = Column(String)
    price = Column(Float)
    status = Column(StatusAdvertisementEnum, nullable=False, default=StatusAdvertisementEnum.OPEN)
    user_id = Column(Integer, ForeignKey('user.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
    user = relationship('DbUser', back_populates='advertisements')


class DbCategory(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, index=True)  
    title = Column(String)  