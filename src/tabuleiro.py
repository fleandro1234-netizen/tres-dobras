# -*- coding: utf-8 -*-
"""
TRÊS DOBRAS — TABULEIRO
Formato final 400 x 300 mm · vinco vertical em x = 200 mm (200 + 200)
Sangria 3 mm · 300 dpi equivalente (arte 100% vetorial)
Zona morta do vinco: 7 mm para cada lado — nenhum texto, número ou ícone entra ali.
"""
import os
from comum import *
from dados import (TRILHA, VERSICULO, VERSICULO_REF, PACTO, REGRAS_RESUMO)
from marca import marca_casal, assinatura

W, H = 400.0, 300.0
CEL = 26.0          # lado da casa
RCEL = 4.0          # raio da casa

# --------------------------------------------------------------------------
# Geometria da trilha (30 casas, sentido horário, INÍCIO no canto inf. esq.)
# --------------------------------------------------------------------------
XS_ESQ = [32.0, 64.0, 96.0, 128.0, 160.0]
XS_DIR = [240.0, 272.0, 304.0, 336.0, 368.0]
YS_COL = [71.3, 110.7, 150.0, 189.3, 228.7]
Y_TOPO, Y_BASE = 268.0, 32.0
X_COL_E, X_COL_D = 32.0, 368.0


def posicoes():
    p = [(X_COL_E, Y_BASE)]                       # 1  INÍCIO
    p += [(X_COL_E, y) for y in YS_COL]           # 2-6   sobe pela esquerda
    p += [(X_COL_E, Y_TOPO)]                      # 7     canto sup. esq.
    p += [(x, Y_TOPO) for x in XS_ESQ[1:]]        # 8-11  topo, metade esquerda
    p += [(x, Y_TOPO) for x in XS_DIR[:-1]]       # 12-15 topo, metade direita
    p += [(X_COL_D, Y_TOPO)]                      # 16    canto sup. dir.
    p += [(X_COL_D, y) for y in reversed(YS_COL)] # 17-21 desce pela direita
    p += [(X_COL_D, Y_BASE)]                      # 22    canto inf. dir.
    p += [(x, Y_BASE) for x in reversed(XS_DIR[:-1])]   # 23-26 base, direita
    p += [(x, Y_BASE) for x in reversed(XS_ESQ[1:])]    # 27-30 base, esquerda
    return p


POS = posicoes()
assert len(POS) == 30 == len(TRILHA), (len(POS), len(TRILHA))

# Verificação da zona morta do vinco: nenhuma casa pode encostar nela.
for (x, y) in POS:
    assert x + CEL / 2 <= DOBRA_X - ZONA_MORTA or x - CEL / 2 >= DOBRA_X + ZONA_MORTA, \
        f"Casa em x={x} invade a zona morta do vinco"


# --------------------------------------------------------------------------
def moldura(p):
    p.fundo_sangria(CREME)
    # textura suave de fundo nas duas metades
    p.ret(-SANGRIA, -SANGRIA, W + 2 * SANGRIA, H + 2 * SANGRIA, fill=CREME)
    p.ret(10, 10, W - 20, H - 20, stroke=tinta(DOURADO, 70), lw=0.6)
    p.ret(12.5, 12.5, W - 25, H - 25, stroke=tinta(PETROLEO, 35), lw=0.25)
    # cantos ornamentais
    for (cx, cy, sx, sy) in [(10, 10, 1, 1), (W - 10, 10, -1, 1),
                             (10, H - 10, 1, -1), (W - 10, H - 10, -1, -1)]:
        p.linha(cx + sx * 4, cy + sy * 4, cx + sx * 4, cy + sy * 13, tinta(DOURADO, 70), 0.6)
        p.linha(cx + sx * 4, cy + sy * 4, cx + sx * 13, cy + sy * 4, tinta(DOURADO, 70), 0.6)


