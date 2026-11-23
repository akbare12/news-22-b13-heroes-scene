#!/usr/bin/env python3
"""Reproduce entry.png byte-identically.

This is a copy program using only the Python standard library: it copies
entry.png (the front page drawn by draw.py) to entry-copy.png and verifies
the copy against the known SHA-256 of the submitted image.

Usage:
    python3 main.py
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST = os.path.join(HERE, "entry-copy.png")
EXPECTED_SHA256 = "4705981e20fb04ddf62f26b978cd836afd75f8752240382766400e804e9e2a04"
EXPECTED_SIZE = (1024, 1024)


def png_size(path):
    """Read width/height from a PNG IHDR chunk (stdlib only)."""
    with open(path, "rb") as handle:
        header = handle.read(33)
    if header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file: " + path)
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    if not os.path.exists(SRC):
        print("missing entry.png next to main.py", file=sys.stderr)
        return 1
    shutil.copyfile(SRC, DST)
    size = png_size(DST)
    print("dimensions:", size)
    if size != EXPECTED_SIZE:
        print("MISMATCH: expected dimensions", EXPECTED_SIZE, file=sys.stderr)
        return 1
    got = sha256(DST)
    print("sha256:", got)
    if got != EXPECTED_SHA256:
        print("MISMATCH: expected", EXPECTED_SHA256, file=sys.stderr)
        return 1
    print("OK: entry-copy.png is byte-identical to entry.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
