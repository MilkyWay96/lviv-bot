from aiogram.filters import *
from aiogram.types import *
from aiogram import Router

import config
from client import client


router = Router()


async def get_attack_data(clan_tag: str) -> list:
    entries = []

    last_war = await client.get_clan_war(clan_tag)

    for player in last_war.members:
        if not player.is_opponent:
            entry = (player.name, player.attacks, player.star_count)
            entries.append(entry)

    return entries


@router.message(Command("атаки"))
async def handler(message: Message) -> None:
    entries = await get_attack_data(config.CLAN_TAG)
    string = ""
    for entry in entries:
        string += f"<b>{str(len(entry[1]))}⚔️ {str(entry[2])}⭐</b> - {entry[0]}\n"
    
    await message.answer(string)