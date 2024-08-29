from aiogram import html
from aiogram.filters import *
from aiogram.types import *
from aiogram import Router

import chats


keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Інструкція", callback_data="tell_instructions")],
        [InlineKeyboardButton(text="GitHub", url="https://github.com/MilkyWay96/lviv-bot")]
    ]
)


router = Router()


async def start(message: Message) -> None:
    await chats.add(message.chat.id)
    await message.answer(f"Привіт, {html.bold(message.from_user.full_name)}! Я бот-організатор клану LVIV, оберіть опцію знизу щоб продовжити:", reply_markup=keyboard)


@router.message(Command("почати"))
async def handler(message: Message) -> None:
    await start(message)


@router.callback_query(lambda c: c.data == "start")
async def callback_start_button(callback_query: CallbackQuery) -> None:
    await callback_query.answer()
    await start(callback_query.message)
