import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import coc

import config
from client import client
from register_handlers import register_handlers

# Створення телеграм боту
bot = Bot(token=config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Реєструє усі хендлери команд бота
register_handlers(dp)


async def main() -> None:
    try:
        await client.login(config.EMAIL, config.PASSWORD)
        await dp.start_polling(bot)

    except coc.InvalidCredentials as error:
        logging.error("Invalid credentials. Exiting...")
        exit(1)
        
    # Зупинити бота комбінацією клавіш Ctrl+C в терміналі
    except KeyboardInterrupt:
        logging.info("Bot is shutting down...")
        
    finally:
        await client.close()
        


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
