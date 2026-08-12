"""Legal boilerplate !!!
"""

"""A scraper and a data type enum

The scraper scrapes data and the data type enum prevents a reliance on parsing
string to determine data types
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
    """A bot that scrapes data based on timepoints and writes to JSON files

    This class decides on a timepoint to start scraping from based on the last 
    timestamp written on file. Scraping is asynchronously done across multiple 
    methods, with each method scraping a certain type of data. Each method 
    scrapes data and stores it locally within their respective method and when 
    they are done scraping, the data is pushed to a queue. In the background 
    while scraping occurs, a processor takes items in the queue and sequentially
    updates a dictionary that contains all the scraped data. Finally, the data 
    on the dictionary is written to an output file and a new timepoint is 
    written.

    Attributes:
        _CURRENT_DATETIME (datetime): The current local datetime.
        _guild (discord.Guild): The guild this bot is scraping from
        _guild_id (int): The guild ID.
        _have_initialized_timestamp_file: Whether or not the timestamp file
            has already been intialized.
        _output_file (Path): The output file.
        _queue: (ayncio.Queue[QueueData]): Where the scraper methods will
            initially push their data into.
        _scraped_data (dict(DataType, DictValue)): Dictionary containing the
            scraped data.
        _timestamp_file (datetime): The file with the last timestamp.
        _timestamp_readpoint: The last timepoint the bot was up.
    """

    def __init__(self, guild_id: int):
        """Initializes depedencies

        To satisfy the Discord API, intents is configured and a guild_id is
        stored so the guild can be set later. File paths are initialized based
        on the "src" directory, an unbounded queue is used, and a dictionary
        is used as an intermediary to hold scraped data. Timepoints and a
        boolean to regulate the intialization of a starting timepoint are also
        created.

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

        self._CURRENT_DATETIME: datetime = datetime.today()

        self._guild: discord.Guild = None

        self._output_file: Path = SRC / "output" / "output.json"
        self._queue: asyncio.Queue[QueueData] = asyncio.Queue(UNBOUNDED)
        self._timestamp_file: Path = SRC / "persistence" / "timestamp.json"
        self._timestamp_readpoint: datetime = None

        self._scraped_data: dict[DataType, DictValue] = {
            DataType.ChannelNames: [],
            DataType.Guild: None,
            DataType.NumberOfMembers: 0
        }

        self._guild_id: int = guild_id
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
        """Update _timestamp_file with self._CURRENT_TIME
        """
        
        ... # !!!

class DataType(Enum):
    """Data types that ScraperBot scrapes
    """

    ChannelNames = auto()
    Guild = auto()
    NumberOfMembers = auto()
