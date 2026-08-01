import asyncio
import os

from dotenv import load_dotenv

from src.source_bot.scraping import ScraperBot

async def main() -> None:
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')

    await ScraperBot(1514322664473366559).start(token)

if __name__ == "__main__":
    asyncio.run(main())
