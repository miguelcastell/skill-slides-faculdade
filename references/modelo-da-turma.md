# O modelo da turma

O padrão desta skill é o modelo mais comum de apresentação coletiva de
turma: cada integrante tem as suas páginas, todas com o mesmo cabeçalho.
O slide é 16:9, **720×405 pt**, com fundo branco.

| elemento | posição (pt) | formato | de onde vem |
|---|---|---|---|
| título ("Atividades - Fulano") | x 17, y 10, altura 34 | Arial 29, preto | `titulo` no `slides.json` |
| subtítulo ("Tasks") | x 17, y 42, altura 24 | Arial 21, preto | `subtitulo` |
| logo da instituição | x 493, y 0, caixa 223×62 | imagem, encaixada na caixa | `logo` (opcional) |
| área de conteúdo (o PNG do slide) | x 20, y 68, 680×330 | imagem 1360×660 a 2x | o deck |

As mesmas medidas estão em `scripts/montar_pptx.js` (para o .pptx) e em
`montar_pdf` de `scripts/construir.py` (para o .pdf). Se o modelo da sua
turma for diferente, mude nos dois lugares.

## Adaptar a um PDF modelo da turma

1. Abra uma página do PDF modelo e meça as posições do cabeçalho em
   pontos. Um visualizador de PDF mostra o tamanho da página: em 16:9 ele
   costuma ter 720×405 pt.
2. Ajuste as coordenadas nos dois arquivos acima.
3. **O logo:** recorte-o renderizando a página do PDF modelo, em vez de
   extrair a imagem embutida. A extração direta costuma sair em branco ou
   sem transparência. Com `pymupdf`:

   ```python
   import pymupdf
   pagina = pymupdf.open("modelo.pdf")[0]
   pagina.get_pixmap(dpi=400, clip=pymupdf.Rect(493, 0, 716, 62), alpha=False).save("logo.png")
   ```

4. Troque as cores do tema (`CSS` em `scripts/componentes.py`) por duas
   cores do logo, para o conteúdo combinar com o cabeçalho.

## Nome do arquivo

O padrão é `Sprint NN - <nome>` (`arquivo` no `slides.json`, com
`{sprint:02d}` e `{nome}`). Use o número da sprint que está no **título
das tasks** e não o de outro documento: é o que a turma usa para achar a
sua parte.
