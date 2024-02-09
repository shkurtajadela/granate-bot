import asyncio
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.database import db_start, db_close
from bot.main_handlers import *
from aiogram import Bot
from dotenv import load_dotenv
import os

load_dotenv('.env')
token = os.getenv("TOKEN_API")
bot = Bot(token)

def register_handler(dp: Dispatcher) -> None:
    register_handlers(dp=dp)

async def main() -> None:
    db_start()

    storage = MemoryStorage()

    dp = Dispatcher(bot, storage=storage)

    register_handler(dp=dp)

    try:
        await dp.start_polling()
    except Exception as _ex:
        pass
    finally:
        db_close()


if __name__ == "__main__":
    asyncio.run(main())