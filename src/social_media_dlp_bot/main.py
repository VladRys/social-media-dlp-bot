import logging
import asyncio
from bot import TelegramBot
from downloader import DownloadService

logging.basicConfig(
    level=logging.INFO,
    filename="logs.log",
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)
service = DownloadService(logger)

if __name__ == "__main__":
    bot = TelegramBot(logger, service)
    asyncio.run(bot.polling())
