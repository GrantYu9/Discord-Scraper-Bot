"""!!!
"""

import asyncio
import json
import logging

from pathlib import Path

import discord

class ScraperBot(discord.Client):
    """!!!
    """

    def __init__(self, guild_id: int):
        self._INTENTS = discord.Intents.default()
        self._INTENTS.members = True
        self._INTENTS.message_content = True
        super().__init__(intents=self._INTENTS)

        self._guild_id: int = 0 # !!!
        self._setUp: bool = False # !!!

        pass # !!!

    async def activate(self) -> None:
        pass # !!!

    def _cleanUp(self) -> None:
        """!!!
        """
        pass # !!!

    async def _processItemsInQueue(self) -> None:
        """!!!
        """
        pass # !!!

    def _readTimestamps(self) -> None:
        """!!!
        """
        pass # !!!

    def _resetTimestamps(self) -> None:
        """!!!
        """

    async def _setGuild(self) -> None:
        """!!!
        """
        pass # !!!

    async def _setUp(self) -> None:
        """!!!
        """
        pass # !!!

    async def _scrape(self) -> None:
        """!!!
        """
        pass # !!!

    async def _scrapeChannelNames(self) -> None:
        """!!!
        """
        pass # !!!
    
    async def _scrapeNumberOfMembers(self) -> None:
        """!!!
        """
        pass # !!!

    def _writeTimestamps(self) -> None:
        """!!!
        """
        pass # !!!

    def _writeToOutput(self) -> None:
        """!!!
        """
        pass # !!!
