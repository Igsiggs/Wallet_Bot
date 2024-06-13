from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    wallets = relationship("Wallet", back_populates="owner")

class Wallet(Base):
    __tablename__ = 'wallets'
    id = Column(Integer, primary_key=True, index=True)
    currency = Column(String, index=True)
    balance = Column(Float, default=0.0)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="wallets")
