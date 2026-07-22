# -*- coding: utf-8 -*-
"""Rasteriza as peças para uso na web e escolhe o menor formato (PNG-256 vs JPEG)."""
import os, io, base64, fitz
from PIL import Image

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (chave, pdf relativo, pagina 1-based, largura alvo em px)
FIGURAS = [
    ("tab_frente", "01-TABULEIRO/TABULEIRO_400x300_SANGRIA-3mm.pdf", 1, 1500),
    ("tab_verso",  "01-TABULEIRO/TABULEIRO_400x300_SANGRIA-3mm.pdf", 2, 1100),
    ("cx_tampa",   "02-CAIXA/CAIXA-TAMPA_267x367_faca.pdf",          1,  760),
    ("cx_fundo",   "02-CAIXA/CAIXA-FUNDO_259x359_faca.pdf",          1,  760),
    ("cartela",    "03-PECAS/CARTELA-PECAS_200x280_sangria-3mm.pdf", 1,  700),
    ("dado",       "03-PECAS/DADO-MONTAVEL_100x90_sangria-3mm.pdf",  1,  620),
    ("envelope",   "03-PECAS/ENVELOPE-SELADO_108x305_faca.pdf",      1,  420),
    ("verso_jogo",   "03-PECAS/CARTAS_VERSOS_70x120_sangria-3mm.pdf", 1,  300),
    ("verso_selado", "03-PECAS/CARTAS_VERSOS_70x120_sangria-3mm.pdf", 60, 300),
]


def _rasterizar(pdf, pagina, larg_px):
    doc = fitz.open(pdf)
    pg = doc[pagina - 1]
    zoom = larg_px / (pg.rect.width / 72.0 * 96.0)
    pix = pg.get_pixmap(matrix=fitz.Matrix(zoom * 96 / 72, zoom * 96 / 72),
                        colorspace=fitz.csRGB)
    img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
    doc.close()
    if img.width != larg_px:
        img = img.resize((larg_px, round(img.height * larg_px / img.width)),
                         Image.LANCZOS)
    return img


def _menor(img):
    """Devolve (bytes, mime). Arte chapada costuma ficar menor em PNG paletizado."""
    b_png = io.BytesIO()
    img.convert("P", palette=Image.ADAPTIVE, colors=200).save(
        b_png, "PNG", optimize=True)
    b_jpg = io.BytesIO()
    img.save(b_jpg, "JPEG", quality=82, optimize=True, progressive=True)
    if b_png.tell() <= b_jpg.tell():
        return b_png.getvalue(), "image/png"
    return b_jpg.getvalue(), "image/jpeg"


def gerar():
    saida = {}
    total = 0
    for chave, rel, pagina, larg in FIGURAS:
        img = _rasterizar(os.path.join(RAIZ, rel.replace("/", os.sep)), pagina, larg)
        dados, mime = _menor(img)
        total += len(dados)
        saida[chave] = {
            "uri": f"data:{mime};base64,{base64.b64encode(dados).decode()}",
            "w": img.width, "h": img.height,
        }
        print(f"  {chave:14s} {img.width}x{img.height}  {len(dados)/1024:7.0f} KB  {mime}")
    print(f"  {'TOTAL':14s} {'':13s} {total/1024:7.0f} KB")
    return saida


def em_arquivos(destino):
    """Grava as mesmas imagens como PNG/JPEG em disco (para o README do GitHub)."""
    os.makedirs(destino, exist_ok=True)
    for chave, rel, pagina, larg in FIGURAS:
        img = _rasterizar(os.path.join(RAIZ, rel.replace("/", os.sep)), pagina, larg)
        dados, mime = _menor(img)
        ext = ".png" if mime == "image/png" else ".jpg"
        cam = os.path.join(destino, chave + ext)
        with open(cam, "wb") as f:
            f.write(dados)
        print(f"  {os.path.basename(cam):20s} {img.width}x{img.height}  "
              f"{len(dados)/1024:6.0f} KB")


if __name__ == "__main__":
    import sys
    if "--arquivos" in sys.argv:
        em_arquivos(os.path.join(RAIZ, "docs", "img"))
    else:
        gerar()
