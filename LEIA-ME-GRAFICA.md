# TRÊS DOBRAS — jogo de tabuleiro para casais
### Ficha técnica de produção · offset

> *"O cordão de três dobras não se rebenta com facilidade."* — Eclesiastes 4.12

Três projetos independentes: **tabuleiro**, **caixa** e **peças**.
Toda a arte é **vetorial** (PDF), em **CMYK**, com **sangria de 3 mm**.
Resolução não é limite: pode ser rasterizada em qualquer dpi. Há um lote pronto em
**300 dpi** na pasta `_png-300dpi`.

---

## 1 · TABULEIRO — pasta `01-TABULEIRO`

| Item | Especificação |
|---|---|
| Formato final (aberto) | **400 × 300 mm** |
| Formato fechado | 200 × 300 mm |
| Com sangria 3 mm | 406 × 306 mm |
| A 300 dpi | **4796 × 3615 px** |
| Vinco | vertical, em **x = 200 mm** (200 + 200) |
| **Zona morta do vinco** | **7 mm para cada lado** — verificado por código, nenhum texto, número ou ícone entra ali |
| Páginas | 1 = frente (trilha) · 2 = verso (Pacto + Regras) |
| Suporte | cartão 300 g/m², **4/4**, laminação fosca na frente |
| Acabamento | vinco central + refile |

**Arquivos**
- `TABULEIRO_400x300_COM-MARCAS.pdf` — 424 × 324 mm, com marcas de corte, marca de vinco e barra de registro
- `TABULEIRO_400x300_SANGRIA-3mm.pdf` — 406 × 306 mm exatos, sem marcas

**O que atravessa a dobra:** apenas a trança decorativa do "cordão" — traços finos,
sem texto. É proposital: o cordão é o que une as duas metades.
No **verso**, a dobra recebe uma faixa creme de 30 mm para **reduzir a carga de tinta
no vinco** (fundo petróleo puro na dobra trincaria).

---

## 2 · CAIXA — pasta `02-CAIXA`

Caixa de **tampa e fundo**. A tampa cobre o fundo por inteiro.

| | Interno | Planificado |
|---|---|---|
| **TAMPA** | 207 × 307 × 30 mm | **267 × 367 mm** |
| **FUNDO** | 203 × 303 × 28 mm | **259 × 359 mm** |

- Suporte: cartão triplex 350 g/m², **4/0**, laminação fosca, colagem dos 4 cantos.
- Arte impressa na **face externa**. Painel central + 4 paredes + 4 abas de canto.
- **FACA** em magenta 100% e **VINCO** em ciano 100%, ambos em sobreimpressão —
  isolar numa camada técnica e **não imprimir**.
- Folga de 2 mm entre tampa e fundo (207 vs 203/303 vs 307).

> A lista de conteúdo está no painel externo do fundo. Se quiser que ela apareça
> ao **abrir** a caixa, imprima o fundo em 4/4 e peça o espelhamento do painel.

---

## 3 · PEÇAS — pasta `03-PECAS`

### 3.1 Cartas — 60 unidades
| Item | Especificação |
|---|---|
| Formato final | **70 × 120 mm** (tarô) |
| Com sangria | 76 × 126 mm |
| Cantos | arredondados **r = 4 mm** |
| Margem de segurança | 5 mm |
| Suporte | couché 300 g/m², **4/4**, laminação fosca nas 2 faces |

- `CARTAS_FRENTES_70x120_sangria-3mm.pdf` — 60 páginas, 1 carta por página
- `CARTAS_VERSOS_70x120_sangria-3mm.pdf` — 60 páginas, casadas 1:1 com as frentes
- `_CONFERENCIA_todas-as-cartas.pdf` — **só para aprovação, não imprimir**

**Só existem 2 artes de verso** (50 cartas do jogo + 10 do envelope selado). As
60 páginas vêm casadas para a imposição não errar. Composição:

