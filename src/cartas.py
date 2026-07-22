# -*- coding: utf-8 -*-
"""
TRÊS DOBRAS — CARTAS
Formato final 70 x 120 mm (tarô) · sangria 3 mm · cantos r = 4 mm
Margem de segurança 5 mm — nenhum texto encosta na faca.

60 cartas:
  40 de linguagem (8 x 5 naipes) com 3 níveis cada
   6 de ESPELHO
   4 de ALTAR
  10 do ENVELOPE SELADO (verso próprio)
"""
import os
from comum import *
from dados import (LINGUAGENS, NIVEIS, ESPELHO, ALTAR, SELADO,
                   SELADO_TITULO, SELADO_EPIGRAFE, VERSICULO_REF)

CW, CH = 70.0, 120.0      # formato final da carta
RC = 4.0                  # raio do canto (faca)
SEG = 5.0                 # margem de segurança
CAB = 24.0                # altura da faixa de cabeçalho


# --------------------------------------------------------------------- BASE --
def _sangria(p, cor):
    """Fundo da CARTA (não da página) — necessário para a folha de conferência."""
    p.ret(-SANGRIA, -SANGRIA, CW + 2 * SANGRIA, CH + 2 * SANGRIA, fill=cor)


def _fundo(p, cor_borda):
    _sangria(p, CREME)
    p.ret(-SANGRIA, CH - CAB, CW + 2 * SANGRIA, CAB + SANGRIA, fill=cor_borda)
    p.ret(-SANGRIA, -SANGRIA, CW + 2 * SANGRIA, 3.0, fill=cor_borda)


def _cabecalho(p, tipo, titulo=None, sub=None):
    cor = NAIPES[tipo]["cor"]
    _fundo(p, cor)
    cy = CH - CAB / 2
    p.circ(14.0, cy, 7.4, fill=BRANCO)
    ICONES[tipo](p, 14.0, cy, 9.4, cor)
    p.txt_fit(24.5, cy + 0.8, titulo or NAIPES[tipo]["nome"], "TextoBold", 7.0,
              CW - 24.5 - SEG, BRANCO, tracking=1.0)
    p.txt_fit(24.5, cy - 5.0, sub if sub is not None else NAIPES[tipo]["sub"],
              "TituloIt", 4.4, CW - 24.5 - SEG, BRANCO)


def _rodape(p, ident, cor):
    p.txt(SEG, 5.6, "TRÊS DOBRAS", "TextoBold", 3.6, tinta(PETROLEO, 60), tracking=0.7)
    p.txt(CW - SEG, 5.6, ident, "Texto", 3.6, tinta(cor, 85), "r", tracking=0.4)


# ------------------------------------------------------------ FRENTES --------
def frente_linguagem(p, tipo, niveis, ident):
    cor = NAIPES[tipo]["cor"]
    _cabecalho(p, tipo)
    topo, base = CH - CAB - 4.0, 11.0
    bloco = (topo - base) / 3.0
    for i, (num, rot) in enumerate(NIVEIS):
        yt = topo - i * bloco
        if i:
            p.linha(SEG + 3, yt + 2.2, CW - SEG - 3, yt + 2.2, tinta(cor, 28), 0.35)
        p.circ(SEG + 2.4, yt - 2.6, 2.4, fill=cor)
        p.txt(SEG + 2.4, yt - 3.7, num, "TextoBold", 3.4, BRANCO, "c")
        p.txt(SEG + 6.6, yt - 3.9, rot, "TextoBold", 4.0, cor, tracking=0.9)
        y, t = p.texto_caixa(SEG, yt - 8.2, CW - 2 * SEG, bloco - 10.6, niveis[i],
                             "Texto", 4.6, 3.2, tinta(PETROLEO, 92), lead=1.22)
        assert y - t * 0.30 >= yt - bloco + 1.5, f"{ident} nivel {num} estourou o bloco"
    _rodape(p, ident, cor)


def frente_espelho(p, pergunta, ident):
    cor = NAIPES["ESPELHO"]["cor"]
    _cabecalho(p, "ESPELHO", "ESPELHO", "o quanto eu te conheço")
    p.texto_caixa(SEG, CH - CAB - 8.0, CW - 2 * SEG, 42.0, pergunta,
                  "TituloIt", 6.6, 4.2, PETROLEO, lead=1.26, al="c", vcenter=True)
    p.ret(SEG, 20.0, CW - 2 * SEG, 24.0, fill=tinta(cor, 8), r=3)
    p.ret(SEG, 20.0, CW - 2 * SEG, 24.0, stroke=tinta(cor, 50), lw=0.5, r=3)
    p.txt(CW / 2, 38.6, "COMO FUNCIONA", "TextoBold", 3.8, cor, "c", tracking=1.0)
    p.texto_caixa(SEG + 3, 35.0, CW - 2 * SEG - 6, 13.0,
                  "Responda PELO seu cônjuge, sem perguntar. Acertou? Andem 2 casas. "
                  "Errou? Ele(a) conta a resposta e vocês plantam 1 semente na "
                  "linguagem que ele(a) escolher.",
                  "Texto", 3.9, 3.0, tinta(PETROLEO, 85), lead=1.20, al="c")
    _rodape(p, ident, cor)


