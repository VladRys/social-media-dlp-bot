import os
from telebot import types
from telebot.async_telebot import AsyncTeleBot
from config import cfg
from downloader import DownloadService
import re
from exceptions import WrongFormatException

class TelegramBot:
    def __init__(self, logger, service: DownloadService) -> None:
        self.logger = logger
        self.bot = AsyncTeleBot(cfg.BOT_TOKEN)
        self.service = service

        self._register_handlers()
        self.logger.info("Bot status: Online! Handlers: registered!")

    def _register_handlers(self):
        @self.bot.message_handler(commands=["start"])
        async def start(message: types.Message) -> types.Message:
            return await self.bot.send_message(message.chat.id, "Привет!")
        

        async def filter_support_link(link: str) -> str | None:
            for platform, patterns in cfg.SUPPORTED_LINKS.items():
                for pattern in patterns:
                    if re.match(pattern, link):
                        return platform
                    
            raise WrongFormatException

        @self.bot.message_handler(func=lambda message: True)
        async def link_handler(message) -> None:
            user = message.from_user.username or message.from_user.id # Data for logs
            link = str(message.text)
            platform = await filter_support_link(link)
            if platform:
                self.logger.info(f"Started handling request from user: {user} link: {link}")
                loading_status_message = await self.bot.send_message(message.chat.id, "Обрабатываю запрос....")
                try:
                    video = self.service.download_with_service(platform, link)

                    with open(video, "rb") as f:
                        await self.bot.send_video(message.chat.id, video=f)
                        self.logger.info(f"[TELEGRAM] Video: {f.name} was successfuly sended to user {user}!")
                        os.remove(video)
                        return
                    
                except WrongFormatException:
                    await self.bot.send_message(message.chat.id, cfg.UNSUPPORTED_PLATFORM_MESSAGE)

                except Exception as e:
                    self.logger.error(f"Error while handling request from user: {user} link: {link}: {e}")
                    await self.bot.send_message(message.chat.id, cfg.ERROR_MESSAGE)

                finally:
                    await self.bot.delete_message(message.chat.id, loading_status_message.message_id)
        
    async def polling(self):
        await self.bot.polling(non_stop=True)    

