# -*- coding: utf-8 -*-
"""
Marca d'água "Casados para a Glória de Deus".

Duas fontes possíveis, nesta ordem de preferência:
  1) assets/casal.png  — a arte ORIGINAL do usuário (silhueta do casal).
     Se existir, é tingida na cor do material e usada como marca d'água.
  2) fallback vetorial — silhueta do casal recriada em curvas (abaixo),
     para não travar o trabalho enquanto o PNG oficial não é colocado.

Uso típico (bem sutil):
    marca_casal(p, cx, cy, larg=26, cor=PETROLEO, opacidade=7)
    assinatura(p, cx, cy, larg=52, cor=PETROLEO, opacidade=22)  # casal + frase
"""
import os
from comum import (MM, tinta, PETROLEO, DOURADO, CREME, BRANCO)

_ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "assets")
FRASE = "CASADOS PARA A GLÓRIA DE DEUS"

# Enquanto a arte OFICIAL (assets/casal.png) não estiver na pasta, a marca só
# aparece se TD_STANDIN=1 (para previews de posição). Assim os arquivos finais
# não saem com a silhueta recriada — trocam sozinhos quando o PNG oficial chega.
USAR_STANDIN = os.environ.get("TD_STANDIN") == "1"


def _png_oficial():
    for nome in ("casal.png", "casal.PNG", "casal.jpg"):
        cam = os.path.join(_ASSETS, nome)
        if os.path.exists(cam):
            return cam
    return None


# ---------------------------------------------------------------------------
# Silhueta vetorial do casal (fallback) — desenhada num quadrado ~[-0.5,0.5],
# centro em (cx,cy), altura = s. Dois perfis frente a frente sobre uma base
# de mãos em concha.
# ---------------------------------------------------------------------------
def _casal_vetor(p, cx, cy, s, cor):
    c = p.c
    c.setFillColor(cor)
    c.setLineJoin(1); c.setLineCap(1)

    def X(u): return cx + u * s
    def Y(v): return cy + v * s

    def perfil(pts):
        assert (len(pts) - 1) % 3 == 0, f"pontos={len(pts)} (precisa 1+3k)"
        pth = c.beginPath()
        pth.moveTo(X(pts[0][0]), Y(pts[0][1]))
        for i in range(1, len(pts), 3):
            (x1, y1), (x2, y2), (x3, y3) = pts[i], pts[i + 1], pts[i + 2]
            pth.curveTo(X(x1), Y(y1), X(x2), Y(y2), X(x3), Y(y3))
        pth.close()
        c.drawPath(pth, stroke=0, fill=1)

    # ---- base: mãos em concha ancorando o casal --------------------------
    pth = c.beginPath()
    pth.moveTo(X(-0.50), Y(-0.14))
    pth.curveTo(X(-0.30), Y(-0.42), X(0.30), Y(-0.42), X(0.50), Y(-0.14))
    pth.curveTo(X(0.30), Y(-0.30), X(-0.30), Y(-0.30), X(-0.50), Y(-0.14))
    pth.close()
    c.drawPath(pth, stroke=0, fill=1)

    # ---- ELE (direita), perfil voltado para a ESQUERDA, mais alto --------
    #  sequência: topo -> desce a FRENTE (testa,nariz,lábio,queixo,pescoço)
    #  -> base -> sobe a NUCA/cabelo -> topo
    perfil([
        (0.22, 0.50),
        (0.12, 0.47), (0.075, 0.40), (0.075, 0.33),      # testa
        (0.075, 0.30), (0.010, 0.27), (0.015, 0.235),    # nariz
        (0.055, 0.225), (0.045, 0.205), (0.035, 0.195),  # sulco + lábio sup.
        (0.030, 0.175), (0.055, 0.165), (0.070, 0.130),  # lábio inf. + queixo
        (0.095, 0.075), (0.135, 0.020), (0.160, -0.070), # mandíbula + pescoço
        (0.230, -0.100), (0.300, -0.110), (0.360, -0.060),  # base do pescoço
        (0.420, 0.010), (0.470, 0.150), (0.450, 0.300),  # nuca
        (0.440, 0.400), (0.360, 0.510), (0.220, 0.500),  # cabelo/topo
    ])

    # ---- ELA (esquerda), perfil voltado para a DIREITA, menor, coque -----
    perfil([
        (-0.26, 0.40),
        (-0.150, 0.375), (-0.110, 0.320), (-0.110, 0.270),  # testa
        (-0.110, 0.245), (-0.045, 0.220), (-0.050, 0.190),  # nariz
        (-0.090, 0.180), (-0.078, 0.163), (-0.070, 0.153),  # sulco + lábio
        (-0.066, 0.135), (-0.090, 0.128), (-0.105, 0.098),  # lábio inf. + queixo
        (-0.130, 0.050), (-0.170, -0.005), (-0.190, -0.075),# mandíbula + pescoço
        (-0.250, -0.100), (-0.320, -0.100), (-0.380, -0.055),# base do pescoço
        (-0.440, 0.020), (-0.470, 0.150), (-0.420, 0.245),  # nuca
        (-0.470, 0.300), (-0.380, 0.360), (-0.310, 0.320),  # coque
        (-0.300, 0.360), (-0.260, 0.430), (-0.260, 0.400),  # topo
    ])


