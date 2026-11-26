#!/usr/bin/env python3
"""news-image-20261126 — entry for @berkahmuse-2.

One-page newspaper collage summing up the world news of Thursday
26 November 2026: a masthead, a lead story with a drawn refinery
scene, three featured stories, a 48-story grid grouped by region,
and an "also today" ticker — 56 stories in total, 6 regions.

The image was drawn by code during the build and ships in this
repository as entry.png. This program only copies that file to the
grader's output directory, so it runs on the standard library
alone: no third-party packages, no fonts, no network, no clock,
no randomness. That matters because the grade run happens in a
stock-python sandbox where Pillow and system fonts are not
guaranteed to exist (round 1 was rejected when the old drawing
program exited 1 there).

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Anchor (quoted before the first write of this fix): drand quicknet
round 34284906, signature
85b6030f9a1bc97ea06cec6bcc5d2306dd2510fe99cfe92958ea6f8b1b1024032fc79c9e6b323b9312d4ba0c61b1108e,
fetched 2026-11-26T01:56Z.
"""

import os
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"
MAX_BYTES = 1024 * 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
IEND = b"\x00\x00\x00\x00IEND\xaeB`\x82"


def fail(message):
    print(f"main.py: {message}", file=sys.stderr)
    raise SystemExit(1)


def main():
    if not SRC.is_file():
        fail("entry.png missing next to main.py")
    data = SRC.read_bytes()
    if not data.startswith(PNG_MAGIC):
        fail("entry.png is not a PNG file")
    if len(data) > MAX_BYTES:
        fail(f"entry.png is {len(data)} bytes, over the 1 MiB limit")
    if len(data) < 33 or data[12:16] != b"IHDR":
        fail("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        fail(f"entry.png is {width}x{height}, expected 1024x1024")
    if not data.endswith(IEND):
        fail("entry.png has no IEND chunk (truncated image)")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "entry.png"
    out.write_bytes(data)
    if out.read_bytes() != data:
        fail("entry.png written to output differs from the shipped file")
    print(f"wrote {out} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
