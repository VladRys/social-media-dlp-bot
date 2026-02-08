from yt_dlp import YoutubeDL
from config import cfg

from dataclasses import dataclass
from pathlib import Path

from dataclasses import dataclass
from pathlib import Path

@dataclass(slots=True)
class DownloadResult:
    path: Path
    title: str
    size: int 

class Downloader:
    def download_video(self, url: str) -> DownloadResult:
        return DownloadResult

class YdlpDownloader(Downloader):
    def __init__(self, logger):
        self.ydl_opts = cfg.YDLP_ydlp_opts
        self.logger = logger

    def download_video(self, url: str)  -> DownloadResult | None:
        try:
            self.logger.info(f"[YT] Starting download video: {url}")
            with YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                path = Path(ydl.prepare_filename(info))
                self.logger.info(f"[YT] Video: {url} was successfully downloaded")
                return DownloadResult(
                    path=path,
                    title=info.get("title", path.name),
                    size=path.stat().st_size
                )
        
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