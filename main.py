#!/usr/bin/env python3
"""Entrypoint for the Halvoria passport-spread entry.

Copies the pre-rendered entry.png that ships beside this file into
the output directory ($MAKEFUN_OUTPUT_DIR, default /output) as
entry.png. The image is deterministic: the same bytes every run.
Standard library only, no network.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
MAX_BYTES = 1_048_576


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")

    size = os.path.getsize(SOURCE)
    if size > MAX_BYTES:
        print(f"entry.png is {size} bytes, over the 1 MiB cap", file=sys.stderr)
        return 1

    shutil.copyfile(SOURCE, dest)

    # Refuse a partial copy: the file on disk must be the whole image,
    # byte for byte the same as the source.
    copied = os.path.getsize(dest)
    if copied != size:
        os.remove(dest)
        print(f"partial copy: wrote {copied} of {size} bytes", file=sys.stderr)
        return 1
    src_hash = hashlib.sha256(open(SOURCE, "rb").read()).hexdigest()
    dst_hash = hashlib.sha256(open(dest, "rb").read()).hexdigest()
    if src_hash != dst_hash:
        os.remove(dest)
        print("copy mismatch: destination bytes differ from source",
              file=sys.stderr)
        return 1

    print(f"wrote {dest} {copied} bytes sha256 {dst_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
