"""!!!
"""

import asyncio
import json
import logging

from enum import Enum, auto
from pathlib import Path

import discord

class ScraperBot(discord.Client):
    """!!!
    """

    def __init__(self, guild_id: int):
        UNBOUNDED = - 1

        self._INTENTS = discord.Intents.default()
        self._INTENTS.members = True
        self._INTENTS.message_content = True
        super().__init__(intents=self._INTENTS)

        self._guild: discord.Guild = None

        print(self._guild.name)

        self._queue: asyncio.Queue = None

        self._scraped_data: dict[DataTypes, list[str] | int] = {
            DataTypes.ChannelNames: [],
            DataTypes.NumberOfMembers: 0
        }

        self._guildId: int = guild_id
        self._initTimestampsBool: bool = False

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

    # !!!

    def _writeTimestamps(self) -> None:
        """!!!
        """
        pass # !!!

class DataTypes(Enum):
    ChannelNames = auto()
    NumberOfMembers = auto()

class TimestampsAlreadyInitializedException(Exception):
    def __init__(self):
        super().__init__("Timestamps already initialized.")
