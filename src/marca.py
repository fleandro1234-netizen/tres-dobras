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


def _png_arquivo(base):
    for ext in (".png", ".PNG", ".jpg", ".jpeg"):
        cam = os.path.join(_ASSETS, base + ext)
        if os.path.exists(cam):
            return cam
    return None


def _png_oficial():
    return _png_arquivo("casal")


def marca_logo(p, cx, cy, larg=60.0, cor=PETROLEO, opacidade=90):
    """Letreiro 'Casados para a Glória de Deus' (assets/logo.png), tingido."""
    cam = _png_arquivo("logo")
    if cam:
        _imagem(p, cam, cx, cy, larg, cor, opacidade)


# ---------------------------------------------------------------------------
# Silhueta vetorial do casal (fallback) — desenhada num quadrado ~[-0.5,0.5],
# centro em (cx,cy), altura = s. Dois perfis frente a frente sobre uma base
# de mãos em concha.
# ---------------------------------------------------------------------------
def _suave(c, pts, X, Y):
    """Curva fechada e suave passando por TODOS os âncoras (Catmull-Rom→Bézier)."""
    n = len(pts)
    def P(i): return pts[i % n]
    pth = c.beginPath()
    pth.moveTo(X(P(0)[0]), Y(P(0)[1]))
    for i in range(n):
        p0, p1, p2, p3 = P(i - 1), P(i), P(i + 1), P(i + 2)
        c1 = (p1[0] + (p2[0] - p0[0]) / 6.0, p1[1] + (p2[1] - p0[1]) / 6.0)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6.0, p2[1] - (p3[1] - p1[1]) / 6.0)
        pth.curveTo(X(c1[0]), Y(c1[1]), X(c2[0]), Y(c2[1]), X(p2[0]), Y(p2[1]))
    pth.close()
    c.drawPath(pth, stroke=0, fill=1)


# Traçado fiel da figura oficial "Casados para a Glória de Deus".
# Âncoras lidas na imagem de referência 1080x1080 (x→direita, y→BAIXO);
# um único contorno (o vão central é aberto no topo, entre os narizes).
_CX_IMG, _CY_IMG, _ESC = 537.0, 512.0, 1035.0
_CASAL_IMG = [
    (585, 150), (700, 158), (785, 205), (828, 300), (838, 378),     # coroa/nuca dele
    (846, 400), (856, 406), (856, 434), (812, 432), (818, 454),     # gola
    (833, 505), (895, 548), (985, 585), (1050, 632),                # ombro → folha dir.
    (1000, 715), (905, 808), (838, 862), (768, 815), (712, 762),    # folha dir. embaixo
    (620, 822), (470, 830), (330, 808), (195, 772),                 # base
    (95, 752), (30, 742), (48, 712),                                # folha esq.
    (95, 672), (128, 592), (150, 512), (185, 455), (232, 428),      # nuca dela (fora)
    (300, 418), (352, 420),                                         # topo cabeça dela
    (388, 398), (405, 420),                                         # cachinho da testa
    (418, 452), (432, 486), (452, 505),                             # testa/sobrancelha
    (500, 520), (470, 536),                                         # nariz dela
    (482, 556), (460, 566), (476, 582),                            # boca dela
    (450, 598), (432, 620),                                        # queixo dela
    (435, 672), (458, 728),                                        # pescoço dela → base
    (540, 772), (612, 758),                                        # base topo (vão central)
    (642, 712), (620, 632), (616, 602),                           # queixo dele
    (598, 584), (582, 566), (600, 548),                           # boca dele
    (585, 530), (556, 514),                                        # nariz dele
    (570, 488), (574, 462), (562, 428),                           # testa dele
    (550, 388), (508, 356), (462, 326),                           # franja até a ponta
    (502, 344), (540, 300), (556, 232), (562, 185),               # topete → coroa
]


def _casal_vetor(p, cx, cy, s, cor):
    """Desenha a figura oficial do casal, centrada em (cx,cy), largura = s.
       (altura ≈ 0.70·s). Curva suave sobre o traçado da referência."""
    c = p.c
    c.setFillColor(cor)
    c.setLineJoin(1); c.setLineCap(1)
    def X(u): return cx + u * s
    def Y(v): return cy + v * s
    uv = [((x - _CX_IMG) / _ESC, (_CY_IMG - y) / _ESC) for (x, y) in _CASAL_IMG]
    _suave(c, uv, X, Y)


def _tem_alpha(c):
    return hasattr(c, "setFillAlpha")


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------
def marca_casal(p, cx, cy, larg=26.0, cor=PETROLEO, opacidade=8):
    """Marca do casal, sutil. Usa o PNG oficial (assets/casal.png) se existir;
       senão, o traçado vetorial fiel da figura."""
    oficial = _png_oficial()
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


# limiares do fundo do JPEG (cinza-claro ~239) → transparente; escuro → tinta
_LIMIAR_HI, _LIMIAR_LO = 205, 90
_CACHE_IMG = {}


def _rgba_tingido(caminho, cor, opacidade):
    """RGBA da arte tingida em `cor` na opacidade dada, com fundo removido.
       Cacheado por (arquivo, mtime, cor, opacidade) — roda em 60 cartas."""
    from PIL import Image
    rr, gg, bb = _rgb_de_cmyk(cor)
    r, g, b = int(rr * 255), int(gg * 255), int(bb * 255)
    op = (opacidade or 100) / 100.0
    chave = (caminho, os.path.getmtime(caminho), r, g, b, round(op, 3))
    if chave in _CACHE_IMG:
        return _CACHE_IMG[chave]
    img = Image.open(caminho).convert("L")
    # LUT: mapeia cinza -> alfa (soft-threshold), já com a opacidade embutida
    lut = []
    for tom in range(256):
        if tom >= _LIMIAR_HI:
            frac = 0.0
        elif tom <= _LIMIAR_LO:
            frac = 1.0
        else:
            frac = (_LIMIAR_HI - tom) / (_LIMIAR_HI - _LIMIAR_LO)
        lut.append(int(frac * 255 * op))
    alpha = img.point(lut).convert("L")
    rgba = Image.new("RGBA", img.size, (r, g, b, 0))
    rgba.putalpha(alpha)
    _CACHE_IMG[chave] = rgba
    return rgba


def _imagem(p, caminho, cx, cy, larg, cor, opacidade):
    """Desenha a arte oficial, tingida em `cor`, centrada em (cx,cy)."""
    from reportlab.lib.utils import ImageReader
    rgba = _rgba_tingido(caminho, cor, opacidade)
    w, h = rgba.size
    alt = larg * h / w
    p.c.drawImage(ImageReader(rgba), cx - larg / 2, cy - alt / 2, larg, alt,
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
