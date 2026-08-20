import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import config
from database import db
from handlers.main import router

async def main():
    if not config.bot_token:
        raise RuntimeError("BOT_TOKEN .env faylida ko‘rsatilmagan")
    logging.basicConfig(level=logging.INFO)
    await db.init()
    bot = Bot(config.bot_token)
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

