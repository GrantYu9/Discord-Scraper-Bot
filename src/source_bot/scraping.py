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
        self._initTimestampsBool: bool = False # !!!

    async def activate(self) -> None:
        pass # !!!

    async def _setUp(self) -> None:
        """!!!
        """
        pass # !!!

    def _readTimestamps(self) -> None:
        """!!!
        """
        pass # !!!

    def _initTimestamps(self) -> None:
        """!!!
        """

    async def _setGuild(self) -> None:
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

    async def _processItemsInQueue(self) -> None:
        """!!!
        """
        pass # !!!

    def _pushPayload(self) -> None:
        """!!!
        """
        pass # !!!

    def _writeToOutput(self) -> None:
        """!!!
        """
        pass # !!!

    def _writeTimestamps(self) -> None:
        """!!!
        """
        pass # !!!

class TimestampsAlreadyInitializedException(Exception):
    def __init__(self):
        super().__init__("Timestamps already initialized.")
