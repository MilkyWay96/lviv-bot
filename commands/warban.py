from aiogram import html
from aiogram.filters import *
from aiogram.types import *
from aiogram import Router

import config
import coc
import Levenshtein
from client import client
import warban as wb

from datetime import datetime


router = Router()


async def warban_list(message: Message) -> None:
    players = await wb.load_data()
    answer = "Список ВП:\n"
    passed = []

    for tag in players:
        if await wb.get_datetime(tag) < datetime.now():
            passed.append(tag)
            continue
        player = await client.get_player(tag)
        time_diff = await wb.get_datetime(tag) - datetime.now()
        time_str = str(round(time_diff.total_seconds() / 3600 + 0.5)) + " год"
        if time_diff.total_seconds() < 3600:
                ime_str = "&lt;1 год"
        answer += f"{player.name} (залишилось {time_str})\n"

    for tag in passed:
        del players[tag]
    await wb.save_data(players)

    if len(players) == 0:
        await message.answer("Список ВП пустий, молодці!")
    else:
        await message.answer(answer)


async def clear_warban_list(message: Message) -> None:
    data = {}
    await wb.save_data(data)
    await message.answer("Список ВП очищено")


async def get_member(string: str, max_distance: int) -> coc.ClanMember:
    closest = None
    clan = await client.get_clan(config.CLAN_TAG)
    if string[0] == "#":
        return clan.get_member(string)
    else:
        names = []
        min_distance = max_distance + 1
        for member in clan.members:
            distance = Levenshtein.distance(string, member.name)
            if distance <= max_distance and distance < min_distance:
                closest = member
                min_distance = distance

        return closest


async def warban(args: list, message: Message) -> None:
    answer = ""
        
    for i in range(0, len(args), 2):
        string = args[i]
        try:
            add_time = int(args[i+1])
        except (ValueError, IndexError):
            await message.answer(f"Кількість годин ВП може бути лише цілим числом")
            continue

        try:
            member = await get_member(string, round(len(string) / 2))
        except Exception as e:
            await message.answer(f"Сталась непередбачувана помилка: {str(e)}")

        if member is None:
            answer += f"Гравця {string} не знайдено\n"
            continue

        await wb.add_time(member.tag, add_time)
        answer += f"Додано {str(add_time)} год гравцю \"{member.name}\"\n"
        
    await message.answer(answer)


@router.message(Command("вп"))
async def handler(message: Message) -> None:
    command_parts = message.text.split(maxsplit=1)
    
    if len(command_parts) > 1:
        args = command_parts[1].split()

        if len(args) == 1 and args[0] == "0":
            await clear_warban_list(message)
        elif len(args) % 2 == 0:
            await warban(args, message)
        else:
            await message.answer("Невірна структура команди. Надавайте аргументи за схемою: /вп тег_гравця1 час_ВП_в_год тег_гравця2 час_ВП_в_год...")
    else:
        await warban_list(message)