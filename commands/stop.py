from aiogram import html
from aiogram.filters import *
from aiogram.types import *
from aiogram import Router

import chats


router = Router()


keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Почати", callback_data="start")]
    ]
)


@router.message(Command("зупинити"))
async def handler(message: Message) -> None:
    await chats.remove(message.chat.id)
    await message.answer(f"Роботу подій призупинено, щоб відновити скористайтесь командою /почати або виберіть опцію знизу:", reply_markup=keyboard)
