from aiohttp import web
from pathlib import Path
import logging

class FileHttpServer:
    def __init__(
        self,
        files_dir: Path,
        host: str = "0.0.0.0",
        port: int = 8080,
        logger: logging.Logger | None = None,
    ):
        self.files_dir = files_dir
        self.host = host
        self.port = port
        self.logger = logger or logging.getLogger(__name__)

        self._app = web.Application()
        self._runner: web.AppRunner | None = None
        self._site: web.TCPSite | None = None

        self._setup_routes()

    # ---------- routes ----------
    def _setup_routes(self):
        self._app.add_routes([
            web.get("/files/{name}", self._file_handler)
        ])

    async def _file_handler(self, request: web.Request):
        name = request.match_info["name"]
        path = self.files_dir / name

        if not path.exists():
            return web.Response(status=404, text="Not found")

        return web.FileResponse(path)

    # ---------- lifecycle ----------
    async def start(self):
        self._runner = web.AppRunner(self._app)
        await self._runner.setup()

        self._site = web.TCPSite(self._runner, self.host, self.port)
        await self._site.start()

        self.logger.info(
            f"File server started: http://{self.host}:{self.port}/files/<name>"
        )

    async def stop(self):
        if self._runner:
            await self._runner.cleanup()
            self.logger.info("File server stopped")
