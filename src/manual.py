# -*- coding: utf-8 -*-
"""
Gera o MANUAL INTERATIVO (HTML autônomo) do jogo TRÊS DOBRAS.
Imagens embutidas em base64; textos das cartas vêm de dados.py (fonte única).
"""
import os, json
import imagens_web
from dados import (LINGUAGENS, ESPELHO, ALTAR, SELADO, NIVEIS,
                   TRILHA, REGRAS_RESUMO)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(RAIZ, "MANUAL-TRES-DOBRAS.html")

NAIPE_INFO = {
    "PALAVRA":  ("PALAVRA",  "palavras que edificam",      "#C9A227"),
    "TEMPO":    ("TEMPO",    "tempo de qualidade",         "#2A6F8E"),
    "PRESENTE": ("PRESENTE", "o cuidado que se vê",        "#6B7F5C"),
    "SERVICO":  ("SERVIÇO",  "amor que arregaça a manga",  "#C4664F"),
    "TOQUE":    ("TOQUE",    "presença e afeto",           "#8C3A4A"),
    "ESPELHO":  ("ESPELHO",  "o quanto eu te conheço",     "#10323F"),
    "ALTAR":    ("ALTAR",    "a terceira dobra",           "#C9A227"),
    "SELADO":   ("JARDIM",   "só para os dois",            "#8C3A4A"),
}
SIGLAS = {"PALAVRA": "PAL", "TEMPO": "TEM", "PRESENTE": "PRE",
          "SERVICO": "SER", "TOQUE": "TOQ"}


def montar_cartas():
    cartas = []
    for tipo, lista in LINGUAGENS:
        for i, niveis in enumerate(lista, start=1):
            cartas.append({"naipe": tipo, "id": f"{SIGLAS[tipo]} {i:02d}",
                           "niveis": list(niveis)})
    for i, q in enumerate(ESPELHO, start=1):
        cartas.append({"naipe": "ESPELHO", "id": f"ESP {i:02d}", "texto": q,
                       "nota": "Responda PELO seu cônjuge, sem perguntar. "
                               "Acertou? Andem 2 casas."})
    for i, (tit, txt) in enumerate(ALTAR, start=1):
        cartas.append({"naipe": "ALTAR", "id": f"ALT {i:02d}", "titulo": tit,
                       "texto": txt})
    for i, txt in enumerate(SELADO, start=1):
        cartas.append({"naipe": "SELADO", "id": f"JAR {i:02d}", "texto": txt,
                       "nota": "Vai lacrada no envelope. Não se abre no evento."})
    return cartas


# marcadores sobre a foto do tabuleiro — % da imagem (que inclui 3mm de sangria)
def pc(tx, ty):
    return round((tx + 3) / 406 * 100, 2), round((306 - (ty + 3)) / 306 * 100, 2)


PONTOS = [
    (*pc(32, 32),    "Início",
     "O casal começa aqui, no canto inferior esquerdo, com um único peão. "
     "A partida é sempre a dois — nunca há dois peões no tabuleiro."),
    (*pc(96, 268),   "As 30 casas",
     "A trilha corre pela borda, no sentido horário. Cada casa traz só um ícone "
     "e uma cor: a pergunta está na carta, nunca no tabuleiro. Foi essa decisão "
     "que deixou o miolo livre para a dobra."),
    (*pc(200, 215),  "O cordão sobre o vinco",
     "É a única coisa que atravessa a dobra: uma trança de três fios em traço "
     "fino, sem nenhum texto. Proposital — o cordão é o que une as duas metades. "
     "Ligue o botão acima da imagem para ver a faixa de segurança."),
    (*pc(114, 137),  "O Altar",
     "A chegada. Completada a volta, o casal vem para cá e abre as quatro cartas "
     "de Altar: Gratidão, Perdão, Bênção e Pacto — que se assina no verso."),
    (*pc(286, 171),  "Mapa das cinco linguagens",
     "Cada carta cumprida planta uma semente no canteiro da linguagem "
     "correspondente. No fim da partida, o canteiro que ficou vazio é o "
     "diagnóstico: é a linguagem que o casal anda negligenciando."),
    (*pc(368, 71.3), "Casa Espelho",
     "Quatro casas no percurso. Aqui você responde PELO seu cônjuge, sem "
     "perguntar. Acertou, andam duas casas. Errou, ele(a) conta a resposta — "
     "e essa costuma ser a melhor parte da rodada."),
    (*pc(114, 70),   "Regras resumidas",
     "Os seis passos ficam impressos no próprio tabuleiro, para o casal não "
     "precisar procurar folheto no meio da conversa. As regras completas estão "
     "no verso."),
]

PASSOS = [
    ("Escolham o nível",
     "Antes de tudo, os dois decidem: 1 Conhecer, 2 Aproximar ou 3 Aprofundar. "
     "O marcador fica à vista. Podem subir de nível a qualquer momento — e é "
     "isso que faz o mesmo jogo servir a quem namora há um mês e a quem é "
     "casado há vinte anos."),
    ("Rolem o dado e avancem",
     "Um peão só, movido pelos dois. Ninguém está na frente de ninguém."),
    ("Puxem a carta da cor da casa",
     "Leiam em voz alta a pergunta do nível escolhido. Responde quem parou ali; "
     "na rodada seguinte, o outro."),
    ("Plantem a semente",
     "Cumpriram a carta? Marquem uma semente no canteiro daquela linguagem. "
     "Ninguém confere nada: a única regra do jogo é a honestidade."),
    ("Cheguem ao Altar",
     "Fechada a volta, as quatro cartas de Altar. Sem pressa — é aqui que o "
     "jogo vira casamento. O Pacto é assinado no verso do tabuleiro, com data."),
    ("Levem o envelope para casa",
     "As dez cartas do Jardim Fechado saem lacradas e não se abrem no evento. "
     "São para casais casados, a sós, em casa."),
]

