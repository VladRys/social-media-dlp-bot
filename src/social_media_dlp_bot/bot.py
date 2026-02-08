import re
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.filters import CommandStart

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

        # user_id -> {"link": str, "platform": str}
        self._user_requests: dict[int, dict] = {}

        self._register_handlers()
        self.logger.info("Bot status: Online! Handlers registered")

    # ---------- Handlers registration ----------

    def _register_handlers(self):
        self.dp.message.register(self.start, CommandStart())
        self.dp.message.register(self.link_handler, F.text)
        self.dp.callback_query.register(
            self.quality_handler, F.data.startswith("q:")
        )

    # ---------- UI ----------

    @staticmethod
    def _quality_keyboard() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="480p", callback_data="q:480"),
                    InlineKeyboardButton(text="720p", callback_data="q:720"),
                    InlineKeyboardButton(text="1080p", callback_data="q:1080"),
                ]
            ]
        )

    # ---------- Logic ----------

    async def start(self, message: Message):
        await message.answer("Привет! Отправь ссылку на видео.")

    async def _detect_platform(self, link: str) -> str:
        for platform, patterns in cfg.SUPPORTED_LINKS.items():
            for pattern in patterns:
                if re.match(pattern, link):
                    return platform
        raise WrongFormatException

    async def link_handler(self, message: Message):
        link = message.text.strip()
        user_id = message.from_user.id
        user = message.from_user.username or user_id

        try:
            platform = await self._detect_platform(link)
        except WrongFormatException:
            await message.answer(cfg.UNSUPPORTED_PLATFORM_MESSAGE)
            return

        self._user_requests[user_id] = {
            "link": link,
            "platform": platform,
        }

        self.logger.info(
            f"User {user} sent link: {link}, waiting for quality selection"
        )

        await message.answer(
            "Выбери качество видео:",
            reply_markup=self._quality_keyboard(),
        )

    async def quality_handler(self, callback: CallbackQuery):
        user_id = callback.from_user.id
        user = callback.from_user.username or user_id

        data = self._user_requests.get(user_id)
        if not data:
            await callback.answer("Время запроса вышло", show_alert=True)
            return

        quality = callback.data.split(":")[1]
        link = data["link"]
        platform = data["platform"]

        await self.bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=f"Скачиваю видео в {quality}p..."
        )

        self.logger.info(
            f"User {user} | platform={platform} | quality={quality}"
        )

        try:
            result = self.service.download_with_service(
                platform=platform,
                link=link,
                quality=quality,
            )

            video_path = result.path

            sender = self.sender.get_sender(video_path)
            self.logger.info(
                f"Selected sender: {sender.__class__.__name__}"
            )

            await sender.send(callback.message, video_path)

            os.remove(video_path)
            self.logger.info(f"Video sent and removed: {video_path}")

        except Exception:
            self.logger.exception(
                f"Error while handling request from user: {user}"
            )
            await callback.message.answer(cfg.ERROR_MESSAGE)

        finally:
            self._user_requests.pop(user_id, None)

    # ---------- Run ----------

    async def polling(self):
        await self.dp.start_polling(self.bot)
