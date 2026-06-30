"""
Word Roots Generator — Flask application.

Routes
------
GET  /                        Serve the single-page UI
POST /api/analyze             Analyse a word → prefix / root / suffix
GET  /api/prefixes            Return all known prefixes
GET  /api/suffixes            Return all known suffixes
GET  /api/roots               Return all known roots
POST /api/create              Build a new word from components
POST /api/save                Persist a created word to SQLite
GET  /api/words               List all saved words (with avg rating)
GET  /api/export/<id>         Download a saved word as JSON
POST /api/feedback            Submit a star rating + comment
GET  /api/share/<id>          Return shareable text for a saved word
"""

import io
import json
import os
import sqlite3

from flask import Flask, g, jsonify, render_template, request, send_file

from data.linguistic_data import (
    PREFIXES,
    ROOTS,
    SUFFIXES,
    analyze_word,
    create_word,
    generate_definition,
    generate_example,
)

app = Flask(__name__)
app.config["DATABASE"] = os.path.join(os.path.dirname(__file__), "word_roots.db")


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_error):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create tables if they do not already exist."""
    db = sqlite3.connect(app.config["DATABASE"])
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS saved_words (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            word        TEXT    NOT NULL,
            prefix      TEXT,
            root        TEXT    NOT NULL,
            suffix      TEXT,
            definition  TEXT,
            example     TEXT,
            created_at  TEXT    DEFAULT (datetime('now'))
        )
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS feedback (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            word_id    INTEGER NOT NULL,
            rating     INTEGER CHECK(rating BETWEEN 1 AND 5),
            comment    TEXT,
            created_at TEXT    DEFAULT (datetime('now')),
            FOREIGN KEY (word_id) REFERENCES saved_words(id)
        )
        """
    )
    db.commit()
    db.close()


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    word = (data.get("word") or "").strip()
    if not word:
        return jsonify({"error": "No word provided"}), 400
    return jsonify(analyze_word(word))


@app.route("/api/prefixes")
def get_prefixes():
    return jsonify(PREFIXES)


@app.route("/api/suffixes")
def get_suffixes():
    return jsonify(SUFFIXES)


@app.route("/api/roots")
def get_roots():
    return jsonify(ROOTS)


@app.route("/api/create", methods=["POST"])
def create():
    data = request.get_json(silent=True) or {}
    prefix = (data.get("prefix") or "").strip() or None
    root = (data.get("root") or "").strip()
    suffix = (data.get("suffix") or "").strip() or None

    if not root:
        return jsonify({"error": "Root is required"}), 400

    word = create_word(prefix, root, suffix)
    definition = generate_definition(prefix, root, suffix)
    example = generate_example(word, prefix, root, suffix)

    return jsonify(
        {
            "word": word,
            "prefix": prefix,
            "root": root,
            "suffix": suffix,
            "definition": definition,
            "example": example,
            "prefix_info": PREFIXES.get(prefix),
            "root_info": ROOTS.get(root),
            "suffix_info": SUFFIXES.get(suffix),
        }
    )


@app.route("/api/save", methods=["POST"])
def save():
    data = request.get_json(silent=True) or {}
    word = (data.get("word") or "").strip()
    prefix = (data.get("prefix") or "").strip() or None
    root = (data.get("root") or "").strip()
    suffix = (data.get("suffix") or "").strip() or None
    definition = (data.get("definition") or "").strip()
    example = (data.get("example") or "").strip()

    if not word or not root:
        return jsonify({"error": "word and root are required"}), 400

    db = get_db()
    cursor = db.execute(
        "INSERT INTO saved_words (word, prefix, root, suffix, definition, example) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (word, prefix, root, suffix, definition, example),
    )
    db.commit()
    return jsonify({"id": cursor.lastrowid, "message": "Word saved successfully"})


@app.route("/api/words")
def get_words():
    db = get_db()
    rows = db.execute(
        """
        SELECT sw.*,
               COALESCE(AVG(f.rating), 0) AS avg_rating,
               COUNT(f.id)                AS feedback_count
          FROM saved_words sw
          LEFT JOIN feedback f ON sw.id = f.word_id
         GROUP BY sw.id
         ORDER BY sw.created_at DESC
        """
    ).fetchall()
    return jsonify([dict(r) for r in rows])


@app.route("/api/export/<int:word_id>")
def export_word(word_id):
    db = get_db()
    row = db.execute(
        "SELECT * FROM saved_words WHERE id = ?", (word_id,)
    ).fetchone()
    if not row:
        return jsonify({"error": "Word not found"}), 404

    json_bytes = json.dumps(dict(row), indent=2).encode()
    filename = f"{dict(row)['word']}.json"
    return send_file(
        io.BytesIO(json_bytes),
        mimetype="application/json",
        as_attachment=True,
        download_name=filename,
    )


@app.route("/api/feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json(silent=True) or {}
    word_id = data.get("word_id")
    rating = data.get("rating")
    comment = (data.get("comment") or "").strip()

    if word_id is None or rating is None:
        return jsonify({"error": "word_id and rating are required"}), 400
    try:
        rating = int(rating)
    except (TypeError, ValueError):
        return jsonify({"error": "rating must be an integer"}), 400
    if not 1 <= rating <= 5:
        return jsonify({"error": "Rating must be between 1 and 5"}), 400

    db = get_db()
    if not db.execute(
        "SELECT id FROM saved_words WHERE id = ?", (word_id,)
    ).fetchone():
        return jsonify({"error": "Word not found"}), 404

    db.execute(
        "INSERT INTO feedback (word_id, rating, comment) VALUES (?, ?, ?)",
        (word_id, rating, comment),
    )
    db.commit()
    return jsonify({"message": "Feedback submitted successfully"})


@app.route("/api/share/<int:word_id>")
def share_word(word_id):
    db = get_db()
    row = db.execute(
        "SELECT * FROM saved_words WHERE id = ?", (word_id,)
    ).fetchone()
    if not row:
        return jsonify({"error": "Word not found"}), 404

    word_dict = dict(row)
    return jsonify(
        {
            "share_text": (
                f"New word: '{word_dict['word']}' — {word_dict['definition']}"
            ),
            "word_data": word_dict,
        }
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

with app.app_context():
    init_db()

if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(debug=debug)
