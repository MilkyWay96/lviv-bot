import asyncio
import logging
import sys

import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import *
from aiogram.types import *

import coc
import cocreq


load_dotenv("config.env")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
CLAN_TAG = os.getenv("CLAN_TAG")
TOKEN = os.getenv("BOT_TOKEN")


coc_client = coc.Client()
dp = Dispatcher()


instructions = f'''
/інструкція - вивести цей текст
/атаки - подивитись хто виконав атаки на поточній КВ
'''


keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Інструкція", callback_data="tell_instructions")]
    ]
)


@dp.message(Command("почати"))
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привіт, {html.bold(message.from_user.full_name)}! Я бот-організатор клану LVIV, оберіть опцію знизу щоб продовжити:", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "tell_instructions")
async def process_callback_button_click(callback_query: CallbackQuery) -> None:
    await callback_query.answer()
    await callback_query.message.answer(instructions)


@dp.message(Command("інструкція"))
async def command_start_handler(message: Message) -> None:
    await message.answer(instructions)


@dp.message(Command("атаки"))
async def command_start_handler(message: Message) -> None:
    await message.answer("Отримання данних з сервера...")

    entries = await cocreq.get_attack_data(coc_client, CLAN_TAG)
    string = ""
    for entry in entries:
        string += str(len(entry[1])) + " - " + entry[0] + "\n"
    
    await message.answer(string)


async def main() -> None:
    try:
        await coc_client.login(EMAIL, PASSWORD)
        bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        await dp.start_polling(bot)

    except coc.InvalidCredentials as error:
        logging.error("Invalid credentials. Exiting...")
        exit(1)

    except KeyboardInterrupt:
        logging.info("Bot is shutting down...")
        
    finally:
        await coc_client.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
