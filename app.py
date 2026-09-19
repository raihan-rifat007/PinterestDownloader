import os
import re
from urllib.parse import urlparse, quote

from flask import Flask, request, jsonify, send_from_directory, Response, stream_with_context

from pinterest_downloader import Pinterest

app = Flask(__name__)
client = Pinterest(timeout=30)

PIN_ID_RE = re.compile(r"/pin/(\d+)")
PIN_SHORT_RE = re.compile(r"pin\.it/", re.IGNORECASE)


def is_pinterest_url(value):
    try:
        parsed = urlparse(value)
    except ValueError:
        return False
    if parsed.scheme not in ("http", "https"):
        return False
    host = (parsed.hostname or "").lower()
    return host == "pinterest.com" or host.endswith(".pinterest.com")


ALLOWED_MEDIA_HOSTS = ("pinimg.com", "pinterest.com")


def is_pinterest_media_url(value):
    try:
        parsed = urlparse(value)
    except ValueError:
        return False
    if parsed.scheme != "https":
        return False
    host = (parsed.hostname or "").lower()
    return any(host == h or host.endswith("." + h) for h in ALLOWED_MEDIA_HOSTS)


def path_segments(value):
    parsed = urlparse(value)
    return [p for p in parsed.path.strip("/").split("/") if p]


def classify_input(value):
    """Decide which library call a given input should route to.

    Returns one of: "pin", "board", "profile", "search".
    """
    value = value.strip()

    if PIN_ID_RE.search(value) or re.fullmatch(r"\d+", value):
        return "pin"

    if PIN_SHORT_RE.search(value):
        return "pin"

    if is_pinterest_url(value):
        segments = path_segments(value)
        if len(segments) >= 2:
            return "board"
        if len(segments) == 1:
            return "profile"

    return "search"


def simplify_pin(pin):
    """Flatten a library pin object into only what the UI needs."""
    images = pin.get("images") or {}
    thumbnail = None
    for size_key in ["474x", "236x", "736x", "170x"]:
        candidate = images.get(size_key, {}).get("url")
        if candidate:
            thumbnail = candidate
            break
    if not thumbnail and images:
        thumbnail = list(images.values())[0].get("url")

    is_video = pin.get("media_type") == "video"
    download_url = None
    if is_video:
        formats = (pin.get("video") or {}).get("formats") or []
        mp4s = [f for f in formats if (f.get("url") or "").lower().endswith(".mp4")]
        if mp4s:
            download_url = mp4s[0]["url"]
        elif formats:
            download_url = formats[0].get("url")
    else:
        for size_key in ["orig", "736x", "474x", "236x"]:
            candidate = images.get(size_key, {}).get("url")
            if candidate:
                download_url = candidate
                break

    ext = ".mp4" if is_video else (".gif" if pin.get("media_type") == "gif" else ".jpg")

    return {
        "id": pin.get("id"),
        "title": pin.get("title") or "Untitled pin",
        "pin_url": pin.get("url"),
        "thumbnail_url": thumbnail,
        "download_url": download_url,
        "is_video": is_video,
        "filename": f"{pin.get('id')}{ext}",
    }


@app.route("/")
def index():
    return send_from_directory(app.static_folder or "static", "index.html")


@app.route("/api/resolve", methods=["POST"])
def resolve():
    body = request.get_json(silent=True) or {}
    value = (body.get("input") or "").strip()
    bookmark = body.get("bookmark")
    try:
        page_size = min(int(body.get("page_size", 25)), 50)
    except (TypeError, ValueError):
        page_size = 25

    if not value:
        return jsonify({"ok": False, "error": "No input provided"}), 400

    kind = classify_input(value)

    try:
        return _dispatch(kind, value, page_size, bookmark)
    except Exception as exc:
        return jsonify({"ok": False, "error": f"Unexpected error: {exc}"}), 500


def _dispatch(kind, value, page_size, bookmark):
    if kind == "pin":
        result = client.get_pin(value)
        if not result.get("ok"):
            return jsonify({"ok": False, "error": result.get("error", {}).get("message", "Pin not found")}), 404
        return jsonify({
            "ok": True,
            "type": "pin",
            "title": result["pin"].get("title") or "Pin",
            "pins": [simplify_pin(result["pin"])],
            "bookmark": None,
        })

    if kind == "board":
        result = client.get_board_pins(value, page_size=page_size, bookmark=bookmark)
        if not result.get("ok"):
            return jsonify({"ok": False, "error": result.get("error", {}).get("message", "Board not found")}), 404
        board_name = (result.get("board") or {}).get("name") or "Board"
        return jsonify({
            "ok": True,
            "type": "board",
            "title": board_name,
            "pins": [simplify_pin(p) for p in result.get("pins", [])],
            "bookmark": result.get("bookmark"),
        })

    if kind == "profile":
        segments = path_segments(value)
        username = segments[0] if segments else value
        result = client.get_user_pins(username, page_size=page_size, bookmark=bookmark)
        if not result.get("ok"):
            return jsonify({"ok": False, "error": result.get("error", {}).get("message", "Profile not found")}), 404
        return jsonify({
            "ok": True,
            "type": "profile",
            "title": f"@{username}",
            "pins": [simplify_pin(p) for p in result.get("pins", [])],
            "bookmark": result.get("bookmark"),
        })

    result = client.search(value, page_size=page_size, bookmark=bookmark)
    if not result.get("ok"):
        return jsonify({"ok": False, "error": result.get("error", {}).get("message", "Search failed")}), 502
    return jsonify({
        "ok": True,
        "type": "search",
        "title": f'Results for "{value}"',
        "pins": [simplify_pin(p) for p in result.get("pins", [])],
        "bookmark": result.get("bookmark"),
    })


@app.route("/api/download")
def download():
    media_url = request.args.get("url")
    filename = request.args.get("filename", "download")

    if not media_url:
        return jsonify({"ok": False, "error": "Missing url parameter"}), 400
    if not is_pinterest_media_url(media_url):
        return jsonify({"ok": False, "error": "URL is not a recognized Pinterest media host"}), 400

    try:
        upstream = client.session.get(media_url, stream=True, timeout=client.timeout)
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 502
    if upstream.status_code != 200:
        return jsonify({"ok": False, "error": f"Upstream returned {upstream.status_code}"}), 502

    safe_name = quote(filename)
    headers = {
        "Content-Disposition": f'attachment; filename="{safe_name}"',
        "Content-Type": upstream.headers.get("Content-Type", "application/octet-stream"),
    }
    if "Content-Length" in upstream.headers:
        headers["Content-Length"] = upstream.headers["Content-Length"]

    return Response(
        stream_with_context(upstream.iter_content(chunk_size=65536)),
        headers=headers,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
