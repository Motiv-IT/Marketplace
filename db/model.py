from db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
import enum
from sqlalchemy import Enum as SqlEnum
from datetime import datetime



# Enum Class for defining status of ads
class StatusAdvertisementEnum(str, enum.Enum):
    OPEN = "OPEN"
    SOLD = "SOLD"
    RESERVED = "RESERVED"
# user table
class DbUser (Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, index=True, nullable=False, unique=True)
    # password = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    address = Column(String)
    phone = Column(String)
    advertisements = relationship('DbAdvertisement', back_populates='user')

# advertisement table
class DbAdvertisement(Base):
    __tablename__ = 'advertisement'
    id = Column(Integer, primary_key=True, index=True)    
    title = Column(String, nullable=False)
    content = Column(String)
    price = Column(Float, nullable=False)
    status = Column(SqlEnum(StatusAdvertisementEnum), nullable=False, default=StatusAdvertisementEnum.OPEN)
    created_at= Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id'))
    category_id = Column(Integer, ForeignKey('category.id'))
    user = relationship('DbUser', back_populates='advertisements')
    category = relationship('DbCategory', back_populates='advertisements')

#category table
class DbCategory(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, index=True)  
    title = Column(String,nullable=False)  
    advertisements = relationship('DbAdvertisement', back_populates='category')
