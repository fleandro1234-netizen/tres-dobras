# -*- coding: utf-8 -*-
"""
TRÊS DOBRAS — jogo de tabuleiro para casais
Módulo comum: paleta CMYK, fontes, marcas de impressão, ícones vetoriais e helpers.

Todas as medidas em MILÍMETROS. Origem (0,0) = canto inferior esquerdo da ÁREA
DE CORTE (trim). A sangria vive em coordenadas negativas (-3) e além do trim.
"""
import os
import io
import time
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.colors import CMYKColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

MM = 72.0 / 25.4  # 1 mm em pontos PostScript

# ----------------------------------------------------------------------------
# ESPECIFICAÇÕES DE IMPRESSÃO
# ----------------------------------------------------------------------------
SANGRIA = 3.0          # mm de sangria em todos os lados
SEGURANCA = 8.0        # mm de margem de segurança (tabuleiro)
MARGEM_MARCAS = 12.0   # mm extras na página para as marcas de corte
DOBRA_X = 200.0        # posição do vinco no tabuleiro (eixo vertical)
ZONA_MORTA = 7.0       # mm livres de texto para CADA lado do vinco

# ----------------------------------------------------------------------------
# PALETA CMYK (offset — soma de tinta sempre <= 300%)
# ----------------------------------------------------------------------------
def cmyk(c, m, y, k):
    return CMYKColor(c / 100.0, m / 100.0, y / 100.0, k / 100.0)

PETROLEO  = cmyk(88, 62, 48, 38)   # 236%  azul petróleo — cor institucional
AZUL      = cmyk(75, 40, 22,  3)   # 140%  TEMPO
DOURADO   = cmyk(20, 33,100,  6)   # 159%  PALAVRA
OLIVA     = cmyk(58, 33, 70, 15)   # 176%  PRESENTE
TERRACOTA = cmyk(15, 70, 70,  3)   # 158%  SERVIÇO
VINHO     = cmyk(35, 88, 60, 25)   # 208%  TOQUE
CREME     = cmyk( 4,  5, 12,  0)   #  21%  fundo
AREIA     = cmyk(10, 13, 25,  0)   #  48%  fundo secundário
BRANCO    = cmyk( 0,  0,  0,  0)
PRETO_TXT = cmyk( 0,  0,  0,100)   # texto preto = 100% K puro
PRETO_RICO= cmyk(60, 40, 40,100)   # 240%  áreas grandes de preto
REGISTRO  = CMYKColor(1, 1, 1, 1)  # cor de registro (só marcas, fora do trim)


def tinta(cor, pct):
    """Retícula (tint) de uma cor CMYK — mantém a mesma chapa, só reduz o %."""
    f = pct / 100.0
    return CMYKColor(cor.cyan * f, cor.magenta * f, cor.yellow * f, cor.black * f)


# ----------------------------------------------------------------------------
# NAIPES / LINGUAGENS
# ----------------------------------------------------------------------------
NAIPES = {
    "PALAVRA":  {"nome": "PALAVRA",  "cor": DOURADO,   "sub": "palavras que edificam"},
    "TEMPO":    {"nome": "TEMPO",    "cor": AZUL,      "sub": "tempo de qualidade"},
    "PRESENTE": {"nome": "PRESENTE", "cor": OLIVA,     "sub": "o cuidado que se vê"},
    "SERVICO":  {"nome": "SERVIÇO",  "cor": TERRACOTA, "sub": "amor que arregaça a manga"},
    "TOQUE":    {"nome": "TOQUE",    "cor": VINHO,     "sub": "presença e afeto"},
    "ESPELHO":  {"nome": "ESPELHO",  "cor": PETROLEO,  "sub": "o quanto eu te conheço"},
    "ALTAR":    {"nome": "ALTAR",    "cor": PETROLEO,  "sub": "a terceira dobra"},
    "SELADO":   {"nome": "JARDIM",   "cor": VINHO,     "sub": "só para os dois"},
    "INICIO":   {"nome": "INÍCIO",   "cor": PETROLEO,  "sub": ""},
}

# ----------------------------------------------------------------------------
# FONTES (embutidas no PDF)
# ----------------------------------------------------------------------------
_FONTES = {
    "Titulo":     "pala.ttf",
    "TituloBold": "palab.ttf",
    "TituloIt":   "palai.ttf",
    "Texto":      "corbel.ttf",
    "TextoBold":  "corbelb.ttf",
    "Serif":      "constan.ttf",
    "SerifBold":  "constanb.ttf",
}
_registradas = False


