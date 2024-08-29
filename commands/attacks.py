from aiogram.filters import *
from aiogram.types import *
from aiogram import Router

import config
import coc
from client import client


router = Router()


async def get_attack_data(war: coc.ClanWar) -> list:
    entries = []
    for player in war.members:
        if not player.is_opponent:
            entry = (player.map_position, player.name, player.attacks, player.star_count)
            entries.append(entry)

    return entries


@router.message(Command("атаки"))
async def handler(message: Message) -> None:
    war = await client.get_clan_war(config.CLAN_TAG)
    entries = await get_attack_data(war)
    string = f"<b>{war.clan.name}</b>  <i>проти</i>  <b>{war.opponent.name}</b>\n"
    for entry in entries:
        string += f"<b>{str(len(entry[2]))}⚔️  {str(entry[3])}⭐</b>  -  {str(entry[0])}. {entry[1]}\n"
    
    await message.answer(string)