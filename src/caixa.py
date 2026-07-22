# -*- coding: utf-8 -*-
"""
TRÊS DOBRAS — CAIXA (tampa e fundo)
Comporta o tabuleiro dobrado (200 x 300 mm) + 60 cartas + cartela + envelope.

  TAMPA : interno 207 x 307 x 30 mm  ->  planificado 267 x 367 mm
  FUNDO : interno 203 x 303 x 28 mm  ->  planificado 259 x 359 mm

Sangria 3 mm. FACA em magenta 100% / VINCO em ciano 100%, ambos em sobreimpressão,
para a gráfica isolar numa camada técnica. Arte impressa só na FACE EXTERNA.
"""
import os
from comum import *
from dados import VERSICULO, VERSICULO_REF

FACA = cmyk(0, 100, 0, 0)
VINCO_C = cmyk(100, 0, 0, 0)

TAMPA = dict(W=207.0, L=307.0, H=30.0, nome="TAMPA")
FUNDO = dict(W=203.0, L=303.0, H=28.0, nome="FUNDO")


def flat(cx):
    return cx["H"] * 2 + cx["W"], cx["H"] * 2 + cx["L"]


def _tec(p, cor):
    c = p.c
    c.setStrokeColor(cor); c.setStrokeOverprint(True); c.setLineWidth(0.25)
    return c


def vinco(p, x1, y1, x2, y2):
    c = _tec(p, VINCO_C)
    c.setDash([2.0, 1.5]); c.line(x1, y1, x2, y2)
    c.setDash([]); c.setStrokeOverprint(False)


def contorno(p, cx):
    """Faca da planificação: painel central + 4 paredes + 4 abas de canto."""
    W, L, H = cx["W"], cx["L"], cx["H"]
    ab = H - 2.0                       # largura útil da aba de canto
    rec = 2.5                          # recuo do trapézio
    c = _tec(p, FACA)
    pth = c.beginPath()
    # canto inferior esquerdo -> percorrendo no sentido horário
    pth.moveTo(0, H)
    pth.lineTo(0, H + L)                       # parede esquerda
    pth.lineTo(rec, H + L + ab)                # aba canto sup. esq.
    pth.lineTo(H, H + L + ab)
    pth.lineTo(H, H + L + H)                   # parede topo
    pth.lineTo(H + W, H + L + H)
    pth.lineTo(H + W, H + L + ab)              # aba canto sup. dir.
    pth.lineTo(H + W + H - rec, H + L + ab)
    pth.lineTo(H + W + H, H + L)
    pth.lineTo(H + W + H, H)                   # parede direita
    pth.lineTo(H + W + H - rec, H - ab)        # aba canto inf. dir.
    pth.lineTo(H + W, H - ab)
    pth.lineTo(H + W, 0)                       # parede base
    pth.lineTo(H, 0)
    pth.lineTo(H, H - ab)                      # aba canto inf. esq.
    pth.lineTo(rec, H - ab)
    pth.close()
    c.drawPath(pth, stroke=1, fill=0)
    c.setStrokeOverprint(False)
    # vincos: as 4 dobras do painel central + as 4 dobras das abas
    vinco(p, H, H, H + W, H)
    vinco(p, H, H + L, H + W, H + L)
    vinco(p, H, H, H, H + L)
    vinco(p, H + W, H, H + W, H + L)
    vinco(p, 0, H, H, H)
    vinco(p, 0, H + L, H, H + L)
    vinco(p, H + W, H, H + W + H, H)
    vinco(p, H + W, H + L, H + W + H, H + L)


def _paredes(p, cx, cor):
    """Paredes + abas. As bordas EXTERNAS avançam a sangria (não podem ficar
       sem tinta se o corte deslocar)."""
    W, L, H = cx["W"], cx["L"], cx["H"]
    s = SANGRIA
    p.ret(H, H + L, W, H + s, fill=cor)                # parede topo
    p.ret(H, -s, W, H + s, fill=cor)                   # parede base
    p.ret(-s, H, H + s, L, fill=cor)                   # parede esquerda
    p.ret(H + W, H, H + s, L, fill=cor)                # parede direita
    p.ret(-s, 2.0 - s, H + s, H - 2.0 + s, fill=cor)   # abas de canto
    p.ret(-s, H + L, H + s, H - 2.0 + s, fill=cor)
    p.ret(H + W, 2.0 - s, H + s, H - 2.0 + s, fill=cor)
    p.ret(H + W, H + L, H + s, H - 2.0 + s, fill=cor)


