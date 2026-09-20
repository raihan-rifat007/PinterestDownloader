<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=E60023&height=200&section=header&text=Pinterest%20Scraper&fontSize=52&fontColor=ffffff&fontAlignY=38&desc=Production-grade%20scraping%20%C2%B7%20Premium%20web%20UI%20%C2%B7%20Full%20metadata&descAlignY=58&descFontSize=16&descFontColor=ffffff" width="100%">

<br>

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Render](https://img.shields.io/badge/Deploy-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com)
[![License](https://img.shields.io/badge/License-MIT-E60023?style=for-the-badge)](LICENSE)

<br>

**A production-ready Pinterest scraper with a premium black & white web UI.**  
Search, board-scrape, download, deduplicate, export — all from a single interface.

<br>

[Features](#-features) · [Screenshots](#-screenshots) · [Quick Start](#-quick-start) · [API Reference](#-api-reference) · [Deployment](#-deployment) · [Config](#-configuration)

</div>

---

## Features

<table>
<tr>
<td width="50%">

**Core**
- Search pins by keyword or batch query
- Board scraping via URL
- Full metadata extraction (saves, comments, creator, board, colors, dimensions)
- High-res image upgrade (`/originals/` path injection)
- Video pin detection + direct MP4 URL extraction
- Concurrent downloading with configurable workers

</td>
<td width="50%">

**Web UI**
- Premium masonry grid with lazy-load reveal
- Live progress via Server-Sent Events (SSE)
- Video playback inline in pin modal
- Typeahead search suggestions with user results
- Dark / light mode with system preference detection
- Gallery view for all downloaded images
- Long-press selection mode for batch delete

</td>
</tr>
<tr>
<td>

**Export**
- ZIP archive of all downloaded images
- XLSX spreadsheet with full metadata columns
- JSON + CSV saved automatically per run

</td>
<td>

**Advanced**
- Deduplication across runs (hash + URL)
- Scheduled scrapes (cron-style, configurable hours)
- Visual / related pin search
- Engagement insights chart (top pins by saves)
- Proxy pool support
- Infinite scroll pagination

</td>
</tr>
</table>

---

## Screenshots

> _Add screenshots of your deployed instance here._

| Search View | Pin Modal | Gallery |
|:-----------:|:---------:|:-------:|
| `docs/search.png` | `docs/modal.png` | `docs/gallery.png` |

---

## Project Structure

```
pinterest-scraper/
├── api/
│   ├── __init__.py
│   └── server.py          # FastAPI app — all endpoints + Job runner
├── core/
│   ├── __init__.py
│   ├── config.py          # URLs, user-agents, CSV columns
│   ├── dedupe.py          # Cross-run deduplication store
│   ├── downloader.py      # Concurrent image downloader
│   ├── http.py            # Session builder, retry logic, rate-limit handling
│   ├── scraper.py         # Pinterest API calls — search, board, related, suggest
│   └── storage.py         # JSON + CSV persistence
├── static/
│   ├── index.html         # Single-page app shell
│   ├── css/style.css      # Design system — tokens, dark mode, animations
│   └── js/app.js          # Vanilla JS — no build step required
├── __main__.py            # Entry point
├── requirements.txt
└── render.yaml            # One-click Render deployment
```

---

## Quick Start

### Prerequisites

- Python 3.10+

### Local setup

```bash
git clone https://github.com/your-username/pinterest-scraper
cd pinterest-scraper

pip install -r requirements.txt

uvicorn api.server:app --host 0.0.0.0 --port 8000 --reload
```

Open [http://localhost:8000](http://localhost:8000).

### Docker (optional)

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t pinterest-scraper .
docker run -p 8000:8000 pinterest-scraper
```

---

## Deployment

### Render (recommended)

The repo ships with `render.yaml` — deploy in one click.

1. Push to GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your repo — Render auto-detects `render.yaml`
4. Click **Deploy**

> **Note:** Render's free tier uses ephemeral storage. Downloaded images are lost on restart. Use a paid plan or mount a persistent disk at `/app/web_output`.

### Manual VPS

```bash
pip install -r requirements.txt
uvicorn api.server:app --host 0.0.0.0 --port 80 --workers 1
```

For production, put Nginx in front and use a systemd service or `supervisor`.

---

## API Reference

All endpoints return JSON unless noted.

### Scrape

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/scrape` | Start a scrape job |
| `GET` | `/api/jobs/{id}/events` | SSE stream — live progress |
| `GET` | `/api/jobs/{id}/result` | Final result after job completes |
| `POST` | `/api/jobs/{id}/cancel` | Cancel a running job |

**POST `/api/scrape` body:**

```json
{
  "query": "dark academia",
  "mode": "search",
  "limit": 50,
  "download": true,
  "details": true,
  "dedup": false,
  "workers": 4,
  "delay": 1.0,
  "jitter": 0.5,
  "batch_size": 10,
  "min_width": 0,
  "min_height": 0,
  "proxy": ""
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `query` | string | — | Search term or board URL. Comma-separate for batch. |
| `mode` | `search` \| `board` | `search` | Scrape mode |
| `limit` | int | `25` | Max pins per query (1–500) |
| `download` | bool | `true` | Download images to disk |
| `details` | bool | `true` | Fetch full pin details (saves, comments…) |
| `dedup` | bool | `false` | Skip pins seen in previous runs |
| `workers` | int | `4` | Concurrent download threads (1–16) |
| `delay` | float | `1.0` | Seconds between paginated requests |
| `jitter` | float | `0.5` | Random jitter added to delay |
| `proxy` | string | `""` | Proxy URL or comma-separated pool |

### Images & Gallery

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/images/{name}` | Serve a downloaded image |
| `GET` | `/api/gallery` | All downloaded pins with metadata |
| `GET` | `/api/gallery/export/zip` | ZIP of all gallery images |
| `POST` | `/api/images/delete` | Delete images by filename |

### Export

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/jobs/{id}/export/zip` | ZIP of job images |
| `GET` | `/api/jobs/{id}/export/xlsx` | XLSX metadata spreadsheet |

### Suggestions & Visual Search

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/suggest?q=term` | Typeahead suggestions |
| `GET` | `/api/visual-search?pin_id=123` | Related pins by ID |

### Schedules

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/schedules` | List all schedules |
| `POST` | `/api/schedules` | Create a schedule |
| `DELETE` | `/api/schedules/{id}` | Delete a schedule |

**POST `/api/schedules` body:**

```json
{
  "mode": "search",
  "query": "wallpaper 4k",
  "interval_hours": 24,
  "limit": 50
}
```

### SSE Events

The `/api/jobs/{id}/events` stream emits these event types:

| Event | Fields | Description |
|-------|--------|-------------|
| `phase` | `phase`, `total`, `message` | Phase started (collect / details / download) |
| `progress` | `phase`, `count`, `total` | Progress within a phase |
| `query_start` | `query`, `index`, `total` | Batch query started |
| `nothing_new` | `total` | All pins already exist |
| `saved` | `json_file`, `csv_file` | Metadata saved to disk |
| `done` | `status`, `total`, `stats`, `error` | Job completed |

---

## Configuration

Settings are saved per-browser in `localStorage`. The backend reads all options from the request body — no server-side config file required.

### Output structure

Each scrape writes to `web_output/`:

```
web_output/
├── {stem}.json        # Full pin metadata array
├── {stem}.csv         # Flat CSV with all columns
├── .seen_pins.json    # Deduplication store (when dedup=true)
└── images/
    ├── {pin_id}.jpg
    ├── {pin_id}.mp4   # (videos not downloaded, URL stored)
    └── ...
```

### Proxy support

Pass a single proxy or comma-separated pool in the `proxy` field:

```
http://user:pass@host:port
http://proxy1:port,http://proxy2:port
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.10+, FastAPI, uvicorn |
| HTTP | `requests` with retry + rate-limit handling |
| Concurrency | `concurrent.futures.ThreadPoolExecutor` |
| Export | `openpyxl` (XLSX), `zipfile`, `csv` |
| Frontend | Vanilla JS (no build step), CSS custom properties |
| Charts | Chart.js 4 |
| Deployment | Render, Docker-compatible |

---

## Metadata Fields

Every pin object contains:

| Field | Type | Description |
|-------|------|-------------|
| `pin_id` | string | Pinterest pin ID |
| `pin_url` | string | Full Pinterest URL |
| `title` | string | Pin title |
| `description` | string | Pin description |
| `alt_text` | string | Auto-generated alt text |
| `image_url` | string | Highest-resolution image URL |
| `width` / `height` | int | Image dimensions in px |
| `aspect_ratio` | float | width / height |
| `saves` | int | Total saves |
| `repin_count` | int | Repin count |
| `likes` | int | Like count |
| `comments` | int | Comment count |
| `creator_username` | string | Pinterest username |
| `creator_name` | string | Display name |
| `creator_profile` | string | Profile URL |
| `board_name` | string | Board name |
| `board_url` | string | Board URL |
| `external_link` | string | External link on pin |
| `domain` | string | External link domain |
| `dominant_color` | string | Hex color code |
| `created_at` | string | ISO creation timestamp |
| `is_video` | bool | True if video pin |
| `video_url` | string | Direct MP4 URL (if video) |
| `local_file` | string | Downloaded filename (if saved) |

---

## Legal

This project is for **personal, educational, and research use only**.  
Respect Pinterest's [Terms of Service](https://policy.pinterest.com/en/terms-of-service) and `robots.txt`.  
Do not use at scale or for commercial scraping without explicit permission.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=E60023&height=100&section=footer" width="100%">

Made with Python and FastAPI · Deployed on Render

</div>
