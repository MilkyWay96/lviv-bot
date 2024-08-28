import json
from datetime import datetime, timedelta
import aiofiles
import asyncio


DATA_FILE = "data/warban.json"


async def load_data():
    try:
        async with aiofiles.open(DATA_FILE, "r") as file:
            content = await file.read()
            data = json.loads(content)
            for player, info in data.items():
                if "end_datetime" in info:
                    info["end_datetime"] = datetime.fromisoformat(info["end_datetime"])
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return data


async def save_data(data):
    for player, info in data.items():
        if "end_datetime" in info and isinstance(info["end_datetime"], datetime):
            info["end_datetime"] = info["end_datetime"].isoformat()
    async with aiofiles.open(DATA_FILE, "w") as file:
        await file.write(json.dumps(data, indent=4))


async def add_time(tag, add_hours):
    players = await load_data()
    players[tag] = {"end_datetime": await get_datetime(tag) + timedelta(hours=add_hours)}
    await save_data(players)


async def get_datetime(tag):
    players = await load_data()
    player = players.get(tag)
    if player is None:
        return datetime.now()
    end_datetime = player.get("end_datetime")
    if end_datetime is str:
        end_datetime = datetime.fromisoformat(end_datetime).strftime("%Y-%m-%d %H:%M:%S")
    return end_datetime
