#!/usr/bin/env python3
"""Troca a foto do CTA final pelo formulario do RD Station usado nas LPs."""
import re, glob, os, time

REPO = "/Users/nicolasrocha/Library/CloudStorage/OneDrive-CommexTech/Marketing - Documentos/Site Institucional/site-novo"
FORM_ID = "lp-catalogo-produtos-2710b9dd7eace4d68d95"

FORM = f'''<div class="commex-rd-form">
							<div role="main" id="{FORM_ID}"></div>
							<script type="text/javascript" src="https://d335luupugsy2.cloudfront.net/js/rdstation-forms/stable/rdstation-forms.min.js"></script>
							<script type="text/javascript">
								new RDStationForms('{FORM_ID}', 'null').createForm();
							</script>
						</div>'''

def rd(p):
    for _ in range(8):
        try: return open(p, encoding="utf-8", errors="ignore").read()
        except OSError: time.sleep(1)
    raise SystemExit("leitura falhou: " + p)

def wr(p, s):
    for _ in range(8):
        try:
            open(p, "w", encoding="utf-8").write(s); return
        except OSError: time.sleep(1)
    raise SystemExit("escrita falhou: " + p)

os.chdir(REPO)
n = 0
for p in sorted(glob.glob("*.html")):
    s = rd(p)
    if FORM_ID in s:
        continue
    # so a primeira foto vira formulario (contato.html tem duas: bloco de contato e CTA final)
    novo, qtd = re.subn(r'<img[^>]*src="assets/img/fale-com-a-commex\.png"[^>]*/?>', FORM, s, count=1)
    if qtd == 0:
        print("  sem foto:", p); continue
    wr(p, novo); n += 1
    print("  formulario em", p)
print(f"{n} paginas")
