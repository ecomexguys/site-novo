#!/usr/bin/env python3
"""Monta as imagens do site a partir dos prints do portal, no mesmo padrao visual
das capturas que o designer usou (mockup de notebook no hero, moldura laranja no meio)."""
from PIL import Image, ImageDraw

IMG = "/Users/nicolasrocha/Library/CloudStorage/OneDrive-CommexTech/Marketing - Documentos/Site Institucional/site-novo/assets/img"
LARANJA = (255, 89, 5, 255)

def hero(print_png, saida):
    """Encaixa o print na tela do mockup de notebook (mesmo mockup dos outros modulos)."""
    base = Image.open(f"{IMG}/Duimp-1.png").convert("RGBA")
    tela = (105, 65, 895, 556)                      # area util da tela, medida no mockup
    w, h = tela[2] - tela[0], tela[3] - tela[1]
    shot = Image.open(print_png).convert("RGBA").resize((w, h), Image.LANCZOS)
    base.paste(shot, (tela[0], tela[1]), shot)
    base.save(saida)
    print("hero:", saida, base.size)

def moldura(print_png, saida, raio=18, borda=13):
    """Moldura laranja arredondada, como em tela-DUIMP.png."""
    shot = Image.open(print_png).convert("RGBA")
    w, h = shot.size
    out = Image.new("RGBA", (w + 2 * borda, h + 2 * borda), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)
    d.rounded_rectangle([0, 0, out.width - 1, out.height - 1], radius=raio + borda, fill=LARANJA)
    # recorta o print com cantos arredondados
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=raio, fill=255)
    out.paste(shot, (borda, borda), mask)
    out.save(saida)
    print("moldura:", saida, out.size)

hero("ex-sugestoes.png", f"{IMG}/ex-tarifario.png")
moldura("ex-falta.png", f"{IMG}/Tela-ex-tarifario.png")
