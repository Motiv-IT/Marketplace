from db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Enum, DateTime, Text
from sqlalchemy.orm import relationship
import enum
from sqlalchemy import Enum as SqlEnum
from datetime import datetime
import uuid



# Enum Class for defining status of ads
class StatusAdvertisementEnum(str, enum.Enum):
    OPEN = "OPEN"
    SOLD = "SOLD"
    RESERVED = "RESERVED"
# user table
class DbUser (Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True) #remove default=lambda: str(uuid.uuid4()) to avoid type mismatch.
    username = Column(String, nullable=False)
    email = Column(String, index=True, nullable=False, unique=True)
    # password = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    address = Column(String)
    phone = Column(String)
    advertisements   = relationship("DbAdvertisement", back_populates="user", cascade="all, delete-orphan")
    given_ratings    = relationship("Rating", foreign_keys="Rating.rater_id", back_populates="rater", cascade="all, delete-orphan")
    received_ratings = relationship("Rating", foreign_keys="Rating.ratee_id", back_populates="ratee", cascade="all, delete-orphan")
    purchases        = relationship("Transaction", foreign_keys="Transaction.buyer_id", back_populates="buyer", cascade="all, delete-orphan")
    sales            = relationship("Transaction", foreign_keys="Transaction.seller_id", back_populates="seller", cascade="all, delete-orphan")
    
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
    transactions  = relationship("Transaction",  foreign_keys="Transaction.advertisement_id" , back_populates="advertisement", cascade="all, delete-orphan")


#category table
class DbCategory(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, index=True)  
    title = Column(String,nullable=False)  
    advertisements = relationship('DbAdvertisement', back_populates='category')

#Tina Sprint2 beginning
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True) #remove default=lambda: str(uuid.uuid4()) to avoid type mismatch.
    buyer_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    advertisement_id = Column(Integer, ForeignKey("advertisement.id"), nullable=False)

    buyer         = relationship("DbUser",  foreign_keys=[buyer_id],         back_populates="purchases")
    seller        = relationship("DbUser", foreign_keys=[seller_id],        back_populates="sales")
    advertisement = relationship("DbAdvertisement", foreign_keys=[advertisement_id], back_populates="transactions")
    ratings       = relationship("Rating", foreign_keys="Rating.transaction_id", back_populates="transaction", cascade="all, delete-orphan")
    
class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True) #remove default=lambda: str(uuid.uuid4()) to avoid type mismatch.
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=False)
    rater_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    ratee_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    score = Column(Integer, nullable=False)
    comment = Column(Text)

    rater = relationship("DbUser", foreign_keys=[rater_id], back_populates="given_ratings")
    ratee = relationship("DbUser", foreign_keys=[ratee_id], back_populates="received_ratings")
    transaction   = relationship("Transaction", foreign_keys=[transaction_id] , back_populates="ratings")
    
# Tina Sprint2 end