from yt_dlp import YoutubeDL
from dataclasses import dataclass
from pathlib import Path
from config import cfg


# ---------- Result ----------

@dataclass(slots=True)
class DownloadResult:
    path: Path
    title: str
    size: int


# ---------- Base ----------

class Downloader:
    def download_video(self, url: str, quality: str) -> DownloadResult:
        raise NotImplementedError


# ---------- yt-dlp based ----------

class YdlpDownloader(Downloader):
    def __init__(self, logger):
        self.logger = logger

    def _build_opts(self, quality: str) -> dict:
        """
        quality: '480' | '720' | '1080'
        """
        return {
            **cfg.YDLP_ydlp_opts,
            "format": f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]",
            "merge_output_format": "mp4",
        }

    def download_video(self, url: str, quality: str) -> DownloadResult:
        try:
            self.logger.info(
                f"[YTDLP] Download start | url={url} | quality={quality}p"
            )

            opts = self._build_opts(quality)

            with YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                path = Path(ydl.prepare_filename(info))

            result = DownloadResult(
                path=path,
                title=info.get("title", path.stem),
                size=path.stat().st_size,
            )

            self.logger.info(
                f"[YTDLP] Download finished | {path.name} | {result.size / 1024 / 1024:.1f} MB"
            )

            return result

        except Exception as e:
            self.logger.exception("[YTDLP] Download error")
            raise


# ---------- Kick ----------

class KickDownloader(Downloader):
    def __init__(self, logger):
        self.logger = logger

    def download_video(self, url: str, quality: str) -> DownloadResult:
        """
        Kick ignores quality selection (platform limitation)
        """
        try:
            self.logger.info(f"[KICK] Download start | url={url}")

            with YoutubeDL(cfg.KICK_ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                path = Path(ydl.prepare_filename(info))

            return DownloadResult(
                path=path,
                title=info.get("title", path.stem),
                size=path.stat().st_size,
            )

        except Exception:
            self.logger.exception("[KICK] Download error")
            raise


# ---------- Service ----------

class DownloadService:
    def __init__(self, logger) -> None:
        self.logger = logger
        self._downloaders = {
            "youtube": YdlpDownloader,
            "instagram": YdlpDownloader,
            "tiktok": YdlpDownloader,
            "twitch": YdlpDownloader,
            "kick": KickDownloader,
        }

    def download_with_service(
        self,
        platform: str,
        link: str,
        quality: str,
    ) -> DownloadResult:
        downloader_cls = self._downloaders[platform]
        downloader = downloader_cls(logger=self.logger)
        return downloader.download_video(link, quality)