def casa(p, i, x, y, tipo):
    cor = NAIPES[tipo]["cor"]
    if tipo == "INICIO":
        p.ret(x - CEL / 2, y - CEL / 2, CEL, CEL, fill=PETROLEO, r=RCEL)
        ICONES["INICIO"](p, x, y + 2.6, 11.5, DOURADO)
        p.txt(x, y - 9.6, "INÍCIO", "TextoBold", 6.2, BRANCO, "c", tracking=0.7)
        return
    p.ret(x - CEL / 2, y - CEL / 2, CEL, CEL, fill=tinta(cor, 13), r=RCEL)
    p.ret(x - CEL / 2, y - CEL / 2, CEL, CEL, stroke=cor, lw=0.7, r=RCEL)
    ICONES[tipo](p, x, y + 1.8, 12.0, cor)
    p.txt_fit(x, y - 10.4, NAIPES[tipo]["nome"], "TextoBold", 4.8, CEL - 5.0,
              cor, "c", tracking=0.45)
    # número da casa — PADRÃO único em todas: círculo petróleo, número branco,
    # borda dourada. (antes cada um usava a cor do naipe, sem padrão.)
    bx, by = x - CEL / 2 + 4.0, y + CEL / 2 - 4.0
    p.circ(bx, by, 2.9, fill=PETROLEO)
    p.circ(bx, by, 2.9, stroke=tinta(DOURADO, 90), lw=0.35)
    p.txt_fit(bx, by - 1.55, str(i), "TextoBold", 4.6, 4.4, BRANCO, "c")


def seta(p, x, y, ang):
    """Triângulo indicando o sentido da caminhada."""
    c = p.c
    c.saveState(); c.translate(x, y); c.rotate(ang)
    c.setFillColor(tinta(DOURADO, 90))
    pth = c.beginPath()
    pth.moveTo(2.6, 0); pth.lineTo(-1.8, 2.3); pth.lineTo(-1.8, -2.3); pth.close()
    c.drawPath(pth, stroke=0, fill=1)
    c.restoreState()


def painel_esquerdo(p):
    """Metade esquerda: marca, versículo, Altar (chegada) e resumo das regras.
       Limites rígidos: x 56..172 — nada encosta no vinco (x=200)."""
    x0, x1 = 56.0, 172.0
    cx = (x0 + x1) / 2
    LARG = x1 - x0

    # ---- marca ------------------------------------------------------------
    p.txt_fit(cx, 233, "TRÊS", "TituloBold", 25, LARG - 4, PETROLEO, "c", tracking=4.0)
    p.txt_fit(cx, 213, "DOBRAS", "TituloBold", 25, LARG - 4, PETROLEO, "c", tracking=4.0)
    p.linha(x0 + 6, 206, cx - 6, 206, tinta(DOURADO, 80), 0.5)
    p.linha(cx + 6, 206, x1 - 6, 206, tinta(DOURADO, 80), 0.5)
    ico_altar(p, cx, 206.2, 6.4, DOURADO)
    p.txt_fit(cx, 196, "UM JOGO PARA CASAIS", "Texto", 6.2, LARG - 10,
              tinta(PETROLEO, 70), "c", tracking=2.2)

    # ---- versículo --------------------------------------------------------
    y = 186
    for ln in p.quebrar(VERSICULO, "TituloIt", 7.0, LARG - 8):
        p.txt_fit(cx, y, ln, "TituloIt", 7.0, LARG - 8, tinta(PETROLEO, 88), "c")
        y -= 8.0
    p.txt_fit(cx, y + 0.5, VERSICULO_REF, "Texto", 5.2, LARG - 20, DOURADO, "c",
              tracking=1.6)

    # ---- ALTAR (chegada) --------------------------------------------------
    #  texto travado dentro da corda do círculo, para nada escapar do símbolo
    ay, ar = 137.0, 27.5
    import math as _m
    def _corda(dy):                          # largura útil do círculo à altura dy
        return 2.0 * _m.sqrt(max(0.0, ar ** 2 - dy ** 2)) - 5.0
    p.circ(cx, ay, ar + 3.0, stroke=tinta(DOURADO, 60), lw=0.5)
    p.circ(cx, ay, ar, fill=PETROLEO)
    ico_altar(p, cx, ay + 8.0, 17.0, DOURADO)
    p.txt_fit(cx, ay - 8.5, "ALTAR", "TituloBold", 10.0, _corda(8.5), BRANCO, "c",
              tracking=1.6)
    p.txt_fit(cx, ay - 16.0, "A TERCEIRA DOBRA", "Texto", 4.6, _corda(19.0),
              tinta(DOURADO, 90), "c", tracking=1.1)
    p.txt_fit(cx, 101, "chegada · completem a volta e venham para cá", "TituloIt",
              6.0, LARG - 6, tinta(PETROLEO, 70), "c")

    # ---- resumo das regras ------------------------------------------------
    p.linha(x0 + 14, 94, x1 - 14, 94, tinta(DOURADO, 70), 0.5)
    p.txt(cx, 88, "COMO JOGAR", "TextoBold", 6.2, PETROLEO, "c", tracking=1.8)
    y = 80.5
    for n, txt in REGRAS_RESUMO:
        p.circ(x0 + 3.4, y + 0.9, 2.3, fill=tinta(PETROLEO, 85))
        p.txt(x0 + 3.4, y + 0.1, n, "TextoBold", 4.1, BRANCO, "c")
        p.txt_fit(x0 + 8.0, y, txt, "Texto", 5.3, LARG - 9.0, tinta(PETROLEO, 80))
        y -= 5.5
    assert y + 5.5 >= 52.0, "resumo das regras invade a fileira inferior de casas"


