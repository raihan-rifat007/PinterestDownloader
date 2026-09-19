# Pinterest Downloader — Web App

A small Flask web app wrapped around the `pinterest_downloader` library
(originally by Ahmed Negm, https://github.com/x7007x/PinterestDownloader,
MIT licensed — see LICENSE). The original project is a Python library
with no web interface; this adds a single-page web UI and an HTTP API
so it can be deployed as a live service and called from a bot.

## What this does

Paste a Pinterest pin, board, or profile link, or type a search term.
Results show as a grid with a direct download button per item (images,
GIFs, and videos are all handled).

## What changed from the original project

- `pinterest_downloader/pinterest.py` and `__init__.py` are **unchanged**
  — this is the original author's code, untouched.
- Added: `app.py` (Flask backend), `static/index.html` (the web UI).
- Removed (not needed to run this as a service):
  - `setup.py` — PyPI packaging metadata, only relevant if publishing
    this as an installable pip package.
  - `test_features.py`, `test_live.py` — legitimate test scripts, but
    they call the real Pinterest servers directly and exist to verify
    the library during development, not to run the app.
  - `.github/workflows/python-package.yml` — CI that auto-publishes to
    PyPI on every push; needs a PyPI token you don't have for this use.

None of this is "bad code" — it served the original project's purpose
(a published, tested pip package), which is different from what this
does (a running web service).

## API

**POST /api/resolve**
```json
{ "input": "https://www.pinterest.com/pin/123.../", "bookmark": null }
```
`input` can be a pin URL, a `pin.it` short link, a bare pin ID, a board
URL, a profile URL, or a plain search term — the type is auto-detected.
Returns `{ "ok": true, "type": "pin|board|profile|search", "title": "...",
"pins": [...], "bookmark": "..." }`. Pass the returned `bookmark` back
in a follow-up request to get the next page.

**GET /api/download?url=...&filename=...**
Streams the file back with a `Content-Disposition: attachment` header,
so it downloads instead of opening in the browser. Only proxies URLs on
`pinimg.com` or `pinterest.com` — anything else is rejected.

## Running locally

```
pip install -r requirements.txt
python app.py
```
Open http://localhost:5000

## Deploying to Render

Render deploys from a connected Git repository — there's no direct zip
upload. Steps:

1. Push this folder to a new GitHub repository.
2. In the Render dashboard: click **New +**, choose **Web Service**, and connect that
   repository.
3. Set:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. Click **Create Web Service**.

Your app will be live at `https://<your-service-name>.onrender.com`.

**Worth knowing**: on Render's free tier, the service sleeps after 15
minutes with no traffic and takes about 60 seconds to wake up on the
next request. That first request after a quiet period will be slow —
this is normal, not a bug.

## A note on reliability

This wraps Pinterest's own internal (undocumented) endpoints, the same
way the original library always has — there's no official API key or
contract involved. If Pinterest changes something on their end, this
can break without warning, the same as any project in this category.
