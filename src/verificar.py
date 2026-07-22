# -*- coding: utf-8 -*-
"""
Verificação de pré-impressão do TABULEIRO.
Lê o PDF gerado e confere, palavra por palavra, se algum texto invade a
ZONA MORTA DO VINCO (200 mm ± 7 mm). É o requisito crítico do projeto.
"""
import os, sys, fitz

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PT = 72.0 / 25.4

TRIM_W, TRIM_H = 400.0, 300.0
SANGRIA = 3.0
DOBRA = 200.0
ZONA = 7.0


def verificar(pdf):
    doc = fitz.open(pdf)
    # margem da página até o trim: (largura_pagina - trim) / 2
    marg = (doc[0].rect.width / PT - TRIM_W) / 2.0
    z0 = (marg + DOBRA - ZONA) * PT
    z1 = (marg + DOBRA + ZONA) * PT
    print(f"{os.path.basename(pdf)}")
    print(f"  pagina {doc[0].rect.width/PT:.1f} x {doc[0].rect.height/PT:.1f} mm  "
          f"| margem ate o trim: {marg:.1f} mm")
    print(f"  zona morta do vinco: x de {z0/PT - marg:.1f} a {z1/PT - marg:.1f} mm "
          f"(coords do trim)")
    # só interessa o que está DENTRO da área de corte: as marcas de impressão
    # (inclusive o rótulo "VINCO") vivem fora do trim e não são impressas na peça.
    ty0, ty1 = marg * PT, (marg + TRIM_H) * PT
    tx0, tx1 = marg * PT, (marg + TRIM_W) * PT

    falhas = []
    for i, pg in enumerate(doc, start=1):
        todas = pg.get_text("words")      # x0, y0, x1, y1, texto, ...
        palavras = [p for p in todas
                    if p[0] >= tx0 - 0.5 and p[2] <= tx1 + 0.5
                    and p[1] >= ty0 - 0.5 and p[3] <= ty1 + 0.5]
        for x0, y0, x1, y1, w, *_ in palavras:
            if x1 > z0 and x0 < z1:
                falhas.append((i, w, (x0 / PT - marg), (x1 / PT - marg)))
        # menor distância de qualquer palavra até o eixo da dobra
        eixo = (marg + DOBRA) * PT
        d = min((0.0 if x0 <= eixo <= x1 else min(abs(x0 - eixo), abs(x1 - eixo)) / PT
                 for x0, _, x1, _, *_ in palavras), default=999)
        print(f"  pagina {i}: {len(palavras)} palavras dentro do trim "
              f"({len(todas) - len(palavras)} fora, marcas) | folga minima ate o "
              f"eixo da dobra: {d:.1f} mm")
    doc.close()
    return falhas


if __name__ == "__main__":
    pdf = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        RAIZ, "01-TABULEIRO", "TABULEIRO_400x300_SANGRIA-3mm.pdf")
    f = verificar(pdf)
    if f:
        print("\n  FALHOU — texto dentro da zona morta:")
        for pg, w, a, b in f:
            print(f"    pag {pg}: '{w}' em x {a:.1f}..{b:.1f} mm")
        sys.exit(1)
    print("\n  OK — nenhum texto invade a zona morta do vinco.")
