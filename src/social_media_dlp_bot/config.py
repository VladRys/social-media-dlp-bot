import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
    TG_API_ID = os.getenv("TG_API_ID")
    TG_API_HASH = os.getenv("TG_API_HASH")
    USE_LOCAL_API: bool = True
    FILE_SERVER_PORT: str| None = os.getenv("FILE_SERVER_PORT")
    LOCAL_BOT_API_URL = os.getenv("LOCAL_BOT_API_URL")
    EXTERNAL_BASE_URL: str | None = os.getenv("EXTERNAL_BASE_URL")  
    DOWNLOADS_FOLDER = "downloads"
    YDLP_OPTH_OUT_PATH = f"src/social_media_dlp_bot/{DOWNLOADS_FOLDER}/%(title)s.%(ext)s"
    YDLP_ydlp_opts = {
            "format": "bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4][abr<=128]",
            "merge_output_format": "mp4",
            "outtmpl": YDLP_OPTH_OUT_PATH,
            "quiet": False,
            "verbose": True,
            "http_headers": {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            },
            "postprocessors": [{
                "key": "FFmpegVideoRemuxer",
                "preferedformat": "mp4"
            }],
            "progress_hooks": [
                lambda d: print(d)  
            ]
        }
    
    KICK_ydl_opts = {
    "format": "best",
    "outtmpl": YDLP_OPTH_OUT_PATH,
    "merge_output_format": "mp4",
    "http_headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
        "Accept": "*/*",
        "Referer": "https://kick.com/",
    },
}
    
    SUPPORTED_LINKS = {
    "youtube": [
        # Обычные видео
        r"https?://(www\.)?youtube\.com/watch\?v=[\w-]+",
        r"https?://youtu\.be/[\w-]+",
        # Shorts
        r"https?://(www\.)?youtube\.com/shorts/[\w-]+",
        # Плейлисты
        r"https?://(www\.)?youtube\.com/playlist\?list=[\w-]+",
        # Каналы / по username
        r"https?://(www\.)?youtube\.com/@[\w-]+",
    ],
    "instagram": [
        # Посты
        r"https?://(www\.)?instagram\.com/p/[\w-]+/?",
        # Reels
        r"https?://(www\.)?instagram\.com/reel/[\w-]+/?",
        # Stories
        r"https?://(www\.)?instagram\.com/stories/[\w-]+/[\d]+/?",
        # Профиль пользователя
        r"https?://(www\.)?instagram\.com/[\w-]+/?",
        # IGTV
        r"https?://(www\.)?instagram\.com/tv/[\w-]+/?",
    ],
    "tiktok": [
        # Отдельные видео
        r"https?://(www\.)?tiktok\.com/@[\w.-]+/video/[\d]+",
        # Профили
        r"https?://(www\.)?tiktok\.com/@[\w.-]+/?",
        # Тренды / хэштеги (для скачивания видео с этих страниц)
        r"https?://(www\.)?tiktok\.com/tag/[\w-]+/?",
        r"https?://(www\.)?tiktok\.com/music/[\w-]+/?",
    ],
    "twitch": [
        # Клипы
        r"https?://(www\.)?twitch\.tv/[\w-]+/clip/[\w-]+",
        # VOD
        r"https?://(www\.)?twitch\.tv/videos/[\d]+",
        # Каналы
        r"https?://(www\.)?twitch\.tv/[\w-]+/?",
    ],
    "kick": [
        # Видео
        r"https?://(www\.)?kick\.com/[\w-]+/video/[\d]+",
        # Каналы
        r"https?://(www\.)?kick\.com/[\w-]+/?",
    ],
}
    UNSUPPORTED_PLATFORM_MESSAGE = "Неверная ссылка или неизвестный формат."
    ERROR_MESSAGE = "При обработке вашего запроса произошла ошибка. Проверьте ссылку либо попробуйте использовать другой формат."
    
cfg = Config()