# Pinterest Downloader

A web application for downloading Pinterest pins, boards, and search results.

## Features

- Download individual pins
- Download entire boards
- Search Pinterest and download results
- Support for images, GIFs, and videos
- Clean and responsive web interface

## Installation

### Prerequisites

- Python 3.7+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/raihan-rifat007/PinterestDownloader.git
cd PinterestDownloader
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Local Development

```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Deploy to Vercel

1. Create a `vercel.json` file in the project root:
```json
{
  "buildCommand": "pip install -r requirements.txt",
  "outputDirectory": ".vercel/output"
}
```

2. Install Vercel CLI and deploy:
```bash
npm i -g vercel
vercel
```

### Deploy to Heroku

1. Create a Heroku app:
```bash
heroku create your-app-name
```

2. Deploy:
```bash
git push heroku main
```

## API Endpoints

### POST /api/resolve

Resolve a Pinterest URL or search query.

**Request body:**
```json
{
  "input": "pinterest.com/pin/1234567890",
  "page_size": 25,
  "bookmark": null
}
```

**Response:**
```json
{
  "ok": true,
  "type": "pin",
  "title": "Pin Title",
  "pins": [
    {
      "id": "1234567890",
      "title": "Pin Title",
      "pin_url": "https://pinterest.com/pin/1234567890",
      "thumbnail_url": "https://...",
      "download_url": "https://...",
      "is_video": false,
      "filename": "1234567890.jpg"
    }
  ],
  "bookmark": null
}
```

### GET /api/download

Download media directly.

**Query parameters:**
- `url`: Media URL to download
- `filename`: Output filename

## Project Structure

```
PinterestDownloader/
├── app.py
├── requirements.txt
├── Procfile
├── pinterest_downloader/
│   ├── __init__.py
│   └── pinterest.py
├── static/
│   ├── index.html
│   └── asset/
└── README.md
```

## Technologies

- Flask - Web framework
- Requests - HTTP library
- BeautifulSoup - HTML parsing
- Gunicorn - WSGI server

## License

MIT License

## Support

For issues and feature requests, please open an issue on GitHub.
