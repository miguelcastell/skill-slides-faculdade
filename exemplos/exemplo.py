"""Deck de EXEMPLO — projeto fictício, NÚMEROS INVENTADOS.

Mostra os padrões de layout da skill num projeto qualquer de faculdade
(um classificador de spam). Nenhum número aqui é medida real: o deck
existe para servir de molde, e cada slide traz "dados fictícios" na nota.

    python scripts/construir.py exemplos/exemplo.py --nome "Fulano de Tal" --saida "Exemplo"
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from componentes import Deck, barra, card, chip, destaque, escala, fmt, numero, rotulo  # noqa: E402

DECK = Deck()
ESC, MED = "var(--esc)", "var(--med)"
FICTICIO = " (Exemplo: dados fictícios.)"

# 1 — abertura: as perguntas da sprint, uma por task
DECK.slide(f"""
<h1>Sprint 3: dá para separar spam sem ler o e-mail inteiro?</h1>
<div class='linha'>
 {card(f"<p style='font-size:30px;font-weight:600'>Só o {destaque('assunto')} basta para achar spam?</p>"
       "<p class='mudo'>Sem abrir o corpo da mensagem.</p>", "task #12 · modelo pelo assunto")}
 {card(f"<p style='font-size:30px;font-weight:600'>O modelo {destaque('erra mais', False)} em e-mails curtos?</p>"
       "<p class='mudo'>Mensagens com menos de 20 palavras.</p>", "task #13 · análise de erros")}
</div>
<p class='mudo' style='margin-top:26px;font-size:22px'>Tudo medido no conjunto de validação; o teste continua guardado para o fim.</p>
""", nota="Duas tasks na sprint: modelo só com o assunto e onde ele erra." + FICTICIO)

# 2 — método: um card de contexto + grade de passos
passos = [("só o assunto", "a pergunta da task #12"),
          ("assunto + corpo", "a referência para comparar"),
          ("embaralhar o assunto", "controle: o modelo lê ou chuta?"),
          ("separar por tamanho", "a pergunta da task #13")]
DECK.slide(f"""
<h1>Como medimos: o mesmo modelo, entradas diferentes</h1>
<div class='linha' style='align-items:stretch'>
 {card(f"<p>Mesmo modelo, mesmos e-mails, {destaque('3 repetições')} com sorteios diferentes.</p>"
       "<p class='mudo peq'>Uma rodada sozinha não conclui nada.</p>", "o que fica fixo", "width:400px")}
 <div style='flex:1'>
  {rotulo('o que muda em cada braço', 'margin-bottom:12px')}
  <div class='grade2' style='gap:18px'>{''.join(card(f"<b>{a}</b><div class='mudo peq' style='margin-top:6px'>{b}</div>", estilo='padding:20px 22px') for a, b in passos)}</div>
 </div>
</div>
""", nota="Explicar o controle: com o assunto embaralhado, o modelo deveria cair para o acaso." + FICTICIO)


# 3 — resultado em barras, com a escala dita no eixo
def esc(v):
    return (v - 0.5) / 0.5


DECK.slide(f"""
<h1>Só o assunto já chega perto do e-mail inteiro</h1>
<div class='linha'>
 <div style='flex:1.35'>
  {rotulo('AUC média das 3 repetições', 'margin-bottom:4px')}
  {barra('assunto + corpo', fmt(0.94, 2), esc(0.94), ESC, 270)}
  {barra('só o assunto', fmt(0.90, 2), esc(0.90), ESC, 270)}
  {barra('assunto embaralhado', fmt(0.52, 2), esc(0.52), MED, 270)}
  {escala('0,5 = acaso', '1,0', 270)}
 </div>
 <div style='flex:1;padding-top:30px'>
  <p>O assunto sozinho perde só {destaque('0,04')} de AUC.</p>
  <p>Embaralhado, cai para o {destaque('acaso', False)}: o modelo lê o assunto de verdade.</p>
  <p class='mudo peq'>AUC: 0,5 é chute, 1 é acerto perfeito.</p>
 </div>
</div>
""", nota="O controle embaralhado é o que prova que o modelo usa o assunto." + FICTICIO)

# 4 — número grande → seta → número grande
DECK.slide(f"""
<h1>E-mail curto é onde o modelo mais erra</h1>
<div class='linha' style='align-items:center'>
 {card(numero('4%', 'de erro nos e-mails longos'), 'mais de 20 palavras')}
 <div class='seta'>→</div>
 {card(numero('11%', 'de erro nos e-mails curtos', MED), 'até 20 palavras')}
</div>
<p style='margin-top:26px'>Nos curtos o assunto é quase tudo o que existe, e {destaque('nas 3 repetições', False)} o erro foi maior.</p>
""", nota="O erro quase triplica nos e-mails curtos." + FICTICIO)

# 5 — ressalvas
cuid = ["<b>Uma base só.</b> Os e-mails vêm de uma única caixa; outra empresa pode ter outro tipo de spam.",
        "<b>3 repetições.</b> Diferença menor que 0,02 de AUC é empate.",
        "<b>Tudo na validação.</b> O número final sai do teste, no fim do projeto.",
        "<b>Spam muda com o tempo.</b> O modelo precisa ser reavaliado de tempos em tempos."]
DECK.slide(f"""
<h1>O que ler com cuidado</h1>
<div class='grade2' style='gap:22px'>{''.join(card(t, estilo='font-size:23px') for t in cuid)}</div>
""", nota="Ressalvas sempre têm slide próprio." + FICTICIO)

# 6 — próximos passos amarrados às tasks
prox = [("#14", "Testar com outra caixa de e-mail", "ver se o resultado se mantém fora da base atual."),
        ("#15", "Tratar e-mails curtos à parte", "um modelo próprio para eles."),
        ("com o grupo", "Decidir o limiar de alerta", "quanto spam pode passar contra quanto e-mail bom vai para a lixeira.")]
DECK.slide(f"""
<h1>Próximos passos</h1>
<div style='display:flex;flex-direction:column;gap:16px'>{''.join(card(chip(t, ESC, 'width:200px;text-align:center;flex:none') + f"<div><b>{a}</b> <span class='mudo'>· {b}</span></div>", estilo='display:flex;gap:24px;align-items:center;padding:18px 26px') for t, a, b in prox)}</div>
""", nota="Cada próximo passo aponta para uma task já criada." + FICTICIO)
