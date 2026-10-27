---
name: slides-faculdade
description: Gera slides de apresentação de projetos de faculdade (sprint, entrega parcial, resultado de task ou issue) no modelo da turma — cabeçalho "Atividades - <nome>", subtítulo e logo da instituição — e entrega .pptx e .pdf. Use sempre que pedirem slides, apresentação, deck, "o slide da sprint", "o pdf/pptx para apresentar" ou "slides dizendo o que foi feito, como, resultados e próximos passos" de um projeto acadêmico, mesmo que não digam "skill". Parte do material do próprio projeto e nunca inventa número.
---

# Slides de apresentação de projeto de faculdade

Transforma o que foi feito num projeto (uma sprint, uma task, uma
entrega) num deck curto, de 6 a 12 slides, que **alguém de fora da área
entende** na hora em que a pessoa apresenta. Sai em dois formatos com o
mesmo visual: `.pptx` (cabeçalho editável, notas do apresentador) e
`.pdf`.

**Antes de escrever um deck novo, leia `exemplos/exemplo.py`.** Ele é a
referência de tom, densidade e layout. Os números dele são fictícios:
servem de molde, nunca de conteúdo.

## Como funciona (por que é assim)

O modelo típico de apresentação de turma é um slide 16:9 branco, com um
cabeçalho fixo em cima (título, subtítulo e logo à direita) e a área de
conteúdo livre embaixo. O conteúdo é desenhado em **HTML**
(1360×660 px = 680×330 pt a 2 px/pt), porque HTML dá tipografia, barras
e cards com um controle fino que o PowerPoint gerado por código não dá.
O Chrome/Edge headless tira o print de cada slide, e o cabeçalho é
colocado **nativo** por cima: editável no .pptx e texto real no .pdf.

```
deck.py ──► HTML por slide ──► Chrome: sonda de estouro + print 2x
                                   │
                    grades de revisão (você OLHA)
                                   │
              ┌────────────────────┴────────────────────┐
         pptxgenjs (cabeçalho nativo + PNG + nota)   Chrome print-to-pdf
              └──────────────► <destino>/<nome>.pptx / .pdf
```

`<skill>` abaixo é a pasta desta skill (onde está este arquivo).

## Fluxo

### 1. Configurar (uma vez por projeto)

Veja se existe um `slides.json` na raiz do projeto. Se não existir,
pergunte o nome de quem apresenta e crie um:

```json
{
  "nome": "Fulano de Tal",
  "titulo": "Atividades - {nome}",
  "subtitulo": "Tasks",
  "logo": "caminho/para/logo.png",
  "destino": "docs",
  "arquivo": "Sprint {sprint:02d} - {nome}"
}
```

Só `nome` é obrigatório. Sem `logo`, o cabeçalho sai sem imagem. Se a
turma tiver um PDF modelo, confira as medidas em
`references/modelo-da-turma.md`. Coloque `.slides-build/` no
`.gitignore` do projeto: é a pasta dos intermediários.

### 2. Juntar o material (ainda sem escrever slide)

- A **fonte dos números** é o material do projeto: o relatório ou
  documento de resultados, o README, as issues/tasks, os logs. Se não
  existir nada escrito, escreva o resumo primeiro. Slide sem documento
  por trás vira número sem rastro.
- As tasks da sprint (o título manda) e as da próxima sprint, para o
  slide de próximos passos.
- As regras do próprio projeto (CLAUDE.md, README) valem por cima desta
  skill: o que não pode ser publicado, como numerar a sprint, o tom.

### 3. Roteiro

Siga `references/roteiro.md`: abertura com as perguntas → método (como
foi feito) → **um resultado por slide** → o que ler com cuidado →
próximos passos. Escreva primeiro só a lista de títulos. Cada título é
uma **frase que diz a conclusão** ("Só o assunto já chega perto do
e-mail inteiro"), nunca um rótulo ("Resultados").

### 4. Escrever o deck

Crie o arquivo do deck dentro de `.slides-build/` (ex.:
`.slides-build/deck_sprint3.py`), copiando a estrutura de
`exemplos/exemplo.py`. Ajuste o `sys.path.insert` para apontar para
`<skill>/scripts`. O arquivo importa `componentes`, cria `DECK = Deck()`
e chama `DECK.slide(corpo_html, nota=...)` para cada slide. Os blocos
prontos (`card`, `barra`, `numero`, `chip`, `destaque`, `escala`,
`rotulo`, `fmt`) e as regras visuais estão em `references/estilo.md`.

### 5. Renderizar e REVISAR

Rode na raiz do projeto, onde está o `slides.json`:

```bash
python <skill>/scripts/construir.py .slides-build/deck_sprint3.py --sprint 3 --so-revisao
```

- O script **falha** se algum elemento passar da área de conteúdo
  (texto cortado não chega ao slide).
- Depois disso, **abra com Read cada `revisao_*.png`** que ele imprimir
  e passe o checklist de `references/estilo.md#revisao`. Defeitos como
  legenda quebrada, chip partido e título longo demais só aparecem
  olhando. Corrija e rode de novo até a grade passar limpa.

### 6. Montar e entregar

```bash
python <skill>/scripts/construir.py .slides-build/deck_sprint3.py --sprint 3
```

Isso gera `<destino>/Sprint 03 - <nome>.pptx` e `.pdf`. Use `--saida
"..."` para dar outro nome. Na primeira vez ele instala o `pptxgenjs`
sozinho. Confira uma página do PDF e responda em linguagem simples: o
que o deck conta, quantos slides tem e onde estão os arquivos.

## Regras que não se negociam

- **Nenhum número que não esteja no material do projeto.** Arredondar
  pode; inventar, estimar ou "completar" não.
- **A ressalva aparece no deck**, num slide próprio. Resultado incerto é
  apresentado como incerto, em português claro.
- **Nada sensível no slide:** nenhum dado pessoal, identificador,
  imagem clínica ou credencial. O deck sai do projeto e vai para a
  turma.
- **Linguagem para quem não é da área:** explique o conceito na
  primeira vez que ele aparece, sem fórmula. Nome de arquivo, flag e
  variável de ambiente não entram.
- Não faça commit dos arquivos finais sem a pessoa pedir.

## Arquivos da skill

| arquivo | para quê |
|---|---|
| `scripts/construir.py` | orquestra tudo: HTML, sonda, PNG, grades, .pptx, .pdf |
| `scripts/componentes.py` | CSS do tema e blocos reutilizáveis |
| `scripts/montar_pptx.js` | monta o .pptx (pptxgenjs) |
| `exemplos/exemplo.py` | deck de exemplo, com dados fictícios |
| `references/roteiro.md` | arco narrativo e o que vai em cada slide |
| `references/estilo.md` | paleta, tipografia, padrões de layout e checklist de revisão |
| `references/modelo-da-turma.md` | medidas do cabeçalho e como adaptar ao modelo da sua turma |
