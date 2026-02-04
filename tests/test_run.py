"""
Tests for all video platform downloading
"""
import logging
from src.social_media_dlp_bot.downloader import YdlpDownloader



def test_download_all_platform_test():
    urls = ["https://www.youtube.com/watch?v=vKEK6VpPNV8",
        "https://www.tiktok.com/@sa_vivi_1/video/7595882556583808279"]

    logging.basicConfig(
        level=logging.INFO,
        filename="logs.log",
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    logger = logging.getLogger(__name__)

    ydl = YdlpDownloader(logger)

    for url in urls:
        ydl.download_video(url)
