"""A scraper and a data type enum

!!!
"""

import asyncio
import json

from asyncio import Queue
from datetime import datetime
from enum import Enum, auto
from pathlib import Path

import discord

from discord import Guild

class Scraper(discord.Client):
    """!!!

    !!!

    Attributes:
        !!!
    """

    def __init__(self):
        """!!!
        """

        INTENTS = discord.Intents.default()
        INTENTS.members = True
        INTENTS.message_content = True

        UNIX_EPOCH: int = 0

        super().__init__(intents=INTENTS)

        self._CURRENT_DATETIME: datetime = datetime.today()
        self._SRC: Path = Path(__file__).parent.parent
        self._UNBOUNDED: int = -1
        self._UNIX_EPOCH: datetime = datetime.fromtimestamp(UNIX_EPOCH)

        self._guilds: list[str] = []
        self._readpoint: datetime = None
        self._timestamp_file: Path = (
            self._SRC / "persistence" / "timestamp.json"
        )
    
    async def activate(self) -> None:
        """!!!
        """
        data = {}
        queue: Queue[tuple[DataType | str, dict]] = Queue(self._UNBOUNDED)

        self._setUp()

        processor = asyncio.create_task(self._process_queue(queue, data))

        await self._scrape_guilds(queue)

        processor.cancel()

        self._finish(data)

        ... # !!!

    def _setUp(self) -> None:
        ... # !!!

    def _read_guilds_file(self) -> None:
        """!!!
        """
        ... # !!!
    
    def _read_timestamp_file(self) -> None:
        """Reads _timestamp_file to initialize _timestamp_readpoint.

        If no valid JSON to read, pass.
        """

        ... # !!!
    
    async def _scrape_guilds(self, queue: Queue) -> None:
        """!!!!
        """

        tasks = []

        for guild in self.guilds:
            if guild in self._guilds:
                timepoint = self._readpoint
            else:
                timepoint = self._UNIX_EPOCH
            
            tasks.append(self._scrape_guild(guild, queue, timepoint))
        
        await asyncio.gather(*tasks)
                

        ... # !!!

    async def _scrape_guild(self, 
        guild: Guild, queue_guilds: Queue, readpoint: datetime) -> None:
        """!!!
        """

        queue_guild = Queue(self._UNBOUNDED)

        data = {}

        inner_processor = asyncio.create_task(self._process_queue(queue_guild, data))

        await asyncio.gather(
            self._scrape_channel_names(guild, queue_guild, readpoint),
            self._scrape_number_of_members(guild, queue_guild, readpoint)
        )

        inner_processor.cancel()

        await queue_guilds.put((guild.name, data))

        ... # !!!

    async def _scrape_channel_names(self, 
        guild: Guild, queue: Queue, readpoint: datetime) -> None:
        """!!!
        """

        channel_names: list[str] = []

        for channel in await guild.fetch_channels():
            channel_names.append(channel.name)

        await queue.put((DataType.ChannelNames.value, channel_names))
        ... # !!!
    
    async def _scrape_number_of_members(self, 
        guild: Guild, queue: Queue, readpoint: datetime) -> None:
        """!!!
        """

        ... # !!!

    async def _process_queue(self, queue: Queue, output: dict) -> None:
        """!!!
        """
        KEY: int = 0
        VALUE: int = 1

        while True:
            item = await queue.get()

            output[item[KEY]] = item[VALUE]

        ... # !!!

    def _finish(self, data: dict) -> None:
        self._write_to_output_file(data)
        self._write_timestamp_file()
        ... # !!!

    def _write_to_output_file(self, data: dict) -> None:
        """Write _scraped_data as valid JSON to _output_file. !!!
        """

        OUTPUT_FILE: Path = self._SRC / "output" / "output.json"

        with OUTPUT_FILE.open(mode='w') as file:
            file.write(json.dumps(data, indent=4))

        ... # !!!

    def _write_timestamp_file(self) -> None:
        """Update _timestamp_file with self._CURRENT_TIME
        """
        
        ... # !!!

class DataType(Enum):
    """Data types that ScraperBot scrapes
    """

    ChannelNames = "channel_names"
    NumberOfMembers = "number_of_members"
