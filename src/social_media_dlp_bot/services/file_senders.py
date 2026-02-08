import os
from abc import ABC, abstractmethod
from telebot.types import Message
from aiogram.types import FSInputFile
from pathlib import Path

class BaseFileSender(ABC):
    @abstractmethod
    async def send(self, message: Message, file_path):
        raise NotImplemented
    
class TelegramBotAPISender(BaseFileSender):
    MAX_SIZE = 50 * 1024 * 1024

    def __init__(self, bot):
        self.bot = bot

    async def send(self, message, file_path):
        video_file = FSInputFile(file_path) 
        await self.bot.send_video(
            chat_id=message.chat.id,
            video=video_file,
            caption=file_path.name
        )

class LocalBotAPISender(BaseFileSender):
    def __init__(self, bot):
        self.bot = bot

    async def send(self, message, file_path):
        video_file = FSInputFile(file_path)
        await self.bot.send_video(
            chat_id=message.chat.id,
            video=video_file,
            caption=file_path.name
        )

class HttpLinkSender(BaseFileSender):
    def __init__(self, base_url: str, bot):
        self.base_url = base_url
        self.bot = bot

    async def send(self, message, file_path: Path):
        link = f"{self.base_url}/files/{file_path.name}"
        await self.bot.send_message(
            message.chat.id,
            f"Файл большой.\nСкачать: {link}\n{file_path.name}"
        )

class FileSenderFactory:
    def __init__(self, bot, use_local_api: bool, base_url: str | None):
        self.bot = bot
        self.use_local_api = use_local_api
        self.base_url = base_url

    def get_sender(self, file) -> BaseFileSender:
        if self.use_local_api:
            return LocalBotAPISender(self.bot)

        if file.size <= 50 * 1024 * 1024:
            return TelegramBotAPISender(self.bot)

        if self.base_url:
            return HttpLinkSender(self.base_url, self.bot)

        raise RuntimeError("File too large and no delivery method available")