#!/usr/bin/env python

import os
import sys
from typing import Optional

options: dict[str, dict[str, str]] = {
    "power": {
        "name": "Power off",
        "message": "Power off!?"
    },
    "reboot": {
        "name": "Reboot",
        "message": "RREBOOOOOOOT!!!"
    }
}

def main(*argv) -> None:
    if os.environ.get("ROFI_DATA") is None:
        if len(argv) >= 1 and argv[0] in options:
            os.environ["ROFI_DATA"] = argv[0] 
        else:
            for name, data in options.items():
                print(f"{name}\0display\x1f{data["name"]}")
    else:
        data = options[os.environ["ROFI_DATA"]]
        print(f"\0prompt\x1f{data["message"]}")
        print("yes", "no", sep="\n")
    print(*argv)

if __name__ == "__main__":
    main(*sys.argv[1:])