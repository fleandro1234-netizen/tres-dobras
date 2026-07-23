# -*- coding: utf-8 -*-
"""
TRÊS DOBRAS — PEÇAS DESTACÁVEIS
  1) CARTELA 200 x 280 mm (papelão 1,5 mm, faca de destaque)
     30 sementes + peão do casal (2 figuras + base) + 3 marcadores de nível
  2) DADO montável — planificação de cubo 20 mm
  3) ENVELOPE SELADO "O JARDIM FECHADO" — faca plana
Sangria 3 mm em tudo. Linhas de FACA em magenta 100% com sobreimpressão.
"""
import os
from comum import *

FACA = cmyk(0, 100, 0, 0)          # cor técnica: mover para camada própria
VINCO_C = cmyk(100, 0, 0, 0)       # ciano 100% = linha de vinco/dobra


def _faca(p, fechar=None):
    c = p.c
    c.setStrokeColor(FACA)
    c.setStrokeOverprint(True)
    c.setLineWidth(0.25)
    c.setDash([])


def faca_circ(p, x, y, r):
    _faca(p)
    p.c.circle(x, y, r, stroke=1, fill=0)
    p.c.setStrokeOverprint(False)


def faca_ret(p, x, y, w, h, r=0):
    _faca(p)
    if r:
        p.c.roundRect(x, y, w, h, r, stroke=1, fill=0)
    else:
        p.c.rect(x, y, w, h, stroke=1, fill=0)
    p.c.setStrokeOverprint(False)


def vinco(p, x1, y1, x2, y2):
    c = p.c
    c.setStrokeColor(VINCO_C); c.setStrokeOverprint(True)
    c.setLineWidth(0.25); c.setDash([2.0, 1.5])
    c.line(x1, y1, x2, y2)
    c.setDash([]); c.setStrokeOverprint(False)


# =========================================================== 1) CARTELA ======
CW, CHh = 200.0, 280.0
CORES_SEMENTE = ["PALAVRA", "TEMPO", "PRESENTE", "SERVICO", "TOQUE"]