def _texto_lateral(p, x, y, ang, texto, fonte, tam, cor, tracking=0):
    c = p.c
    c.saveState(); c.translate(x, y); c.rotate(ang)
    p.txt(0, 0, texto, fonte, tam, cor, "c", tracking)
    c.restoreState()


# --------------------------------------------------------------- TAMPA ------
def tampa(p):
    cx = TAMPA
    W, L, H = cx["W"], cx["L"], cx["H"]
    p.fundo_sangria(CREME)
    _paredes(p, cx, PETROLEO)

    # ---- painel central (a capa) -----------------------------------------
    px, py = H, H
    p.ret(px, py, W, L, fill=PETROLEO)
    p.ret(px + 10, py + 10, W - 20, L - 20, stroke=tinta(DOURADO, 75), lw=0.6)
    p.ret(px + 13, py + 13, W - 26, L - 26, stroke=tinta(DOURADO, 35), lw=0.25)

    ccx = px + W / 2
    # cordão pendendo do alto (ornamento; nunca sobre texto)
    cordao_vertical(p, ccx, py + L - 44, py + L - 16, 22.0,
                    (tinta(DOURADO, 55), tinta(TERRACOTA, 35), tinta(AZUL, 35)),
                    lw=0.8, ciclos=1)

    p.txt_fit(ccx, py + 232, "TRÊS", "TituloBold", 34, W - 64, CREME, "c",
              tracking=5.0)
    p.txt_fit(ccx, py + 198, "DOBRAS", "TituloBold", 34, W - 64, CREME, "c",
              tracking=5.0)
    p.linha(px + 30, py + 185, ccx - 9, py + 185, tinta(DOURADO, 85), 0.6)
    p.linha(ccx + 9, py + 185, px + W - 30, py + 185, tinta(DOURADO, 85), 0.6)
    ico_altar(p, ccx, py + 186, 11.0, DOURADO)
    p.txt_fit(ccx, py + 170, "UM JOGO PARA CASAIS", "Texto", 8.0, W - 72,
              tinta(DOURADO, 95), "c", tracking=3.4)

    y = py + 152
    for ln in p.quebrar(VERSICULO, "TituloIt", 9.0, W - 70):
        p.txt(ccx, y, ln, "TituloIt", 9.0, CREME, "c")
        y -= 11.5
    p.txt(ccx, y - 1, VERSICULO_REF, "Texto", 6.0, tinta(DOURADO, 95), "c",
          tracking=2.0)

    # selo das cinco linguagens
    p.txt_fit(ccx, py + 112, "CINCO LINGUAGENS · TRÊS NÍVEIS", "TextoBold", 6.0,
              W - 60, tinta(DOURADO, 95), "c", tracking=2.0)
    ys = py + 86
    for k, tipo in enumerate(["PALAVRA", "TEMPO", "PRESENTE", "SERVICO", "TOQUE"]):
        x = ccx + (k - 2) * 32
        p.circ(x, ys, 13.0, fill=CREME)
        ICONES[tipo](p, x, ys, 15.0, NAIPES[tipo]["cor"])

    p.txt_fit(ccx, py + 56, "60 cartas · tabuleiro dobrável · 36 peças", "TituloIt",
              7.4, W - 56, CREME, "c")
    p.txt_fit(ccx, py + 44, "+ envelope selado para levar para casa", "TituloIt",
              7.4, W - 56, tinta(DOURADO, 95), "c")
    p.linha(px + 46, py + 34, px + W - 46, py + 34, tinta(DOURADO, 55), 0.4)
    p.txt_fit(ccx, py + 22, "CONGRESSO DE CASAIS", "Texto", 5.6, W - 70,
              tinta(DOURADO, 85), "c", tracking=2.4)

    # ---- paredes ----------------------------------------------------------
    LOMBADA = "TRÊS DOBRAS · UM JOGO PARA CASAIS"
    p.txt_fit(px + W / 2, H / 2 - 2.4, LOMBADA, "TextoBold", 7.0, W - 20,
              tinta(DOURADO, 95), "c", tracking=2.6)
    p.txt_fit(px + W / 2, py + L + H / 2 - 2.4, LOMBADA, "TextoBold", 7.0, W - 20,
              tinta(DOURADO, 95), "c", tracking=2.6)
    _texto_lateral(p, H / 2 - 2.4, py + L / 2, 90, "TRÊS DOBRAS · ECLESIASTES 4.12",
                   "TextoBold", 7.0, tinta(DOURADO, 95), 2.6)
    _texto_lateral(p, px + W + H / 2 + 2.4, py + L / 2, 270,
                   "TRÊS DOBRAS · ECLESIASTES 4.12", "TextoBold", 7.0,
                   tinta(DOURADO, 95), 2.6)

    contorno(p, cx)
    p.marcas_corte(rotulo="TRES DOBRAS · CAIXA TAMPA · interno 207x307x30mm · planificado 267x367mm · faca MAGENTA / vinco CIANO")


