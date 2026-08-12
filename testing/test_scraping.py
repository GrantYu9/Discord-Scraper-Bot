import asyncio

from unittest.mock import AsyncMock, MagicMock

import pytest

from pytest_mock import MockerFixture

from src.source_bot.scraping import ScraperBot

class TestScraping:
    @pytest.fixture
    def scraper_bot() -> ScraperBot:
        DUMMY_NUMBER = 0

        return ScraperBot(DUMMY_NUMBER)

    # !!!
    
    class Spy:
        ... # !!!