| Naipe | Qtd | Conteúdo |
|---|---|---|
| PALAVRA / TEMPO / PRESENTE / SERVIÇO / TOQUE | 8 cada = 40 | 3 níveis por carta |
| ESPELHO | 6 | pergunta única |
| ALTAR | 4 | Gratidão · Perdão · Bênção · Pacto |
| **JARDIM FECHADO** | 10 | **vão lacradas no envelope** |

### 3.2 Cartela de peças
- `CARTELA-PECAS_200x280_sangria-3mm.pdf` — 206 × 286 mm com sangria
- Papelão 1,5 mm cartonado com couché 150 g/m², **4/0**, **faca de destaque**
- 36 peças: 30 sementes (6 por linguagem) + peão do casal (Ele + Ela + base) + 3 marcadores de nível
- A base tem uma **fenda de 19,6 × 1,8 mm** para encaixar as duas figuras

### 3.3 Dado montável
- `DADO-MONTAVEL_100x90_sangria-3mm.pdf` — cubo de 20 mm, 7 abas de colagem
- Cartão 250 g/m², 4/0, faca + vinco

### 3.4 Envelope selado
- `ENVELOPE-SELADO_108x305_faca.pdf` — planificado **108 × 305 mm**
- Comporta as 10 cartas de 70 × 120 mm · offset 180 g/m², 4/0, faca + vinco, colagem lateral
- Vai **lacrado**. É o único item do kit que não se abre no evento.

---

## Padrão de cor (vale para tudo)

| | |
|---|---|
| Espaço | **CMYK** · perfil Coated FOGRA39 |
| Limite de tinta | **≤ 300 %** (a cor mais pesada da paleta é o petróleo, 236 %) |
| Preto de texto | **100 % K puro** |
| Preto de área | 60 / 40 / 40 / 100 (240 %) |
| Fontes | Palatino Linotype + Corbel, **embutidas** no PDF |
| Saída sugerida | PDF/X-1a ou PDF/X-4 |

**Paleta**

| Cor | CMYK | Uso |
|---|---|---|
| Petróleo | 88 · 62 · 48 · 38 | institucional / Espelho / Altar |
| Dourado | 20 · 33 · 100 · 6 | PALAVRA |
| Azul | 75 · 40 · 22 · 3 | TEMPO |
| Oliva | 58 · 33 · 70 · 15 | PRESENTE |
| Terracota | 15 · 70 · 70 · 3 | SERVIÇO |
| Vinho | 35 · 88 · 60 · 25 | TOQUE / Jardim Fechado |
| Creme | 4 · 5 · 12 · 0 | fundo |

---

## Alavancas de custo (se o orçamento apertar)

1. **Cartas 70 × 120 → 63 × 88 mm** (formato pôquer). Economia grande em papel.
   O texto reflui sozinho — é só mudar `CW, CH` em `src/cartas.py` e rodar de novo.
2. **Cartela em cartão 400 g** em vez de papelão 1,5 mm cartonado. Peça mais mole,
   metade do preço.
3. **Caixa só com tampa** (fundo em cartão liso 4/0 sem arte).
4. **Dado**: usar dado plástico comprado a granel em vez do montável.

---

## Como regerar a arte

Requer Python 3 com `reportlab`, `pillow` e `pymupdf` (já instalados nesta máquina).

```bash
python "src/gerar_tudo.py" --png300
```

Gera os 3 projetos, os previews em 100 dpi e os PNG em 300 dpi.

> ⚠️ A pasta fica no OneDrive. Se algum PDF estiver aberto no Acrobat, o script
> avisa quais arquivos pulou — feche-os e rode de novo.

Ajustes de conteúdo (perguntas das cartas, regras, Pacto) ficam todos em
`src/dados.py`. Layouts em `src/tabuleiro.py`, `src/caixa.py`, `src/cartas.py`
e `src/pecas.py`. Paleta, fontes e ícones em `src/comum.py`.