def cartela(p):
    p.fundo_sangria(CREME)
    p.ret(6, 6, CW - 12, CHh - 12, stroke=tinta(DOURADO, 60), lw=0.5)

    logo(p, CW / 2, CHh - 22, s=1.0, cor=PETROLEO, cor2=DOURADO, larg=96)
    p.txt(CW / 2, CHh - 36, "PEÇAS DO JOGO · destaque com cuidado", "Texto", 4.2,
          tinta(PETROLEO, 70), "c", tracking=1.2)

    # ---- 30 sementes: 6 por linguagem -----------------------------------
    RS = 12.0
    xs = [25 + i * 30 for i in range(6)]
    ys = [226, 199, 172, 145, 118]
    for tipo, y in zip(CORES_SEMENTE, ys):
        cor = NAIPES[tipo]["cor"]
        for x in xs:
            p.circ(x, y, RS, fill=tinta(cor, 20))
            p.circ(x, y, RS, stroke=cor, lw=0.6)
            ICONES[tipo](p, x, y + 1.6, 10.5, cor)
            p.txt_fit(x, y - 8.2, NAIPES[tipo]["nome"], "TextoBold", 3.1, 19.0,
                      cor, "c", tracking=0.35)
            faca_circ(p, x, y, RS)
    assert ys[0] + RS < CHh - 40, "sementes colidem com o cabeçalho"

    p.linha(14, 100, CW - 14, 100, tinta(DOURADO, 60), 0.4)

    # ---- peão do casal: duas figuras encaixadas numa base ----------------
    p.txt(58, 93, "O PEÃO DO CASAL", "TextoBold", 4.2, PETROLEO, "c", tracking=1.1)
    for dx, rot, cor in ((-15, "ELE", AZUL), (15, "ELA", VINHO)):
        cxp, yb = 58 + dx, 40.0        # yb = base da lingueta
        w, tab_w, tab_h, corpo = 24.0, 19.0, 7.0, 38.0
        x = cxp - w / 2
        # corpo: retângulo com topo semicircular + lingueta de encaixe
        c = p.c
        c.setFillColor(tinta(cor, 16))
        pth = c.beginPath()
        pth.moveTo(x, yb + tab_h)
        pth.lineTo(x, yb + tab_h + corpo - w / 2)
        pth.curveTo(x, yb + tab_h + corpo, x + w, yb + tab_h + corpo,
                    x + w, yb + tab_h + corpo - w / 2)
        pth.lineTo(x + w, yb + tab_h)
        pth.lineTo(cxp + tab_w / 2, yb + tab_h)
        pth.lineTo(cxp + tab_w / 2, yb)
        pth.lineTo(cxp - tab_w / 2, yb)
        pth.lineTo(cxp - tab_w / 2, yb + tab_h)
        pth.close()
        c.drawPath(pth, stroke=0, fill=1)
        ico_toque(p, cxp, yb + tab_h + corpo - 13, 13.0, cor)
        p.txt(cxp, yb + tab_h + 6.0, rot, "TextoBold", 4.8, cor, "c", tracking=1.0)
        _faca(p); c.drawPath(pth, stroke=1, fill=0); c.setStrokeOverprint(False)

    p.circ(58, 20, 16.0, fill=tinta(DOURADO, 18))
    p.circ(58, 20, 16.0, stroke=DOURADO, lw=0.6)
    p.txt(58, 26.5, "BASE", "TextoBold", 3.8, tinta(PETROLEO, 80), "c", tracking=0.9)
    faca_circ(p, 58, 20, 16.0)
    faca_ret(p, 58 - 9.8, 19.1, 19.6, 1.8, r=0.9)   # fenda de encaixe do peão

    # ---- marcadores de nível ---------------------------------------------
    p.txt(142, 93, "MARCADOR DE NÍVEL", "TextoBold", 4.2, PETROLEO, "c", tracking=1.1)
    for k, (num, rot) in enumerate([("1", "CONHECER"), ("2", "APROXIMAR"),
                                    ("3", "APROFUNDAR")]):
        x, y = 112 + k * 30, 64
        p.circ(x, y, RS, fill=tinta(PETROLEO, 12))
        p.circ(x, y, RS, stroke=PETROLEO, lw=0.6)
        p.txt(x, y + 1.0, num, "TituloBold", 10.0, PETROLEO, "c")
        p.txt_fit(x, y - 7.8, rot, "TextoBold", 3.1, 19.0, tinta(PETROLEO, 80), "c",
                  tracking=0.3)
        faca_circ(p, x, y, RS)

    p.txt(142, 34, "Deixem o marcador à vista.", "TituloIt", 4.4,
          tinta(PETROLEO, 70), "c")
    p.txt(142, 27, "Podem subir de nível quando quiserem.", "TituloIt", 4.4,
          tinta(PETROLEO, 70), "c")

    p.marcas_corte(rotulo="TRES DOBRAS · CARTELA DE PECAS · 200x280mm · papelao 1,5mm · faca em MAGENTA")


# ============================================================== 2) DADO ======
DW, DH = 100.0, 90.0
LADO = 20.0
ABA = 5.0


def _pips(p, cx, cy, n, cor):
    d = LADO * 0.22
    pos = {
        1: [(0, 0)],
        2: [(-1, 1), (1, -1)],
        3: [(-1, 1), (0, 0), (1, -1)],
        4: [(-1, 1), (1, 1), (-1, -1), (1, -1)],
        5: [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)],
        6: [(-1, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (1, -1)],
    }[n]
    for ux, uy in pos:
        p.circ(cx + ux * LADO * 0.26, cy + uy * LADO * 0.26, d / 2, fill=cor)


def _aba(p, x, y, w, h, lado):
    """Aba de colagem trapezoidal. lado: 'topo','base','esq','dir'."""
    c = p.c
    _faca(p)
    pth = c.beginPath()
    i = ABA * 0.55
    if lado == "topo":
        pth.moveTo(x, y + h); pth.lineTo(x + i, y + h + ABA)
        pth.lineTo(x + w - i, y + h + ABA); pth.lineTo(x + w, y + h)
    elif lado == "base":
        pth.moveTo(x, y); pth.lineTo(x + i, y - ABA)
        pth.lineTo(x + w - i, y - ABA); pth.lineTo(x + w, y)
    elif lado == "esq":
        pth.moveTo(x, y); pth.lineTo(x - ABA, y + i)
        pth.lineTo(x - ABA, y + h - i); pth.lineTo(x, y + h)
    else:
        pth.moveTo(x + w, y); pth.lineTo(x + w + ABA, y + i)
        pth.lineTo(x + w + ABA, y + h - i); pth.lineTo(x + w, y + h)
    c.drawPath(pth, stroke=1, fill=0)
    c.setStrokeOverprint(False)