def _tem_alpha(c):
    return hasattr(c, "setFillAlpha")


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------
def marca_casal(p, cx, cy, larg=26.0, cor=PETROLEO, opacidade=8):
    """Só a silhueta do casal, como marca d'água sutil (opacidade em %)."""
    oficial = _png_oficial()
    if not oficial and not USAR_STANDIN:
        return                               # sem arte oficial: não desenha nada
    c = p.c
    usa_alpha = _tem_alpha(c)
    if usa_alpha:
        c.saveState(); c.setFillAlpha(opacidade / 100.0); c.setStrokeAlpha(opacidade / 100.0)
        tom = cor
    else:                                    # sem alpha: simula com retícula clara
        tom = tinta(cor, opacidade)
    if oficial:
        _imagem(p, oficial, cx, cy, larg, cor, opacidade if usa_alpha else None)
    else:
        _casal_vetor(p, cx, cy, larg, tom)
    if usa_alpha:
        c.restoreState()


def assinatura(p, cx, cy, larg=52.0, cor=PETROLEO, opacidade=22, frase=True):
    """Lockup: silhueta do casal + a frase, centrado em (cx,cy)."""
    s = larg * 0.42
    marca_casal(p, cx, cy + (larg * 0.10 if frase else 0), s, cor, opacidade)
    if frase:
        c = p.c
        usa = _tem_alpha(c)
        if usa:
            c.saveState(); c.setFillAlpha(min(1.0, opacidade / 100.0 * 2.2))
            tom = cor
        else:
            tom = tinta(cor, min(100, int(opacidade * 2.2)))
        p.txt_fit(cx, cy - larg * 0.24, frase if isinstance(frase, str) else FRASE,
                  "Texto", larg * 0.085, larg, tom, "c", tracking=larg * 0.018)
        if usa:
            c.restoreState()


def _imagem(p, caminho, cx, cy, larg, cor, opacidade):
    """Desenha a arte oficial (PNG), tingida em `cor`, centrada em (cx,cy)."""
    from PIL import Image
    from reportlab.lib.utils import ImageReader
    img = Image.open(caminho).convert("L")
    w, h = img.size
    alt = larg * h / w
    # constrói RGBA: pixel escuro -> tinge em `cor`; claro -> transparente
    rgba = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px_src = img.load()
    px_dst = rgba.load()
    rr, gg, bb = _rgb_de_cmyk(cor)
    r, g, b = int(rr * 255), int(gg * 255), int(bb * 255)
    op = (opacidade or 100) / 100.0
    for j in range(h):
        for i in range(w):
            escuro = 255 - px_src[i, j]           # 255 = tinta cheia
            a = int(escuro * op)
            if a:
                px_dst[i, j] = (r, g, b, a)
    c = p.c
    c.drawImage(ImageReader(rgba), cx - larg / 2, cy - alt / 2, larg, alt,
                mask="auto")


# CMYKColor não expõe .red/.green/.blue — helper para o tingimento de imagem
def _rgb_de_cmyk(cor):
    cy_, m, y, k = cor.cyan, cor.magenta, cor.yellow, cor.black
    return ((1 - cy_) * (1 - k), (1 - m) * (1 - k), (1 - y) * (1 - k))


if __name__ == "__main__":
    from comum import Prancha
    out = os.path.join(os.path.dirname(_ASSETS), "_previews", "DIAG-CASAL.pdf")
    W, H = 120.0, 80.0
    p = Prancha(out, W, H, marcas=False)
    p.ret(-5, -5, W + 10, H + 10, fill=CREME)
    # silhueta sólida grande (para conferir o desenho)
    _casal_vetor(p, 30, 45, 46, PETROLEO)
    p.txt(30, 12, "silhueta (solida)", "Texto", 4, PETROLEO, "c")
    # como marca d'água sutil
    p.ret(66, 20, 48, 50, fill=CREME, stroke=tinta(PETROLEO, 30), lw=0.3)
    marca_casal(p, 90, 45, 40, PETROLEO, 12)
    assinatura(p, 90, 30, 44, PETROLEO, 26)
    p.txt(90, 12, "marca d'agua + frase", "Texto", 4, PETROLEO, "c")
    p.salvar()
    print("ok:", out)
