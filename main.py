import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import coc

import config
import coclayer
import reghandlers


dp = Dispatcher()
reghandlers.register_handlers(dp)


async def main() -> None:
    try:
        await coclayer.login(config.EMAIL, config.PASSWORD)
        bot = Bot(token=config.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        await dp.start_polling(bot)

    except coc.InvalidCredentials as error:
        logging.error("Invalid credentials. Exiting...")
        exit(1)

    except KeyboardInterrupt:
        logging.info("Bot is shutting down...")
        
    finally:
        await coclayer.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
