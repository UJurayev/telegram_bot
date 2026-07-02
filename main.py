import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
from handlers import router


async def main():
    if not config.BOT_TOKEN:
        print("XATOLIK: .env faylida BOT_TOKEN ko'rsatilmagan!")
        sys.exit(1)
    if not config.CHANNEL_ID:
        print("XATOLIK: .env faylida CHANNEL_ID ko'rsatilmagan!")
        sys.exit(1)

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    logging.info("Bot ishga tushdi...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")
