# -*- coding: utf-8 -*-
"""
TRÊS DOBRAS — gera os 3 projetos de impressão + previews.
Uso:  python gerar_tudo.py [--png300]
"""
import os, sys, time

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tabuleiro, caixa, cartas, pecas
from preview import render


TRAVADOS = []


def tentar(rotulo, fn, *a, **kw):
    """Executa um gerador; se o PDF estiver aberto em outro programa, anota e segue."""
    try:
        return fn(*a, **kw)
    except PermissionError as e:
        TRAVADOS.append(str(e).split(" continua")[0])
        print(f"  !! {rotulo}: arquivo aberto em outro programa — PULADO")
        return None


def main(png300=False):
    t0 = time.time()

    print("\n[1/3] TABULEIRO")
    d = os.path.join(RAIZ, "01-TABULEIRO"); os.makedirs(d, exist_ok=True)
    tentar("tabuleiro c/ marcas", tabuleiro.gerar,
           os.path.join(d, "TABULEIRO_400x300_COM-MARCAS.pdf"), marcas=True)
    tab = tentar("tabuleiro sangria", tabuleiro.gerar,
                 os.path.join(d, "TABULEIRO_400x300_SANGRIA-3mm.pdf"), marcas=False)
    print(f"  frente + verso  ->  {d}")

    print("\n[2/3] CAIXA")
    tentar("caixa", caixa.gerar, os.path.join(RAIZ, "02-CAIXA"))

    print("\n[3/3] PEÇAS")
    d = os.path.join(RAIZ, "03-PECAS")
    tentar("cartas", cartas.gerar, d)
    tentar("conferência", cartas.montagem, d)
    tentar("peças", pecas.gerar, d)

    print("\n[previews 100 dpi]")
    prev = os.path.join(RAIZ, "_previews"); os.makedirs(prev, exist_ok=True)
    n = 0
    for pasta in ("01-TABULEIRO", "02-CAIXA", "03-PECAS"):
        for f in sorted(os.listdir(os.path.join(RAIZ, pasta))):
            if f.endswith(".pdf") and "FRENTES" not in f and "VERSOS" not in f:
                n += len(render(os.path.join(RAIZ, pasta, f), 100, prev))
    print(f"  {n} imagens em {prev}")

    if png300:
        print("\n[PNG 300 dpi — todas as peças -> 04-PNG-300DPI]")
        d300 = os.path.join(RAIZ, "04-PNG-300DPI"); os.makedirs(d300, exist_ok=True)
        PECAS_300 = [
            ("01-TABULEIRO", "TABULEIRO_400x300_SANGRIA-3mm.pdf"),   # frente + verso
            ("02-CAIXA",     "CAIXA-TAMPA_267x367_faca.pdf"),
            ("02-CAIXA",     "CAIXA-FUNDO_259x359_faca.pdf"),
            ("03-PECAS",     "CARTELA-PECAS_200x280_sangria-3mm.pdf"),
            ("03-PECAS",     "DADO-MONTAVEL_100x90_sangria-3mm.pdf"),
            ("03-PECAS",     "ENVELOPE-SELADO_108x305_faca.pdf"),
        ]
        n300 = 0
        for pasta, arq in PECAS_300:
            for c, w, h in render(os.path.join(RAIZ, pasta, arq), 300, d300):
                n300 += 1
                print(f"  {w}x{h}px  {os.path.basename(c)}")
        # cartas: as 60 frentes + as 2 artes de verso (páginas 1 e 60), em subpasta
        dcar = os.path.join(d300, "cartas"); os.makedirs(dcar, exist_ok=True)
        n300 += len(render(os.path.join(RAIZ, "03-PECAS",
                    "CARTAS_FRENTES_70x120_sangria-3mm.pdf"), 300, dcar))
        n300 += len(render(os.path.join(RAIZ, "03-PECAS",
                    "CARTAS_VERSOS_70x120_sangria-3mm.pdf"), 300, dcar, paginas=[1, 60]))
        print(f"  {n300} imagens 300 dpi em {d300}")

    print(f"\nConcluído em {time.time()-t0:.1f}s")
    if TRAVADOS:
        print("\n!! ARQUIVOS NAO ATUALIZADOS (abertos em outro programa):")
        for t in TRAVADOS:
            print("   " + t)
        print("   Feche-os e rode este script de novo.")


if __name__ == "__main__":
    main(png300="--png300" in sys.argv)
