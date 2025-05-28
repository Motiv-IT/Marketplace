from db.database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    ForeignKey,
    Enum,
    DateTime,
    Text,
)
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


class ScoreTypeEnum(str, enum.Enum):
    BUYER_SCORE = "BUYER_SCORE"
    SELLER_SCORE = "SELLER_SCORE"


# user table
class DbUser(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, index=True, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    address = Column(String)
    phone = Column(String)
    advertisements = relationship("DbAdvertisement", back_populates="user")
    purchases = relationship(
        "DbTransaction",
        back_populates="buyer",
        foreign_keys=lambda: [DbTransaction.buyer_id],
    )


# advertisement table
class DbAdvertisement(Base):
    __tablename__ = "advertisement"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String)
    price = Column(Float, nullable=False)
    status = Column(
        SqlEnum(StatusAdvertisementEnum),
        nullable=False,
        default=StatusAdvertisementEnum.OPEN,
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("user.id"))
    category_id = Column(Integer, ForeignKey("category.id"))
    user = relationship("DbUser", back_populates="advertisements")
    category = relationship("DbCategory", back_populates="advertisements")
    transaction = relationship("DbTransaction", back_populates="advertisement")


# category table
class DbCategory(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    advertisements = relationship("DbAdvertisement", back_populates="category")


# transaction table
class DbTransaction(Base):
    __tablename__ = "transactions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    buyer_id = Column(String, ForeignKey("user.id"), nullable=False)
    advertisement_id = Column(Integer, ForeignKey("advertisement.id"), nullable=False)
    completed = Column(Boolean, default=False)
    buyer = relationship("DbUser", foreign_keys=[buyer_id], back_populates="purchases")
    advertisement = relationship("DbAdvertisement", back_populates="transaction")
    rating = relationship("DbRating", back_populates="transaction")


# rating table
class DbRating(Base):
    __tablename__ = "ratings"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    transaction_id = Column(String, ForeignKey("transactions.id"), nullable=False)
    score_type = Column(SqlEnum(ScoreTypeEnum), nullable=False)
    score = Column(Integer, nullable=False)
    comment = Column(Text)
    transaction = relationship("DbTransaction", back_populates="rating")
