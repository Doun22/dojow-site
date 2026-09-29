#!/usr/bin/env python3
"""
Génère les icônes du site : carré noir, « D » blanc (SPEC 7.3).

Sortie :
- favicon.ico (16, 32, 48 px) à la racine, pour les navigateurs et robots qui le demandent
- assets/img/brand/favicon.png (32 px)
- assets/img/brand/apple-touch-icon.png (180 px, écran d'accueil iOS)

Le samouraï du logo est dessiné au trait fin : réduit à 32 px, il devient illisible.
SPEC 7.3 prévoit donc le carré noir avec un « D » blanc en attendant un favicon
dérivé du samouraï, fourni par Stéphane.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
NOIR = (17, 17, 17, 255)
BLANC = (255, 255, 255, 255)

# Police condensée proche de Barlow Condensed, présente sur macOS
POLICES = [
    "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
]


def police(taille: int) -> ImageFont.FreeTypeFont:
    for chemin in POLICES:
        if Path(chemin).exists():
            return ImageFont.truetype(chemin, taille)
    raise SystemExit("Aucune police trouvée parmi : " + ", ".join(POLICES))


def icone(taille: int) -> Image.Image:
    # Dessin en 256 px puis réduction, pour des bords nets
    img = Image.new("RGBA", (256, 256), NOIR)
    dessin = ImageDraw.Draw(img)
    fonte = police(230)
    boite = dessin.textbbox((0, 0), "D", font=fonte)
    x = (256 - (boite[2] - boite[0])) / 2 - boite[0]
    y = (256 - (boite[3] - boite[1])) / 2 - boite[1]
    dessin.text((x, y), "D", font=fonte, fill=BLANC)
    return img if taille == 256 else img.resize((taille, taille), Image.LANCZOS)


def main():
    ico = ROOT / "favicon.ico"
    icone(256).save(ico, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    print("écrit :", ico.name)

    png32 = ROOT / "assets/img/brand/favicon.png"
    icone(32).save(png32, format="PNG", optimize=True)
    print("écrit :", png32.name)

    apple = ROOT / "assets/img/brand/apple-touch-icon.png"
    icone(180).save(apple, format="PNG", optimize=True)
    print("écrit :", apple.name)


if __name__ == "__main__":
    main()
