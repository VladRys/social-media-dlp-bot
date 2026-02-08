import re
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
import os
from config import cfg
from downloader import DownloadService
from exceptions import WrongFormatException
from services.file_senders import FileSenderFactory


class TelegramBot:
    def __init__(
        self,
        logger,
        bot: Bot,
        dispatcher: Dispatcher,
        service: DownloadService,
        sender: FileSenderFactory,
    ) -> None:
        self.logger = logger
        self.bot = bot
        self.dp = dispatcher
        self.service = service
        self.sender = sender

        self._register_handlers()
        self.logger.info("Bot status: Online! Handlers: registered!")

    def _register_handlers(self):
        self.dp.message.register(self.start, CommandStart())
        self.dp.message.register(self.link_handler, F.text)

    async def start(self, message: Message):
        await message.answer("Привет! Отправь ссылку на видео.")

    async def _detect_platform(self, link: str) -> str:
        """Проверка платформы по ссылке"""
        for platform, patterns in cfg.SUPPORTED_LINKS.items():
            for pattern in patterns:
                if re.match(pattern, link):
                    return platform
        raise WrongFormatException

    async def link_handler(self, message: Message):
        link = message.text
        user = message.from_user.username or message.from_user.id

        try:
            platform = await self._detect_platform(link)
        except WrongFormatException:
            await message.answer(cfg.UNSUPPORTED_PLATFORM_MESSAGE)
            return

        self.logger.info(f"Started handling request from user: {user} link: {link}")
        status = await message.answer("Обрабатываю запрос...")

        try:
            # download_with_service теперь возвращает объект DownloadResult
            result = self.service.download_with_service(platform, link)
            video_path = result.path  # Path к файлу

            sender = self.sender.get_sender(video_path)
            self.logger.info(f"Selected sender: {sender.__class__.__name__}")

            # Отправка файла
            await sender.send(message, video_path)
            os.remove(video_path)
            self.logger.info(f"Видео пользователя: {user} успешно отправлено.")

        except Exception as e:
            self.logger.exception(
                f"Error while handling request from user: {user} link: {link}"
            )
            await message.answer(cfg.ERROR_MESSAGE)

        finally:
            await status.delete()


    async def polling(self):
        """Запуск long-polling"""
        await self.dp.start_polling(self.bot)
