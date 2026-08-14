import asyncio
import json
import os

from collections.abc import AsyncGenerator
from enum import StrEnum
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import discord
import pytest

from dotenv import load_dotenv
from pytest_mock import MockerFixture

from src.source_bot.scraping import DataType, Scraper

class TestScraper:
    _PROJECT_ROOT: Path = Path(__file__).parent.parent

    _OUTPUT_FILE: Path = _PROJECT_ROOT / "src" / "output" / "output.json"

    _NAME_TEST: str = "Test"
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
    async def test_through_interface_scrape_channel_names_none(self, mocker: MockerFixture, monkeypatch, scraper: Scraper) -> None:
        test_name = "test"

        EXPECTED = {
            self._NAME_TEST: {
                DataType.ChannelNames: [test_name]
            }
        }

        mock_channel = mocker.MagicMock()
        mock_channel.name = test_name
        mock_guild = self._set_up_guild_test(mocker.AsyncMock(), monkeypatch)
        mock_guild.fetch_channels.return_value = [mock_channel]
        self._isolate_subscraper(mocker, self._SubScraper.ScrapeChannelNames)

        await self._activate_scraper(mocker, scraper)

        assert self._read_and_wipe_output_file() == EXPECTED

    @pytest.mark.asyncio
    async def test_through_interface_scrape_channel_names_one(self, mocker: MockerFixture, monkeypatch, scraper: Scraper) -> None:
        EXPECTED = {
            self._NAME_TEST: {
                DataType.ChannelNames: []
            }
        }

        mock_guild = self._set_up_guild_test(mocker.AsyncMock(), monkeypatch)
        mock_guild.fetch_channels.return_value = []
        self._isolate_subscraper(mocker, self._SubScraper.ScrapeChannelNames)

        await self._activate_scraper(mocker, scraper)

        assert self._read_and_wipe_output_file() == EXPECTED

    @pytest.mark.asyncio
    async def test_through_interface_scrape_channel_names_three(self, mocker: MockerFixture, monkeypatch, scraper: Scraper) -> None:
        test_names = ["test_zero", "test_one", "test_two"]

        EXPECTED = {
            self._NAME_TEST: {
                DataType.ChannelNames: test_names
            }
        }

        mock_channels = [mocker.MagicMock() for name in test_names]
        for i in range(len(test_names)):
            mock_channels[i].name = test_names[i]
        mock_guild = self._set_up_guild_test(mocker.AsyncMock(), monkeypatch)
        mock_guild.fetch_channels.return_value = mock_channels
        self._isolate_subscraper(mocker, self._SubScraper.ScrapeChannelNames)

        await self._activate_scraper(mocker, scraper)

        assert self._read_and_wipe_output_file() == EXPECTED

    @pytest.mark.asyncio
    async def test_through_interface_scrape_number_of_members_none(self, mocker: MockerFixture, monkeypatch, scraper: Scraper) -> None:
        EXPECTED = {
            self._NAME_TEST: {
                DataType.NumberOfMembers: 0
            }
        }

        mock_guild = self._set_up_guild_test(mocker.MagicMock(), monkeypatch)
        mock_guild.fetch_members.return_value = self._async_generator([])
        self._isolate_subscraper(mocker, self._SubScraper.ScrapeNumberOfMembers)

        await self._activate_scraper(mocker, scraper)

        assert self._read_and_wipe_output_file() == EXPECTED


    @pytest.mark.asyncio
    async def test_through_interface__scrape_number_of_members_one(self, mocker: MockerFixture, monkeypatch, scraper: Scraper) -> None:
        EXPECTED = {
            self._NAME_TEST: {
                DataType.NumberOfMembers: 1
            }
        }

        mock_guild = self._set_up_guild_test(mocker.MagicMock(), monkeypatch)
        mock_member = mocker.MagicMock()
        mock_guild.fetch_members.return_value = self._async_generator([mock_member])
        self._isolate_subscraper(mocker, self._SubScraper.ScrapeNumberOfMembers)

        await self._activate_scraper(mocker, scraper)

        assert self._read_and_wipe_output_file() == EXPECTED

    @pytest.mark.asyncio
    async def test_through_interface_scrape_number_of_members_three(self, mocker: MockerFixture, monkeypatch, scraper: Scraper) -> None:
        EXPECTED = {
            self._NAME_TEST: {
                DataType.NumberOfMembers: 3
            }
        }

        mock_guild = self._set_up_guild_test(mocker.MagicMock(), monkeypatch)
        mock_members = [mocker.MagicMock() for i in range(3)]
        mock_guild.fetch_members.return_value = self._async_generator(mock_members)
        self._isolate_subscraper(mocker, self._SubScraper.ScrapeNumberOfMembers)

        await self._activate_scraper(mocker, scraper)

        assert self._read_and_wipe_output_file() == EXPECTED

    @pytest.mark.asyncio 
    async def test_through_interface_scrape_guild_empty(self, mocker: MockerFixture, scraper: Scraper) -> None:
        ... # !!!

    @pytest.mark.asyncio
    async def test_through_interface_scrape_guild_something(self, mocker: MockerFixture, scraper: Scraper) -> None:
        ... # !!!

    @pytest.mark.asyncio
    async def test_through_interface_scrape_guilds_none(self, mocker: MockerFixture, scraper: Scraper) -> None:
        ... # !!!
    
    @pytest.mark.asyncio
    async def test_through_interface_scrape_guilds_one(self, mocker: MockerFixture, scraper: Scraper) -> None:
        ... # !!!

    @pytest.mark.asyncio  
    async def test_through_interface_scrape_guilds_three(self, mocker: MockerFixture, scraper: Scraper) -> None:
        ... # !!!

    @pytest.mark.asyncio
    async def test_through_interface_process_queue_no_items(self, mocker: MockerFixture, scraper: Scraper) -> None:
        ... # !!!

    @pytest.mark.asyncio
    async def test_through_interface_process_queue_items_are_empty(self, mocker: MockerFixture, scraper: Scraper) -> None:
        ... # !!!

    @pytest.mark.asyncio
    async def test_through_interface_process_queue_something(self, mocker: MockerFixture, scraper: Scraper) -> None:
        ... # !!!

    def test_through_interface_write_to_output_file_none(self, mocker: MockerFixture, scraper: Scraper) -> None:
        ... # !!!

    def test_through_interface_write_to_output_file_something(self, mocker: MockerFixture, scraper: Scraper) -> None:
        ... # !!!

    @pytest.mark.asyncio
    async def test_activate(self, mocker: MockerFixture) -> None:
        ... # !!!

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

    async def _async_generator(self, content: list[MagicMock]) -> AsyncGenerator[MagicMock]:
        for item in content:
            yield item
    
    def _isolate_subscraper(self, mocker: MockerFixture, subscraper: _SubScraper) -> None:
        for enumeration in self._SubScraper:
            if enumeration != subscraper:
                mocker.patch(self._SCRAPER_PATH + enumeration)

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

    def _set_up_guild_test(self, mock_guild, monkeypatch) -> AsyncMock:
        mock_guild.name = self._NAME_TEST
        monkeypatch.setattr(Scraper, "guilds", [mock_guild])

        return mock_guild
    
    class _SubScraper(StrEnum):
        ScrapeChannelNames = "_scrape_channel_names"
        ScrapeNumberOfMembers = "_scrape_number_of_members"