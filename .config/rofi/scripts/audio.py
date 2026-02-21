#!/usr/bin/env python

import argparse
import subprocess
import sys
import os
import json
import urllib.parse

def parse_args(args) -> argparse.Namespace:
    parser = argparse.ArgumentParser("audio")
    parser.add_argument("type", choices=["sinks", "sources"])
    parser.add_argument("select", nargs="?", default=None)
    return parser.parse_args(args)

def main(*args: str) -> None:
    print("\0use-hot-keys\x1ftrue")
    parsed_args: argparse.Namespace = parse_args(args)
    print(f"\0prompt\x1f{parsed_args.type.title()}")
    if parsed_args.select is not None:
        # noinspection SpellCheckingInspection
        retv: int = int(os.getenv("ROFI_RETV"))
        actions: dict[int, list[str]] = {
            1:  ["pactl", f"set-default-{parsed_args.type[:-1]}", parsed_args.select],
            10: ["pactl", f"set-{parsed_args.type[:-1]}-volume", parsed_args.select, "-5%"],
            11: ["pactl", f"set-{parsed_args.type[:-1]}-volume", parsed_args.select, "-1%"],
            12: ["pactl", f"set-{parsed_args.type[:-1]}-volume", parsed_args.select, "+5%"],
            13: ["pactl", f"set-{parsed_args.type[:-1]}-volume", parsed_args.select, "+1%"],
            14: ["pactl", f"set-{parsed_args.type[:-1]}-mute", parsed_args.select, "toggle"]
        }
        if retv in actions:
            subprocess.run(actions[retv])
    icons: dict[str, tuple[str, str]] = {
        "sinks":   ("󰋋", "󰟎"),
        "sources": ("󰍬", "󰍭")
    }

    # noinspection SpellCheckingInspection
    default: str = subprocess.run(
        ["pactl", f"get-default-{parsed_args.type[:-1]}"],
        capture_output=True,
        text=True
    ).stdout[:-1]

    items: list[dict] = sorted(
        json.loads(
            subprocess.run(
                ["pactl", "-f", "json", "list", parsed_args.type],
                capture_output=True
            ).stdout
        ),
        key=lambda item: (
            item["name"] == default,
            item["mute"],
            item["properties"]["node.nick"]
        ),
        reverse=True
    )
    for index, item in enumerate(items):
        volume: int = round(sum(int(side["value_percent"][:-1]) for side in item["volume"].values()) / len(item["volume"]))
        print(
            f"{item["name"]}\0",
            "display\x1f",
            f"{icons[parsed_args.type][int(item["mute"])]} ",
            f"{item["properties"]["node.nick"][:32]:<32}",
            *(
                chr({0: 0xEE00, 29: 0xEE02}.get(i, 0xEE01) + (3 * int(i < round(volume / 5))))
                for i in range(0, 30)
            ),
            f"{volume:>5}%",
            sep=""
        )


if __name__ == "__main__":
    main(*sys.argv[1:])
