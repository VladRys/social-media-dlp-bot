from yt_dlp import YoutubeDL
from config import cfg

class Downloader:
    def download_video(self, url: str):
        raise NotImplementedError

class YdlpDownloader(Downloader):
    def __init__(self, logger):
        self.ydl_opts = cfg.YDLP_ydlp_opts
        self.logger = logger

    def download_video(self, url: str):
        try:
            self.logger.info(f"[YT] Starting download video: {url}")
            with YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                self.logger.info(f"[YT] Video: {url} was successfully downloaded")
                return ydl.prepare_filename(info)
        
        except Exception as e:
            self.logger.error(f"[YT] Error occurred while downloading video: {e}")
            return

class KickDownloader(Downloader):
    def __init__(self, logger):
        self.ydl_opts = cfg.KICK_ydl_opts
        self.logger = logger

    def download_video(self, url: str):
        try:
            self.logger.info(f"[KICK] Starting download video: {url}")
            with YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                self.logger.info(f"[KICK] Video: {url} was successfully downloaded")
                return ydl.prepare_filename(info)
        
        except Exception as e:
            self.logger.error(f"[KICK] Error occurred while downloading video: {e}")
            return

class DownloadService:
    def __init__(self, logger) -> None:
        self.dls = {
            "youtube": YdlpDownloader,
            "instagram": YdlpDownloader,
            "tiktok": YdlpDownloader,
            "twitch": YdlpDownloader,
            "kick": KickDownloader
        }
        self.logger = logger

    def download_with_service(self, platform: str, url: str):
        return self.dls[platform](logger=self.logger).download_video(url)