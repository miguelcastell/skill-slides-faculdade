"""Componentes visuais dos slides de sprint.

Cada slide é um HTML que desenha SÓ a área de conteúdo (680x330 pt do
slide, renderizada a 2 px/pt = 1360x660 px). O cabeçalho do modelo da
turma ("Atividades - <nome>", "Tasks" e o logo) é posto depois, pelo
`construir.py`, em texto nativo no .pptx e no .pdf.

Uso, num arquivo de deck:

    from componentes import Deck, card, barra, numero, chip, rotulo, destaque

    deck = Deck()
    deck.slide("<h1>Título que é uma frase</h1>" + card(...), nota="fala do slide")
"""

LARGURA, ALTURA = 1360, 660  # px da área de conteúdo (680x330 pt a 2 px/pt)

# Paleta vinho (troque pelas cores do logo da sua instituição). --esc é o
# braço principal / o que é bom; --med é o contraste / o que chama atenção.
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700&family=IBM+Plex+Sans:wght@400;600&family=IBM+Plex+Mono:wght@400;500&display=block');
:root{--esc:#5c1a2b;--med:#a8445e;--card:#f7eff1;--borda:#ecd9de;--txt:#231a1d;--mudo:#7a6a6f;--trilho:#f1e4e8}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1360px;height:660px;background:#fff;color:var(--txt);font-family:'IBM Plex Sans',sans-serif;font-size:25px;line-height:1.45;overflow:hidden}
.pag{padding:4px 40px 0 18px;height:660px}
h1{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:54px;line-height:1.12;letter-spacing:-.5px;margin-bottom:30px;max-width:1300px}
b{font-weight:600}
.mono{font-family:'IBM Plex Mono',monospace;font-size:21px;color:var(--mudo)}
.card{background:var(--card);border:2px solid var(--borda);border-radius:22px;padding:26px 30px}
.esc{color:var(--esc);font-weight:600}.med{color:var(--med);font-weight:600}
.mudo{color:var(--mudo)}.peq{font-size:21px}
.linha{display:flex;gap:30px}
.grade2{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.big{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:72px;line-height:1;color:var(--esc)}
.bar{height:40px;border-radius:10px;background:var(--trilho);position:relative;flex:1}
.bar>i{position:absolute;left:0;top:0;bottom:0;border-radius:10px}
.chip{display:inline-block;background:#fff;border:2px solid var(--borda);border-radius:12px;padding:4px 14px;white-space:nowrap;font-family:'IBM Plex Mono',monospace;font-size:20px}
.seta{font-family:'Space Grotesk',sans-serif;font-size:60px;color:var(--med)}
p+p{margin-top:16px}
"""

# Marca no DOM se algo passou da área de conteúdo. O construir.py lê isso
# com --dump-dom e falha alto: texto cortado no slide não é aceitável.
_SONDA = """<script>
addEventListener('load',()=>setTimeout(()=>{
 const W=%d,H=%d,f=[];
 document.querySelectorAll('.pag *').forEach(e=>{const r=e.getBoundingClientRect();
  if(r.width&&(r.right>W+1||r.bottom>H+1))f.push(e.tagName+'.'+(e.className||'')+' '+Math.round(r.right)+'x'+Math.round(r.bottom));
  if(e.scrollWidth>e.clientWidth+2&&getComputedStyle(e).overflow!=='visible')f.push('corte '+e.tagName);});
 document.body.setAttribute('data-estouro',f.slice(0,5).join(' | ')||'ok');},1500));
</script>""" % (LARGURA, ALTURA)


def pagina_html(corpo):
    return (f"<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><style>{CSS}</style></head>"
            f"<body><div class='pag'>{corpo}</div>{_SONDA}</body></html>")


class Deck:
    """Lista ordenada de slides: (corpo HTML, nota do apresentador)."""

    def __init__(self):
        self.slides = []

    def slide(self, corpo, nota=""):
        assert "<h1>" in corpo, "todo slide abre com um <h1> que é uma frase"
        assert nota.strip(), "todo slide precisa de nota do apresentador"
        self.slides.append((corpo, nota))


# ── Blocos ─────────────────────────────────────────────────────────────

def rotulo(texto, estilo=""):
    """Legenda pequena em mono, acima de um bloco ("passo 1 · correlação")."""
    return f"<div class='mono' style='{estilo}'>{texto}</div>"


def card(conteudo, titulo=None, estilo="flex:1"):
    topo = rotulo(titulo, "margin-bottom:8px") if titulo else ""
    return f"<div class='card' style='{estilo}'>{topo}{conteudo}</div>"


def numero(valor, legenda, cor="var(--esc)"):
    """Número grande com uma linha de explicação embaixo."""
    return (f"<div class='big' style='margin-top:6px;color:{cor}'>{valor}</div>"
            f"<p style='margin-top:8px'>{legenda}</p>")


def chip(texto, cor="var(--esc)", estilo=""):
    return f"<span class='chip' style='color:{cor};{estilo}'>{texto}</span>"


def destaque(texto, forte=True):
    """Trecho colorido dentro de uma frase: forte=True usa --esc, senão --med."""
    return f"<span class='{'esc' if forte else 'med'}'>{texto}</span>"


def barra(rotulo_txt, valor_txt, frac, cor="var(--esc)", larg_rot=230, altura=40, fonte=25, extra=""):
    """Barra horizontal: rótulo | trilho com preenchimento `frac` (0..1) | valor.

    `frac` é a posição já normalizada pela escala do gráfico — quem chama
    decide a escala (ex.: AUC de 0,5 a 0,85) e diz a escala no slide.
    """
    assert 0 <= frac <= 1.0001, f"frac fora de 0..1: {frac}"
    return (f"<div style='display:flex;align-items:center;gap:22px;margin:10px 0'>"
            f"<div style='width:{larg_rot}px;font-size:{fonte}px'>{rotulo_txt}</div>"
            f"<div class='bar' style='height:{altura}px'><i style='width:{frac*100:.1f}%;background:{cor}'></i></div>"
            f"<div class='mono' style='width:110px;color:var(--txt);font-size:24px'>{valor_txt}</div>{extra}</div>")


def escala(minimo, maximo, larg_rot=230):
    """Legenda do eixo embaixo de um grupo de barras."""
    return (f"<div class='mono' style='display:flex;justify-content:space-between;"
            f"margin-left:{larg_rot + 22}px;margin-right:132px;font-size:19px'>"
            f"<span style='white-space:nowrap'>{minimo}</span><span style='white-space:nowrap'>{maximo}</span></div>")


def fmt(x, casas=3):
    """Número no formato brasileiro: 0.764 -> '0,764'."""
    return f"{x:.{casas}f}".replace(".", ",")
