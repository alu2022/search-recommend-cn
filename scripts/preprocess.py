#!/usr/bin/env python3
"""Chinese corpus preprocessing: jieba tokenization + stopword removal.

Each non-empty input line is one document. Output is one tokenized document
per line, tokens separated by spaces.

Example:
    python scripts/preprocess.py --input data/corpus.txt --output data/corpus_cleaned.txt
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import jieba
except ImportError as exc:  # pragma: no cover - env issue, not logic
    raise SystemExit(
        "未安装 jieba。请先执行: pip install -r requirements.txt"
    ) from exc

# CJK / ASCII punctuation that should not become tokens.
_PUNCTUATION = set(
    "，。！？、；：""\"''‘’（）【】《》〈〉—…·,.!?;:()[]{}<>"
    "`~@#$%^&*-_=+|\\/"
)
_PUNCT_RE = re.compile(r"^[\s]+$")
_ASCII_WORD_RE = re.compile(r"^[A-Za-z0-9]+$")


def load_stopwords(path: Path | None) -> set[str]:
    if path is None or not path.exists():
        return set()
    words: set[str] = set()
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            word = line.strip()
            if word and not word.startswith("#"):
                words.add(word)
    return words


def load_userdict(path: Path | None) -> None:
    if path is None or not path.exists():
        return
    jieba.load_userdict(str(path))


def is_useful_token(token: str, stopwords: set[str]) -> bool:
    token = token.strip()
    if not token or token in stopwords:
        return False
    if _PUNCT_RE.match(token):
        return False
    if all(ch in _PUNCTUATION for ch in token):
        return False
    return True


def tokenize_document(text: str, stopwords: set[str]) -> list[str]:
    text = text.strip()
    if not text:
        return []
    tokens: list[str] = []
    for raw in jieba.lcut(text, cut_all=False):
        token = raw.strip()
        if _ASCII_WORD_RE.match(token):
            token = token.lower()
        if is_useful_token(token, stopwords):
            tokens.append(token)
    return tokens


def preprocess_lines(
    lines: list[str],
    stopwords: set[str],
) -> list[str]:
    output: list[str] = []
    for line in lines:
        tokens = tokenize_document(line, stopwords)
        if tokens:
            output.append(" ".join(tokens))
    return output


def preprocess_file(
    input_path: Path,
    output_path: Path,
    stopwords_path: Path | None = None,
    userdict_path: Path | None = None,
) -> int:
    load_userdict(userdict_path)
    stopwords = load_stopwords(stopwords_path)
    with input_path.open("r", encoding="utf-8") as handle:
        lines = handle.readlines()
    cleaned = preprocess_lines(lines, stopwords)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        handle.write("\n".join(cleaned))
        if cleaned:
            handle.write("\n")
    return len(cleaned)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="中文语料预处理：jieba 分词、去停用词、可选自定义词典",
    )
    parser.add_argument("--input", required=True, help="输入语料路径（每行一篇）")
    parser.add_argument("--output", required=True, help="分词后输出路径")
    parser.add_argument(
        "--stopwords",
        default="data/stopwords.txt",
        help="停用词文件（默认 data/stopwords.txt）",
    )
    parser.add_argument(
        "--userdict",
        default="data/userdict.txt",
        help="jieba 自定义词典（默认 data/userdict.txt）",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"输入文件不存在: {input_path}", file=sys.stderr)
        return 1
    n_docs = preprocess_file(
        input_path=input_path,
        output_path=Path(args.output),
        stopwords_path=Path(args.stopwords) if args.stopwords else None,
        userdict_path=Path(args.userdict) if args.userdict else None,
    )
    print(f"预处理完成: {n_docs} 篇文档 -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
