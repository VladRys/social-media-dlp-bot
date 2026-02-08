# Social Media DLP Bot

Telegram bot for downloading videos from YouTube, TikTok, Kick, and other platforms.

Supports sending videos directly in chat up to **2 GB** via  **Local Bot API** , or provides a download link through a built-in HTTP server.

---

## Features

* Download videos from popular platforms:
  * YouTube, TikTok, Instagram, Twitch, Kick
* Send videos in chat:
  * Standard Bot API (up to 50 MB)
  * Local Bot API (up to 2 GB)
* Serve large files via built-in HTTP server
* Extensible architecture with `DownloadService` + `FileSenderFactory`
* Logging of actions and errors
* Handles multiple senders and platforms seamlessly

---

## Installation (Poetry)

1. Clone the repository:

<pre class="overflow-visible! px-0!" data-start="822" data-end="922"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>git </span><span>clone</span><span> https://github.com/<username>/social-media-dlp-bot.git
</span><span>cd</span><span> social-media-dlp-bot
</span></span></code></div></div></pre>

2. Install dependencies:

<pre class="overflow-visible! px-0!" data-start="950" data-end="989"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>poetry install
poetry shell
</span></span></code></div></div></pre>

3. Configure environment variables in `.env` or `config.py`:

<pre class="overflow-visible! px-0!" data-start="1053" data-end="1557"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-python"><span><span>BOT_TOKEN = </span><span>"YOUR_BOT_TOKEN"</span><span>
USE_LOCAL_API = </span><span>True</span><span></span><span># Enable Local Bot API</span><span>
LOCAL_BOT_API_URL = </span><span>"http://127.0.0.1:8080"</span><span>
EXTERNAL_BASE_URL = </span><span>"https://example.com"</span><span></span><span># External link fallback</span><span>
DOWNLOADS_FOLDER = </span><span>"downloads"</span><span>
FILE_SERVER_PORT = </span><span>8088</span><span>

SUPPORTED_LINKS = {
    </span><span>"youtube"</span><span>: [</span><span>r"https?://(www\.)?youtube\.com/watch.*"</span><span>, </span><span>r"https?://youtu\.be/.*"</span><span>],
    </span><span>"tiktok"</span><span>: [</span><span>r"https?://(www\.)?tiktok\.com/.*"</span><span>],
    </span><span>"kick"</span><span>: [</span><span>r"https?://(www\.)?kick\.com/.*"</span><span>]
}

ALLOWED_CAPTION = </span><span>"Authorized"</span><span>
</span></span></code></div></div></pre>

---

## Running Locally

<pre class="overflow-visible! px-0!" data-start="1587" data-end="1649"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>poetry run python -m src.social_media_dlp_bot.main
</span></span></code></div></div></pre>

* Bot and HTTP server will start
* Downloaded videos will be saved in the `downloads/` folder

---

## Docker / Deployment

The bot and its HTTP file server can be easily deployed using Docker Compose.
A ready-to-use docker-compose.botapi.yml file is included in the repository.

Run with Docker Compose
`docker-compose -f docker-compose.botapi.yml up -d`


The bot will start along with the HTTP server.

Port `8088` (or configured in `.env`) will expose the file server for large video downloads.

Environment variables for bot token, local API, and download folder should be configured in the compose file or `.env`.

You do not need to build the Docker image manually — Compose handles it automatically.

---

## Usage

1. Send `/start` to the bot
2. Send a video link (YouTube/TikTok/Kick)
3. Bot behavior:
   * **Local Bot API enabled** → sends video directly (up to 2 GB)
   * **Local Bot API disabled** → returns a download link via HTTP server
4. Large files (>50 MB) are served through `http://<host>:<port>/files/<filename>`

---

## Project Structure

<pre class="overflow-visible! px-0!" data-start="2552" data-end="2972"><div class="contain-inline-size rounded-2xl corner-superellipse/1.1 relative bg-token-sidebar-surface-primary"><div class="sticky top-[calc(var(--sticky-padding-top)+9*var(--spacing))]"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>src/social_media_dlp_bot/
├─ bot.py               </span><span># Bot logic (aiogram)</span><span>
├─ downloader.py        </span><span># DownloadService & platform downloaders</span><span>
├─ main.py              </span><span># Entry point</span><span>
├─ config.py            </span><span># Settings</span><span>
├─ exceptions.py        </span><span># Custom exceptions</span><span>
├─ services/
│  ├─ file_senders.py   </span><span># File sending logic</span><span>
│  ├─ file_http_server.py </span><span># Local HTTP server for large files</span><span>
└─ downloads/           </span><span># Saved videos</span><span>
</span></span></code></div></div></pre>

---

## Architecture

* **DownloadService**

  Abstracts platform downloads and returns `DownloadResult` with `filepath`, `title`, and `filesize`
* **FileSenderFactory**

  Selects the appropriate sender: Local Bot API / standard Bot API / HTTP server
* **FileHttpServer**

  Serves files via `/files/<filename>` in parallel with the bot
* **TelegramBot (aiogram 3.x)**

  Handles `/start` and video links, delegates downloading and sending

---

```

```

Notes

* Supports sending videos up to **2 GB** with Local Bot API
* Large videos fallback to HTTP server if Local API is disabled
* Logging available in `logs.log`
