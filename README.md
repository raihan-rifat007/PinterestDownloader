<div align="center">

# 📌 Pinterest Downloader

**A production-grade Pinterest downloader with a premium web UI**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success?style=flat-square)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=flat-square)]()

**Download pins, boards, and profiles from Pinterest in original quality — no signup, no API key**

[Features](#-features) · [Quick Start](#-quick-start) · [API Reference](#-api-reference) · [Architecture](#-architecture) · [Deployment](#-deployment)

</div>

---

## 📖 Overview

**PinGrab** is a modern, self-hosted Pinterest downloader that scrapes public Pinterest content and delivers it through a clean REST API with a stunning web interface. Built with Flask and a sophisticated vanilla-JS frontend, it handles pins, boards, profiles, and search queries — all with automatic type detection.

### Why PinGrab?

- 🎯 **Smart URL Detection** — Auto-routes pins, boards, profiles, and search terms
- 🎨 **Premium UI** — Glassmorphic design with dark/light themes
- ⚡ **Blazing Fast** — Optimized scraping with connection pooling
- 🎬 **Multi-Media** — Images, GIFs, and MP4 videos supported
- 💾 **Favorites System** — Save pins locally with one click
- 📜 **Search History** — Track recent queries
- ⌨️ **Command Palette** — Raycast-style ⌘K menu
- 📱 **Fully Responsive** — Mobile-first design
- 🔒 **Safe Downloads** — Streams with host validation

---

## ✨ Features

### Core Capabilities

| Feature | Description | Status |
|---------|-------------|--------|
| **Pin Download** | Single pin extraction with metadata | ✅ |
| **Board Download** | Full board pin iteration | ✅ |
| **Profile Scraping** | User pins + profile info | ✅ |
| **Keyword Search** | Pinterest search results | ✅ |
| **Video Support** | MP4 video download for video pins | ✅ |
| **GIF Support** | Animated GIF handling | ✅ |
| **Pagination** | Bookmark-based infinite scroll | ✅ |
| **Auto Type Detection** | URL/ID/keyword routing | ✅ |
| **Metadata Extraction** | Author, board, engagement stats | ✅ |
| **Stream Downloads** | Chunked streaming for large files | ✅ |

### UI Highlights

- 🎭 **Glassmorphic Design** — Frosted glass aesthetic
- 🌈 **Red-Rose Gradient** — Pinterest-inspired palette
- ✨ **Micro-animations** — 60fps smooth transitions
- 🖼️ **Lightbox Viewer** — Full-screen with zoom
- 🎛️ **Command Palette** — Raycast-style ⌘K menu
- 📊 **Filter System** — All / Video / Image / Favorites
- 🎚️ **Layout Modes** — Compact, Default, Large
- 🔔 **Toast Notifications** — Elegant feedback
- 🌗 **Theme Toggle** — Dark/light with auto-detect

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **pip** package manager
- **Modern browser** (Chrome, Firefox, Safari, Edge)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/raihan07/PinterestDownloader.git
cd pingrab

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
python app.py
```

Open your browser: http://localhost:5000

Using Gunicorn (Production)

```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:app
```

---

🔌 API Reference

Base URL

```
http://localhost:5000
```

Endpoints

1. Home Page

```http
GET /
```

Serves the main web interface.

---

2. Resolve Input

```http
POST /api/resolve
Content-Type: application/json
```

Universal endpoint — automatically routes pins, boards, profiles, or search queries.

Request Body:

```json
{
  "input": "https://pinterest.com/pin/123456789",
  "page_size": 25,
  "bookmark": null
}
```

Parameters:

Parameter Type Required Default Description
input string ✅ Yes — Pin URL, board URL, profile, or keyword
page_size integer ❌ No 25 Pins per page (max 50)
bookmark string ❌ No null Pagination cursor

Auto-Detection Rules:

Input Type Detected As Example
Pin URL pin pinterest.com/pin/123456
Numeric ID pin 123456789
Board URL board pinterest.com/user/board-name
Profile URL profile pinterest.com/username
Keyword search minimal wallpaper

Response (Pin):

```json
{
  "ok": true,
  "type": "pin",
  "title": "Beautiful sunset",
  "pins": [
    {
      "id": "123456789",
      "title": "Beautiful sunset",
      "pin_url": "https://pinterest.com/pin/123456789/",
      "thumbnail_url": "https://i.pinimg.com/474x/...",
      "download_url": "https://i.pinimg.com/originals/...",
      "is_video": false,
      "filename": "123456789.jpg"
    }
  ],
  "bookmark": null
}
```

Response (Search):

```json
{
  "ok": true,
  "type": "search",
  "title": "Results for \"minimal wallpaper\"",
  "pins": [
    {
      "id": "987654321",
      "title": "Minimalist desktop wallpaper",
      "pin_url": "https://pinterest.com/pin/987654321/",
      "thumbnail_url": "https://i.pinimg.com/474x/...",
      "download_url": "https://i.pinimg.com/originals/...",
      "is_video": false,
      "filename": "987654321.jpg"
    }
  ],
  "bookmark": "Y2Jvb2ttYXJr..."
}
```

Response (Video):

```json
{
  "ok": true,
  "type": "search",
  "title": "Results for \"cooking tutorial\"",
  "pins": [
    {
      "id": "555444333",
      "title": "Quick pasta recipe",
      "pin_url": "https://pinterest.com/pin/555444333/",
      "thumbnail_url": "https://i.pinimg.com/474x/...",
      "download_url": "https://v1.pinimg.com/videos/.../720p.mp4",
      "is_video": true,
      "filename": "555444333.mp4"
    }
  ],
  "bookmark": null
}
```

Error Response:

```json
{
  "ok": false,
  "error": "Pin not found"
}
```

Status Codes:

Code Meaning
200 Success
400 Missing/invalid input
404 Pin/board/profile not found
500 Internal error
502 Pinterest upstream error

---

3. Download Media

```http
GET /api/download?url=MEDIA_URL&filename=NAME
```

Query Parameters:

Parameter Type Required Description
url string ✅ Yes Pinterest media URL (pinimg.com)
filename string ❌ No Download filename (default: download)

Security: Only accepts URLs from pinimg.com and pinterest.com hosts.

Response: Binary file stream with:

· Content-Disposition: attachment; filename="..."
· Content-Type: image/jpeg | image/png | video/mp4
· Content-Length (when available)

Example:

```bash
curl -OJ "http://localhost:5000/api/download?url=https://i.pinimg.com/originals/...&filename=sunset.jpg"
```

---

🎨 Available Features

Pin Types

Type Extensions Download Source
Image .jpg, .png images.orig (original size)
GIF .gif images.orig
Video .mp4 Highest quality video format

Filter Modes

Filter Shows
All Every pin in the result set
Video Video pins only
Image Image pins only (excludes videos)
Favorites Locally saved pins

Layout Modes

Mode Grid Columns Best For
Compact Many small cards Quick browsing
Default Balanced medium cards Daily use
Large Few large cards High-res previews

---

🏗️ Architecture

System Design

```
┌─────────────────────────────────────────────────────────┐
│                   Client Browser                        │
│  ┌───────────────────────────────────────────────────┐  │
│  │  HTML + CSS + Vanilla JS (Single Page)           │  │
│  │  • Command palette (⌘K)                          │  │
│  │  • Grid + Lightbox + Drawers                     │  │
│  │  • Favorites + History (localStorage)            │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP/JSON
                      ▼
┌─────────────────────────────────────────────────────────┐
│                  Flask Application                      │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Routes: /, /api/resolve, /api/download          │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  URL Classifier (pin/board/profile/search)        │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Pinterest Client (resource API + HTML scrape)   │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTPS
                      ▼
┌─────────────────────────────────────────────────────────┐
│              Pinterest (public content)                 │
│  • www.pinterest.com/resource/* (JSON)                  │
│  • www.pinterest.com/{user}/ (HTML)                     │
│  • i.pinimg.com (images)                                │
│  • v.pinimg.com (videos)                                │
└─────────────────────────────────────────────────────────┘
```

Input Classification

```python
def classify_input(value):
    if PIN_ID_RE.search(value) or value.isdigit():
        return "pin"                    # Pin URL or numeric ID
    if is_pinterest_url(value):
        segments = path_segments(value)
        if len(segments) >= 2:
            return "board"              # /user/board-name
        if len(segments) == 1:
            return "profile"            # /username
    return "search"                     # Keyword search
```

Response Flow

```
1. Client sends { input, bookmark }
         ↓
2. Classify input → pin/board/profile/search
         ↓
3. Call appropriate Pinterest endpoint
         ↓
4. Parse pin data → simplify for UI
         ↓
5. Return normalized JSON + bookmark
         ↓
6. Client renders grid + pagination
```

---

🚢 Deployment

Option 1: Render

1. Push code to GitHub
2. Create New Web Service on Render
3. Connect repository
4. Configure:
   · Build: pip install -r requirements.txt
   · Start: gunicorn app:app
   · Port: 5000
5. Deploy

Option 2: Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

Option 3: Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]
```

```bash
docker build -t pingrab .
docker run -p 5000:5000 pingrab
```

Option 4: Vercel

Add vercel.json:

```json
{
  "version": 2,
  "builds": [
    { "src": "app.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "app.py" }
  ]
}
```

Option 5: Manual VPS

```bash
# Install gunicorn
pip install gunicorn

# Systemd service
sudo nano /etc/systemd/system/pingrab.service
```

```ini
[Unit]
Description=PinGrab Pinterest Downloader
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/pingrab
Environment="PATH=/var/www/pingrab/venv/bin"
ExecStart=/var/www/pingrab/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable pingrab
sudo systemctl start pingrab
```

---

⚙️ Configuration

Environment Variables

Variable Required Default Description
PORT ❌ No 5000 Server port

Custom Headers / Timeouts

Edit pinterest.py:

```python
client = Pinterest(
    timeout=30,             # Request timeout
    proxies=None,           # Optional proxy dict
    headers={               # Custom headers
        "User-Agent": "custom..."
    }
)
```

---

⌨️ Keyboard Shortcuts

Shortcut Action
⌘K / Ctrl+K Open command palette
/ Focus search bar
⌘J / Ctrl+J Toggle theme
⌘F / Ctrl+F Open favorites
⌘⇧C / Ctrl+Shift+C Clear results
? Show shortcuts
Esc Close overlays

---

🧪 Testing

API Tests

```bash
# Test with pin URL
curl -X POST http://localhost:5000/api/resolve \
  -H "Content-Type: application/json" \
  -d '{"input": "https://pinterest.com/pin/123456789"}'

# Test with keyword search
curl -X POST http://localhost:5000/api/resolve \
  -H "Content-Type: application/json" \
  -d '{"input": "minimal wallpaper", "page_size": 10}'

# Test with board URL
curl -X POST http://localhost:5000/api/resolve \
  -H "Content-Type: application/json" \
  -d '{"input": "https://pinterest.com/username/board-name"}'

# Test pagination
curl -X POST http://localhost:5000/api/resolve \
  -H "Content-Type: application/json" \
  -d '{"input": "cooking", "bookmark": "Y2Jvb2ttYXJr"}'
```

Python Client

```python
import requests

class PinGrab:
    def __init__(self, base_url="http://localhost:5000"):
        self.base = base_url.rstrip("/")
    
    def resolve(self, input_str, page_size=25, bookmark=None):
        r = requests.post(
            f"{self.base}/api/resolve",
            json={"input": input_str, "page_size": page_size, "bookmark": bookmark},
            timeout=30,
        )
        r.raise_for_status()
        return r.json()
    
    def download(self, media_url, filename="download.jpg"):
        r = requests.get(
            f"{self.base}/api/download",
            params={"url": media_url, "filename": filename},
            stream=True,
        )
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(65536):
                f.write(chunk)
        return filename

# Usage
grab = PinGrab()
result = grab.resolve("minimal wallpaper", page_size=20)
for pin in result["pins"][:5]:
    print(f"• {pin['title']} → {pin['download_url']}")
```

---

🎯 Use Cases

· Content Curation — Build mood boards and references
· Design Inspiration — Save visual references
· Social Media — Collect content for posts
· Wallpapers — Grab high-res backgrounds
· Research — Analyze trends and aesthetics
· Bot Integration — Discord/Telegram/Messenger bots
· Personal Archive — Backup favorite pins

---

🔒 Security & Best Practices

· ✅ Host Validation — Only pinimg.com / pinterest.com for downloads
· ✅ Stream Download — Chunked transfer, no memory bloat
· ✅ URL Scheme Check — HTTPS only
· ✅ Input Sanitization — Regex-validated inputs
· ✅ No User Data Stored — All client-side
· ✅ No Tracking — Zero analytics

Recommendations

· 🔐 Add rate limiting for public deployments
· 🔐 Enable HTTPS in production
· 🔐 Use a reverse proxy (Nginx/Caddy)
· 🔐 Monitor resource usage
· 🔐 Respect Pinterest's rate limits

---

🐛 Troubleshooting

Common Issues

Issue Solution
Pin not found URL may be private/deleted — verify in browser
Slow search Pinterest throttling — wait 30s and retry
Empty results Query may be filtered — try different keyword
Download fails Media may be geo-restricted
Port in use Change port: app.run(port=5001)
Module not found Activate venv: source venv/bin/activate

Debug Mode

```python
if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

Enable Request Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

📈 Performance

Metric Value
Cold start ~2s
Pin resolve 1–3s
Search (25 pins) 2–5s
Concurrent users 20+
Memory usage ~80MB
Download speed Network-limited

Optimization Tips

· Use page_size=50 to reduce requests
· Cache results via CDN in front
· Run behind Nginx/Caddy for static assets
· Enable HTTP/2 for parallelism
· Use Redis for cross-instance caching

---

🤝 Contributing

Contributions welcome! Follow these steps:

```bash
# 1. Fork the repo
# 2. Create feature branch
git checkout -b feature/amazing-feature

# 3. Commit changes
git commit -m "Add amazing feature"

# 4. Push to branch
git push origin feature/amazing-feature

# 5. Open Pull Request
```

Development Guidelines

· Follow PEP 8 for Python
· Use semantic HTML for templates
· Keep JS vanilla (no frameworks)
· Test before submitting
· Update README for new features

---

📄 License

Licensed under the MIT License — see LICENSE for details.

---

⚖️ Legal Disclaimer

This tool is for personal, educational use only. It scrapes publicly available Pinterest content. Users are responsible for:

· Respecting Pinterest's Terms of Service
· Respecting copyright of content creators
· Not using for commercial redistribution
· Complying with local laws

The developers are not liable for misuse. Always credit original creators when sharing content.

---

🙏 Acknowledgments

· Pinterest — Public content platform
· Flask — Web framework
· BeautifulSoup — HTML parsing
· Requests — HTTP library
· Open Source Community — Tools and inspiration

---

📞 Contact & Support

Channel Link
GitHub Issues Report Bug
Discussions Ask Questions
Creator @raihan07

---

<div align="center">

Built with ❤️ by raihan07

⭐ Star this project if you find it useful! ⭐

</div>
