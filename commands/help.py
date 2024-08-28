from aiogram.filters import *
from aiogram.types import *
from aiogram import Router


instructions = f"""
/інструкція - вивести цей текст
/атаки - подивитись хто виконав атаки на поточній КВ
/вп - список гравців на випробовчому терміні
/вп тег_гравця час_ВП_в_год - дати одному або декільком гравцям ВП
"""


router = Router()


@router.callback_query(lambda c: c.data == "tell_instructions")
async def process_callback_button_click(callback_query: CallbackQuery) -> None:
    await callback_query.answer()
    await callback_query.message.answer(instructions)


@router.message(Command("інструкція"))
async def command_start_handler(message: Message) -> None:
    await message.answer(instructions)
