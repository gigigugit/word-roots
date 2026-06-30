# Word Roots Generator

A web application that lets you explore, analyse, and create words by combining roots, prefixes, and suffixes.

## Features

1. **Root Identification** — paste any English word; the app detects its prefix, root, and suffix from a curated linguistic database (29 prefixes, 25 suffixes, 31 roots).
2. **Prefix & Suffix Suggestions** — interactive pill selectors list every available prefix and suffix with meaning, origin, and example words.
3. **Word Creation** — select a prefix + root + suffix; get an instant preview, auto-generated definition, and example sentence.
4. **Save & Export** — store created words in a local SQLite database; download any word as a JSON file.
5. **Social Sharing** — copy a share-ready text snippet to the clipboard or open a pre-filled Twitter/X tweet.
6. **User Feedback** — rate saved words 1–5 stars and leave comments; average ratings are shown in the word list.
7. **Visual Interface** — colour-coded breakdown of word components (green = prefix, blue = root, orange = suffix) with hover tooltips.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server
python app.py
```

Open <http://127.0.0.1:5000> in your browser.

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

## Project Structure

```
word-roots/
├── app.py                  # Flask application & API routes
├── requirements.txt
├── data/
│   └── linguistic_data.py  # Roots, prefixes, suffixes + analysis helpers
├── templates/
│   └── index.html          # Single-page UI (Bootstrap 5)
├── static/
│   ├── css/style.css
│   └── js/app.js
└── tests/
    └── test_app.py
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/` | Serve the UI |
| `POST` | `/api/analyze` | Analyse a word |
| `GET`  | `/api/prefixes` | List all prefixes |
| `GET`  | `/api/suffixes` | List all suffixes |
| `GET`  | `/api/roots` | List all roots |
| `POST` | `/api/create` | Build a new word |
| `POST` | `/api/save` | Save a word to DB |
| `GET`  | `/api/words` | List saved words |
| `GET`  | `/api/export/<id>` | Download word as JSON |
| `POST` | `/api/feedback` | Submit rating + comment |
| `GET`  | `/api/share/<id>` | Get shareable text |
