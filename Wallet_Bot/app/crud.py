
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas

async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()

async def get_user_by_telegram_id(db: AsyncSession, telegram_id: str):
    result = await db.execute(select(models.User).filter(models.User.telegram_id == telegram_id))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    db_user = models.User(telegram_id=user.telegram_id)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_wallets(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.Wallet).filter(models.Wallet.owner_id == user_id))
    return result.scalars().all()

async def create_wallet(db: AsyncSession, wallet: schemas.WalletCreate, user_id: int):
    db_wallet = models.Wallet(**wallet.dict(), owner_id=user_id)
    db.add(db_wallet)
    await db.commit()
    await db.refresh(db_wallet)
    return db_wallet

async def update_wallet_balance(db: AsyncSession, wallet_id: int, amount: float):
    wallet = await db.get(models.Wallet, wallet_id)
    if wallet:
        wallet.balance += amount
        await db.commit()
        await db.refresh(wallet)
    return wallet
