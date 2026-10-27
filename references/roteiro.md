# Roteiro de um deck de apresentação

O deck responde, nesta ordem: **o que perguntamos, como fizemos, o que
deu, o que ainda não dá para afirmar e o que vem agora.** É o pedido
clássico de apresentação de sprint: "o que foi feito, como foi feito,
resultados e próximos passos".

## O arco (6 a 12 slides)

| # | slide | o que leva | exemplo (`exemplos/exemplo.py`) |
|---|---|---|---|
| 1 | **Abertura** | a pergunta de cada task, em linguagem comum, com o número da task num rótulo pequeno; uma linha de contexto (sobre que dados, em que conjunto) | "Sprint 3: dá para separar spam sem ler o e-mail inteiro?" |
| 2 | **Método** (um por task, se os métodos forem diferentes) | os passos, com a lógica de cada um em uma frase; diga qual é o CONTROLE | "Como medimos: o mesmo modelo, entradas diferentes" |
| 3…n | **Um resultado por slide** | título = a conclusão; um gráfico OU um número grande; à direita, 2 ou 3 frases que leem o gráfico | "Só o assunto já chega perto do e-mail inteiro" |
| n+1 | **O que ler com cuidado** | 3 ou 4 ressalvas em cards, cada uma com a frase-chave em negrito | "O que ler com cuidado" |
| n+2 | **Próximos passos** | 3 ou 4 linhas: chip com o código da task (ou "com o grupo"), a ação e o porquê | "Próximos passos" |

Projeto sem experimento (um app, um sistema, uma pesquisa
bibliográfica) segue o mesmo arco: "método" vira "como foi construído"
e "resultado" vira "o que funciona hoje", mostrado com número sempre que
houver (telas prontas, testes passando, usuários atendidos).

## Regras de conteúdo

- **O título é uma frase com verbo e conclusão.** Quem ler só os títulos
  precisa sair com a história inteira. No máximo ~2 linhas a 54 px; se
  passar, encurte.
- **Um gráfico ou um número grande por slide de resultado.** Dois
  gráficos competem, e o público não sabe para onde olhar.
- **O texto da direita LÊ o gráfico** em vez de repetir o título: diz o
  tamanho do efeito, quantas vezes ele se repetiu e o que significa.
- **Estatística aparece como frase**, não como fórmula: "nas 3
  repetições", "o erro quase triplica". Teste de hipótese, graus de
  liberdade e p-valor ficam no relatório, não no slide.
- **Conceito explicado na primeira aparição**, em meia frase: "AUC (0,5
  é chute, 1 é acerto perfeito)".
- **Cada resultado diz se é firme ou não.** Empate é dito como empate.
- **Nota do apresentador em todo slide:** 1 ou 2 frases com o que falar,
  incluindo a ressalva que o slide não mostra. É o roteiro de fala.
- **Próximos passos amarrados a tasks reais**, já criadas. Nada de
  "resultado final" enquanto o semestre não acabou.

## O que NÃO entra

- Nome de arquivo, script, flag, variável de ambiente ou chave interna
  (`exp3_seed42`). Use o nome legível ("modelo só com o assunto").
- Tabela grande copiada do relatório. Escolha os 2 a 7 números que
  contam a história e desenhe-os.
- Dado pessoal, identificador ou material sensível de qualquer tipo
  (ver SKILL.md).
