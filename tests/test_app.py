"""
Tests for the Word Roots Generator application.
Covers the linguistic data helpers and all Flask API endpoints.
"""

import json
import os
import sys
import tempfile
import pytest

# Ensure repository root is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import app as app_module
from data.linguistic_data import (
    PREFIXES,
    ROOTS,
    SUFFIXES,
    analyze_word,
    create_word,
    generate_definition,
    generate_example,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client(tmp_path):
    """Provide a Flask test client backed by a temporary SQLite database."""
    db_path = str(tmp_path / "test_word_roots.db")
    app_module.app.config["DATABASE"] = db_path
    app_module.app.config["TESTING"] = True
    app_module.init_db()
    with app_module.app.test_client() as client:
        yield client


# ---------------------------------------------------------------------------
# Linguistic data — unit tests
# ---------------------------------------------------------------------------

class TestLinguisticData:
    def test_prefixes_not_empty(self):
        assert len(PREFIXES) > 0

    def test_suffixes_not_empty(self):
        assert len(SUFFIXES) > 0

    def test_roots_not_empty(self):
        assert len(ROOTS) > 0

    def test_prefix_has_required_keys(self):
        for key, info in PREFIXES.items():
            assert "display" in info, f"prefix '{key}' missing 'display'"
            assert "meaning" in info, f"prefix '{key}' missing 'meaning'"
            assert "origin"  in info, f"prefix '{key}' missing 'origin'"
            assert "examples" in info, f"prefix '{key}' missing 'examples'"

    def test_suffix_has_required_keys(self):
        for key, info in SUFFIXES.items():
            assert "display"        in info
            assert "meaning"        in info
            assert "part_of_speech" in info

    def test_root_has_required_keys(self):
        for key, info in ROOTS.items():
            assert "display"  in info
            assert "meaning"  in info
            assert "origin"   in info
            assert "examples" in info


class TestAnalyzeWord:
    def test_known_prefix_and_root(self):
        result = analyze_word("transport")
        assert result["prefix"] == "trans"
        assert result["root"]   == "port"
        assert result["root_in_database"] is True

    def test_known_prefix_root_suffix(self):
        result = analyze_word("autograph")
        assert result["prefix"] == "auto"
        assert result["root"]   == "graph"
        assert result["root_in_database"] is True

    def test_root_with_logy_suffix(self):
        result = analyze_word("biology")
        assert result["root"] == "bio"
        assert result["suffix"] == "logy"
        assert result["root_in_database"] is True

    def test_geo_logy(self):
        result = analyze_word("geology")
        assert result["root"] == "geo"
        assert result["suffix"] == "logy"
        assert result["root_in_database"] is True

    def test_case_insensitive(self):
        r1 = analyze_word("Transport")
        r2 = analyze_word("TRANSPORT")
        assert r1["root"] == r2["root"] == "port"

    def test_unknown_word_returns_dict(self):
        result = analyze_word("zzzyxw")
        assert "original_word" in result
        assert "root"          in result

    def test_original_word_preserved(self):
        result = analyze_word("  Biology  ")
        assert result["original_word"] == "biology"

    def test_prefix_info_populated(self):
        result = analyze_word("transport")
        assert result["prefix_info"] is not None
        assert result["prefix_info"]["meaning"] == PREFIXES["trans"]["meaning"]

    def test_root_info_populated(self):
        result = analyze_word("transport")
        assert result["root_info"] is not None

    def test_no_prefix_suffix(self):
        result = analyze_word("bio")
        assert result["root"] == "bio"
        assert result["root_in_database"] is True


class TestCreateWord:
    def test_full_combination(self):
        assert create_word("re", "port", "er") == "reporter"

    def test_prefix_and_root(self):
        assert create_word("trans", "port", None) == "transport"

    def test_root_and_suffix(self):
        assert create_word(None, "bio", "logy") == "biology"

    def test_root_only(self):
        assert create_word(None, "port", None) == "port"


class TestGenerateDefinition:
    def test_all_components(self):
        definition = generate_definition("trans", "port", "er")
        assert isinstance(definition, str)
        assert len(definition) > 0

    def test_prefix_and_root(self):
        definition = generate_definition("trans", "port", None)
        assert isinstance(definition, str)

    def test_root_only(self):
        definition = generate_definition(None, "bio", None)
        assert isinstance(definition, str)

    def test_unknown_root_fallback(self):
        definition = generate_definition(None, "zorb", None)
        assert "zorb" in definition


class TestGenerateExample:
    def test_returns_string(self):
        example = generate_example("reporter", "re", "port", "er")
        assert isinstance(example, str)
        assert len(example) > 0

    def test_word_in_example(self):
        example = generate_example("transport", "trans", "port", None)
        assert "transport" in example


# ---------------------------------------------------------------------------
# Flask API — integration tests
# ---------------------------------------------------------------------------

class TestIndexRoute:
    def test_index_returns_200(self, client):
        res = client.get("/")
        assert res.status_code == 200
        assert b"Word Roots Generator" in res.data


class TestAnalyzeEndpoint:
    def test_analyze_valid_word(self, client):
        res = client.post(
            "/api/analyze",
            json={"word": "transport"},
            content_type="application/json",
        )
        assert res.status_code == 200
        data = res.get_json()
        assert data["root"] == "port"

    def test_analyze_empty_word(self, client):
        res = client.post("/api/analyze", json={"word": ""})
        assert res.status_code == 400

    def test_analyze_missing_body(self, client):
        res = client.post("/api/analyze", json={})
        assert res.status_code == 400

    def test_analyze_returns_all_fields(self, client):
        res = client.post("/api/analyze", json={"word": "biology"})
        data = res.get_json()
        for field in ("original_word", "prefix", "root", "suffix",
                      "prefix_info", "root_info", "suffix_info",
                      "root_in_database"):
            assert field in data


class TestPrefixesSuffixesRootsEndpoints:
    def test_prefixes_returns_dict(self, client):
        res = client.get("/api/prefixes")
        assert res.status_code == 200
        data = res.get_json()
        assert isinstance(data, dict)
        assert len(data) > 0

    def test_suffixes_returns_dict(self, client):
        res = client.get("/api/suffixes")
        assert res.status_code == 200
        assert isinstance(res.get_json(), dict)

    def test_roots_returns_dict(self, client):
        res = client.get("/api/roots")
        assert res.status_code == 200
        assert isinstance(res.get_json(), dict)


class TestCreateEndpoint:
    def test_create_valid(self, client):
        res = client.post(
            "/api/create",
            json={"prefix": "trans", "root": "port", "suffix": "er"},
        )
        assert res.status_code == 200
        data = res.get_json()
        assert data["word"] == "transporter"
        assert "definition" in data
        assert "example"    in data

    def test_create_root_only(self, client):
        res = client.post("/api/create", json={"root": "bio"})
        assert res.status_code == 200
        assert res.get_json()["word"] == "bio"

    def test_create_missing_root(self, client):
        res = client.post("/api/create", json={"prefix": "trans"})
        assert res.status_code == 400


class TestSaveAndWordsEndpoints:
    def _save_word(self, client, word="transporter", root="port"):
        return client.post(
            "/api/save",
            json={
                "word": word,
                "prefix": "trans",
                "root": root,
                "suffix": "er",
                "definition": "One who carries across.",
                "example":    "'transporter' is used in logistics.",
            },
        )

    def test_save_returns_id(self, client):
        res = self._save_word(client)
        assert res.status_code == 200
        data = res.get_json()
        assert "id" in data
        assert isinstance(data["id"], int)

    def test_save_missing_root(self, client):
        res = client.post("/api/save", json={"word": "test"})
        assert res.status_code == 400

    def test_get_words_empty(self, client):
        res = client.get("/api/words")
        assert res.status_code == 200
        assert res.get_json() == []

    def test_get_words_after_save(self, client):
        self._save_word(client)
        res = client.get("/api/words")
        data = res.get_json()
        assert len(data) == 1
        assert data[0]["word"] == "transporter"

    def test_get_words_includes_avg_rating(self, client):
        self._save_word(client)
        res = client.get("/api/words")
        data = res.get_json()
        assert "avg_rating" in data[0]
        assert "feedback_count" in data[0]


class TestExportEndpoint:
    def test_export_existing_word(self, client):
        save_res = client.post(
            "/api/save",
            json={"word": "biology", "root": "bio",
                  "definition": "study of life", "example": "example"},
        )
        word_id = save_res.get_json()["id"]
        res = client.get(f"/api/export/{word_id}")
        assert res.status_code == 200
        assert res.content_type == "application/json"
        payload = json.loads(res.data)
        assert payload["word"] == "biology"

    def test_export_nonexistent(self, client):
        res = client.get("/api/export/9999")
        assert res.status_code == 404


class TestFeedbackEndpoint:
    def _setup_word(self, client):
        res = client.post(
            "/api/save",
            json={"word": "testword", "root": "test",
                  "definition": "d", "example": "e"},
        )
        return res.get_json()["id"]

    def test_submit_feedback_valid(self, client):
        wid = self._setup_word(client)
        res = client.post(
            "/api/feedback",
            json={"word_id": wid, "rating": 4, "comment": "Great word!"},
        )
        assert res.status_code == 200

    def test_feedback_reflected_in_words(self, client):
        wid = self._setup_word(client)
        client.post("/api/feedback",
                    json={"word_id": wid, "rating": 5, "comment": ""})
        words = client.get("/api/words").get_json()
        word = next(w for w in words if w["id"] == wid)
        assert word["avg_rating"] == 5.0
        assert word["feedback_count"] == 1

    def test_feedback_missing_fields(self, client):
        res = client.post("/api/feedback", json={"word_id": 1})
        assert res.status_code == 400

    def test_feedback_invalid_rating(self, client):
        wid = self._setup_word(client)
        res = client.post(
            "/api/feedback",
            json={"word_id": wid, "rating": 10},
        )
        assert res.status_code == 400

    def test_feedback_nonexistent_word(self, client):
        res = client.post(
            "/api/feedback",
            json={"word_id": 9999, "rating": 3},
        )
        assert res.status_code == 404


class TestShareEndpoint:
    def test_share_existing(self, client):
        save_res = client.post(
            "/api/save",
            json={"word": "biology", "root": "bio",
                  "definition": "study of life", "example": "e"},
        )
        wid = save_res.get_json()["id"]
        res = client.get(f"/api/share/{wid}")
        assert res.status_code == 200
        data = res.get_json()
        assert "share_text" in data
        assert "biology"    in data["share_text"]

    def test_share_nonexistent(self, client):
        res = client.get("/api/share/9999")
        assert res.status_code == 404
