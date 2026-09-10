#!/usr/bin/env python3
"""Devolve as duas capturas de tela para a pagina de Ex-Tarifario,
reaproveitando os mesmos blocos de imagem que a pagina de NCM usa."""
import re, time

REPO = "/Users/nicolasrocha/Library/CloudStorage/OneDrive-CommexTech/Marketing - Documentos/Site Institucional/site-novo"

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

def bloco(html, marca, subir=1):
    """Div balanceada que contem `marca`; subir=N pega o N-esimo ancestral."""
    i = html.find(marca)
    if i < 0: raise SystemExit("nao achei " + marca)
    tag = re.compile(r"<(/?)div\b[^>]*>", re.I)
    fim_busca = i
    for _ in range(subir):
        start = html.rfind('<div class="elementor-element', 0, fim_busca)
        depth, pos = 0, start
        while True:
            m = tag.search(html, pos)
            depth += -1 if m.group(1) else 1
            pos = m.end()
            if depth == 0: break
        fim_busca = start
    return html[start:pos]

def fecha_de(html, marca_inicio):
    """Posicao logo apos o fechamento da div que comeca em marca_inicio."""
    start = html.find(marca_inicio)
    start = html.rfind("<div", 0, start + 1)
    tag = re.compile(r"<(/?)div\b[^>]*>", re.I)
    depth, pos = 0, start
    while True:
        m = tag.search(html, pos)
        depth += -1 if m.group(1) else 1
        pos = m.end()
        if depth == 0: return pos

ncm = rd(f"{REPO}/ncm.html")
alvo = rd(f"{REPO}/ex-tarifario.html")

if "ex-tarifario.png" in alvo:
    raise SystemExit("ja aplicado")

# --- hero: coluna da direita com a captura
hero_col = bloco(ncm, 'src="assets/img/NCM-comex-2.png"', subir=2)
hero_col = re.sub(r'<img[^>]*>',
                  '<img decoding="async" width="1008" height="632" src="assets/img/ex-tarifario.png" '
                  'class="attachment-full size-full" alt="Tela de Sugestão de Ex-Tarifário na plataforma Commex Tech" />',
                  hero_col)
pos = fecha_de(alvo, 'elementor-element-54ed3164')
alvo = alvo[:pos] + "\n\t\t" + hero_col + alvo[pos:]

# --- meio: captura do detalhe da sugestao
meio = bloco(ncm, 'src="assets/img/NCM2.gif"', subir=1)
meio = re.sub(r'<img[^>]*>',
              '<img decoding="async" width="1626" height="1026" src="assets/img/Tela-ex-tarifario.png" '
              'class="attachment-full size-full" alt="Detalhe de uma sugestão de ex-tarifário com a lista do que falta informar" '
              'loading="lazy" />',
              meio)
pos = fecha_de(alvo, 'A decisão <span style="color:#FF5905">continua sendo humana</span>')
# insere depois do texto de apoio da secao, antes do botao
marca = "Nada é aplicado ao produto automaticamente."
pos = fecha_de(alvo, marca)
alvo = alvo[:pos] + "\n\t\t" + meio + alvo[pos:]

# nao precisa mais do ajuste de hero sem captura nem do aviso
alvo = alvo.replace("commex-sem-captura ", "")
alvo = re.sub(r"<!-- Copy baseada na spec do vault[^>]*-->\n", "", alvo)
alvo = alvo.replace("<body ",
                    "<!-- Copy baseada na spec do vault (04 - Regras de Negócio/Sugestão de Ex-Tarifário por IA); "
                    "capturas tiradas do portal em 10/09/2026. -->\n<body ", 1)
wr(f"{REPO}/ex-tarifario.html", alvo)
print("imagens inseridas")
