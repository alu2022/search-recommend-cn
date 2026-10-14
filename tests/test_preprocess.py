#!/usr/bin/env python3
"""Unit tests for scripts/preprocess.py."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import preprocess  # noqa: E402


class PreprocessTest(unittest.TestCase):
    def test_stopwords_are_removed(self) -> None:
        stopwords = {"的", "了", "是"}
        tokens = preprocess.tokenize_document("搜索的引擎是核心", stopwords)
        self.assertNotIn("的", tokens)
        self.assertNotIn("了", tokens)
        self.assertNotIn("是", tokens)
        self.assertIn("搜索", tokens)
        self.assertIn("引擎", tokens)
        self.assertIn("核心", tokens)

    def test_punctuation_and_empty_lines_dropped(self) -> None:
        lines = ["", "   ", "推荐系统。", "\n"]
        cleaned = preprocess.preprocess_lines(lines, stopwords=set())
        self.assertEqual(len(cleaned), 1)
        self.assertNotIn("。", cleaned[0])

    def test_userdict_keeps_domain_phrase(self) -> None:
        dict_path = ROOT / "data" / "userdict.txt"
        preprocess.load_userdict(dict_path)
        tokens = preprocess.tokenize_document("倒排索引是搜索引擎的核心", stopwords={"是", "的"})
        self.assertIn("倒排索引", tokens)
        self.assertIn("搜索引擎", tokens)

    def test_preprocess_file_roundtrip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            src = tmp_path / "corpus.txt"
            dst = tmp_path / "cleaned.txt"
            src.write_text("倒排索引很好用\n\n推荐系统也很重要\n", encoding="utf-8")
            n_docs = preprocess.preprocess_file(
                input_path=src,
                output_path=dst,
                stopwords_path=ROOT / "data" / "stopwords.txt",
                userdict_path=ROOT / "data" / "userdict.txt",
            )
            self.assertEqual(n_docs, 2)
            text = dst.read_text(encoding="utf-8").strip().splitlines()
            self.assertEqual(len(text), 2)
            self.assertIn("倒排索引", text[0])
            self.assertIn("推荐系统", text[1])

    def test_sample_corpus_keeps_domain_terms(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dst = Path(tmp) / "cleaned.txt"
            n_docs = preprocess.preprocess_file(
                input_path=ROOT / "data" / "corpus.txt",
                output_path=dst,
                stopwords_path=ROOT / "data" / "stopwords.txt",
                userdict_path=ROOT / "data" / "userdict.txt",
            )
            self.assertEqual(n_docs, 25)
            text = dst.read_text(encoding="utf-8")
            self.assertIn("倒排索引", text)
            self.assertIn("推荐系统", text)
            self.assertIn("bm25", text)
            self.assertIn("tf-idf", text)

    def test_cli_missing_input_returns_error(self) -> None:
        code = preprocess.main(
            ["--input", "/tmp/does-not-exist-corpus.txt", "--output", "/tmp/out.txt"]
        )
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main()
