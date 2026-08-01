import asyncio
import json

from pathlib import Path

import discord

class ScraperBot(discord.Client):
    def __init__(self, guild_id: int):
        UNBOUNDED = -1

        self._intents = discord.Intents.default()
        self._intents.members = True
        self._intents.message_content = True

        super().__init__(intents=self._intents)

        self._guild_id = guild_id
        self._lock = asyncio.Lock()
        self._scraped_data = []

        self._guild: discord.Guild = None
    
    async def on_ready(self) -> None:
        await self._setUp()

        await self._scrape()
        self._writeToFile()

        await self.close()

    async def start(self, token: str) -> None:
        await super().start(token)

    async def _getMembers(self) -> None:
        async for member in self._guild.fetch_members():
            member_data = {
                "id": member.id,
                "name": member.name
            }

            self._scraped_data.append(member_data)

    async def _scrape(self) -> None:
        await self._getMembers()

    async def _setGuild(self) -> None:
        self._guild = await super().fetch_guild(self._guild_id)  

    async def _setUp(self) -> None:
        await self._setGuild()
    
    def _writeToFile(self) -> None:
        SRC = Path(__file__).parent.parent
        JSON = SRC / "json"
        MEMBERS = JSON / "members.json"
    
        with open(MEMBERS, mode='w') as file:
            file.write(json.dumps(self._scraped_data, indent=4))
