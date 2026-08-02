import asyncio
import json
import logging

from pathlib import Path

import discord

class ScraperBot(discord.Client):
    def __init__(self, guild_id: int):
        pass # !!!

    async def on_ready(self) -> None:
        pass # !!!

    async def setup_hook(self) -> None:
        pass # !!!

    async def _processItemsInQueue(self) -> None:
        pass # !!!

    async def _readTimestamps(self) -> None:
        pass # !!!

    async def _setUpScrapingDependencies(self) -> None:
        pass # !!!

    async def _scrape(self) -> None:
        pass # !!!

    async def _scrapeChannelNames(self) -> None:
        pass # !!!
    
    async def _scrapeNumberOfMembers(self) -> None:
        pass # !!!

    async def _writeToJSON(self) -> None:
        pass # !!!
