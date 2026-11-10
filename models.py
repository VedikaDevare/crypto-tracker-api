from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship

class Price_history(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    coin_id = Column(String, index=True, nullable=False)
    price_usd = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    watchlists = relationship("Watchlist", back_populates="user")

class Watchlist(Base):
    __tablename__ = "watchlists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column( Integer,ForeignKey("user.id"), nullable=False)
    coin_id = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "coin_id", name="unique_user_coin"),
    )
    user = relationship("User", back_populates="watchlists") 