def frente_altar(p, titulo, texto, ident):
    _sangria(p, PETROLEO)
    p.ret(SEG - 1.5, SEG - 1.5, CW - 2 * (SEG - 1.5), CH - 2 * (SEG - 1.5),
          stroke=tinta(DOURADO, 75), lw=0.5, r=2.5)
    ico_altar(p, CW / 2, CH - 28.0, 20.0, DOURADO)
    p.txt(CW / 2, CH - 44.0, "ALTAR", "Texto", 4.0, tinta(DOURADO, 85), "c", tracking=2.2)
    p.txt_fit(CW / 2, CH - 57.0, titulo, "TituloBold", 10.0, CW - 2 * SEG - 6,
              BRANCO, "c", tracking=1.4)
    p.linha(CW / 2 - 13, CH - 62.0, CW / 2 + 13, CH - 62.0, tinta(DOURADO, 80), 0.5)
    p.texto_caixa(SEG + 3, CH - 68.0, CW - 2 * SEG - 6, 34.0, texto,
                  "Texto", 4.8, 3.4, BRANCO, lead=1.26, al="c")
    p.txt(CW / 2, 10.5, "A TERCEIRA DOBRA", "Texto", 3.6, tinta(DOURADO, 85), "c",
          tracking=1.2)
    p.txt(CW / 2, 5.6, ident, "Texto", 3.2, tinta(DOURADO, 50), "c")


def frente_selado(p, texto, ident, i):
    cor = VINHO
    _sangria(p, CREME)
    p.ret(-SANGRIA, CH - 20.0, CW + 2 * SANGRIA, 20.0 + SANGRIA, fill=cor)
    p.ret(-SANGRIA, -SANGRIA, CW + 2 * SANGRIA, 3.0, fill=cor)
    p.txt_fit(CW / 2, CH - 11.5, SELADO_TITULO, "TituloBold", 7.4, CW - 10.0,
              BRANCO, "c", tracking=1.5)
    p.txt(CW / 2, CH - 17.0, "só para os dois", "TituloIt", 4.2, BRANCO, "c")
    p.circ(CW / 2, CH - 32.0, 4.6, stroke=tinta(cor, 55), lw=0.5)
    p.txt(CW / 2, CH - 33.8, str(i), "TituloBold", 5.4, cor, "c")
    p.texto_caixa(SEG + 2, CH - 42.0, CW - 2 * SEG - 4, 40.0, texto,
                  "Texto", 5.4, 3.6, tinta(PETROLEO, 92), lead=1.28, al="c",
                  vcenter=True)
    p.linha(CW / 2 - 12, 30.0, CW / 2 + 12, 30.0, tinta(VINHO, 45), 0.4)
    p.texto_caixa(SEG + 2, 26.0, CW - 2 * SEG - 4, 13.0, SELADO_EPIGRAFE,
                  "TituloIt", 3.8, 3.0, tinta(VINHO, 85), lead=1.20, al="c")
    _rodape(p, ident, cor)


# -------------------------------------------------------------- VERSOS -------
def verso_jogo(p):
    _sangria(p, PETROLEO)
    p.ret(SEG - 2.0, SEG - 2.0, CW - 2 * (SEG - 2.0), CH - 2 * (SEG - 2.0),
          stroke=tinta(DOURADO, 70), lw=0.5, r=2.5)
    cordao_vertical(p, CW / 2, 12.0, CH - 12.0, 26.0,
                    (tinta(DOURADO, 60), tinta(TERRACOTA, 45), tinta(AZUL, 45)),
                    lw=0.7, ciclos=4)
    p.ret(6.0, CH / 2 - 15.0, CW - 12.0, 30.0, fill=PETROLEO)
    logo(p, CW / 2, CH / 2 + 2.0, s=1.0, cor=BRANCO, cor2=DOURADO, larg=CW - 20.0)
    p.txt(CW / 2, CH / 2 - 9.5, VERSICULO_REF, "Texto", 3.6, tinta(DOURADO, 90),
          "c", tracking=1.2)


