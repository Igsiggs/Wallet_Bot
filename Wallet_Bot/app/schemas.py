
from pydantic import BaseModel
from typing import List

class WalletBase(BaseModel):
    currency: str
    balance: float

class WalletCreate(WalletBase):
    pass

class Wallet(WalletBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    telegram_id: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    wallets: List[Wallet] = []

    class Config:
        orm_mode = True
