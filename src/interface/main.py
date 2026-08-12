import asyncio
import os

from dotenv import load_dotenv

from source_bot.scraping import ScraperBot

async def main() -> None:
    GUILD_ID = 1514322664473366559

    load_dotenv()
    bot = ScraperBot(GUILD_ID)
    session = asyncio.create_task(bot.start(os.getenv('DISCORD_TOKEN')))

    await bot.activate()

    await bot.close()
    session.cancel()

if __name__ == "__main__":
    asyncio.run(main())