def painel_direito(p):
    """Metade direita: o Mapa das Cinco Linguagens (diagnóstico do casal).
       Limites rígidos: x 228..344."""
    x0, x1 = 228.0, 344.0
    cx = (x0 + x1) / 2
    p.txt_fit(cx, 240, "MAPA DAS CINCO LINGUAGENS", "TextoBold", 6.4, x1 - x0,
              PETROLEO, "c", tracking=1.5)
    p.txt_fit(cx, 232.5, "plantem uma semente a cada carta cumprida", "TituloIt", 5.8,
              x1 - x0 - 4, tinta(PETROLEO, 70), "c")

    ys = [206.0, 171.0, 136.0, 101.0, 66.0]
    ALT = 31.0
    for tipo, y in zip(["PALAVRA", "TEMPO", "PRESENTE", "SERVICO", "TOQUE"], ys):
        cor = NAIPES[tipo]["cor"]
        p.ret(x0, y - ALT / 2, x1 - x0, ALT, fill=tinta(cor, 9), r=4)
        p.ret(x0, y - ALT / 2, x1 - x0, ALT, stroke=tinta(cor, 85), lw=0.6, r=4)
        p.circ(x0 + 15.5, y, 11.0, fill=BRANCO)
        p.circ(x0 + 15.5, y, 11.0, stroke=tinta(cor, 55), lw=0.4)
        ICONES[tipo](p, x0 + 15.5, y, 13.0, cor)
        tx = x0 + 31.5
        larg = x1 - tx - 5
        p.txt_fit(tx, y + 8.0, NAIPES[tipo]["nome"], "TextoBold", 8.2, larg, cor,
                  tracking=1.0)
        p.txt_fit(tx, y + 1.2, NAIPES[tipo]["sub"], "TituloIt", 5.8, larg,
                  tinta(PETROLEO, 75))
        for k in range(5):
            p.circ(tx + 3.4 + k * 8.0, y - 7.6, 3.0, stroke=tinta(cor, 70), lw=0.45)


def cordao_central(p):
    # trança vertical sobre o vinco (decoração pura: nenhum texto)
    cordao_vertical(p, DOBRA_X, 50, 250, 9.0,
                    (tinta(DOURADO, 80), tinta(TERRACOTA, 55), tinta(PETROLEO, 45)),
                    lw=0.85)
    # trança horizontal fechando a trilha no topo e na base
    for y in (Y_TOPO, Y_BASE):
        cordao_horizontal(p, y, 174, 226, 8.0,
                          (tinta(DOURADO, 80), tinta(TERRACOTA, 55), tinta(PETROLEO, 45)),
                          lw=0.85, ciclos=2)


