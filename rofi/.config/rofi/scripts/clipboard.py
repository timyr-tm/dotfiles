#!/usr/bin/env python

import subprocess
import re
import sys
import os
from re import Pattern

def main(*args) -> None:
    print("\0use-hot-keys\x1ftrue")
    retv: int = int(os.environ.get("ROFI_RETV", 0))
    if len(args) > 0:
        if retv == 1:
            subprocess.run(
                ("wl-copy",),
                input=subprocess.run(
                    ("cliphist", "decode", args[0]),
                    capture_output=True
                ).stdout
            )
            return
        if retv == 11:
            subprocess.run(("cliphist", "wipe"))
            return
        if retv == 10:
            subprocess.run(
                ("cliphist", "delete"),
                input=args[0].encode()
            )
        

    icons: dict[Pattern, str] = {
        re.compile(r"text\/.*"): r"󰈚",
        re.compile(r"image\/.*"): r"󰋩",
        re.compile(r".*"): r""
    }
    for line in subprocess.run(("cliphist", "list"), capture_output=True).stdout.decode("utf-8").splitlines():
        key, value = line.split("\t", 1)
        mime: str = subprocess.run(
            ("file", "-b", "--mime-type", "-"),
            input=subprocess.run(
                ("cliphist", "decode", key),
                capture_output=True
            ).stdout,
            capture_output=True
        ).stdout.decode("utf-8").strip()
        icon: str = [icon for pattern, icon in icons.items() if pattern.fullmatch(mime)]
        print(
            f"{key}\0"
            f"display\x1f"
            f"{icon[0]} "
            f"{value}"
        )


if __name__ == "__main__":
    main(*sys.argv[1:])