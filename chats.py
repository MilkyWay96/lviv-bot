import json
import aiofiles


DATA_FILE = "data/chats.json"


async def load_data() -> list:
    try:
        async with aiofiles.open(DATA_FILE, "r") as file:
            content = await file.read()
            data = json.loads(content)
            if "chats" in data and isinstance(data["chats"], list):
                return data["chats"]
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    return []


async def save_data(chat_ids: list) -> None:
    try:
        data = {"chats": chat_ids}
        async with aiofiles.open(DATA_FILE, "w") as file:
            await file.write(json.dumps(data, indent=4))
    except Exception as e:
        print(f"An error occurred: {e}")


async def add(id: int) -> None:
    chat_ids = await load_data()
    if id not in chat_ids:
        chat_ids.append(id)
        await save_data(chat_ids)


async def remove(id: int) -> None:
    chat_ids = await load_data()
    chat_ids.remove(id)
    await save_data(chat_ids)