def frente(p):
    moldura(p)
    cordao_central(p)
    for i, ((x, y), tipo) in enumerate(zip(POS, TRILHA), start=1):
        casa(p, i, x, y, tipo)
    # setas de sentido
    seta(p, X_COL_E, (YS_COL[1] + YS_COL[2]) / 2, 90)
    seta(p, (XS_DIR[1] + XS_DIR[2]) / 2, Y_TOPO + 16.5, 0)
    seta(p, X_COL_D, (YS_COL[1] + YS_COL[2]) / 2, 270)
    seta(p, (XS_ESQ[1] + XS_ESQ[2]) / 2, Y_BASE - 16.5, 180)
    painel_esquerdo(p)
    painel_direito(p)
    # marca d'água grande e bem transparente, POR CIMA de tudo (overlay uniforme)
    marca_casal(p, 200, 152, 205, PETROLEO, 15)
    p.marcas_corte(vinco_x=DOBRA_X, rotulo="TRES DOBRAS · TABULEIRO · FRENTE · 400x300mm · sangria 3mm · CMYK")


BLOCOS_REGRAS = [
    ("O QUE É", "Um jogo cooperativo. Vocês não competem entre si — caminham juntos, "
                "com um único peão, até o Altar."),
    ("PREPARO", "Separem as cartas por cor e ponham o peão no INÍCIO. Decidam juntos "
                "o NÍVEL: 1 para começar, 2 para se abrir, 3 para aprofundar. Podem "
                "subir de nível quando quiserem."),
    ("NA SUA VEZ", "Rolem o dado e avancem. Puxem a carta da cor da casa e leiam a "
                   "pergunta do nível escolhido. Responde quem parou ali; na rodada "
                   "seguinte, o outro."),
    ("A SEMENTE", "Cumpriram a carta? Marquem uma semente no canteiro daquela "
                  "linguagem, no Mapa. Ninguém confere nada: a única regra é a "
                  "honestidade."),
    ("ESPELHO", "Você responde PELO seu cônjuge, sem perguntar. Acertou? Andem duas "
                "casas. Errou? Ele(a) conta a resposta — e essa é a melhor parte: "
                "plantem uma semente na linguagem que ele(a) escolher."),
    ("O ALTAR", "Completada a volta, vão ao Altar. Quatro cartas: Gratidão, Perdão, "
                "Bênção e Pacto. Não corram: é aqui que o jogo vira casamento."),
    ("O MAPA", "No fim, olhem os canteiros. O que ficou vazio é a linguagem que "
               "vocês têm negligenciado. Escolham uma e cuidem dela neste mês."),
    ("O ENVELOPE", "O envelope lacrado é só para casais casados e não se abre aqui. "
                   "Levem-no para casa e abram a sós."),
]


