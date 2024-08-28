import coc


coc_client = coc.Client()


async def get_attack_data(clan_tag: str) -> list:
    entries = []

    last_war = await coc_client.get_clan_war(clan_tag)

    for player in last_war.members:
        if not player.is_opponent:
            entry = (player.name, player.attacks)
            entries.append(entry)

    return entries


async def login(email, password) -> None:
    await coc_client.login(email, password)


async def close() -> None:
    await coc_client.close()
