from aiogram import html
from aiogram.filters import *
from aiogram.types import *
from aiogram import Router


router = Router()


keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Інструкція", callback_data="tell_instructions")],
        [InlineKeyboardButton(text="GitHub", url="https://github.com/MilkyWay96/lviv-bot")]
    ]
)


@router.message(Command("почати"))
async def handler(message: Message) -> None:
    await message.answer(f"Привіт, {html.bold(message.from_user.full_name)}! Я бот-організатор клану LVIV, оберіть опцію знизу щоб продовжити:", reply_markup=keyboard)