# --------------------------------------------------------------- FUNDO ------
CONTEUDO = [
    "1 tabuleiro dobrável 400 × 300 mm",
    "60 cartas 70 × 120 mm",
    "30 sementes das cinco linguagens",
    "1 peão do casal (Ele + Ela + base)",
    "3 marcadores de nível",
    "1 dado montável",
    "1 envelope selado — O Jardim Fechado",
]


def fundo(p):
    cx = FUNDO
    W, L, H = cx["W"], cx["L"], cx["H"]
    p.fundo_sangria(CREME)
    _paredes(p, cx, tinta(PETROLEO, 90))

    px, py = H, H
    p.ret(px, py, W, L, fill=CREME)
    p.ret(px + 10, py + 10, W - 20, L - 20, stroke=tinta(DOURADO, 70), lw=0.5)
    ccx = px + W / 2

    logo(p, ccx, py + L - 46, s=1.55, cor=PETROLEO, cor2=DOURADO, larg=W - 60)
    p.txt(ccx, py + L - 62, "CONTEÚDO DA CAIXA", "TextoBold", 6.4, PETROLEO, "c",
          tracking=2.2)

    y = py + L - 78
    for item in CONTEUDO:
        p.circ(px + 34, y + 1.6, 1.7, fill=DOURADO)
        p.txt(px + 40, y, item, "Texto", 7.4, tinta(PETROLEO, 88))
        y -= 12.0

    p.linha(px + 30, y - 2, px + W - 30, y - 2, tinta(DOURADO, 60), 0.4)
    y -= 16
    p.txt(ccx, y, "COMO COMEÇAR", "TextoBold", 6.4, PETROLEO, "c", tracking=2.2)
    y -= 13
    for ln in p.quebrar("Abram o tabuleiro. Separem as cartas por cor. Escolham "
                        "juntos o nível. E não tenham pressa: o jogo termina no "
                        "Altar, e o Altar não tem relógio.", "TituloIt", 8.0, W - 66):
        p.txt(ccx, y, ln, "TituloIt", 8.0, tinta(PETROLEO, 85), "c")
        y -= 10.5

    # bloco de fecho posicionado a partir do fim do texto (nunca sobrepõe)
    ico_altar(p, ccx, y - 16, 24.0, tinta(DOURADO, 90))
    p.txt(ccx, y - 38, VERSICULO_REF, "Texto", 6.0, tinta(PETROLEO, 70), "c",
          tracking=2.0)
    p.txt(ccx, y - 49, "não é um jogo sobre vencer", "TituloIt", 6.6,
          tinta(PETROLEO, 60), "c")
    assert y - 49 >= py + 16, "bloco de fecho do fundo estourou o painel"

    contorno(p, cx)
    p.marcas_corte(rotulo="TRES DOBRAS · CAIXA FUNDO · interno 203x303x28mm · planificado 259x359mm · faca MAGENTA / vinco CIANO")


# ----------------------------------------------------------------------------
def gerar(base):
    os.makedirs(base, exist_ok=True)
    saidas = []
    for cxd, fn in ((TAMPA, tampa), (FUNDO, fundo)):
        w, h = flat(cxd)
        cam = os.path.join(base, f"CAIXA-{cxd['nome']}_{w:.0f}x{h:.0f}_faca.pdf")
        p = Prancha(cam, w, h, marcas=True, titulo=f"TRES DOBRAS - caixa {cxd['nome']}")
        fn(p)
        p.salvar()
        print(f"  {cxd['nome']}: planificado {w:.0f} x {h:.0f} mm  ->  {cam}")
        saidas.append(cam)
    return saidas


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "02-CAIXA")
    gerar(base)
