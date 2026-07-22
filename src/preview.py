# -*- coding: utf-8 -*-
"""Rasteriza PDFs para conferência visual e para entrega em 300 dpi."""
import sys, os, fitz

def render(pdf, dpi=100, saida=None, prefixo=None, paginas=None):
    doc = fitz.open(pdf)
    saida = saida or os.path.dirname(pdf)
    os.makedirs(saida, exist_ok=True)
    prefixo = prefixo or os.path.splitext(os.path.basename(pdf))[0]
    feitos = []
    for i, pg in enumerate(doc):
        if paginas and (i + 1) not in paginas:
            continue
        pix = pg.get_pixmap(dpi=dpi, colorspace=fitz.csRGB)
        nome = f"{prefixo}_p{i+1}_{dpi}dpi.png"
        cam = os.path.join(saida, nome)
        pix.save(cam)
        feitos.append((cam, pix.width, pix.height))
    doc.close()
    return feitos

if __name__ == "__main__":
    pdf = sys.argv[1]
    dpi = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    out = sys.argv[3] if len(sys.argv) > 3 else None
    for cam, w, h in render(pdf, dpi, out):
        print(f"{w}x{h}px  {cam}")
