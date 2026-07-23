# Arte da marca "Casados para a Glória de Deus"

Arte oficial do ministério, usada como marca do jogo.

| Arquivo | O que é | Origem |
|---|---|---|
| `casal.png` | silhueta do casal (1071×737) | enviada pelo usuário, margens recortadas |
| `logo.png`  | letreiro "CASADOS PARA GLÓRIA DE DEUS" (1036×330) | idem |

O motor (`src/marca.py`) lê a forma escura, joga fora o fundo claro do JPEG e
tinge na cor do material (petróleo, dourado…) na opacidade da marca d'água.
Aplicada no verso do Pacto (acima das assinaturas) e no rodapé das costas das cartas.

Para trocar por uma versão nova, é só substituir o arquivo (mesmo nome) e rodar
`python src/gerar_tudo.py --png300`. Se um dia faltar `casal.png`, o motor cai
num traçado vetorial fiel da figura (fallback em `src/marca.py`).
