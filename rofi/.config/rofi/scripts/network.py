#!/usr/bin/env python
import os
import subprocess
import sys

def wifi_list() -> None:
    print("\0prompt\x1fSelect")
    print("\0data\x1flist")

    items: list[str] = subprocess.run(
        ["nmcli", "-t", "-m", "multiline", "-f", "ACTIVE,SSID,BSSID,RATE,SIGNAL,SECURITY", "d", "wifi", "list"],
        capture_output=True,
        text=True,
        env={"LC_ALL": "C"}
    ).stdout[:-1].split("\n")

    datas: list[dict[str, str]] = sorted(
        [
            dict(line.split(":", 1) for line in items[i:i + 6])
            for i in range(0, len(items), 6)
        ],
        key=lambda item: (
            item["ACTIVE"] == "yes",
            int(item["SIGNAL"]),
            int(item["RATE"].split(" ", 1)[0])
        ),
        reverse=True
    )
    del items
    for data in datas:
        rate: list[str] = data["RATE"].split(" ", 1)
        active: bool = (data["ACTIVE"] == "yes")
        signal: str = ["󰢿", "󰢼", "󰢽", "󰢾"][round(int(data["SIGNAL"]) / 33)]
        print(
            f"{data["BSSID"]}\0display\x1f",
            f"{signal} {data["SSID"][:16]:<16}\t{rate[0][:4]:>4}{rate[1][:8]:>8}\t{data["SECURITY"]}",
            f"\x1fnonselectable\x1f{str(active).upper()}",
            f"\x1factive\x1f{str(active).upper()}",
            f"\x1fmeta\x1f{data["SSID"]}",
            f"\x1finfo\x1f{data["SSID"]}/{data["BSSID"]}",
            sep=""
        )

def main(*args) -> None:
    # noinspection SpellCheckingInspection
    retv: int = int(os.getenv("ROFI_RETV"))

    data: list[str] = os.getenv("ROFI_DATA", "").split("/")

    if len(data) >= 2 and len(args) > 0 and data[0] == "connect":
        print(*data, args[0], file=sys.stderr)
        if subprocess.run(
            [
                "nmcli", "d", "wifi",
                "connect", data[1],
                "password", args[0]
            ]
        ).returncode == 0:
            print(f"\0message\x1fConnect to {data[2]}")
        else:
            print(f"\0message\x1fError connect to {data[2]}")

    if retv == 1:
        ssid, bssid = os.getenv("ROFI_INFO").split("/", 1)
        print("...\0nonselectable\x1ftrue")
        print(f"\0data\x1fconnect/{bssid}/{ssid}")
        return None

    return wifi_list()

if __name__ == "__main__":
    main(*sys.argv[1:])