def dado(p):
    p.fundo_sangria(CREME)
    x0, y0 = 10.0, 15.0
    faces_meio = [5, 1, 2, 6]
    p.txt(DW / 2, DH - 8, "DADO — recorte, vinque e cole", "TextoBold", 4.6,
          PETROLEO, "c", tracking=1.1)

    # corpo do cubo (fundo)
    for i in range(4):
        p.ret(x0 + i * LADO, y0 + LADO, LADO, LADO, fill=tinta(PETROLEO, 8))
    p.ret(x0 + LADO, y0 + 2 * LADO, LADO, LADO, fill=tinta(PETROLEO, 8))
    p.ret(x0 + LADO, y0, LADO, LADO, fill=tinta(PETROLEO, 8))

    for i, n in enumerate(faces_meio):
        _pips(p, x0 + i * LADO + LADO / 2, y0 + LADO * 1.5, n, PETROLEO)
    _pips(p, x0 + LADO * 1.5, y0 + LADO * 2.5, 3, PETROLEO)
    _pips(p, x0 + LADO * 1.5, y0 + LADO * 0.5, 4, PETROLEO)

    # vincos internos
    for i in range(1, 4):
        vinco(p, x0 + i * LADO, y0 + LADO, x0 + i * LADO, y0 + 2 * LADO)
    vinco(p, x0 + LADO, y0 + 2 * LADO, x0 + 2 * LADO, y0 + 2 * LADO)
    vinco(p, x0 + LADO, y0 + LADO, x0 + 2 * LADO, y0 + LADO)

    # contorno de corte
    _faca(p)
    c = p.c
    pth = c.beginPath()
    pth.moveTo(x0, y0 + LADO)
    pth.lineTo(x0 + LADO, y0 + LADO); pth.lineTo(x0 + LADO, y0)
    pth.lineTo(x0 + 2 * LADO, y0); pth.lineTo(x0 + 2 * LADO, y0 + LADO)
    pth.lineTo(x0 + 4 * LADO, y0 + LADO); pth.lineTo(x0 + 4 * LADO, y0 + 2 * LADO)
    pth.lineTo(x0 + 2 * LADO, y0 + 2 * LADO); pth.lineTo(x0 + 2 * LADO, y0 + 3 * LADO)
    pth.lineTo(x0 + LADO, y0 + 3 * LADO); pth.lineTo(x0 + LADO, y0 + 2 * LADO)
    pth.lineTo(x0, y0 + 2 * LADO); pth.close()
    c.drawPath(pth, stroke=1, fill=0)
    c.setStrokeOverprint(False)

    # abas de colagem — exatamente as 7 necessárias para fechar o cubo
    for i in (0, 2, 3):
        _aba(p, x0 + i * LADO, y0 + LADO, LADO, LADO, "topo")
        _aba(p, x0 + i * LADO, y0 + LADO, LADO, LADO, "base")
    _aba(p, x0 + 3 * LADO, y0 + LADO, LADO, LADO, "dir")

    p.txt(DW / 2, 8, "abas em cinza colam por dentro", "TituloIt", 3.8,
          tinta(PETROLEO, 60), "c")

    p.marcas_corte(rotulo="TRES DOBRAS · DADO MONTAVEL · cubo 20mm · faca MAGENTA · vinco CIANO")


# ========================================================== 3) ENVELOPE ======
EP_W, EP_H = 80.0, 130.0     # painel (comporta 10 cartas de 70x120)
EP_LAT, EP_FLAP = 14.0, 45.0
EW = EP_W + 2 * EP_LAT       # 108
EH = EP_FLAP + EP_H * 2      # 305


