#!/usr/bin/env python3
"""
Générateur de placeholders pour le site Dojow (dojow.fr)
Génère les images unies #D9D9D6 avec texte centré #555555 (section 7 de SPEC.md).

Usage :
  python3 scripts/generate_placeholders.py          crée uniquement les fichiers absents
  python3 scripts/generate_placeholders.py --force  régénère les 10 placeholders du lieu

Les fichiers de marque (logo, favicon, image OG) ne sont jamais écrasés s'ils existent :
ils proviennent des fichiers fournis par Stéphane (voir scripts/process_logos.py).
Une photo réelle déposée à la place d'un placeholder n'est pas écrasée sans --force.
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT_DIR = Path(__file__).resolve().parent.parent

# Définition des images selon le tableau 7.2 de SPEC.md
IMAGES_LIEU = [
    {
        "code": "IMG-01",
        "file": "assets/img/lieu/img-01-open-space.webp",
        "width": 1600,
        "height": 900,
        "subject": "Open space, lumière naturelle",
        "format": "WEBP",
    },
    {
        "code": "IMG-02",
        "file": "assets/img/lieu/img-02-salle-reunion.webp",
        "width": 1200,
        "height": 900,
        "subject": "Salle de réunion, table et écran",
        "format": "WEBP",
    },
    {
        "code": "IMG-03",
        "file": "assets/img/lieu/img-03-coin-cafe.webp",
        "width": 1200,
        "height": 900,
        "subject": "Coin café, machine et mugs",
        "format": "WEBP",
    },
    {
        "code": "IMG-04",
        "file": "assets/img/lieu/img-04-entree.webp",
        "width": 1200,
        "height": 900,
        "subject": "Entrée ou façade du 23 rue Claudot",
        "format": "WEBP",
    },
    {
        "code": "IMG-05",
        "file": "assets/img/lieu/img-05-poste.webp",
        "width": 1200,
        "height": 900,
        "subject": "Un poste de travail en détail",
        "format": "WEBP",
    },
    {
        "code": "IMG-06",
        "file": "assets/img/lieu/img-06-open-space-2.webp",
        "width": 1600,
        "height": 900,
        "subject": "Open space, second angle",
        "format": "WEBP",
    },
    {
        "code": "IMG-07",
        "file": "assets/img/lieu/img-07-equipe.webp",
        "width": 1200,
        "height": 900,
        "subject": "2 ou 3 postes côte à côte occupés",
        "format": "WEBP",
    },
    {
        "code": "IMG-08",
        "file": "assets/img/lieu/img-08-stephane.webp",
        "width": 900,
        "height": 1200,
        "subject": "Portrait de Stéphane dans le lieu",
        "format": "WEBP",
    },
    {
        "code": "IMG-09",
        "file": "assets/img/lieu/img-09-acces-badge.webp",
        "width": 1200,
        "height": 900,
        "subject": "Porte d'entrée avec lecteur de badge",
        "format": "WEBP",
    },
    {
        "code": "IMG-10",
        "file": "assets/img/lieu/img-10-quartier.webp",
        "width": 1600,
        "height": 900,
        "subject": "La rue ou les abords (parc de la Pépinière)",
        "format": "WEBP",
    },
]

BRAND_IMAGES = [
    {
        "code": "LOGO",
        "file": "assets/img/brand/logo-dojow.png",
        "width": 480,
        "height": 120,
        "subject": "Dojow · Coworking Nancy",
        "format": "PNG",
        "is_logo": True,
    },
    {
        "code": "OG",
        "file": "assets/img/brand/og-dojow.jpg",
        "width": 1200,
        "height": 630,
        "subject": "Dojow · Coworking à Nancy",
        "format": "JPEG",
    },
    {
        "code": "FAVICON",
        "file": "assets/img/brand/favicon.png",
        "width": 32,
        "height": 32,
        "subject": "D",
        "format": "PNG",
        "is_favicon": True,
    },
]

BG_COLOR = (217, 217, 214)     # #D9D9D6
TEXT_COLOR = (85, 85, 85)       # #555555
WHITE = (255, 255, 255)
BLACK = (17, 17, 17)            # #111111


def get_font(size: int):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def generate_favicon(dest_path: Path):
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGBA", (32, 32), color=(17, 17, 17, 255))
    draw = ImageDraw.Draw(img)
    font = get_font(22)
    bbox = draw.textbbox((0, 0), "D", font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (32 - text_w) / 2 - bbox[0]
    y = (32 - text_h) / 2 - bbox[1]
    draw.text((x, y), "D", fill=(255, 255, 255, 255), font=font)
    img.save(dest_path, format="PNG")
    print(f"Créé : {dest_path}")


def generate_logo(dest_path: Path, width: int, height: int):
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGBA", (width, height), color=(255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Wordmark DOJOW sobre et rigoureux
    font_main = get_font(44)
    font_sub = get_font(16)

    title = "DOJOW"
    sub = "COWORKING NANCY"

    bbox_t = draw.textbbox((0, 0), title, font=font_main)
    w_t = bbox_t[2] - bbox_t[0]
    h_t = bbox_t[3] - bbox_t[1]

    bbox_s = draw.textbbox((0, 0), sub, font=font_sub)
    w_s = bbox_s[2] - bbox_s[0]
    h_s = bbox_s[3] - bbox_s[1]

    gap = 8
    total_h = h_t + gap + h_s

    start_y = (height - total_h) / 2 - bbox_t[1]
    x_t = (width - w_t) / 2 - bbox_t[0]
    draw.text((x_t, start_y), title, fill=BLACK, font=font_main)

    start_y_s = start_y + h_t + gap + (bbox_t[1] - bbox_s[1])
    x_s = (width - w_s) / 2 - bbox_s[0]
    draw.text((x_s, start_y_s), sub, fill=TEXT_COLOR, font=font_sub)

    # Filet fin de séparation
    draw.rectangle([0, height - 1, width, height], fill=(218, 218, 214))

    img.save(dest_path, format="PNG")
    print(f"Créé : {dest_path}")


def generate_standard_placeholder(item: dict):
    dest_path = ROOT_DIR / item["file"]
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    w = item["width"]
    h = item["height"]
    fmt = item["format"]

    img = Image.new("RGB", (w, h), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Filet discret intérieur de 1px
    draw.rectangle([0, 0, w - 1, h - 1], outline=(210, 210, 206), width=1)

    # Tailles de polices proportionnelles
    font_size_1 = max(18, min(36, w // 38))
    font_size_2 = max(14, min(24, w // 52))

    font_title = get_font(font_size_1)
    font_meta = get_font(font_size_2)

    line1 = f"{item['code']} · {item['subject']}"
    line2 = f"{w} x {h} px"

    bbox1 = draw.textbbox((0, 0), line1, font=font_title)
    w1 = bbox1[2] - bbox1[0]
    h1 = bbox1[3] - bbox1[1]

    bbox2 = draw.textbbox((0, 0), line2, font=font_meta)
    w2 = bbox2[2] - bbox2[0]
    h2 = bbox2[3] - bbox2[1]

    gap = int(font_size_1 * 0.6)
    total_h = h1 + gap + h2

    start_y = (h - total_h) / 2 - bbox1[1]
    x1 = (w - w1) / 2 - bbox1[0]
    x2 = (w - w2) / 2 - bbox2[0]

    draw.text((x1, start_y), line1, fill=TEXT_COLOR, font=font_title)
    draw.text((x2, start_y + h1 + gap + (bbox1[1] - bbox2[1])), line2, fill=(110, 110, 110), font=font_meta)

    save_kwargs = {}
    if fmt == "WEBP":
        save_kwargs = {"quality": 80, "method": 6}
    elif fmt == "JPEG":
        save_kwargs = {"quality": 85}

    img.save(dest_path, format=fmt, **save_kwargs)
    print(f"Créé : {dest_path} ({w}x{h}, {fmt})")


def main():
    force = "--force" in sys.argv[1:]

    print("Images du lieu...")
    for item in IMAGES_LIEU:
        if (ROOT_DIR / item["file"]).exists() and not force:
            print(f"Déjà présent, conservé : {item['file']}")
            continue
        generate_standard_placeholder(item)

    print("\nÉléments de marque...")
    for item in BRAND_IMAGES:
        dest_path = ROOT_DIR / item["file"]
        if dest_path.exists():
            print(f"Déjà présent, conservé : {item['file']}")
            continue
        if item.get("is_favicon"):
            generate_favicon(dest_path)
        elif item.get("is_logo"):
            generate_logo(dest_path, item["width"], item["height"])
        else:
            generate_standard_placeholder(item)

    print("\nTerminé.")


if __name__ == "__main__":
    main()
