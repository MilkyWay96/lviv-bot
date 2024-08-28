from aiogram.filters import *
from aiogram.types import *
from aiogram import Router

import config
import coclayer


router = Router()


@router.message(Command("атаки"))
async def handler(message: Message) -> None:
    entries = await coclayer.get_attack_data(config.CLAN_TAG)
    string = ""
    for entry in entries:
        string += f"{str(len(entry[1]))} - {entry[0]}\n"
    
    await message.answer(string)