def envelope(p):
    p.fundo_sangria(CREME)
    xf = EP_LAT                    # x do painel central
    y_verso, y_frente, y_flap = 0.0, EP_H, EP_H * 2

    # painel FRENTE (fica voltado para fora quando montado)
    p.ret(xf, y_frente, EP_W, EP_H, fill=VINHO)
    p.txt(xf + EP_W / 2, y_frente + EP_H - 26, "O JARDIM", "TituloBold", 11.5, CREME,
          "c", tracking=2.0)
    p.txt(xf + EP_W / 2, y_frente + EP_H - 40, "FECHADO", "TituloBold", 11.5, CREME,
          "c", tracking=2.0)
    p.linha(xf + 18, y_frente + EP_H - 48, xf + EP_W - 18, y_frente + EP_H - 48,
            tinta(DOURADO, 85), 0.5)
    p.texto_caixa(xf + 8, y_frente + EP_H - 56, EP_W - 16, 26,
                  "“Jardim fechado és tu, minha irmã, minha esposa.” — Cântico 4.12",
                  "TituloIt", 5.0, 3.6, tinta(DOURADO, 95), lead=1.25, al="c")
    ico_toque(p, xf + EP_W / 2, y_frente + 46, 20.0, tinta(DOURADO, 90))
    p.texto_caixa(xf + 7, y_frente + 30, EP_W - 14, 24,
                  "Encham um canteiro inteiro no Mapa — as cinco sementes de uma "
                  "linguagem — e rompam o selo.",
                  "TextoBold", 4.4, 3.4, CREME, lead=1.30, al="c")

    # painel VERSO
    p.ret(xf, y_verso, EP_W, EP_H, fill=tinta(VINHO, 12))
    logo(p, xf + EP_W / 2, y_verso + EP_H - 34, s=0.9, cor=VINHO, cor2=DOURADO,
         larg=EP_W - 20)
    p.texto_caixa(xf + 8, y_verso + EP_H - 52, EP_W - 16, 40,
                  "10 convites para a intimidade do casamento, na linguagem do "
                  "Cântico dos Cânticos. Sem pressa, a dois.",
                  "Texto", 4.6, 3.4, tinta(PETROLEO, 90), lead=1.28, al="c")
    p.txt(xf + EP_W / 2, y_verso + 20, "1 CORÍNTIOS 7.3-5", "Texto", 4.0,
          tinta(VINHO, 85), "c", tracking=1.3)

    # aba de fechamento
    p.ret(xf, y_flap, EP_W, EP_FLAP, fill=VINHO)
    p.txt(xf + EP_W / 2, y_flap + EP_FLAP - 16, "SELADO", "TituloBold", 8.0, CREME,
          "c", tracking=2.4)
    p.txt(xf + EP_W / 2, y_flap + EP_FLAP - 26, "só para os dois", "TituloIt", 5.0,
          tinta(DOURADO, 95), "c")

    # abas laterais (colagem)
    for lado in (0, 1):
        x = 0 if lado == 0 else xf + EP_W
        p.ret(x, y_verso, EP_LAT, EP_H, fill=tinta(VINHO, 12))

    # faca + vincos
    _faca(p)
    c = p.c
    pth = c.beginPath()
    pth.moveTo(0, y_verso); pth.lineTo(EW, y_verso)
    pth.lineTo(EW, y_verso + EP_H); pth.lineTo(xf + EP_W, y_verso + EP_H)
    pth.lineTo(xf + EP_W, y_flap); pth.lineTo(xf + EP_W - 6, EH)
    pth.lineTo(xf + 6, EH); pth.lineTo(xf, y_flap)
    pth.lineTo(xf, y_verso + EP_H); pth.lineTo(0, y_verso + EP_H)
    pth.close()
    c.drawPath(pth, stroke=1, fill=0)
    c.setStrokeOverprint(False)
    vinco(p, xf, y_frente, xf + EP_W, y_frente)          # frente <-> verso
    vinco(p, xf, y_flap, xf + EP_W, y_flap)              # aba de fechamento
    vinco(p, xf, y_verso, xf, y_verso + EP_H)            # aba lateral esq.
    vinco(p, xf + EP_W, y_verso, xf + EP_W, y_verso + EP_H)

    p.marcas_corte(rotulo="TRES DOBRAS · ENVELOPE SELADO · planificado 108x305mm · faca MAGENTA · vinco CIANO")


# ============================================================================
def gerar(base):
    os.makedirs(base, exist_ok=True)
    saidas = []

    cam = os.path.join(base, "CARTELA-PECAS_200x280_sangria-3mm.pdf")
    p = Prancha(cam, CW, CHh, marcas=True, titulo="TRES DOBRAS - cartela de pecas")
    cartela(p); p.salvar(); saidas.append(cam)

    cam = os.path.join(base, "DADO-MONTAVEL_100x90_sangria-3mm.pdf")
    p = Prancha(cam, DW, DH, marcas=True, titulo="TRES DOBRAS - dado")
    dado(p); p.salvar(); saidas.append(cam)

    cam = os.path.join(base, "ENVELOPE-SELADO_108x305_faca.pdf")
    p = Prancha(cam, EW, EH, marcas=True, titulo="TRES DOBRAS - envelope selado")
    envelope(p); p.salvar(); saidas.append(cam)

    for s in saidas:
        print(f"  {s}")
    return saidas


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "03-PECAS")
    gerar(base)
