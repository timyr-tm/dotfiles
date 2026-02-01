#!/usr/bin/env python

import os
import sys
import subprocess
import json

icons: list[str] = ["󰕿", "󰖀", "󰕾"]

def label(id: str, name: str, volume: int, muted: bool) -> str:
    return print(
        f"{id!s}\0display\x1f",
        f"{(icons[i] if (i := round((volume / 100) * 3) - 1) >= 0 else icons[0] ) if volume <= 100 else icons[2]} ",
        f"{name:<32}",
        *[chr({1: 0xEE00, 30: 0xEE02}.get(i, 0xEE01) + (3 * int(i < round(volume / 5)))) for i in range(1, 31)],
        f" {volume!s:>4}%",
        sep=""
    )

def main(*args) -> None:
    print("\0use-hot-keys\x1ftrue")

    if len(args) > 0:
        retv: int = int(os.getenv("ROFI_RETV"))
        actions: dict[int, list[str]] = {
            10: ["pactl", "set-sink-volume", args[0], "-5%"],
            11: ["pactl", "set-sink-volume", args[0], "-1%"],
            12: ["pactl", "set-sink-volume", args[0], "+5%"],
            13: ["pactl", "set-sink-volume", args[0], "+1%"]
        }
        subprocess.run(["pactl", "set-default-sink", args[0]])
        if retv in actions:
            subprocess.run(actions[retv])

    current_sink: str = subprocess.run(
        ["pactl", "get-default-sink"],
        capture_output=True,
        text=True
    ).stdout.replace("\n", "")
    
    sinks: list[dict[str, object]] = sorted(
        json.loads(
            subprocess.run(
                ["pactl", "-f", "json", "list", "sinks"],
                capture_output=True
            ).stdout
        ),
        key=lambda sink: [
            sink["name"] != current_sink,
            sink["properties"]["node.nick"]
        ]
    )

    for num, sink in enumerate(sinks):
        label(
            sink["name"],
            sink["properties"]["node.nick"],
            max([int(value["value_percent"][:-1]) for value in sink["volume"].values()]),
            sink["mute"]
        )
        


if __name__ == "__main__":
    main(*sys.argv[1:])