def verso_selado(p):
    _sangria(p, VINHO)
    p.ret(SEG - 2.0, SEG - 2.0, CW - 2 * (SEG - 2.0), CH - 2 * (SEG - 2.0),
          stroke=tinta(DOURADO, 70), lw=0.5, r=2.5)
    cordao_vertical(p, CW / 2, 12.0, CH - 12.0, 26.0,
                    (tinta(DOURADO, 55), tinta(CREME, 45), tinta(CREME, 25)),
                    lw=0.7, ciclos=4)
    p.ret(6.0, CH / 2 - 17.0, CW - 12.0, 34.0, fill=VINHO)
    p.txt_fit(CW / 2, CH / 2 + 5.0, "O JARDIM", "TituloBold", 9.0, CW - 22.0, CREME,
              "c", tracking=1.5)
    p.txt_fit(CW / 2, CH / 2 - 3.5, "FECHADO", "TituloBold", 9.0, CW - 22.0, CREME,
              "c", tracking=1.5)
    p.txt(CW / 2, CH / 2 - 12.0, "CÂNTICO 4.12", "Texto", 3.6, tinta(DOURADO, 95),
          "c", tracking=1.2)


# ------------------------------------------------------------- CATÁLOGO ------
def catalogo():
    """Devolve a lista ordenada de (funcao_frente, kwargs, funcao_verso, ident)."""
    itens = []
    siglas = {"PALAVRA": "PAL", "TEMPO": "TEM", "PRESENTE": "PRE",
              "SERVICO": "SER", "TOQUE": "TOQ"}
    for tipo, cartas in LINGUAGENS:
        for i, niveis in enumerate(cartas, start=1):
            ident = f"{siglas[tipo]} {i:02d}"
            itens.append((frente_linguagem, dict(tipo=tipo, niveis=niveis, ident=ident),
                          verso_jogo, ident))
    for i, q in enumerate(ESPELHO, start=1):
        ident = f"ESP {i:02d}"
        itens.append((frente_espelho, dict(pergunta=q, ident=ident), verso_jogo, ident))
    for i, (tit, txt) in enumerate(ALTAR, start=1):
        ident = f"ALT {i:02d}"
        itens.append((frente_altar, dict(titulo=tit, texto=txt, ident=ident),
                      verso_jogo, ident))
    for i, txt in enumerate(SELADO, start=1):
        ident = f"JAR {i:02d}"
        itens.append((frente_selado, dict(texto=txt, ident=ident, i=i),
                      verso_selado, ident))
    return itens


def gerar(base):
    itens = catalogo()
    os.makedirs(base, exist_ok=True)

    for nome, idx in (("FRENTES", 0), ("VERSOS", 2)):
        cam = os.path.join(base, f"CARTAS_{nome}_70x120_sangria-3mm.pdf")
        p = Prancha(cam, CW, CH, marcas=False, titulo=f"TRES DOBRAS - cartas {nome}")
        for k, item in enumerate(itens):
            if k:
                p.pagina()
            if idx == 0:
                item[0](p, **item[1])
            else:
                item[2](p)
        p.salvar()
        print(f"  {len(itens):>3} paginas  {cam}")
    return len(itens)


def montagem(base):
    """Folha de conferência: todas as frentes lado a lado (NÃO é arquivo de impressão)."""
    itens = catalogo()
    cols, rows = 6, 4
    LW, LH = CW + 6, CH + 6
    W, H = cols * LW + 12, rows * LH + 22
    cam = os.path.join(base, "_CONFERENCIA_todas-as-cartas.pdf")
    p = Prancha(cam, W, H, marcas=False, titulo="TRES DOBRAS - conferencia")
    n = 0
    for pag in range(0, len(itens), cols * rows):
        if pag:
            p.pagina()
        p.ret(-SANGRIA, -SANGRIA, W + 2 * SANGRIA, H + 2 * SANGRIA, fill=BRANCO)
        p.txt(6, H - 12, "TRÊS DOBRAS · conferência de cartas (não usar para impressão)",
              "TextoBold", 7, PRETO_TXT)
        for k, item in enumerate(itens[pag:pag + cols * rows]):
            cx = 6 + (k % cols) * LW
            cy = H - 22 - (k // cols + 1) * LH + 6
            p.c.saveState(); p.c.translate(cx, cy)
            item[0](p, **item[1])
            p.c.restoreState()
            n += 1
    p.salvar()
    print(f"  {n:>3} cartas    {cam}")


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "03-PECAS")
    total = gerar(base)
    montagem(base)
    print(f"TOTAL: {total} cartas 70x120mm")