def registrar_fontes():
    global _registradas
    if _registradas:
        return
    base = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
    for nome, arq in _FONTES.items():
        pdfmetrics.registerFont(TTFont(nome, os.path.join(base, arq)))
    _registradas = True


# ----------------------------------------------------------------------------
# CANVAS
# ----------------------------------------------------------------------------
class Prancha:
    """Canvas em milímetros, com origem no canto inferior esquerdo do trim."""

    def __init__(self, caminho, trim_w, trim_h, marcas=True, titulo=""):
        registrar_fontes()
        self.trim_w, self.trim_h = trim_w, trim_h
        self.marcas = marcas
        self.caminho = caminho
        self._buf = io.BytesIO()      # o PDF é montado em memória; ver salvar()
        self.margem = MARGEM_MARCAS if marcas else SANGRIA
        pw = (trim_w + 2 * self.margem) * MM
        ph = (trim_h + 2 * self.margem) * MM
        self.c = rl_canvas.Canvas(self._buf, pagesize=(pw, ph))
        self.c.setTitle(titulo or "TRES DOBRAS")
        self.c.setAuthor("TRES DOBRAS - jogo para casais")
        self.c.translate(self.margem * MM, self.margem * MM)
        self.c.scale(MM, MM)   # a partir daqui, 1 unidade = 1 mm

    # -- primitivas ----------------------------------------------------------
    def ret(self, x, y, w, h, fill=None, stroke=None, lw=0.3, r=None):
        c = self.c
        if fill is not None:
            c.setFillColor(fill)
        if stroke is not None:
            c.setStrokeColor(stroke)
            c.setLineWidth(lw)
        modo_f = 1 if fill is not None else 0
        modo_s = 1 if stroke is not None else 0
        if r:
            c.roundRect(x, y, w, h, r, stroke=modo_s, fill=modo_f)
        else:
            c.rect(x, y, w, h, stroke=modo_s, fill=modo_f)

    def circ(self, x, y, r, fill=None, stroke=None, lw=0.3):
        c = self.c
        if fill is not None:
            c.setFillColor(fill)
        if stroke is not None:
            c.setStrokeColor(stroke)
            c.setLineWidth(lw)
        c.circle(x, y, r, stroke=1 if stroke is not None else 0,
                 fill=1 if fill is not None else 0)

    def linha(self, x1, y1, x2, y2, cor=PETROLEO, lw=0.3, dash=None):
        c = self.c
        c.setStrokeColor(cor)
        c.setLineWidth(lw)
        c.setDash(dash or [])
        c.line(x1, y1, x2, y2)
        c.setDash([])

    # -- texto ---------------------------------------------------------------
    def larg_txt(self, texto, fonte, tam, tracking=0):
        w = pdfmetrics.stringWidth(texto, fonte, tam)
        return w + (tracking * len(texto) if tracking else 0)

    def txt(self, x, y, texto, fonte="Texto", tam=8, cor=PRETO_TXT,
            al="l", tracking=0):
        c = self.c
        c.setFillColor(cor)
        c.setFont(fonte, tam)
        if not tracking:
            if al == "c":
                c.drawCentredString(x, y, texto)
            elif al == "r":
                c.drawRightString(x, y, texto)
            else:
                c.drawString(x, y, texto)
            return
        w = self.larg_txt(texto, fonte, tam, tracking)
        x0 = x - w / 2 if al == "c" else (x - w if al == "r" else x)
        # saveState/restoreState é obrigatório: no PDF o Tc (char space) faz parte
        # do estado gráfico e vazaria para todos os textos seguintes.
        c.saveState()
        to = c.beginText(x0, y)
        to.setFont(fonte, tam)
        to.setCharSpace(tracking)
        to.setFillColor(cor)
        to.textOut(texto)
        c.drawText(to)
        c.restoreState()

    def txt_fit(self, x, y, texto, fonte, tam, larg, cor=PRETO_TXT, al="l",
                tracking=0, tam_min=3.2):
        """Escreve reduzindo o corpo até caber em `larg` mm. Devolve o corpo usado."""
        t, tr = tam, tracking
        while t > tam_min and self.larg_txt(texto, fonte, t, tr) > larg:
            t -= 0.15
            tr = tracking * (t / tam)
        self.txt(x, y, texto, fonte, t, cor, al, tr)
        return t

    def quebrar(self, texto, fonte, tam, larg):
        """Quebra texto em linhas que cabem em `larg` mm."""
        larg_pt = larg
        linhas, cur = [], ""
        for p in texto.split():
            t = (cur + " " + p).strip()
            if pdfmetrics.stringWidth(t, fonte, tam) <= larg_pt or not cur:
                cur = t
            else:
                linhas.append(cur)
                cur = p
        if cur:
            linhas.append(cur)
        return linhas

    def paragrafo(self, x, y, texto, larg, fonte="Texto", tam=8,
                  entrelinha=None, cor=PRETO_TXT, al="l"):
        """Escreve a partir do TOPO (y = topo da primeira linha). Devolve y final."""
        el = entrelinha or tam * 1.25
        linhas = self.quebrar(texto, fonte, tam, larg)
        yy = y - tam * 0.75
        for ln in linhas:
            xx = x + larg / 2 if al == "c" else x
            self.txt(xx, yy, ln, fonte, tam, cor, al)
            yy -= el
        return yy + el - tam * 0.25

    # -- marcas de impressão -------------------------------------------------
    def marcas_corte(self, vinco_x=None, rotulo="", faca=None, vinco=None):
        """faca / vinco: se informados (cores técnicas da peça), desenha na margem
           uma legenda explicando o que é linha de CORTE (destaque) e de DOBRA."""
        if not self.marcas:
            return
        c = self.c
        c.setStrokeColor(REGISTRO)
        c.setLineWidth(0.25)
        W, H, s, L = self.trim_w, self.trim_h, SANGRIA, 6.0
        for (x, y) in [(0, 0), (W, 0), (0, H), (W, H)]:
            dx = -1 if x == 0 else 1
            dy = -1 if y == 0 else 1
            c.line(x, y + dy * s, x, y + dy * (s + L))       # marca vertical
            c.line(x + dx * s, y, x + dx * (s + L), y)       # marca horizontal
        # marca de vinco (dobra)
        if vinco_x is not None:
            c.setDash([1.2, 1.2])
            c.line(vinco_x, -s - 1.5, vinco_x, -s - L - 1.5)
            c.line(vinco_x, H + s + 1.5, vinco_x, H + s + L + 1.5)
            c.setDash([])
            self.txt(vinco_x + 2, H + s + 3.5, "VINCO / DOBRA", "Texto", 4, REGISTRO)
        # barra de registro + rótulo
        self.txt(0, H + s + L + 3, rotulo, "Texto", 4.5, REGISTRO)
        x0 = W - 44
        for i, cor in enumerate([cmyk(100, 0, 0, 0), cmyk(0, 100, 0, 0),
                                 cmyk(0, 0, 100, 0), cmyk(0, 0, 0, 100),
                                 REGISTRO]):
            self.ret(x0 + i * 9, H + s + L + 2, 8, 4, fill=cor)
        # legenda das linhas técnicas — na margem inferior, fora do trim (some
        # quando a gráfica isola/remove as chapas técnicas magenta/ciano).
        if faca is not None or vinco is not None:
            lx, ly = 1.0, -s - 3.5                  # dentro da margem inferior (12 mm)
            if faca is not None:
                c.setStrokeColor(faca); c.setLineWidth(0.7); c.setDash([])
                c.line(lx, ly, lx + 7, ly)
                self.txt(lx + 9, ly - 1.3, "FACA = corte / destaque", "Texto", 3.6, faca)
            if vinco is not None:
                ly2 = ly - (4.0 if faca is not None else 0.0)
                c.setStrokeColor(vinco); c.setLineWidth(0.7); c.setDash([2.0, 1.5])
                c.line(lx, ly2, lx + 7, ly2); c.setDash([])
                self.txt(lx + 9, ly2 - 1.3, "VINCO = dobra / vinco", "Texto", 3.6, vinco)

    def fundo_sangria(self, cor=CREME):
        s = SANGRIA
        self.ret(-s, -s, self.trim_w + 2 * s, self.trim_h + 2 * s, fill=cor)

    def pagina(self, trim_w=None, trim_h=None):
        """Fecha a página e abre a próxima, restaurando a matriz mm + origem no trim.
           Permite trocar o formato da página (peças de tamanhos diferentes)."""
        self.c.showPage()
        if trim_w:
            self.trim_w, self.trim_h = trim_w, trim_h
            self.c.setPageSize(((trim_w + 2 * self.margem) * MM,
                                (trim_h + 2 * self.margem) * MM))
        self.c.translate(self.margem * MM, self.margem * MM)
        self.c.scale(MM, MM)
        return self

    def texto_caixa(self, x, ytop, larg, alt, texto, fonte="Texto", tmax=7.0,
                    tmin=4.6, cor=PRETO_TXT, lead=1.20, al="l", vcenter=False):
        """Encaixa o texto na caixa reduzindo o corpo. Devolve (baseline_final, corpo)."""
        t = tmax
        while t > tmin:
            n = len(self.quebrar(texto, fonte, t, larg))
            if n * t * lead <= alt:
                break
            t -= 0.1
        if vcenter:
            n = len(self.quebrar(texto, fonte, t, larg))
            ytop -= max(0.0, (alt - n * t * lead) / 2.0)
        y = ytop - t * 0.86
        ultima = y
        for ln in self.quebrar(texto, fonte, t, larg):
            self.txt(x + (larg / 2 if al == "c" else 0), y, ln, fonte, t, cor, al)
            ultima = y
            y -= t * lead
        return ultima, t   # baseline da ÚLTIMA linha

    def salvar(self, tentativas=12, espera=0.5):
        """Fecha o PDF em memória e grava em disco.
           A pasta fica no OneDrive: o sincronizador tranca o arquivo logo após a
           escrita, então é preciso reter e reter até o handle liberar."""
        self.c.save()
        dados = self._buf.getvalue()
        erro = None
        for i in range(tentativas):
            try:
                with open(self.caminho, "wb") as f:
                    f.write(dados)
                return self.caminho
            except PermissionError as e:
                erro = e
                time.sleep(espera)
        raise PermissionError(
            f"{self.caminho} continua bloqueado após {tentativas} tentativas. "
            f"Feche o arquivo no Acrobat/visualizador e rode de novo. ({erro})")

    def _salvar_antigo(self):
        self.c.save()


