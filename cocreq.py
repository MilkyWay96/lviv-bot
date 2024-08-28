import asyncio
import coc


async def get_attack_data(coc_client, clan_tag):
    entries = []

    last_war = await coc_client.get_clan_war(clan_tag)

    for player in last_war.members:
        if not player.is_opponent:
            entry = (player.name, player.attacks)
            entries.append(entry)

    return entries