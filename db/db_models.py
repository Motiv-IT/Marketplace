#sayed sprint2

import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)

    given_ratings = relationship("Rating", foreign_keys="Rating.rater_id", back_populates="rater")
    received_ratings = relationship("Rating", foreign_keys="Rating.ratee_id", back_populates="ratee")


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    buyer_id = Column(String, ForeignKey("users.id"), nullable=False)
    seller_id = Column(String, ForeignKey("users.id"), nullable=False)
    completed = Column(Boolean, default=False)

    buyer = relationship("User", foreign_keys=[buyer_id], backref="purchases")
    seller = relationship("User", foreign_keys=[seller_id], backref="sales")


class Rating(Base):
    __tablename__ = "ratings"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    transaction_id = Column(String, ForeignKey("transactions.id"), nullable=False)
    rater_id = Column(String, ForeignKey("users.id"), nullable=False)
    ratee_id = Column(String, ForeignKey("users.id"), nullable=False)
    score = Column(Integer, nullable=False)
    comment = Column(Text)

    rater = relationship("User", foreign_keys=[rater_id], back_populates="given_ratings")
    ratee = relationship("User", foreign_keys=[ratee_id], back_populates="received_ratings")