# ----------------------------------------------------------------------------
# ÍCONES VETORIAIS (desenhados centrados em (cx,cy), altura ~ `s` mm)
# ----------------------------------------------------------------------------
def ico_palavra(p, cx, cy, s, cor):
    """Balão de conversa — centrado em (cx,cy)."""
    w, h = s * 0.98, s * 0.70
    by = cy + s * 0.10                       # centro do corpo, pouco acima do eixo
    p.ret(cx - w / 2, by - h / 2, w, h, stroke=cor, lw=s * 0.10, r=h * 0.36)
    c = p.c
    c.setStrokeColor(cor); c.setFillColor(cor); c.setLineWidth(s * 0.10)
    c.setLineJoin(1)
    pth = c.beginPath()
    pth.moveTo(cx - s * 0.22, by - h / 2 + s * 0.03)
    pth.lineTo(cx - s * 0.28, cy - s * 0.50)
    pth.lineTo(cx + s * 0.02, by - h / 2 + s * 0.03)
    c.drawPath(pth, stroke=1, fill=1)
    for dx in (-0.20, 0.0, 0.20):            # reticências = fala
        p.circ(cx + dx * s, by, s * 0.052, fill=cor)


def ico_tempo(p, cx, cy, s, cor):
    """Ampulheta — centrada em (cx,cy)."""
    c = p.c
    lw = s * 0.10
    w, h = s * 0.64, s * 0.88
    top, bot = cy + h / 2, cy - h / 2
    c.setStrokeColor(cor); c.setLineWidth(lw); c.setLineCap(1); c.setLineJoin(1)
    pth = c.beginPath()
    pth.moveTo(cx - w / 2, top); pth.lineTo(cx + w / 2, top)
    pth.lineTo(cx - w / 2, bot); pth.lineTo(cx + w / 2, bot)
    pth.close()
    c.drawPath(pth, stroke=1, fill=0)
    p.linha(cx - w / 2 - s * 0.11, top, cx + w / 2 + s * 0.11, top, cor, lw * 1.05)
    p.linha(cx - w / 2 - s * 0.11, bot, cx + w / 2 + s * 0.11, bot, cor, lw * 1.05)
    c.setFillColor(cor)                      # areia acumulada embaixo
    pth = c.beginPath()
    pth.moveTo(cx - w * 0.30, bot + s * 0.03); pth.lineTo(cx + w * 0.30, bot + s * 0.03)
    pth.lineTo(cx, cy - s * 0.02); pth.close()
    c.drawPath(pth, stroke=0, fill=1)


