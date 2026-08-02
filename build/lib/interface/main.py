import asyncio
import os

from dotenv import load_dotenv

from src.source_bot.scraping import ScraperBot

async def main() -> None:
    load_dotenv()
    guild_id = 1514322664473366559

    await ScraperBot(guild_id).start(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    asyncio.run(main())
