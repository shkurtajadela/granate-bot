import asyncio
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from bot.database import db_start, db_close
from django.core.management.base import BaseCommand
from django.conf import settings
from ..bot.main_handlers import *
from aiogram import Bot
from dotenv import load_dotenv
import os

load_dotenv('.env')
token = os.getenv("TOKEN_API")
bot = Bot(token)

def register_handler(dp: Dispatcher) -> None:
    register_handlers(dp=dp)

class Command(BaseCommand):
    help = 'Telegram-bot'

    async def async_handle(self, *args, **options):
        storage = MemoryStorage()

        dp = Dispatcher(bot, storage=storage)

        register_handler(dp=dp)

        try:
            await dp.start_polling()
        except KeyboardInterrupt:
            # Handle Ctrl+C here
            pass
        except Exception as _ex:
            pass


    def handle(self, *args, **options):
        asyncio.run(self.async_handle(*args, **options))
# async def main() -> None:
#     # db_start()

#     storage = MemoryStorage()

#     dp = Dispatcher(bot, storage=storage)

#     register_handler(dp=dp)

#     try:
#         await dp.start_polling()
#     except Exception as _ex:
#         pass
#     # finally:
#     #     db_close()


# if __name__ == "__main__":
#     asyncio.run(main())