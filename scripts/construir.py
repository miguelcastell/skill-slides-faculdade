"""Constrói um deck de apresentação: HTML -> PNG -> .pptx + .pdf no modelo da turma.

    python scripts/construir.py <deck.py> [--saida "Sprint 03 - Fulano"] [--so-revisao]

O <deck.py> define `DECK` (um componentes.Deck). Etapas:

1. cada slide vira um HTML de 1360x660 (só a área de conteúdo);
2. o Chrome/Edge headless confere se algo ESTOUROU a área (falha alto)
   e tira o print a 2x;
3. monta grades de revisão (6 slides por imagem) para conferência visual;
4. o .pptx sai pelo pptxgenjs: cabeçalho e logo nativos, conteúdo como
   imagem, nota do apresentador em cada slide;
5. o .pdf sai do próprio Chrome, com o mesmo layout em pontos.

Configuração: um `slides.json` na pasta onde o comando roda (ver o
README). Os argumentos da linha de comando têm prioridade sobre ele.
"""
import argparse
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import xml.dom.minidom as md
import zipfile
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    _s.reconfigure(encoding="utf-8")

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from componentes import ALTURA, LARGURA, pagina_html  # noqa: E402

PADRAO = {
    "nome": "",
    "titulo": "Atividades - {nome}",
    "subtitulo": "Tasks",
    "logo": "",
    "destino": ".",
    "arquivo": "Sprint {sprint:02d} - {nome}",
    "trabalho": ".slides-build",
}

CHROMES = [os.environ.get("CHROME", ""),
           r"C:\Program Files\Google\Chrome\Application\chrome.exe",
           r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
           r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
           "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
           "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"]


def achar_chrome():
    for c in CHROMES:
        if c and Path(c).exists():
            return c
    raise SystemExit("Chrome/Edge não encontrado. Defina a variável CHROME com o caminho do executável.")


def chrome(exe, *args):
    base = [exe, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
            "--virtual-time-budget=8000"]
    return subprocess.run(base + list(args), capture_output=True, text=True, encoding="utf-8", errors="replace")


def carregar_config(args):
    cfg = dict(PADRAO)
    arquivo = Path("slides.json")
    if arquivo.exists():
        cfg.update(json.loads(arquivo.read_text(encoding="utf-8")))
    for chave in ("nome", "titulo", "subtitulo", "logo", "destino", "trabalho"):
        valor = getattr(args, chave, None)
        if valor is not None:
            cfg[chave] = valor
    if not cfg["nome"]:
        raise SystemExit("Falta o nome de quem apresenta: --nome \"Fulano\" ou \"nome\" no slides.json.")
    if args.saida:
        cfg["base"] = args.saida
    elif args.sprint is not None:
        cfg["base"] = cfg["arquivo"].format(sprint=int(args.sprint), nome=cfg["nome"])
    else:
        raise SystemExit("Diga o nome do arquivo: --saida \"...\" ou --sprint N (usa o modelo do slides.json).")
    cfg["titulo"] = cfg["titulo"].format(nome=cfg["nome"])
    cfg["logo"] = str(Path(cfg["logo"]).resolve()) if cfg["logo"] else ""
    if cfg["logo"] and not Path(cfg["logo"]).exists():
        raise SystemExit(f"Logo não encontrado: {cfg['logo']}")
    return cfg


