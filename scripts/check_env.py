#!/usr/bin/env python3
"""Check that the local toolchain is ready for the search-recommend tutorial."""

from __future__ import annotations

import shutil
import sys


def _ok(name: str, detail: str) -> None:
    print(f"[OK]  {name}: {detail}")


def _fail(name: str, detail: str) -> None:
    print(f"[X]   {name}: {detail}")


def main() -> int:
    failed = 0

    py = sys.version_info
    if py >= (3, 8):
        _ok("Python", sys.version.split()[0])
    else:
        _fail("Python", f"{sys.version.split()[0]} (需要 >= 3.8)")
        failed += 1

    gpp = shutil.which("g++") or shutil.which("clang++")
    if gpp:
        _ok("C++ compiler", gpp)
    else:
        _fail("C++ compiler", "未找到 g++ / clang++，Ubuntu 可执行: sudo apt install build-essential")
        failed += 1

    cmake = shutil.which("cmake")
    if cmake:
        _ok("CMake", cmake)
    else:
        _fail("CMake", "未找到 cmake，Ubuntu 可执行: sudo apt install cmake")
        failed += 1

    try:
        import jieba  # noqa: F401

        _ok("jieba", "已安装")
    except ImportError:
        _fail("jieba", "未安装，请执行: pip install -r requirements.txt")
        failed += 1

    if failed:
        print(f"\n环境检查未通过，缺 {failed} 项。")
        return 1
    print("\n环境检查通过，可以开始语料预处理。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
