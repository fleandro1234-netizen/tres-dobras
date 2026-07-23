# Arte da marca "Casados para a Glória de Deus"

Coloque aqui os dois arquivos originais e a marca d'água passa a usar a **arte real**
(hoje, sem eles, o motor usa uma silhueta recriada só para posicionar).

| Arquivo | O que é | Como deve estar |
|---|---|---|
| `casal.png`  | a **silhueta do casal** | fundo transparente OU fundo branco; desenho escuro. Vira marca d'água tingida na cor do material. |
| `logo.png`   | o **letreiro** "CASADOS PARA GLÓRIA DE DEUS" | idem — fundo transparente/branco, desenho escuro. |

Não precisa recortar nem trocar a cor: o motor lê a forma escura, joga fora o fundo
claro e tinge na cor certa (petróleo, dourado etc.) na opacidade da marca d'água.

Depois de salvar, rode:

```bash
python src/gerar_tudo.py --png300
```

e a marca real aparece no tabuleiro (verso), nas costas das cartas e na caixa,
substituindo a silhueta recriada — sem mexer em mais nada.