def carregar_deck(caminho):
    spec = importlib.util.spec_from_file_location("deck_apresentacao", caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert hasattr(mod, "DECK"), f"{caminho} não define DECK"
    assert mod.DECK.slides, "o deck está vazio"
    return mod.DECK.slides


def renderizar(slides, trab, exe):
    (trab / "html").mkdir(parents=True, exist_ok=True)
    (trab / "png").mkdir(exist_ok=True)
    estouros = []
    for i, (corpo, _) in enumerate(slides, 1):
        n = f"s{i:02d}"
        html = trab / "html" / f"{n}.html"
        html.write_text(pagina_html(corpo), encoding="utf-8")
        dom = chrome(exe, f"--window-size={LARGURA},{ALTURA}", "--dump-dom", html.as_uri()).stdout
        m = re.search(r'data-estouro="([^"]*)"', dom)
        if not m:
            estouros.append(f"{n}: a sonda não rodou (Chrome sem resposta?)")
        elif m.group(1) != "ok":
            estouros.append(f"{n}: {m.group(1)}")
        png = trab / "png" / f"{n}.png"
        chrome(exe, "--force-device-scale-factor=2", f"--window-size={LARGURA},{ALTURA}",
               f"--screenshot={png}", html.as_uri())
        assert png.exists(), f"o Chrome não gerou {png}"
    return estouros


def grades(trab, total):
    from PIL import Image
    pngs = [trab / "png" / f"s{i:02d}.png" for i in range(1, total + 1)]
    saidas = []
    for k in range(0, total, 6):
        lote = [Image.open(p).resize((1020, 495)) for p in pngs[k:k + 6]]
        g = Image.new("RGB", (2050, 505 * 3), "gray")
        for j, im in enumerate(lote):
            g.paste(im, ((j % 2) * 1030, (j // 2) * 505))
        destino = trab / f"revisao_{k // 6 + 1}.png"
        g.save(destino)
        saidas.append(destino)
    return saidas


def montar_pptx(slides, trab, cfg, saida):
    if not (AQUI / "node_modules" / "pptxgenjs").exists():
        print("instalando pptxgenjs (só na primeira vez)...")
        subprocess.run("npm install --no-audit --no-fund", cwd=AQUI, shell=True, check=True)
    dados = {"titulo": cfg["titulo"], "subtitulo": cfg["subtitulo"], "logo": cfg["logo"],
             "slides": [{"png": str(trab / "png" / f"s{i:02d}.png"), "nota": nota}
                        for i, (_, nota) in enumerate(slides, 1)],
             "saida": str(saida)}
    (trab / "pptx.json").write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    r = subprocess.run(["node", str(AQUI / "montar_pptx.js"), str(trab / "pptx.json")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert r.returncode == 0 and saida.exists(), f"pptxgenjs falhou:\n{r.stderr}"


def montar_pdf(total, trab, cfg, saida, exe):
    # Mesmas medidas do .pptx, em pontos (slide 16:9 de 720x405 pt).
    logo = f"<img class='logo' src='{Path(cfg['logo']).as_uri()}'>" if cfg["logo"] else ""
    pags = "".join(
        f"<section><div class='t'>{cfg['titulo']}</div><div class='s'>{cfg['subtitulo']}</div>{logo}"
        f"<img class='c' src='{(trab / 'png' / f's{i:02d}.png').as_uri()}'></section>"
        for i in range(1, total + 1))
    html = trab / "pdf.html"
    html.write_text(
        "<!doctype html><html><head><meta charset='utf-8'><style>"
        "@page{size:720pt 405pt;margin:0}*{margin:0;padding:0}body{font-family:Arial,sans-serif}"
        "section{position:relative;width:720pt;height:405pt;overflow:hidden;page-break-after:always;background:#fff}"
        ".t{position:absolute;left:17pt;top:10pt;font-size:29pt;line-height:34pt;color:#000;white-space:nowrap}"
        ".s{position:absolute;left:17pt;top:42pt;font-size:21pt;line-height:24pt;color:#000}"
        ".logo{position:absolute;left:493pt;top:0;width:223pt;height:62pt;object-fit:contain;object-position:right center}"
        ".c{position:absolute;left:20pt;top:68pt;width:680pt;height:330pt}"
        f"</style></head><body>{pags}</body></html>", encoding="utf-8")
    chrome(exe, "--no-pdf-header-footer", f"--print-to-pdf={saida}", html.as_uri())
    assert saida.exists(), "o Chrome não gerou o PDF"


def conferir_pptx(pptx, esperado):
    z = zipfile.ZipFile(pptx)
    for n in z.namelist():
        if n.endswith((".xml", ".rels")):
            md.parseString(z.read(n))
    n_sl = len([n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)])
    assert n_sl == esperado, f".pptx com {n_sl} slides, esperado {esperado}"


def main():
    ap = argparse.ArgumentParser(description="Monta um deck de apresentação no modelo da turma.")
    ap.add_argument("deck", type=Path, help="arquivo .py que define DECK")
    ap.add_argument("--saida", help="nome do arquivo final, sem extensão")
    ap.add_argument("--sprint", help="número da sprint (preenche o modelo 'arquivo' do slides.json)")
    ap.add_argument("--nome", help="quem apresenta (vai no cabeçalho e no nome do arquivo)")
    ap.add_argument("--titulo", help="título do cabeçalho; aceita {nome}")
    ap.add_argument("--subtitulo", help="linha de baixo do cabeçalho")
    ap.add_argument("--logo", help="imagem do logo no canto direito (opcional)")
    ap.add_argument("--destino", help="pasta dos arquivos finais")
    ap.add_argument("--trabalho", help="pasta dos intermediários (HTML, PNG, grades)")
    ap.add_argument("--so-revisao", action="store_true", help="só HTML, PNG e grades (sem .pptx/.pdf)")
    a = ap.parse_args()

    cfg = carregar_config(a)
    exe = achar_chrome()
    slides = carregar_deck(a.deck)
    trab = Path(cfg["trabalho"]).resolve() / re.sub(r"[^\w-]+", "_", cfg["base"])
    if trab.exists():
        shutil.rmtree(trab)
    trab.mkdir(parents=True)

    estouros = renderizar(slides, trab, exe)
    revisoes = grades(trab, len(slides))
    print(f"{len(slides)} slides renderizados em {trab}")
    for r in revisoes:
        print("revisar:", r)
    if estouros:
        print("\nESTOURO DE ÁREA — corrigir antes de montar:")
        for e in estouros:
            print("  ", e)
        raise SystemExit(1)
    if a.so_revisao:
        return

    destino = Path(cfg["destino"]).resolve()
    destino.mkdir(parents=True, exist_ok=True)
    pptx, pdf = destino / f"{cfg['base']}.pptx", destino / f"{cfg['base']}.pdf"
    montar_pptx(slides, trab, cfg, pptx)
    montar_pdf(len(slides), trab, cfg, pdf, exe)
    conferir_pptx(pptx, len(slides))
    print(f"\nok: {pptx}\nok: {pdf}")


if __name__ == "__main__":
    main()