FICHA = [
    ("Tabuleiro", [
        ("Formato aberto", "400 × 300 mm"),
        ("Fechado", "200 × 300 mm"),
        ("Com sangria 3 mm", "406 × 306 mm"),
        ("A 300 dpi", "4796 × 3615 px"),
        ("Vinco", "vertical em x = 200 mm"),
        ("Zona morta do vinco", "7 mm para cada lado"),
        ("Folga real medida", "28,5 mm (frente) · 22,0 mm (verso)"),
        ("Suporte", "cartão 300 g/m², 4/4, laminação fosca na frente"),
    ]),
    ("Caixa", [
        ("Tampa — interno", "207 × 307 × 30 mm"),
        ("Tampa — planificado", "267 × 367 mm"),
        ("Fundo — interno", "203 × 303 × 28 mm"),
        ("Fundo — planificado", "259 × 359 mm"),
        ("Folga tampa/fundo", "2 mm"),
        ("Suporte", "cartão triplex 350 g/m², 4/0, laminação fosca"),
        ("Acabamento", "faca, vinco e colagem dos 4 cantos"),
    ]),
    ("Peças", [
        ("Cartas", "70 × 120 mm · 60 un. · cantos r = 4 mm"),
        ("Cartas — suporte", "couché 300 g/m², 4/4, fosca 2 faces"),
        ("Cartela", "200 × 280 mm · papelão 1,5 mm · faca de destaque"),
        ("Cartela — conteúdo", "36 peças destacáveis"),
        ("Dado", "cubo 20 mm montável · cartão 250 g/m²"),
        ("Envelope", "planificado 108 × 305 mm · offset 180 g/m²"),
    ]),
]

PALETA = [
    ("Petróleo", "88 · 62 · 48 · 38", "#10323F", "institucional · Espelho · Altar"),
    ("Dourado",  "20 · 33 · 100 · 6", "#C9A227", "PALAVRA"),
    ("Azul",     "75 · 40 · 22 · 3",  "#2A6F8E", "TEMPO"),
    ("Oliva",    "58 · 33 · 70 · 15", "#6B7F5C", "PRESENTE"),
    ("Terracota","15 · 70 · 70 · 3",  "#C4664F", "SERVIÇO"),
    ("Vinho",    "35 · 88 · 60 · 25", "#8C3A4A", "TOQUE · Jardim Fechado"),
    ("Creme",    "4 · 5 · 12 · 0",    "#F3EDE1", "fundo"),
]


def html():
    img = imagens_web.gerar()
    cartas = montar_cartas()

    def fig(chave, legenda, dim, classe=""):
        d = img[chave]
        return (f'<figure class="fig {classe}">'
                f'<div class="crop"><img src="{d["uri"]}" width="{d["w"]}" '
                f'height="{d["h"]}" alt="{legenda}" loading="lazy"></div>'
                f'<figcaption><span>{legenda}</span>'
                f'<span class="dim">{dim}</span></figcaption></figure>')

    pontos_html = "".join(
        f'<button class="hot" style="left:{x}%;top:{y}%" data-i="{i}" '
        f'type="button" aria-label="{t}"><span>{i+1}</span></button>'
        for i, (x, y, t, _) in enumerate(PONTOS))
    pontos_json = json.dumps([{"t": t, "d": d} for _, _, t, d in PONTOS],
                             ensure_ascii=False)

    passos_html = "".join(
        f'<li><h3>{t}</h3><p>{d}</p></li>' for t, d in PASSOS)

    ficha_html = "".join(
        '<div class="speccard"><h3>' + nome + '</h3><dl>' +
        "".join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in linhas) +
        '</dl></div>' for nome, linhas in FICHA)

    paleta_html = "".join(
        f'<tr><td><span class="chip" style="background:{hexv}"></span>{nome}</td>'
        f'<td class="mono">{cmyk}</td><td class="mono">{hexv}</td><td>{uso}</td></tr>'
        for nome, cmyk, hexv, uso in PALETA)

    regras_html = "".join(
        f'<li><b>{n}</b> {t}</li>' for n, t in REGRAS_RESUMO)

    conta = {}
    for c in cartas:
        conta[c["naipe"]] = conta.get(c["naipe"], 0) + 1

    dados_js = json.dumps({
        "cartas": cartas,
        "naipes": {k: {"nome": v[0], "sub": v[1], "cor": v[2]}
                   for k, v in NAIPE_INFO.items()},
        "niveis": [list(n) for n in NIVEIS],
        "pontos": json.loads(pontos_json),
    }, ensure_ascii=False)

    return TEMPLATE \
        .replace("__FIG_TAB_FRENTE__", img["tab_frente"]["uri"]) \
        .replace("__W_TAB__", str(img["tab_frente"]["w"])) \
        .replace("__H_TAB__", str(img["tab_frente"]["h"])) \
        .replace("__FIG_TAB_VERSO__", fig("tab_verso",
                 "Verso — o Pacto e as regras completas", "400 × 300 mm")) \
        .replace("__FIG_CX_TAMPA__", fig("cx_tampa",
                 "Caixa · tampa (planificada)", "267 × 367 mm")) \
        .replace("__FIG_CX_FUNDO__", fig("cx_fundo",
                 "Caixa · fundo (planificado)", "259 × 359 mm")) \
        .replace("__FIG_CARTELA__", fig("cartela",
                 "Cartela — 36 peças destacáveis", "200 × 280 mm")) \
        .replace("__FIG_DADO__", fig("dado",
                 "Dado montável", "cubo 20 mm")) \
        .replace("__FIG_ENVELOPE__", fig("envelope",
                 "Envelope selado, planificado", "108 × 305 mm")) \
        .replace("__FIG_VERSO_JOGO__", fig("verso_jogo",
                 "Verso das 50 cartas do jogo", "70 × 120 mm")) \
        .replace("__FIG_VERSO_SELADO__", fig("verso_selado",
                 "Verso das 10 cartas lacradas", "70 × 120 mm")) \
        .replace("__PONTOS__", pontos_html) \
        .replace("__PASSOS__", passos_html) \
        .replace("__FICHA__", ficha_html) \
        .replace("__PALETA__", paleta_html) \
        .replace("__REGRAS__", regras_html) \
        .replace("__DADOS__", dados_js)