def ico_presente(p, cx, cy, s, cor):
    """Caixa de presente — centrada em (cx,cy)."""
    w, h = s * 0.86, s * 0.60
    box_b = cy - s * 0.42
    p.ret(cx - w / 2, box_b, w, h, stroke=cor, lw=s * 0.10, r=s * 0.05)
    p.linha(cx, box_b, cx, box_b + h, cor, s * 0.10)              # fita vertical
    p.linha(cx - w / 2, box_b + h * 0.60, cx + w / 2, box_b + h * 0.60, cor, s * 0.10)
    ly = box_b + h + s * 0.11                                     # laço acima
    p.circ(cx - s * 0.155, ly, s * 0.135, stroke=cor, lw=s * 0.09)
    p.circ(cx + s * 0.155, ly, s * 0.135, stroke=cor, lw=s * 0.09)


def ico_servico(p, cx, cy, s, cor):
    """Mão aberta — atos de serviço. Centrada em (cx,cy)."""
    c = p.c
    c.setFillColor(cor)
    # palma
    pw, ph = s * 0.50, s * 0.40
    palm_b = cy - s * 0.45
    p.ret(cx - pw / 2, palm_b, pw, ph, fill=cor, r=s * 0.13)
    # quatro dedos, base sobreposta à palma, pontas em arco natural
    base_y = cy - s * 0.10
    for dx, tp in ((-0.195, 0.22), (-0.065, 0.40), (0.065, 0.33), (0.195, 0.16)):
        top_y = cy + tp * s
        p.ret(cx + dx * s - s * 0.054, base_y, s * 0.108, top_y - base_y,
              fill=cor, r=s * 0.054)
    # polegar — maior e inclinado
    c.saveState()
    c.translate(cx - s * 0.22, cy - s * 0.32); c.rotate(43)
    p.ret(-s * 0.06, 0, s * 0.12, s * 0.36, fill=cor, r=s * 0.06)
    c.restoreState()


