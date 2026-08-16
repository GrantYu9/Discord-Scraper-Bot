import asyncio
import json
import os

from collections.abc import AsyncGenerator
from enum import StrEnum
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import discord
import pytest

from pytest_mock import MockerFixture

from src.source_bot.scraping import DataType, Scraper

class TestScraper:
    _PROJECT_ROOT: Path = Path(__file__).parent.parent

    _OUTPUT_FILE: Path = _PROJECT_ROOT / "src" / "output" / "output.json"

    _NAME_GUILD: str = "Test"
    _SCRAPER_PATH: str = "src.source_bot.scraping.Scraper."
    
    @pytest.fixture
    def scraper(self) -> Scraper:
        return Scraper()
    
    def test_constructor_base_class(self, scraper: Scraper) -> None:
        assert type(scraper).__base__ == discord.Client
    
    def test_constructor_intents(self, scraper: Scraper) -> None:
        expected_intents = discord.Intents.default()
        expected_intents.members = True
        expected_intents.message_content = True

        assert scraper.intents == expected_intents

    @pytest.mark.asyncio
    @pytest.mark.parametrize("channel_names", [
        [], # No channels
        ["test"],
        ["test_one", "test_two", "test_three"]
    ])
    async def test_through_interface_scrape_channel_names_three(self, channel_names: list[str], mocker: MockerFixture, monkeypatch, scraper: Scraper) -> None:
        EXPECTED = {
            self._NAME_GUILD: {
                DataType.ChannelNames: channel_names
            }
        }

        self._set_up_guild_scrape_channel_names(channel_names, mocker, monkeypatch)

        await self._activate_scraper(mocker, scraper)

        assert self._read_and_wipe_output_file() == EXPECTED

    @pytest.mark.asyncio
    @pytest.mark.parametrize("number_of_members", [
        0, # No members
        1,
        3
    ])
    async def test_through_interface__scrape_number_of_members(self, mocker: MockerFixture, monkeypatch, number_of_members: int, scraper: Scraper) -> None:
        EXPECTED = {
            self._NAME_GUILD: {
                DataType.NumberOfMembers: number_of_members
            }
        }

        self._set_up_guild_scrape_number_of_members(mocker, monkeypatch, number_of_members)

        await self._activate_scraper(mocker, scraper)

        assert self._read_and_wipe_output_file() == EXPECTED

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("channel_names", "number_of_members"), [
        ([], 0), # Empty guild
        (["yapping", "crying", "star_gazing"], 2) # Guild with stuff
    ])
    async def test_through_interface_scrape_guild(self, channel_names: list[str], mocker: MockerFixture, monkeypatch, number_of_members: int, scraper: Scraper) -> None:
        EXPECTED = {
            self._NAME_GUILD: {
                DataType.ChannelNames: channel_names,
                DataType.NumberOfMembers: number_of_members
            }
        }

        self._set_up_guild_scrape_channel_names_and_number_of_members(channel_names, mocker, monkeypatch, number_of_members)

        await self._activate_scraper(mocker, scraper)

        assert self._read_and_wipe_output_file() == EXPECTED

    @pytest.mark.asyncio
    @pytest.mark.parametrize(("channel_names_list, guild_names, numbers_of_members"), [
        ([], [], []), # No guilds
        ([[], []], ["One", "Two"], [0, 0]), # Two empty guilds
        ([["blah_blah", "ducks"], ["chickens", "whales", "big_lizards"], ["lord_of_the_rings", "BAJA BLAST", "whats_a_pointer", "donde_queda_la_biblioteca"]], ["One", "Two", "Three"], [2, 4, 3]), # Three guilds with stuff
    ])
    async def test_through_interface_scrape_guilds_process_queue_write_to_output_and_activate(self, channel_names_list: list[str], guild_names: list[str], mocker: MockerFixture, monkeypatch, scraper: Scraper, numbers_of_members: list[int]) -> None:
        expected = {}

        for entry in [[guild_names[i], channel_names_list[i], numbers_of_members[i]] for i in range(len(guild_names))]:
            GUILD_NAME = 0
            CHANNEL_NAMES = 1
            NUMBER_OF_MEMBERS = 2
            
            expected[entry[GUILD_NAME]] = {
                DataType.ChannelNames: entry[CHANNEL_NAMES],
                DataType.NumberOfMembers: entry[NUMBER_OF_MEMBERS]
            }

        self._set_up_guilds_scrape_channel_names_and_numbers_of_members(channel_names_list, guild_names, mocker, monkeypatch, numbers_of_members)

        await self._activate_scraper(mocker, scraper)

        assert self._read_and_wipe_output_file() == expected

    async def _activate_scraper(self, mocker: MockerFixture, scraper: Scraper) -> None:
        mocker.patch("discord.Client.login")
        mocker.patch("discord.Client.connect")
        mocker.patch("discord.Client.wait_until_ready")
        mocker.patch("discord.Client.close")

        await scraper.login(os.getenv('DISCORD_TOKEN'))
        session = asyncio.create_task(scraper.connect())
        await scraper.wait_until_ready()

        await scraper.activate()

        await scraper.close()
        session.cancel()

    async def _async_generator_wrapper(self, content: list[MagicMock]) -> AsyncGenerator[MagicMock]:
        for item in content:
            yield item

    async def _coroutine_wrapper(self, content):
        return content
    
    def _create_channels(self, channel_names: list[str], mocker: MockerFixture) -> list[MagicMock]:
        channels = []

        for name in channel_names:
            channel = mocker.MagicMock()
            channel.name = name
            channels.append(channel)

        return channels
    
    def _create_members(self, number_of_members: int, mocker: MockerFixture) -> list[MagicMock]:
        return [mocker.MagicMock() for name in range(number_of_members)]

    def _isolate_subscrapers(self, mocker: MockerFixture, subscrapers: list[_SubScraper]) -> None:
        for enumeration in self._SubScraper:
            if enumeration not in subscrapers:
                mocker.patch(self._SCRAPER_PATH + enumeration)

    def _read_output_file(self) -> str:
        with self._OUTPUT_FILE.open(mode='r') as file:
            return json.load(file)

    def _read_and_wipe_output_file(self) -> str:
        with self._OUTPUT_FILE.open(mode='r+') as file:
            data = json.load(file)
            file.truncate(0)
        
        return data
    
    def _set_up_guild_scrape_channel_names(self, channel_names: list[str], mocker: MockerFixture, monkeypatch) -> None:
        mock_guild = mocker.MagicMock()
        mock_guild.name = self._NAME_GUILD
        mock_guild.fetch_channels.return_value = self._coroutine_wrapper(self._create_channels(channel_names, mocker))
        self._isolate_subscrapers(mocker, [self._SubScraper.ScrapeChannelNames])
        monkeypatch.setattr(Scraper, "guilds", [mock_guild])
    
    def _set_up_guild_scrape_channel_names_and_number_of_members(self, channel_names: list[str], mocker: MockerFixture, monkeypatch, number_of_members: int) -> None:
        mock_guild = mocker.MagicMock()
        mock_guild.name = self._NAME_GUILD
        mock_guild.fetch_channels.return_value = self._coroutine_wrapper(self._create_channels(channel_names, mocker))
        mock_guild.fetch_members.return_value = self._async_generator_wrapper(self._create_members(number_of_members, mocker))
        self._isolate_subscrapers(mocker, [self._SubScraper.ScrapeChannelNames, self._SubScraper.ScrapeNumberOfMembers])
        monkeypatch.setattr(Scraper, "guilds", [mock_guild])
    
    def _set_up_guild_scrape_number_of_members(self, mocker: MockerFixture, monkeypatch, number_of_members: int) -> None:
        mock_guild = mocker.MagicMock()
        mock_guild.name = self._NAME_GUILD
        mock_guild.fetch_members.return_value = self._async_generator_wrapper(self._create_members(number_of_members, mocker))
        self._isolate_subscrapers(mocker, [self._SubScraper.ScrapeNumberOfMembers])
        monkeypatch.setattr(Scraper, "guilds", [mock_guild])
    
    def _set_up_guilds_scrape_channel_names_and_numbers_of_members(self, channel_names_list: list[list[str]], guild_names: list[str], mocker: MockerFixture, monkeypatch, numbers_of_members: list[int]) -> None:
        mock_guilds = []

        for i in range(len(guild_names)):
            mock_guild = mocker.MagicMock()
            mock_guild.name = guild_names[i]
            mock_guild.fetch_channels.return_value = self._coroutine_wrapper(self._create_channels(channel_names_list[i], mocker))
            mock_guild.fetch_members.return_value = self._async_generator_wrapper(self._create_members(numbers_of_members[i], mocker))
            mock_guilds.append(mock_guild)

        self._isolate_subscrapers(mocker, [self._SubScraper.ScrapeChannelNames, self._SubScraper.ScrapeNumberOfMembers])
        monkeypatch.setattr(Scraper, "guilds", mock_guilds)
    
    class _SubScraper(StrEnum):
        ScrapeChannelNames = "_scrape_channel_names"
        ScrapeNumberOfMembers = "_scrape_number_of_members"