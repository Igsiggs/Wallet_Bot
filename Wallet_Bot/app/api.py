from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, models, schemas
from .database import get_db

app = FastAPI()

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_telegram_id(db, telegram_id=user.telegram_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return await crud.create_user(db=db, user=user)

@app.get("/users/{user_id}/wallets/", response_model=List[schemas.Wallet])
async def read_wallets(user_id: int, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await crud.get_wallets(db=db, user_id=user_id)

@app.post("/users/{user_id}/wallets/", response_model=schemas.Wallet)
async def create_wallet_for_user(user_id: int, wallet: schemas.WalletCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await crud.create_wallet(db=db, wallet=wallet, user_id=user_id)