def _coracao(c, cx, cy, s, cor, preencher=True, lw=None):
    c.setFillColor(cor); c.setStrokeColor(cor)
    c.setLineWidth(lw if lw else s * 0.14); c.setLineJoin(1)
    pth = c.beginPath()
    pth.moveTo(cx, cy - s * 0.42)
    pth.curveTo(cx - s * 0.95, cy + s * 0.22, cx - s * 0.36, cy + s * 0.86, cx, cy + s * 0.30)
    pth.curveTo(cx + s * 0.36, cy + s * 0.86, cx + s * 0.95, cy + s * 0.22, cx, cy - s * 0.42)
    pth.close()
    c.drawPath(pth, stroke=0 if preencher else 1, fill=1 if preencher else 0)


def ico_toque(p, cx, cy, s, cor):
    """Duas alianças entrelaçadas — centradas em (cx,cy)."""
    r = s * 0.32
    off = r * 0.62
    p.circ(cx - off, cy, r, stroke=cor, lw=s * 0.11)
    p.circ(cx + off, cy, r, stroke=cor, lw=s * 0.11)


def ico_espelho(p, cx, cy, s, cor):
    """Espelho de mão — o quanto eu te conheço. Centrado em (cx,cy)."""
    c = p.c
    gy = cy + s * 0.16                        # centro do vidro
    rg = s * 0.34
    c.saveState()
    c.translate(cx, gy); c.scale(0.82, 1.0); c.translate(-cx, -gy)
    p.circ(cx, gy, rg, stroke=cor, lw=s * 0.10)
    p.circ(cx, gy, rg - s * 0.12, fill=tinta(cor, 18))
    c.restoreState()
    # cabo
    p.ret(cx - s * 0.05, cy - s * 0.46, s * 0.10, s * 0.30, fill=cor, r=s * 0.05)
    p.ret(cx - s * 0.12, cy - s * 0.50, s * 0.24, s * 0.08, fill=cor, r=s * 0.04)
    # brilho (arco fino no vidro)
    c.setStrokeColor(cor); c.setLineWidth(s * 0.05); c.setLineCap(1)
    pth = c.beginPath()
    pth.moveTo(cx - s * 0.13, gy + s * 0.03)
    pth.curveTo(cx - s * 0.17, gy + s * 0.15, cx - s * 0.05, gy + s * 0.21,
                cx + s * 0.03, gy + s * 0.20)
    c.drawPath(pth, stroke=1, fill=0)


