from aiogram import html
from aiogram.filters import *
from aiogram.types import *
from aiogram import Router

import config
from client import client
import warban as wb

from datetime import datetime


router = Router()


async def warban_list(message: Message) -> None:
    players = await wb.load_data()
    answer = ""
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


async def warban(args: list, message: Message) -> None:
    string = "Список ВП:\n"
        
    for i in range(0, len(args), 2):
        tag = args[i]
        try:
            add_time = int(args[i+1])
        except (ValueError, IndexError):
            await message.answer(f"Кількість годин ВП може бути лише цілим числом")
            continue

        try:
            clan = await client.get_clan(config.CLAN_TAG)
            player = clan.get_member(tag)
            if player is None:
                string += f"Гравця {tag} не знайдено\n"
                continue

            await wb.add_time(tag, add_time)
            string += f"Додано {str(add_time)} год гравцю \"{player.name}\"\n"
        except Exception as e:
            await message.answer(f"Сталась непередбачувана помилка: {str(e)}")
    await message.answer(string)


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