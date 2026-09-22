#!/usr/bin/env python3
"""
Téléchargement des polices auto-hébergées (SPEC.md section 5.2), via Fontsource.
- Barlow Condensed 700 (latin)
- Inter 400 (latin)
- Inter 600 (latin)

Le sous-ensemble « latin » couvre l'ASCII et les accents français (é, è, à, ç, œ...).
Script à lancer une seule fois, les fichiers .woff2 sont ensuite commités.
"""

import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
FONTS_DIR = ROOT_DIR / "assets" / "fonts"
FONTS_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://cdn.jsdelivr.net/fontsource/fonts"

FONTS = [
    ("barlow-condensed", 700, "barlow-condensed-700.woff2"),
    ("inter", 400, "inter-400.woff2"),
    ("inter", 600, "inter-600.woff2"),
]


def download_font(family: str, weight: int, filename: str):
    url = f"{BASE_URL}/{family}@latest/latin-{weight}-normal.woff2"
    target = FONTS_DIR / filename
    print(f"Téléchargement : {url}")
    with urllib.request.urlopen(url) as resp:
        data = resp.read()
    if data[:4] != b"wOF2":
        raise RuntimeError(f"{filename} : le fichier reçu n'est pas un woff2")
    target.write_bytes(data)
    print(f"OK : {filename} ({len(data)} octets)")


def main():
    for family, weight, filename in FONTS:
        download_font(family, weight, filename)
    print("Toutes les polices ont été téléchargées.")


if __name__ == "__main__":
    main()
