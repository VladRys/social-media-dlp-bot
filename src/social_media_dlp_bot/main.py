import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer
from aiogram.enums import ParseMode

from bot import TelegramBot
from downloader import DownloadService
from services.file_senders import FileSenderFactory
from services.file_http_server import FileHttpServer
from config import cfg

logging.basicConfig(
    level=logging.INFO,
    filename="logs.log",
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    # --- downloader ---
    service = DownloadService(logger)

    # --- HTTP file server ---
    file_server = FileHttpServer(
        files_dir=Path(cfg.DOWNLOADS_FOLDER),
        port=cfg.FILE_SERVER_PORT,
        logger=logger,
    )
    await file_server.start()

    # --- aiogram Bot (Local Bot API) ---
    session = None
    if cfg.USE_LOCAL_API:
        api = TelegramAPIServer.from_base(cfg.LOCAL_BOT_API_URL.rstrip("/"))
        session = AiohttpSession(api=api)

    bot = Bot(
        token=cfg.BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()

    # --- sender factory ---
    sender_factory = FileSenderFactory(
        bot=bot,
        use_local_api=cfg.USE_LOCAL_API,
        base_url=cfg.EXTERNAL_BASE_URL,
    )

    tg_bot = TelegramBot(
        logger=logger,
        bot=bot,
        dispatcher=dp,
        service=service,
        sender=sender_factory,
    )

    try:
        await tg_bot.polling()
    finally:
        await bot.session.close()
        await file_server.stop()


if __name__ == "__main__":
    asyncio.run(main())
