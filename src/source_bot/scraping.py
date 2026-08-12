"""!!!
"""

import asyncio
import json
import logging

from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Any

import discord

class ScraperBot(discord.Client):
    """Summary !!!

    More info !!!

    Attributes:
        !!!
    """

    def __init__(self, guild_id: int):
        """Summary !!!

        More info !!!

        Args:
            guild_id (int): The guild ID of the guild the bot needs to scrape
        """

        INTENTS = discord.Intents.default()
        INTENTS.members = True
        INTENTS.message_content = True

        SRC: Path = Path(__file__).parent.parent

        UNBOUNDED: int = -1

        type DictValue = list[str] | discord.Guild | int
        type QueueData = tuple[DataType, list[str] | int]

        super().__init__(intents=INTENTS)

        self._guild: discord.Guild = None # !!!

        self._output_file: Path = SRC / "output" / "output.json"
        self._queue: asyncio.Queue[QueueData] = asyncio.Queue(UNBOUNDED)
        self._timestamp_file: Path = SRC / "persistence" / "timestamp.json"
        self._timestamp_readpoint: datetime = None # !!!

        self._scraped_data: dict[DataType, DictValue] = {
            DataType.ChannelNames: [],
            DataType.Guild: None,
            DataType.NumberOfMembers: 0
        }

        self._guild_id: int = 0 # !!!
        self._have_initialized_timestamp_file: bool = False

    async def activate(self) -> None:
        """The sole entry point and fulfills the purpose of this class.

        Sets up depedencies, scraps data, processes data, and writes data to
        file.
        """

        ... # !!!

    async def _setUp(self) -> None:
        ... # !!!

    def _read_timestamp_file(self) -> None:
        """Reads _timestamp_file to initialize _timestamp_readpoint.

        If not _have_initialized_timestamp, call _init_timestamp
        with the UNIX epoch and set _timestamp_readpoint to the UNIX epoch. 
        Else, read from _timestamp_file and set _timestamp_readpoint to the read
        timestamp.
        """

        ... # !!!

    def _init_timestamp_file(self, timestamp: datetime) -> None:
        """Sets time in self._timestamp_file to timestamp.

        Additionally sets _have_initialized_timestamp_file to true.
        """

        ... # !!!

    async def _set_guild(self) -> None:
        """Sets _guild and modifies _scraped_data.

        Sets _guild to the fetched guild with _guild_id and set
        _scraped_data[DataType.Guild] to _guild.
        """
        ... # !!!

    async def _scrape(self) -> None:
        ... # !!!

    async def _scrape_channel_names(self) -> None:
        """Fetch the channel names and push them all into _queue.

        Initialize a local list. For every fetched channel name, push it into 
        the local list. Push (DataType.ChannelNames, list) into _queue.
        """

        ... # !!!
    
    async def _scrape_number_of_members(self) -> None:
        """Count the number of members and push it to _queue.

        Initialize a local counter. Increment it for every fetched member. Push
        (DataType.NumberOfMembers, counter) into _queue.
        """

        ... # !!!

    async def _process_queue(self) -> None:
        """Continuously process _queue and update _scraped_data

        In an infinite loop, for every item in _queue, update 
        _scraped_data[item[0]] with item[1]. It will terminate externally.
        """

        ... # !!!

    def _write_to_file(self) -> None:
        ... # !!!

    def _write_to_output_file(self) -> None:
        """Write _scraped_data as valid JSON to _output_file.
        """

        ... # !!!

    def _write_timestamp_file(self) -> None:
        """Update _timestamp_file with the current time and date.
        """
        
        ... # !!!

class DataType(Enum):
    """Data types that ScraperBot scrapes
    """

    ChannelNames = auto()
    Guild = auto()
    NumberOfMembers = auto()
