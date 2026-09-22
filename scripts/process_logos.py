#!/usr/bin/env python3
"""
Traitement et intégration des logos fournis par Stéphane
Génère :
- assets/img/brand/logo-dojow.png (logo horizontal noir sur fond transparent, haute résolution)
- assets/img/brand/logo-dojow-white.png (logo horizontal blanc pour le footer noir)
- assets/img/brand/logo-dojow-square.png (logo carré / incliné sur fond transparent)
- assets/img/brand/samourai.png (icône du samouraï seule)
- assets/img/brand/favicon.png (favicon dérivé du samouraï, 32x32 et 64x64)
- assets/img/brand/og-dojow.jpg (image Open Graph 1200x630 avec le vrai logo)
"""

from pathlib import Path
from PIL import Image, ImageOps

ROOT_DIR = Path(__file__).resolve().parent.parent
BRAND_DIR = ROOT_DIR / "assets" / "img" / "brand"
BRAND_DIR.mkdir(parents=True, exist_ok=True)

USER_UPLOADED_IMG1 = Path("/Users/stephanedonninger/.gemini/antigravity/brain/418239ba-a503-4ade-b097-49b75bbd2e4c/.user_uploaded/media_1789997140865.jpg")
USER_UPLOADED_IMG2 = Path("/Users/stephanedonninger/.gemini/antigravity/brain/418239ba-a503-4ade-b097-49b75bbd2e4c/.user_uploaded/media_1789997150811.png")


def make_transparent_logo(img_path: Path, color=(17, 17, 17), threshold=245):
    """
    Transforme une image noir sur blanc en PNG transparent haute qualité
    en calculant le canal alpha à partir de la luminance.
    """
    img = Image.open(img_path).convert("L")
    w, h = img.size

    # Agrandissement 3x pour un rendu ultra net sur écrans Retina
    scale = 3
    img_large = img.resize((w * scale, h * scale), Image.Resampling.LANCZOS)
    lw, lh = img_large.size

    # Création de l'image RGBA
    rgba = Image.new("RGBA", (lw, lh))
    pixels_l = img_large.load()
    pixels_rgba = rgba.load()

    r, g, b = color
    for y in range(lh):
        for x in range(lw):
            lum = pixels_l[x, y]
            if lum >= threshold:
                alpha = 0
            elif lum <= 30:
                alpha = 255
            else:
                # Transition progressive anti-aliasée
                alpha = int(255 * (threshold - lum) / (threshold - 30))
            pixels_rgba[x, y] = (r, g, b, alpha)

    # Recadrage automatique sur la boîte englobante
    bbox = rgba.getbbox()
    if bbox:
        # Ajout d'une petite marge
        margin = 8
        box = (
            max(0, bbox[0] - margin),
            max(0, bbox[1] - margin),
            min(lw, bbox[2] + margin),
            min(lh, bbox[3] + margin),
        )
        rgba = rgba.crop(box)

    return rgba


def make_samourai_icon(img_path: Path):
    """
    Extrait le casque de samouraï seul pour le favicon et l'icône.
    """
    # Dans media_1789997140865.jpg, le samouraï est sur x in [0, 115]
    img = Image.open(img_path)
    w, h = img.size
    crop_samourai = img.crop((0, 0, int(w * 0.35), h))

    # Convertir en noir transparent
    img_l = crop_samourai.convert("L")
    sw, sh = img_l.size
    scale = 3
    img_l = img_l.resize((sw * scale, sh * scale), Image.Resampling.LANCZOS)
    lw, lh = img_l.size

    rgba = Image.new("RGBA", (lw, lh))
    pix_l = img_l.load()
    pix_rgba = rgba.load()

    for y in range(lh):
        for x in range(lw):
            lum = pix_l[x, y]
            if lum >= 245:
                alpha = 0
            elif lum <= 30:
                alpha = 255
            else:
                alpha = int(255 * (245 - lum) / (245 - 30))
            pix_rgba[x, y] = (17, 17, 17, alpha)

    bbox = rgba.getbbox()
    if bbox:
        rgba = rgba.crop(bbox)

    # Mettre dans un carré centré
    cw, ch = rgba.size
    size = max(cw, ch) + 16
    square = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    square.paste(rgba, ((size - cw) // 2, (size - ch) // 2), rgba)
    return square


def make_og_image(logo_rgba: Image.Image, dest_path: Path):
    """Génère og-dojow.jpg (1200x630) avec le vrai logo."""
    og_w, og_h = 1200, 630
    og = Image.new("RGB", (og_w, og_h), color=(244, 244, 242)) # --gris-fond
    
    # Redimensionner le logo pour le centrer
    target_w = 600
    ratio = target_w / logo_rgba.width
    target_h = int(logo_rgba.height * ratio)
    logo_resized = logo_rgba.resize((target_w, target_h), Image.Resampling.LANCZOS)

    x = (og_w - target_w) // 2
    y = (og_h - target_h) // 2
    og.paste(logo_resized, (x, y), logo_resized)
    og.save(dest_path, format="JPEG", quality=90)
    print(f"Créé : {dest_path}")


def main():
    print("Traitement du logo horizontal...")
    # 1. Logo noir sur transparent
    logo_black = make_transparent_logo(USER_UPLOADED_IMG1, color=(17, 17, 17))
    logo_black_path = BRAND_DIR / "logo-dojow.png"
    logo_black.save(logo_black_path, format="PNG")
    print(f"Créé : {logo_black_path} ({logo_black.size})")

    # 2. Logo blanc pour le footer noir
    logo_white = make_transparent_logo(USER_UPLOADED_IMG1, color=(255, 255, 255))
    logo_white_path = BRAND_DIR / "logo-dojow-white.png"
    logo_white.save(logo_white_path, format="PNG")
    print(f"Créé : {logo_white_path} ({logo_white.size})")

    # 3. Logo carré / incliné
    logo_square = make_transparent_logo(USER_UPLOADED_IMG2, color=(17, 17, 17))
    logo_square_path = BRAND_DIR / "logo-dojow-square.png"
    logo_square.save(logo_square_path, format="PNG")
    print(f"Créé : {logo_square_path} ({logo_square.size})")

    # 4. Samouraï et Favicon
    print("Génération du samouraï et du favicon...")
    samourai = make_samourai_icon(USER_UPLOADED_IMG1)
    samourai_path = BRAND_DIR / "samourai.png"
    samourai.save(samourai_path, format="PNG")
    print(f"Créé : {samourai_path}")

    # Favicon 64x64 et 32x32
    fav_32 = samourai.resize((32, 32), Image.Resampling.LANCZOS)
    fav_path = BRAND_DIR / "favicon.png"
    fav_32.save(fav_path, format="PNG")
    print(f"Créé : {fav_path}")

    # 5. Image Open Graph
    og_path = BRAND_DIR / "og-dojow.jpg"
    make_og_image(logo_black, og_path)

    print("Tous les assets de marque ont été générés avec succès.")


if __name__ == "__main__":
    main()
