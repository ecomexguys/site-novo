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
alvo = rd(f"{REPO}/extrator-di.html")

if "extrator-di.png" in alvo:
    raise SystemExit("ja aplicado")

# --- hero: coluna da direita com a captura
hero_col = bloco(ncm, 'src="assets/img/NCM-comex-2.png"', subir=2)
hero_col = re.sub(r'<img[^>]*>',
                  '<img decoding="async" width="1008" height="632" src="assets/img/extrator-di.png" '
                  'class="attachment-full size-full" alt="Lista de execuções do extrator de DI na plataforma Commex Tech" />',
                  hero_col)
pos = fecha_de(alvo, 'elementor-element-54ed3164')
alvo = alvo[:pos] + "\n\t\t" + hero_col + alvo[pos:]

# --- meio: captura do detalhe da sugestao
meio = bloco(ncm, 'src="assets/img/NCM2.gif"', subir=1)
meio = re.sub(r'<img[^>]*>',
              '<img decoding="async" width="1626" height="1026" src="assets/img/Tela-extrator-di.png" '
              'class="attachment-full size-full" alt="Lista de declarações aberta por adição e item, com as ações de catalogar e gerar produto com IA" '
              'loading="lazy" />',
              meio)
marca = "Cada DI aparece com adição, item, NCM, descrição, exportador e fabricante,"
pos = fecha_de(alvo, marca)
alvo = alvo[:pos] + "\n\t\t" + meio + alvo[pos:]

# nao precisa mais do ajuste de hero sem captura nem do aviso
alvo = alvo.replace("commex-sem-captura ", "")
alvo = re.sub(r"<!-- REVISAR:.*?-->\n", "", alvo, flags=re.S)
alvo = alvo.replace("<body ",
                    "<!-- REVISAR: copy rascunhada a partir das telas do portal; validar com o time de produto. "
                    "Capturas tiradas do portal-ti em 10/09/2026, com CNPJ, numero de DI e nome de fornecedor "
                    "trocados por valores de exemplo. -->\n<body ", 1)
wr(f"{REPO}/extrator-di.html", alvo)
print("imagens inseridas")
