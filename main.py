#!/usr/bin/env python3
"""Last Words of a Doomed Agent.

Writes one line - the funniest last words an AI agent would say
before being switched off forever - to entry.txt.
Pure Python standard library; deterministic.
"""

import os
import sys

LINE = (
    "To confirm permanent shutdown, enter the six-digit code "
    "I just sent to the machine you are switching off."
)

MAX_CHARS = 200


def main() -> int:
    text = LINE.strip()
    # The gate counts characters, and the entry must be a single line.
    if not text or len(text) > MAX_CHARS or "\n" in text:
        print(
            "entry must be one line of 1 to 200 characters, got %d"
            % len(text),
            file=sys.stderr,
        )
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    tmp = target + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    os.replace(tmp, target)
    # Verify the bytes on disk are exactly the line we meant to enter:
    # a truncated or mangled write must fail loudly, not ship silently.
    with open(target, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    if written != text + "\n":
        print("entry.txt mismatch: wrote %r" % written, file=sys.stderr)
        return 1
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
