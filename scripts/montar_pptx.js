// Monta o .pptx a partir do JSON gerado pelo construir.py.
// Cabeçalho e logo são nativos (editáveis no PowerPoint); o conteúdo é o PNG.
const fs = require("fs");
const pptxgen = require("pptxgenjs");

const cfg = JSON.parse(fs.readFileSync(process.argv[2], "utf-8"));
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10 x 5,625 pol = 720 x 405 pt
pres.theme = { headFontFace: "Arial", bodyFontFace: "Arial" };
const pt = v => v / 72;

for (const sl of cfg.slides) {
  const s = pres.addSlide();
  s.background = { color: "FFFFFF" };
  s.addText(cfg.titulo, { x: pt(17), y: pt(10), w: pt(cfg.logo ? 470 : 690), h: pt(34), fontFace: "Arial", fontSize: 29, color: "000000", margin: 0, isTextBox: true });
  s.addText(cfg.subtitulo, { x: pt(17), y: pt(42), w: pt(300), h: pt(24), fontFace: "Arial", fontSize: 21, color: "000000", margin: 0, isTextBox: true });
  if (cfg.logo) {
    s.addImage({ path: cfg.logo, x: pt(493), y: 0, w: pt(223), h: pt(62), sizing: { type: "contain", w: pt(223), h: pt(62) }, altText: "Logo" });
  }
  s.addImage({ path: sl.png, x: pt(20), y: pt(68), w: pt(680), h: pt(330), altText: sl.nota });
  s.addNotes(sl.nota);
}
pres.writeFile({ fileName: cfg.saida }).then(f => console.log("ok", f));