TEMPLATE = r"""<meta charset="utf-8">
<title>TRÊS DOBRAS — manual do jogo</title>
<style>
:root{
  --ink:#07171E; --surface:#0E2C38;
  --paper:#F3EDE1; --paper2:#E4DBC8;
  --gold:#C9A227; --gold-dim:#9C7D1E;
  --faca:#E5007E; --vinco:#00A3E0;
  --txt:#EDE6D8; --txt-dim:#9FB0B7; --line:#1E4655;
  --card:#0E2C38; --shadow:0 1px 0 rgba(255,255,255,.04);
  --maxw:1120px;
  --serif:"Palatino Linotype",Palatino,"Book Antiqua","URW Palladio L",Georgia,serif;
  --sans:Corbel,Candara,"Segoe UI",system-ui,-apple-system,sans-serif;
  --mono:Consolas,"Cascadia Mono","SF Mono",ui-monospace,monospace;
}
@media (prefers-color-scheme: light){
  :root{
    --ink:#F3EDE1; --surface:#FFFFFF; --paper:#FFFFFF; --paper2:#EFE8DA;
    --txt:#12303C; --txt-dim:#5C7079; --line:#DBD1BE;
    --card:#FFFFFF; --gold:#9C7D1E; --gold-dim:#B9932A;
    --shadow:0 1px 2px rgba(18,48,60,.07);
  }
}
:root[data-theme="dark"]{
  --ink:#07171E; --surface:#0E2C38; --paper:#F3EDE1; --paper2:#E4DBC8;
  --txt:#EDE6D8; --txt-dim:#9FB0B7; --line:#1E4655; --card:#0E2C38;
  --gold:#C9A227; --gold-dim:#9C7D1E; --shadow:0 1px 0 rgba(255,255,255,.04);
}
:root[data-theme="light"]{
  --ink:#F3EDE1; --surface:#FFFFFF; --paper:#FFFFFF; --paper2:#EFE8DA;
  --txt:#12303C; --txt-dim:#5C7079; --line:#DBD1BE; --card:#FFFFFF;
  --gold:#9C7D1E; --gold-dim:#B9932A; --shadow:0 1px 2px rgba(18,48,60,.07);
}
*{box-sizing:border-box}
body{margin:0;background:var(--ink);color:var(--txt);font-family:var(--sans);
  font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased;
  overflow-wrap:break-word}
img{max-width:100%;height:auto}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 22px}
h1,h2,h3{font-family:var(--serif);font-weight:700;text-wrap:balance;margin:0}
p{margin:0}
a{color:var(--gold)}
.eyebrow{font-family:var(--mono);font-size:.66rem;letter-spacing:.22em;
  text-transform:uppercase;color:var(--gold);margin:0}
.mono{font-family:var(--mono);font-variant-numeric:tabular-nums}

/* ---------- cabeçalho ---------- */
header{border-bottom:1px solid var(--line);padding:0 0 44px}
.regbar{display:flex;height:7px}
.regbar i{flex:1}
.hero{padding-top:52px;display:grid;gap:26px}
.hero h1{font-size:clamp(3rem,11vw,6.4rem);line-height:.88;letter-spacing:.02em}
.hero h1 span{display:block;color:var(--gold)}
.lede{font-size:1.15rem;max-width:62ch;color:var(--txt)}
.verse{font-family:var(--serif);font-style:italic;color:var(--txt-dim);
  font-size:1.05rem;border-left:2px solid var(--gold);padding-left:14px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  gap:1px;background:var(--line);border:1px solid var(--line);margin-top:6px}
.stats div{background:var(--ink);padding:14px 16px}
.stats b{display:block;font-family:var(--serif);font-size:1.7rem;line-height:1.1}
.stats small{font-family:var(--mono);font-size:.62rem;letter-spacing:.16em;
  text-transform:uppercase;color:var(--txt-dim)}

/* ---------- navegação ---------- */
nav{position:sticky;top:0;z-index:30;background:color-mix(in srgb,var(--ink) 92%,transparent);
  backdrop-filter:blur(9px);border-bottom:1px solid var(--line)}
nav ul{list-style:none;display:flex;gap:4px;margin:0;padding:9px 0;overflow-x:auto}
nav a{display:block;white-space:nowrap;font-family:var(--mono);font-size:.66rem;
  letter-spacing:.14em;text-transform:uppercase;color:var(--txt-dim);
  text-decoration:none;padding:7px 11px;border:1px solid transparent;border-radius:2px}
nav a:hover,nav a:focus-visible{color:var(--txt);border-color:var(--line)}

/* ---------- seções ---------- */
section{padding:66px 0;border-bottom:1px solid var(--line)}
.shead{display:grid;gap:10px;margin-bottom:34px;max-width:70ch}
.shead h2{font-size:clamp(1.8rem,4.4vw,2.7rem);line-height:1.1}
.shead p{color:var(--txt-dim)}

/* ---------- figuras ---------- */
.fig{margin:0;display:grid;gap:10px}
.crop{position:relative;padding:16px;background:var(--paper2);border-radius:2px}
.crop::before,.crop::after{content:"";position:absolute;width:11px;height:11px;
  pointer-events:none}
.crop::before{top:5px;left:5px;border-top:1px solid var(--faca);
  border-left:1px solid var(--faca)}
.crop::after{bottom:5px;right:5px;border-bottom:1px solid var(--faca);
  border-right:1px solid var(--faca)}
.crop img{display:block;width:100%;height:auto;border-radius:1px}
figcaption{display:flex;justify-content:space-between;gap:16px;align-items:baseline;
  font-size:.86rem;color:var(--txt-dim);flex-wrap:wrap}
.dim{font-family:var(--mono);font-size:.7rem;letter-spacing:.1em;color:var(--gold)}
.grid2{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:30px}
.grid3{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:30px}

/* ---------- tabuleiro interativo ---------- */
.boardtools{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:14px}
.tgl{display:inline-flex;align-items:center;gap:9px;cursor:pointer;
  font-family:var(--mono);font-size:.68rem;letter-spacing:.13em;text-transform:uppercase;
  color:var(--txt-dim);border:1px solid var(--line);border-radius:2px;padding:8px 12px;
  background:none}
.tgl:hover{color:var(--txt)}
.tgl[aria-pressed="true"]{color:var(--vinco);border-color:var(--vinco)}
.tgl i{width:9px;height:9px;border:1px solid currentColor;border-radius:50%}
.tgl[aria-pressed="true"] i{background:currentColor}
.boardwrap{position:relative;background:var(--paper2);padding:14px;border-radius:2px}
.boardwrap img{display:block;width:100%;height:auto}
.hot{position:absolute;width:30px;height:30px;transform:translate(-50%,-50%);
  border-radius:50%;border:2px solid var(--ink);background:var(--gold);
  color:#07171E;font-family:var(--mono);font-weight:700;font-size:.78rem;
  cursor:pointer;display:grid;place-items:center;padding:0;
  box-shadow:0 2px 7px rgba(0,0,0,.35);transition:transform .14s ease}
.hot:hover,.hot:focus-visible{transform:translate(-50%,-50%) scale(1.22)}
.hot[aria-current="true"]{background:var(--faca);color:#fff}
.foldband,.foldaxis{position:absolute;top:14px;bottom:14px;pointer-events:none;
  opacity:0;transition:opacity .22s ease}
.foldband{background:repeating-linear-gradient(45deg,rgba(0,163,224,.30) 0 6px,
  rgba(0,163,224,.10) 6px 12px);border-left:1px solid var(--vinco);
  border-right:1px solid var(--vinco)}
.foldaxis{border-left:1px dashed var(--vinco)}
.boardwrap.showfold .foldband,.boardwrap.showfold .foldaxis{opacity:1}
.hotinfo{margin-top:16px;border:1px solid var(--line);border-left:3px solid var(--gold);
  padding:18px 20px;display:grid;gap:7px;min-height:118px;background:var(--surface)}
.hotinfo h3{font-size:1.22rem}
.hotinfo p{color:var(--txt-dim)}
.hotinfo .mono{font-size:.66rem;letter-spacing:.16em;text-transform:uppercase;
  color:var(--gold)}

/* ---------- passos ---------- */
ol.passos{list-style:none;counter-reset:p;margin:0;padding:0;display:grid;gap:1px;
  background:var(--line);border:1px solid var(--line)}
ol.passos li{counter-increment:p;background:var(--ink);padding:22px 24px 22px 74px;
  position:relative;display:grid;gap:5px}
ol.passos li::before{content:counter(p,decimal-leading-zero);position:absolute;
  left:24px;top:22px;font-family:var(--mono);font-size:.82rem;color:var(--gold);
  letter-spacing:.06em}
ol.passos h3{font-size:1.12rem}
ol.passos p{color:var(--txt-dim);font-size:.96rem}

/* ---------- navegador de cartas ---------- */
.cardtools{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px}
.pill{font-family:var(--mono);font-size:.65rem;letter-spacing:.12em;
  text-transform:uppercase;padding:7px 12px;border:1px solid var(--line);
  border-radius:2px;background:none;color:var(--txt-dim);cursor:pointer}
.pill:hover{color:var(--txt)}
.pill[aria-pressed="true"]{color:#07171E;border-color:transparent}
.lvltools{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:16px 0 22px}
.lvltools .lbl{font-family:var(--mono);font-size:.65rem;letter-spacing:.14em;
  text-transform:uppercase;color:var(--txt-dim);margin-right:4px}
.cardstage{display:grid;grid-template-columns:minmax(0,300px) minmax(0,1fr);
  gap:34px;align-items:start}
@media (max-width:720px){.cardstage{grid-template-columns:1fr}}
.card{background:var(--paper);color:#12303C;border-radius:4px;overflow:hidden;
  box-shadow:0 10px 30px rgba(0,0,0,.30);aspect-ratio:70/120;display:flex;
  flex-direction:column}
.card .top{padding:15px 16px;color:#fff;display:grid;gap:2px}
.card .top b{font-family:var(--sans);font-weight:700;font-size:1.16rem;
  letter-spacing:.05em}
.card .top i{font-family:var(--serif);font-style:italic;font-size:.82rem;
  opacity:.92}
.card .body{padding:16px;display:flex;flex-direction:column;gap:13px;flex:1;
  overflow:auto}
.card .lvl{display:grid;gap:4px}
.card .lvl .tag{font-family:var(--mono);font-size:.58rem;letter-spacing:.14em;
  text-transform:uppercase;display:flex;align-items:center;gap:6px}
.card .lvl .tag em{width:15px;height:15px;border-radius:50%;color:#fff;
  display:grid;place-items:center;font-style:normal;font-size:.56rem;flex:none}
.card .lvl p{font-size:.83rem;line-height:1.4;color:#1B3C49}
.card .lvl.off{opacity:.26}
.card .foot{padding:9px 16px;display:flex;justify-content:space-between;gap:8px;
  font-family:var(--mono);font-size:.58rem;letter-spacing:.1em;color:#4E656F;
  border-top:1px solid rgba(18,48,60,.12)}
.card.altar{background:#0E2C38}
.card.altar .body{align-items:center;justify-content:center;text-align:center;gap:9px}
.card.altar .body h4{font-family:var(--serif);font-size:1.6rem;color:#fff;margin:0;
  letter-spacing:.06em}
.card.altar .body p{color:#EDE6D8;font-size:.86rem}
.card.altar .foot{color:#7E9099;border-top-color:rgba(255,255,255,.12)}
.cardmeta{display:grid;gap:16px}
.cardmeta .counter{font-family:var(--mono);font-size:.68rem;letter-spacing:.14em;
  text-transform:uppercase;color:var(--txt-dim)}
.cardmeta h3{font-size:1.35rem}
.navbtns{display:flex;gap:8px}
.navbtns button{font-family:var(--mono);font-size:.68rem;letter-spacing:.12em;
  text-transform:uppercase;padding:10px 16px;border:1px solid var(--line);
  background:none;color:var(--txt);border-radius:2px;cursor:pointer}
.navbtns button:hover{border-color:var(--gold);color:var(--gold)}
.note{border:1px solid var(--line);border-left:3px solid var(--faca);
  padding:14px 16px;font-size:.92rem;color:var(--txt-dim);background:var(--surface)}
.legend{display:flex;gap:14px;flex-wrap:wrap;font-family:var(--mono);font-size:.63rem;
  letter-spacing:.1em;text-transform:uppercase;color:var(--txt-dim)}
.legend span{display:inline-flex;align-items:center;gap:6px}
.legend i{width:11px;height:11px;border-radius:2px;flex:none}

/* ---------- ficha técnica ---------- */
.specs{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:1px;
  background:var(--line);border:1px solid var(--line)}
.speccard{background:var(--ink);padding:24px}
.speccard h3{font-size:1.28rem;margin-bottom:14px;color:var(--gold)}
.speccard dl{margin:0;display:grid;grid-template-columns:1fr;gap:9px}
.speccard dt{font-family:var(--mono);font-size:.6rem;letter-spacing:.13em;
  text-transform:uppercase;color:var(--txt-dim)}
.speccard dd{margin:0 0 5px;font-size:.94rem}
.tablewrap{overflow-x:auto;margin-top:30px;border:1px solid var(--line)}
table{border-collapse:collapse;width:100%;min-width:520px;font-size:.9rem}
th,td{text-align:left;padding:11px 15px;border-bottom:1px solid var(--line)}
th{font-family:var(--mono);font-size:.6rem;letter-spacing:.14em;text-transform:uppercase;
  color:var(--txt-dim);font-weight:400}
tr:last-child td{border-bottom:none}
.chip{display:inline-block;width:13px;height:13px;border-radius:2px;margin-right:9px;
  vertical-align:-2px;border:1px solid rgba(127,127,127,.35)}
ul.regras{list-style:none;margin:0;padding:0;display:grid;gap:9px}
ul.regras li{font-size:.95rem;color:var(--txt-dim)}
ul.regras b{display:inline-grid;place-items:center;width:20px;height:20px;
  border-radius:50%;background:var(--gold);color:#07171E;font-family:var(--mono);
  font-size:.66rem;margin-right:9px;vertical-align:-4px}
footer{padding:44px 0 60px;color:var(--txt-dim);font-size:.88rem;display:grid;gap:8px}
:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>

<div class="regbar" aria-hidden="true">
  <i style="background:#00AEEF"></i><i style="background:#EC008C"></i>
  <i style="background:#FFF200"></i><i style="background:#111"></i>
  <i style="background:#C9A227"></i>
</div>

<header>
  <div class="wrap hero">
    <p class="eyebrow">Manual de produção · brinde de congresso de casais</p>
    <h1>TRÊS<span>DOBRAS</span></h1>
    <p class="verse">"O cordão de três dobras não se rebenta com facilidade."
      — Eclesiastes 4.12</p>
    <p class="lede">Um jogo de tabuleiro cooperativo para casais. Um único peão
      para os dois, cinco linguagens do amor, três níveis de profundidade — e um
      envelope que só se abre em casa. Este manual mostra o que foi desenhado,
      como se joga e o que a gráfica precisa saber.</p>
    <div class="stats">
      <div><b>3</b><small>projetos de impressão</small></div>
      <div><b>60</b><small>cartas · 3 níveis cada</small></div>
      <div><b>400×300</b><small>tabuleiro, vinco em 200</small></div>
      <div><b>28,5 mm</b><small>folga até a dobra</small></div>
    </div>
  </div>
</header>

<nav>
  <div class="wrap">
    <ul>
      <li><a href="#jogo">O jogo</a></li>
      <li><a href="#jogar">Como se joga</a></li>
      <li><a href="#tabuleiro">Tabuleiro</a></li>
      <li><a href="#cartas">As 60 cartas</a></li>
      <li><a href="#caixa">Caixa</a></li>
      <li><a href="#pecas">Peças</a></li>
      <li><a href="#ficha">Ficha técnica</a></li>
    </ul>
  </div>
</nav>

<main>
<section id="jogo"><div class="wrap">
  <div class="shead">
    <p class="eyebrow">O jogo</p>
    <h2>Ninguém ganha. Os dois chegam.</h2>
    <p>O casal move um peão só. Não há disputa, não há quem esteja na frente —
      o que existe é uma volta a ser dada juntos e um Altar no fim dela.</p>
  </div>
  <div class="grid3">
    <div>
      <h3>Três níveis em cada carta</h3>
      <p style="color:var(--txt-dim);margin-top:8px">Toda carta traz a mesma
        pergunta em três profundidades. O casal escolhe a altura da barra e pode
        subir quando quiser. É o que permite entregar o mesmo jogo para quem
        namora há um mês e para quem é casado há vinte anos.</p>
    </div>
    <div>
      <h3>Cinco linguagens viram naipes</h3>
      <p style="color:var(--txt-dim);margin-top:8px">Palavra, Tempo, Presente,
        Serviço e Toque. Cada carta cumprida planta uma semente no canteiro
        correspondente, impresso no próprio tabuleiro. O canteiro que ficar
        vazio no fim é o diagnóstico do casal.</p>
    </div>
    <div>
      <h3>O envelope não se abre aqui</h3>
      <p style="color:var(--txt-dim);margin-top:8px">As dez cartas do Jardim
        Fechado tratam da intimidade conjugal na linguagem de Cântico dos
        Cânticos. Saem lacradas: são para casais casados, a sós, em casa. O
        evento fica confortável e o casal leva o melhor para depois.</p>
    </div>
  </div>
  <div style="margin-top:34px">
    <p class="eyebrow" style="margin-bottom:14px">Resumo impresso no tabuleiro</p>
    <ul class="regras">__REGRAS__</ul>
  </div>
</div></section>

<section id="jogar"><div class="wrap">
  <div class="shead">
    <p class="eyebrow">Como se joga</p>
    <h2>Seis passos, na ordem</h2>
    <p>A sequência é curta de propósito: o jogo tem que caber numa conversa,
      não num regulamento.</p>
  </div>
  <ol class="passos">__PASSOS__</ol>
</div></section>

<section id="tabuleiro"><div class="wrap">
  <div class="shead">
    <p class="eyebrow">Tabuleiro · 400 × 300 mm</p>
    <h2>Clique nos pontos para entender o tabuleiro</h2>
    <p>E ligue a faixa da dobra para ver por que nenhum texto é cortado pelo
      vinco.</p>
  </div>
  <div class="boardtools">
    <button class="tgl" id="btnfold" type="button" aria-pressed="false">
      <i></i> Mostrar a zona da dobra</button>
    <span class="dim">vinco em x = 200 mm · zona morta 7 mm para cada lado</span>
  </div>
  <div class="boardwrap" id="boardwrap">
    <img src="__FIG_TAB_FRENTE__" width="__W_TAB__" height="__H_TAB__"
      alt="Frente do tabuleiro Três Dobras">
    <div class="foldband" style="left:48.28%;width:3.45%"></div>
    <div class="foldaxis" style="left:50%"></div>
    __PONTOS__
  </div>
  <div class="hotinfo" id="hotinfo" aria-live="polite">
    <p class="mono" id="hotnum">Ponto 1 de 7</p>
    <h3 id="hottit">Início</h3>
    <p id="hotdesc">Clique em qualquer marcador dourado sobre a imagem.</p>
  </div>
  <div style="margin-top:44px" class="grid2">
    __FIG_TAB_VERSO__
    <div style="display:grid;gap:14px;align-content:start">
      <h3>Por que a dobra não corta nada</h3>
      <p style="color:var(--txt-dim)">As casas do tabuleiro carregam só ícone e
        cor — a pergunta mora na carta. Isso liberou a faixa central inteira.
        Um verificador lê o PDF final palavra por palavra e mede a distância de
        cada uma até o eixo do vinco: a menor folga é de 28,5 mm na frente e
        22,0 mm no verso, contra os 7 mm exigidos.</p>
      <p style="color:var(--txt-dim)">No verso, a dobra ainda recebe uma faixa
        creme de 30 mm. Fundo petróleo sólido sobre o vinco trincaria o cartão
        de 300 g.</p>
      <div class="note">A única coisa que cruza a dobra é a trança do cordão:
        traço fino, sem texto. É proposital — o cordão é o que une as duas
        metades.</div>
    </div>
  </div>
</div></section>

<section id="cartas"><div class="wrap">
  <div class="shead">
    <p class="eyebrow">As 60 cartas · 70 × 120 mm</p>
    <h2>Leia todas as cartas antes de aprovar</h2>
    <p>Filtre por naipe e troque o nível para ver como a mesma carta muda de
      profundidade. Os textos aqui são exatamente os que vão para a gráfica.</p>
  </div>
  <div class="cardtools" id="filtros"></div>
  <div class="lvltools" id="niveis"><span class="lbl">Nível em destaque</span></div>
  <div class="cardstage">
    <div id="cardslot"></div>
    <div class="cardmeta">
      <p class="counter" id="cardcount"></p>
      <h3 id="cardtit"></h3>
      <p id="carddesc" style="color:var(--txt-dim)"></p>
      <div class="navbtns">
        <button id="prev" type="button">← anterior</button>
        <button id="next" type="button">próxima →</button>
      </div>
      <div class="legend" id="legenda"></div>
    </div>
  </div>
  <div class="grid3" style="margin-top:44px">
    __FIG_VERSO_JOGO__
    __FIG_VERSO_SELADO__
    <div style="display:grid;gap:12px;align-content:start">
      <h3>Só duas artes de verso</h3>
      <p style="color:var(--txt-dim)">Uma para as 50 cartas do jogo e outra para
        as 10 lacradas. Mesmo assim o arquivo de versos vai com as 60 páginas
        casadas 1:1 com as frentes, para a imposição não errar.</p>
    </div>
  </div>
</div></section>

<section id="caixa"><div class="wrap">
  <div class="shead">
    <p class="eyebrow">Caixa · tampa e fundo</p>
    <h2>A tampa cobre o fundo por inteiro</h2>
    <p>Duas peças independentes, com 2 mm de folga entre elas. Arte impressa na
      face externa; painel central, quatro paredes e quatro abas de canto.</p>
  </div>
  <div class="grid2">__FIG_CX_TAMPA____FIG_CX_FUNDO__</div>
  <div class="legend" style="margin-top:22px">
    <span><i style="background:#E5007E"></i> faca · magenta 100%</span>
    <span><i style="background:#00A3E0"></i> vinco · ciano 100%</span>
    <span>ambos em sobreimpressão, para isolar em camada técnica — não imprimir</span>
  </div>
  <div class="note" style="margin-top:22px">A lista de conteúdo está no painel
    externo do fundo. Se quiser que ela apareça ao <b>abrir</b> a caixa, o fundo
    precisa ser impresso em 4/4 com o painel espelhado.</div>
</div></section>

<section id="pecas"><div class="wrap">
  <div class="shead">
    <p class="eyebrow">Peças</p>
    <h2>36 peças destacáveis, um dado e o envelope</h2>
    <p>Trinta sementes (seis por linguagem), o peão do casal — duas figuras que
      encaixam numa base só — e três marcadores de nível.</p>
  </div>
  <div class="grid3">__FIG_CARTELA____FIG_DADO____FIG_ENVELOPE__</div>
</div></section>

<section id="ficha"><div class="wrap">
  <div class="shead">
    <p class="eyebrow">Ficha técnica</p>
    <h2>O que mandar para a gráfica</h2>
    <p>Tudo vetorial em CMYK, perfil Coated FOGRA39, tinta total ≤ 300 %, preto
      de texto 100 % K puro e fontes embutidas. Saída em PDF/X-1a ou X-4.</p>
  </div>
  <div class="specs">__FICHA__</div>
  <div class="tablewrap">
    <table>
      <thead><tr><th>Cor</th><th>CMYK</th><th>Hex</th><th>Uso</th></tr></thead>
      <tbody>__PALETA__</tbody>
    </table>
  </div>
  <div class="note" style="margin-top:26px">Alavancas de custo, se apertar:
    cartas de 70 × 120 para 63 × 88 (formato pôquer); cartela em cartão 400 g em
    vez de papelão cartonado; caixa só com tampa; dado plástico comprado no lugar
    do montável.</div>
</div></section>
</main>

<footer><div class="wrap">
  <p>TRÊS DOBRAS · arte gerada por código — <span class="mono">python
    src/gerar_tudo.py --png300</span></p>
  <p>Conteúdo das cartas em <span class="mono">src/dados.py</span> · ficha
    completa em <span class="mono">LEIA-ME-GRAFICA.md</span></p>
</div></footer>

<script>
const D = __DADOS__;

/* ---------- tabuleiro: pontos e faixa da dobra ---------- */
const bw = document.getElementById('boardwrap');
const btn = document.getElementById('btnfold');
btn.addEventListener('click', () => {
  const on = btn.getAttribute('aria-pressed') === 'true';
  btn.setAttribute('aria-pressed', String(!on));
  bw.classList.toggle('showfold', !on);
  btn.lastChild.textContent = on ? ' Mostrar a zona da dobra'
                                 : ' Ocultar a zona da dobra';
});
const hots = [...document.querySelectorAll('.hot')];
function mostrarPonto(i){
  hots.forEach(h => h.setAttribute('aria-current', String(+h.dataset.i === i)));
  document.getElementById('hotnum').textContent = `Ponto ${i+1} de ${D.pontos.length}`;
  document.getElementById('hottit').textContent = D.pontos[i].t;
  document.getElementById('hotdesc').textContent = D.pontos[i].d;
}
hots.forEach(h => h.addEventListener('click', () => mostrarPonto(+h.dataset.i)));
mostrarPonto(0);

/* ---------- navegador de cartas ---------- */
const ORDEM = ['PALAVRA','TEMPO','PRESENTE','SERVICO','TOQUE','ESPELHO','ALTAR','SELADO'];
let filtro = 'PALAVRA', nivel = 0, idx = 0;

const elFiltros = document.getElementById('filtros');
ORDEM.forEach(n => {
  const b = document.createElement('button');
  b.className = 'pill'; b.type = 'button'; b.dataset.n = n;
  const q = D.cartas.filter(c => c.naipe === n).length;
  b.textContent = `${D.naipes[n].nome} ${q}`;
  b.addEventListener('click', () => { filtro = n; idx = 0; pintar(); });
  elFiltros.appendChild(b);
});

const elNiveis = document.getElementById('niveis');
D.niveis.forEach(([num, rot], i) => {
  const b = document.createElement('button');
  b.className = 'pill'; b.type = 'button'; b.dataset.l = i;
  b.textContent = `${num} ${rot}`;
  b.addEventListener('click', () => { nivel = i; pintar(); });
  elNiveis.appendChild(b);
});

document.getElementById('legenda').innerHTML = ORDEM.slice(0,5).map(n =>
  `<span><i style="background:${D.naipes[n].cor}"></i>${D.naipes[n].nome}</span>`
).join('');

function lista(){ return D.cartas.filter(c => c.naipe === filtro); }

function desenhar(c){
  const inf = D.naipes[c.naipe];
  if (c.naipe === 'ALTAR'){
    return `<article class="card altar">
      <div class="body"><p class="mono" style="color:#C9A227;font-size:.6rem;
        letter-spacing:.2em">ALTAR</p><h4>${c.titulo}</h4><p>${c.texto}</p></div>
      <div class="foot"><span>TRÊS DOBRAS</span><span>${c.id}</span></div></article>`;
  }
  if (c.niveis){
    const blocos = c.niveis.map((t, i) => `
      <div class="lvl ${i === nivel ? '' : 'off'}">
        <span class="tag" style="color:${inf.cor}">
          <em style="background:${inf.cor}">${D.niveis[i][0]}</em>${D.niveis[i][1]}</span>
        <p>${t}</p></div>`).join('');
    return `<article class="card">
      <div class="top" style="background:${inf.cor}"><b>${inf.nome}</b>
        <i>${inf.sub}</i></div>
      <div class="body">${blocos}</div>
      <div class="foot"><span>TRÊS DOBRAS</span><span>${c.id}</span></div></article>`;
  }
  return `<article class="card">
    <div class="top" style="background:${inf.cor}"><b>${inf.nome}</b>
      <i>${inf.sub}</i></div>
    <div class="body" style="justify-content:center;text-align:center;gap:16px">
      <p style="font-family:var(--serif);font-style:italic;font-size:1.02rem;
        line-height:1.35">${c.texto}</p>
      ${c.nota ? `<p style="font-size:.72rem;color:#6B818B">${c.nota}</p>` : ''}
    </div>
    <div class="foot"><span>TRÊS DOBRAS</span><span>${c.id}</span></div></article>`;
}

const DESC = {
  PALAVRA:'Palavras de afirmação. O que se diz em voz alta e fica.',
  TEMPO:'Tempo de qualidade. Presença sem tela e sem pressa.',
  PRESENTE:'O cuidado que se vê — inclusive o presente invisível.',
  SERVICO:'Atos de serviço. Amor que arregaça a manga.',
  TOQUE:'Toque físico e afeto, tratado com respeito.',
  ESPELHO:'Você responde pelo seu cônjuge. Quatro casas no percurso, seis cartas.',
  ALTAR:'As quatro cartas finais. Gratidão, Perdão, Bênção e Pacto.',
  SELADO:'As dez cartas lacradas do Jardim Fechado. Não se abrem no evento.'
};

function pintar(){
  const L = lista();
  if (idx >= L.length) idx = 0;
  if (idx < 0) idx = L.length - 1;
  const c = L[idx];
  document.getElementById('cardslot').innerHTML = desenhar(c);
  document.getElementById('cardcount').textContent =
    `${c.id} · carta ${idx+1} de ${L.length}`;
  document.getElementById('cardtit').textContent = D.naipes[filtro].nome;
  document.getElementById('carddesc').textContent = DESC[filtro];
  document.querySelectorAll('#filtros .pill').forEach(b => {
    const on = b.dataset.n === filtro;
    b.setAttribute('aria-pressed', String(on));
    b.style.background = on ? D.naipes[b.dataset.n].cor : 'none';
  });
  const temNivel = !!c.niveis;
  document.querySelectorAll('#niveis .pill').forEach(b => {
    const on = +b.dataset.l === nivel;
    b.setAttribute('aria-pressed', String(on && temNivel));
    b.style.background = (on && temNivel) ? D.naipes[filtro].cor : 'none';
    b.disabled = !temNivel;
    b.style.opacity = temNivel ? 1 : .35;
  });
  document.getElementById('niveis').style.display = temNivel ? 'flex' : 'none';
}
document.getElementById('prev').addEventListener('click', () => { idx--; pintar(); });
document.getElementById('next').addEventListener('click', () => { idx++; pintar(); });
pintar();
</script>
"""


if __name__ == "__main__":
    conteudo = html()
    with open(SAIDA, "w", encoding="utf-8") as f:
        f.write(conteudo)
    print(f"\n  {len(conteudo)/1024:.0f} KB  ->  {SAIDA}")
