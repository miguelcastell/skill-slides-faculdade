# Estilo visual

## Tema

| token | cor | uso |
|---|---|---|
| `--esc` | `#5c1a2b` vinho escuro | braço principal, o que vai bem, destaque forte |
| `--med` | `#a8445e` vinho médio | braço de contraste, o que chama atenção, alerta |
| `--card` / `--borda` | `#f7eff1` / `#ecd9de` | fundo e borda dos cards |
| `--trilho` | `#f1e4e8` | trilho vazio das barras |
| `--txt` / `--mudo` | `#231a1d` / `#7a6a6f` | texto e texto secundário |

A paleta padrão é vinho, para combinar com o logo no canto do slide: o
deck parece parte do modelo, não um enxerto. Para outra instituição,
troque os tokens em `CSS` (`scripts/componentes.py`) por duas cores
tiradas do logo dela: uma escura (`--esc`) e uma média (`--med`). **No
máximo duas cores de dado**: braço A/braço B, estável/instável,
antes/depois. Uma terceira categoria vira cinza (`--mudo`).

Tipografia: **Space Grotesk 700** nos títulos e números grandes, **IBM
Plex Sans** no texto (25 px; 21–23 px para secundário), **IBM Plex
Mono** em rótulos, eixos e valores. Números sempre no formato brasileiro
(`fmt(0.764)` → `0,764`).

## Área e grade

- A área de conteúdo é **1360×660 px**. O `<h1>` ocupa ~80 px por linha;
  com título de 2 linhas sobram ~470 px. Deixe respiro embaixo — os
  slides aprovados usam 70–85% da altura, não 100%.
- Layout padrão de resultado: `<div class='linha'>` com o gráfico à
  esquerda (`flex:1.3`–`1.6`) e o texto à direita (`flex:1`).
- Grade de cards: `<div class='grade2'>` (2 colunas).

## Padrões que funcionaram

Os slides 1 a 6 estão prontos em `exemplos/exemplo.py`.

| padrão | quando | slide de exemplo |
|---|---|---|
| dois cards lado a lado com pergunta grande | abertura, uma task por card | 1 |
| card de contexto + grade 2×2 de cards | método: o que fica fixo → o que muda | 2 |
| barras com a escala dita no eixo | comparar braços numa métrica | 3 |
| número grande → seta → número grande | antes/depois, "suspeito × veredito" | 4 |
| grade 2×2 de cards de texto | ressalvas | 5 |
| lista de cards com chip do código da task | próximos passos | 6 |

Variações que também funcionam, montadas com os mesmos blocos:

- **Barras agrupadas por braço:** `rotulo('Braço A')` + duas `barra`, e
  depois `rotulo('Braço B')` + duas `barra`, cada braço com a sua cor.
- **Barras com linha de referência** (uma régua ou um critério fixado
  antes): um `<div>` posicionado em `absolute` com
  `border-left:3px dashed`, mais uma legenda em `rotulo` embaixo.
  Confira a posição contra um valor conhecido.
- **Barras com coluna extra** (métrica secundária ao lado): o argumento
  `extra=` de `barra()` recebe um `<div class='mono'>`.

Barras: `frac` é a posição na escala que você escolheu; **diga a escala
no slide** (`escala('0,5 = acaso', '1,0')`). Uma barra de AUC que começa
em zero esconde a diferença; começando em 0,5, ela mostra o que é acaso.

## Revisão

Checklist para cada `revisao_*.png` (e uma página do PDF no fim):

- [ ] Nenhum texto quebrado onde não devia: chips, legendas e valores
      numa linha só (use `white-space:nowrap` se preciso).
- [ ] Título com no máximo 2 linhas.
- [ ] Barras proporcionais ao valor e coerentes com a escala escrita.
- [ ] Linhas de referência no lugar certo do eixo (confira contra um
      valor conhecido: 0,43 tem que ficar logo à direita de 0,38).
- [ ] Cores consistentes: o mesmo braço tem a mesma cor em todo o deck.
- [ ] Todo número confere com o documento de resultados.
- [ ] Nada encostado na borda direita ou no rodapé.
- [ ] Acentos e aspas tipográficas certos (“ ” e não " ").