def ico_altar(p, cx, cy, s, cor):
    """Cruz latina — centrada em (cx,cy)."""
    e = s * 0.16
    p.ret(cx - e / 2, cy - s * 0.50, e, s * 1.00, fill=cor)
    p.ret(cx - s * 0.34, cy + s * 0.14, s * 0.68, e, fill=cor)


def ico_inicio(p, cx, cy, s, cor):
    """Coração — o começo, a dois. Centrado em (cx,cy)."""
    _coracao(p.c, cx, cy - s * 0.04, s * 0.78, cor, preencher=False)


ICONES = {
    "PALAVRA": ico_palavra, "TEMPO": ico_tempo, "PRESENTE": ico_presente,
    "SERVICO": ico_servico, "TOQUE": ico_toque, "ESPELHO": ico_espelho,
    "ALTAR": ico_altar, "INICIO": ico_inicio, "SELADO": ico_toque,
}


# ----------------------------------------------------------------------------
# CORDÃO DE TRÊS DOBRAS (trança decorativa — SEM texto, pode cruzar o vinco)
# ----------------------------------------------------------------------------
def cordao_vertical(p, x, y0, y1, larg, cores=(DOURADO, TERRACOTA, PETROLEO),
                    lw=0.9, passos=340, ciclos=None):
    """Três fios trançados no eixo vertical, centrados em x."""
    import math
    c = p.c
    n = ciclos or max(4, int((y1 - y0) / 26))
    c.setLineWidth(lw)
    c.setLineCap(1)
    for i, cor in enumerate(cores):
        c.setStrokeColor(cor)
        fase = i * 2.0 * math.pi / 3.0
        pth = c.beginPath()
        for k in range(passos + 1):
            t = k / passos
            yy = y0 + (y1 - y0) * t
            xx = x + (larg / 2.0) * math.sin(2 * math.pi * n * t + fase)
            pth.moveTo(xx, yy) if k == 0 else pth.lineTo(xx, yy)
        c.drawPath(pth, stroke=1, fill=0)


def cordao_horizontal(p, y, x0, x1, alt, cores=(DOURADO, TERRACOTA, PETROLEO),
                      lw=0.9, passos=260, ciclos=None):
    import math
    c = p.c
    n = ciclos or max(2, int((x1 - x0) / 26))
    c.setLineWidth(lw)
    c.setLineCap(1)
    for i, cor in enumerate(cores):
        c.setStrokeColor(cor)
        fase = i * 2.0 * math.pi / 3.0
        pth = c.beginPath()
        for k in range(passos + 1):
            t = k / passos
            xx = x0 + (x1 - x0) * t
            yy = y + (alt / 2.0) * math.sin(2 * math.pi * n * t + fase)
            pth.moveTo(xx, yy) if k == 0 else pth.lineTo(xx, yy)
        c.drawPath(pth, stroke=1, fill=0)


def logo(p, cx, cy, s=1.0, cor=PETROLEO, cor2=DOURADO, com_versiculo=False,
         larg=None):
    """Marca do jogo, centrada. `s` = escala; `larg` limita a largura em mm."""
    if larg:
        t = p.txt_fit(cx, cy, "TRÊS DOBRAS", "TituloBold", 13 * s, larg, cor, "c",
                      tracking=1.6 * s)
        s = t / 13.0
    else:
        p.txt(cx, cy, "TRÊS DOBRAS", "TituloBold", 13 * s, cor, "c", tracking=1.6 * s)
    p.linha(cx - 21 * s, cy - 3.4 * s, cx - 5 * s, cy - 3.4 * s, cor2, 0.5 * s)
    p.linha(cx + 5 * s, cy - 3.4 * s, cx + 21 * s, cy - 3.4 * s, cor2, 0.5 * s)
    ico_altar(p, cx, cy - 3.2 * s, 4.4 * s, cor2)
    if com_versiculo:
        p.txt(cx, cy - 10 * s, "ECLESIASTES 4.12", "Texto", 4.6 * s, cor2, "c",
              tracking=1.1 * s)
