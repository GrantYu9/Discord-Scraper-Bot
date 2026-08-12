import asyncio
import os

from dotenv import load_dotenv

from src.source_bot.scraping import Scraper

async def main() -> None:
    """!!!
    """

    load_dotenv()

    bot = Scraper()

    await bot.login(os.getenv('DISCORD_TOKEN'))
    session = asyncio.create_task(bot.connect())
    await bot.wait_until_ready()

    await bot.activate()

    await bot.close()
    session.cancel()

if __name__ == "__main__":
    asyncio.run(main())
