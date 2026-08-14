"""A scraper and a data type StrEnum
"""

import asyncio
import json

# from datetime import datetime
from enum import StrEnum
from pathlib import Path

import discord

class Scraper(discord.Client):
    """A bot that scrapes data and writes as JSON to file.

    The bot sets up depedencies, initiates processing of a queue in the
    background, initiates scraping, and writes to file. While scraping, each
    guild has its own internal queue to process data that each subscraper for
    each supported data type will push data into. The internal processor will
    modify an internal dictionary. When scraping is done for a guild, the
    internal dictionary will be pushed into the upper level queue that collects
    data from all guilds and will push it into an upper level dictionary. When
    processing of data from all guilds is complete, the upper level dictionary
    will be converted into a JSON object and written to file.

    Attributes:
        _SRC (Path): The "src" directory. Helps methods with initialization
            of file paths.
        _UNBOUNDED (int): The size indicator for an unbounded asyncio.Queue.
    """

    type Data = dict | list[str] | int

    type QueueData = tuple[str, Data]

    def __init__(self):
        """Initializes depedencies

        Sets up INTENTS for the discord API along with helpful static globals.
        """

        INTENTS = discord.Intents.default()
        INTENTS.members = True
        INTENTS.message_content = True

        # UNIX_EPOCH: int = 0

        super().__init__(intents=INTENTS)

        # self._CURRENT_DATETIME: datetime = datetime.today()
        self._SRC: Path = Path(__file__).parent.parent
        self._UNBOUNDED: int = -1
        # self._UNIX_EPOCH: datetime = datetime.fromtimestamp(UNIX_EPOCH)
        
        # self._guilds: list[str] = []
        # self._readpoint: datetime = None
        # self._timestamp_file: Path = (
        #     self._SRC / "persistence" / "timestamp.json"
        # )
    
    async def activate(self) -> None:
        """The entry point into the class and where the magic happens.

        Activate will prepare the scraper for scraping, scrape the guilds, and
        write to file
        """

        data = {}
        queue = asyncio.Queue(self._UNBOUNDED)

        await self._scrape_guilds(queue, data)

        self._write_to_output_file(data)

        # !!!

    # def _setUp(self) -> None:
    #     ... # !!!

    # def _read_guilds_file(self) -> None:
    #     """!!!
    #     """

    #     ... # !!!
    
    # def _read_timestamp_file(self) -> None:
    #     """Reads _timestamp_file to initialize _timestamp_readpoint.

    #     If no valid JSON to read, pass.
    #     """

    #     ... # !!!
    
    async def _scrape_guilds(
        self, 
        queue: asyncio.Queue[QueueData],
        data: dict) -> None:
        """Initiate scraping of all the guilds.

        Initiate a background processor with "queue" and "data." For each guild
        in self.guilds, initiate a scrape of the guild. Upon completion of all
        scraping, cancel the processor.
        """

        processor = asyncio.create_task(self._process_queue(queue, data))

        await asyncio.gather(
            *(self._scrape_guild(guild, queue) for guild in self.guilds)
        )

        processor.cancel()

        # !!!
    
    async def _scrape_guild(
        self, 
        guild: discord.Guild,
        external_queue: asyncio.Queue[QueueData]) -> None:
        """Internally scrape data for "guild" and push the data into the queue.

        Create a local queue and a local data dict for "guild." A background
        processor will process this queue and modify the local dict when data
        from the subscrapers comes in. Each of the subscrapers takes the local
        queue so it can push data into it. When all the subscrapers are done,
        the dict will be pushed to "external_queue" as a tuple:
        (guild.name, dict)
        """

        data = {}
        internal_queue = asyncio.Queue(self._UNBOUNDED)

        processor = asyncio.create_task(
            self._process_queue(internal_queue, data)
        )

        await asyncio.gather(
            self._scrape_channel_names(guild, internal_queue),
            self._scrape_number_of_members(guild, internal_queue)
        )

        processor.cancel()

        await external_queue.put((guild.name, data))
        
        # !!!

    async def _scrape_channel_names(
        self, 
        guild: discord.Guild, 
        queue: asyncio.Queue[QueueData]) -> None:
        """Fetch channel names from "guild" and push the names into "queue."

        Instantiate a local list. For each channel name in "guild", append it
        to list. Upon completion of iteration, push the list into "queue" as a
        tuple: (DataType.ChannelNames, list).
        """

        channel_names = [
            channel.name for channel in await guild.fetch_channels()
        ]

        await queue.put((DataType.ChannelNames, channel_names))
    
    async def _scrape_number_of_members(
        self, 
        guild: discord.Guild, 
        queue: asyncio.Queue[QueueData]) -> None:
        """Count members from "guild" and push count into "queue."

        Instantiate a local counter. For each member in "guild", increment the
        counter. Upon completion of iteration, push the counter into "queue" as 
        a tuple: (DataType.NumberOfMembers, counter).
        """

        number_of_members = 0

        async for member in guild.fetch_members():
            number_of_members += 1

        await queue.put((DataType.NumberOfMembers, number_of_members))

    async def _process_queue(
        self, 
        queue: asyncio.Queue[QueueData], 
        data: dict) -> None:
        """Update "data" with every item in "queue."

        Let KEY = 0 and VALUE = 1. While True, take an item from "queue" and
        modify "data" such that data[item[KEY]] = item[VALUE]. _process_queue is
        meant to be very general with what data type "data" could be.
        """

        KEY = 0
        VALUE = 1

        while True:
            item = await queue.get()

            data[item[KEY]] = item[VALUE]

        # !!!

    # def _finish(self, data: dict) -> None:
    #     ... # !!!

    def _write_to_output_file(self, data: dict) -> None:
        INDENT = 4
        OUTPUT_FILE = self._SRC / "output" / "output.json"

        with OUTPUT_FILE.open(mode='w') as file:
            json.dump(data, file, indent=INDENT)

        # !!!

    # def _write_timestamp_file(self) -> None:
    #     ... # !!!

class DataType(StrEnum):
    """A StrEnum of types that Scraper scrapes
    """

    ChannelNames = "channel_names"
    NumberOfMembers = "number_of_members"
