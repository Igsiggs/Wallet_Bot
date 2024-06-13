import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from .config import settings
from .database import get_db
from .crud import create_user, get_user_by_telegram_id, get_wallets, create_wallet, update_wallet_balance

logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    async with get_db() as db:
        user = await get_user_by_telegram_id(db, telegram_id=message.from_user.id)
        if user is None:
            user = await create_user(db, schemas.UserCreate(telegram_id=message.from_user.id))
        await message.reply("Привет! Я бот-кошелек. Используйте команды /create_wallet, /wallets, /send.")

@dp.message_handler(commands=["create_wallet"])
async def cmd_create_wallet(message: types.Message):
    currency = message.get_args()
    async with get_db() as db:
        user = await get_user_by_telegram_id(db, telegram_id=message.from_user.id)
        if user:
            wallet = await create_wallet(db, schemas.WalletCreate(currency=currency, balance=0.0), user_id=user.id)
            await message.reply(f"Кошелек {currency} создан с ID {wallet.id}.")

@dp.message_handler(commands=["wallets"])
async def cmd_wallets(message: types.Message):
    async with get_db() as db:
        user = await get_user_by_telegram_id(db, telegram_id=message.from_user.id)
        if user:
            wallets = await get_wallets(db, user_id=user.id)
            response = "\n".join([f"ID: {wallet.id}, Валюта: {wallet.currency}, Баланс: {wallet.balance}" for wallet in wallets])
            await message.reply(response)

@dp.message_handler(commands=["send"])
async def cmd_send(message: types.Message):
    args = message.get_args().split()
    if len(args) != 3:
        await message.reply("Использование: /send <wallet_id> <amount> <target_wallet_id>")
        return
    wallet_id, amount, target_wallet_id = map(int, args)
    async with get_db() as db:
        wallet = await update_wallet_balance(db, wallet_id, -amount)
        if wallet:
            await update_wallet_balance(db, target_wallet_id, amount)
            await message.reply("Перевод выполнен.")
        else:
            await message.reply("Ошибка при переводе.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