def verso(p):
    p.fundo_sangria(PETROLEO)
    # faixa clara sobre o vinco: reduz a carga de tinta na dobra (evita trincar)
    p.ret(DOBRA_X - 15, -SANGRIA, 30, H + 2 * SANGRIA, fill=CREME)
    p.linha(DOBRA_X - 15, -SANGRIA, DOBRA_X - 15, H + SANGRIA, tinta(DOURADO, 70), 0.4)
    p.linha(DOBRA_X + 15, -SANGRIA, DOBRA_X + 15, H + SANGRIA, tinta(DOURADO, 70), 0.4)
    cordao_vertical(p, DOBRA_X, 16, 284, 10.0,
                    (tinta(DOURADO, 85), tinta(TERRACOTA, 60), tinta(PETROLEO, 45)),
                    lw=0.85)
    p.ret(10, 10, DOBRA_X - 25, H - 20, stroke=tinta(DOURADO, 70), lw=0.5)
    p.ret(DOBRA_X + 15, 10, W - 25 - DOBRA_X, H - 20, stroke=tinta(DOURADO, 70), lw=0.5)

    # ------- metade esquerda: O PACTO -------------------------------------
    x0, x1 = 24.0, 172.0
    cx = (x0 + x1) / 2
    p.txt(cx, 256, "O PACTO", "TituloBold", 19, DOURADO, "c", tracking=3.2)
    p.linha(cx - 28, 248, cx + 28, 248, tinta(DOURADO, 80), 0.5)

    y = 231
    for i, frase in enumerate(PACTO):
        fonte, tam = ("TituloIt", 9.0) if i == 0 else ("Texto", 8.2)
        cor = DOURADO if i == 0 else BRANCO
        for ln in p.quebrar(frase, fonte, tam, x1 - x0 - 10):
            p.txt(cx, y, ln, fonte, tam, cor, "c")
            y -= tam * 1.42
        y -= 5.0

    # marca do casal no vão entre o Pacto e as assinaturas — o pacto é do
    # casal diante de Deus, então aqui a silhueta é conteúdo, não só marca d'água.
    vao = y - 90.0
    tam_marca = max(11.0, min(15.0, vao * 0.78))
    marca_casal(p, cx, (y + 90) / 2.0, tam_marca, DOURADO, 90)

    p.txt(cx, 84, "ASSINAMOS HOJE, JUNTOS", "Texto", 5.6, DOURADO, "c", tracking=1.6)
    for k, rot in enumerate(["ELE", "ELA"]):
        yy = 64 - k * 20
        p.linha(x0 + 8, yy, x1 - 8, yy, tinta(DOURADO, 70), 0.5)
        p.txt(x0 + 8, yy - 5.6, rot, "Texto", 5.0, tinta(DOURADO, 90), tracking=1.4)
    p.linha(x0 + 8, 24, x0 + 66, 24, tinta(DOURADO, 70), 0.5)
    p.txt(x0 + 8, 18.4, "DATA", "Texto", 5.0, tinta(DOURADO, 90), tracking=1.4)

    # ------- metade direita: REGRAS COMPLETAS (2 colunas) -----------------
    rx0, rx1 = 222.0, 386.0
    p.txt(rx1, 256, "AS REGRAS", "TituloBold", 19, DOURADO, "r", tracking=3.0)
    p.linha(rx0, 248, rx1, 248, tinta(DOURADO, 80), 0.5)

    COL = 78.0
    colunas = [(rx0, BLOCOS_REGRAS[:4]), (rx0 + COL + 8, BLOCOS_REGRAS[4:])]
    for cx0, blocos in colunas:
        y = 236
        for tit, txt in blocos:
            p.txt(cx0, y, tit, "TextoBold", 6.2, DOURADO, tracking=1.1)
            y -= 7.4
            for ln in p.quebrar(txt, "Texto", 6.0, COL):
                p.txt(cx0, y, ln, "Texto", 6.0, BRANCO)
                y -= 6.9
            y -= 4.2
        assert y >= 16.0, f"coluna de regras estourou (y={y:.1f})"

    p.marcas_corte(vinco_x=DOBRA_X, rotulo="TRES DOBRAS · TABULEIRO · VERSO · 400x300mm · sangria 3mm · CMYK")


def gerar(destino, marcas=True):
    p = Prancha(destino, W, H, marcas=marcas, titulo="TRES DOBRAS - Tabuleiro")
    frente(p)
    p.c.showPage(); p.c.translate(p.margem * MM, p.margem * MM); p.c.scale(MM, MM)
    verso(p)
    p.salvar()
    return destino


if __name__ == "__main__":
    base = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "01-TABULEIRO")
    os.makedirs(base, exist_ok=True)
    print(gerar(os.path.join(base, "TABULEIRO_400x300_COM-MARCAS.pdf"), marcas=True))
    print(gerar(os.path.join(base, "TABULEIRO_400x300_SANGRIA-3mm.pdf"), marcas=False))
