#!/usr/bin/env python3
"""Menu, rodape, grade da home e o bloco novo do modulo de NCM."""
import re, glob, os, time

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

def block_at(html, idx, must_contain=None):
    """Div balanceada mais interna que comeca antes de idx (subindo ate conter must_contain)."""
    tagre = re.compile(r"<(/?)div\b[^>]*>", re.I)
    search_from = idx
    while True:
        start = html.rfind('<div class="elementor-element', 0, search_from)
        if start < 0: raise SystemExit("nao achei container")
        depth, pos = 0, start
        while True:
            m = tagre.search(html, pos)
            if not m: raise SystemExit("desbalanceado")
            depth += -1 if m.group(1) else 1
            pos = m.end()
            if depth == 0: break
        block = html[start:pos]
        if pos > idx and (must_contain is None or must_contain in block):
            return start, pos, block
        search_from = start

# ------------------------------------------------------------ 1. menus
NOVOS_SUB = (
    '\n\t<li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-901">'
    '<a href="extrator-di.html" class="elementor-sub-item">Extrator de DI</a></li>'
    '\n\t<li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-902">'
    '<a href="ex-tarifario.html" class="elementor-sub-item">Sugestão de Ex-Tarifário</a></li>'
)
NOVOS_ITEM = (
    '\n<li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-903">'
    '<a href="extrator-di.html" class="elementor-item">Extrator de DI</a></li>'
    '\n<li class="menu-item menu-item-type-post_type menu-item-object-page menu-item-904">'
    '<a href="ex-tarifario.html" class="elementor-item">Sugestão de Ex-Tarifário</a></li>'
)
ANCORA_SUB  = '<a href="ncm.html" class="elementor-sub-item">Classificador de NCM</a></li>'
ANCORA_ITEM = '<a href="ncm.html" class="elementor-item">Classificador de NCM</a></li>'

def menus(html):
    """Insere os modulos novos logo depois do Classificador de NCM, em todas as
    copias do menu (principal e dropdown mobile, no header e no rodape)."""
    def ins(m):
        item = m.group(0)
        if "extrator-di.html" in html[m.end():m.end() + 400]:
            return item
        novos = NOVOS_SUB if "elementor-sub-item" in item else NOVOS_ITEM
        if 'tabindex="-1"' in item:
            novos = novos.replace('class="elementor-sub-item"', 'class="elementor-sub-item" tabindex="-1"')
            novos = novos.replace('class="elementor-item"', 'class="elementor-item" tabindex="-1"')
        return item + novos
    return re.sub(r'<a href="ncm\.html"[^>]*>Classificador de NCM</a></li>', ins, html)

# ------------------------------------------------------------ 2. cards da home
CARDS = [
    ("Extrator de DI",
     "As declarações de importação do período viram catálogo: cada DI chega aberta por adição e item, "
     "com NCM, descrição, exportador e fabricante prontos para catalogar.",
     "extrator-di.html", "Conhecer o módulo →"),
    ("Sugestão de Ex-Tarifário",
     "Varredura do catálogo em busca de itens de bem de capital e de informática com chance de "
     "enquadramento, priorizados por impacto e com a fundamentação registrada.",
     "ex-tarifario.html", "Conhecer o módulo →"),
]

def home_cards(html):
    if 'href="extrator-di.html">Conhecer o módulo' in html:
        return html
    i = html.rfind('commex-module-card')
    start, end, card = block_at(html, i, must_contain="commex-module-card")
    novos = []
    for titulo, texto, href, cta in CARDS:
        novo = card
        novo = re.sub(r'(<h3 class="elementor-heading-title elementor-size-default">).*?(</h3>)',
                      lambda m: m.group(1) + titulo + m.group(2), novo, count=1, flags=re.S)
        novo = re.sub(r'(data-widget_type="text-editor.default">\s*)<p>.*?</p>',
                      lambda m: m.group(1) + "<p>" + texto + "</p>", novo, count=1, flags=re.S)
        novo = re.sub(r'<h2 class="elementor-heading-title elementor-size-default"><a href="[^"]+">.*?</a></h2>',
                      f'<h2 class="elementor-heading-title elementor-size-default"><a href="{href}">{cta}</a></h2>',
                      novo, count=1, flags=re.S)
        novos.append(novo)
    return html[:end] + "\n\t\t" + "\n\t\t".join(novos) + html[end:]

# a plataforma passa a ter 8 modulos adicionais
CONTAGEM = [
    ("A base da plataforma é o Cadastro de Produtos: cadastro em massa, com IA e trilha de auditoria.<br>Classificação Fiscal NCM, Integrações ERP, DUIMP, LPCO, DU-E e NFe entram como módulos adicionais, contratados à parte conforme a operação precisa.",
     "A base da plataforma é o Cadastro de Produtos: cadastro em massa, com IA e trilha de auditoria.<br>Classificação Fiscal NCM, Extrator de DI, Sugestão de Ex-Tarifário, Integrações ERP, DUIMP, LPCO, DU-E e NFe entram como módulos adicionais, contratados à parte conforme a operação precisa."),
    ("O catálogo que sustenta toda a operação: cadastro de produtos em massa, atributos do Portal Único validados antes do envio e trilha de auditoria por SKU. Os outros seis módulos se somam a essa base.",
     "O catálogo que sustenta toda a operação: cadastro de produtos em massa, atributos do Portal Único validados antes do envio e trilha de auditoria por SKU. Os demais módulos se somam a essa base."),
]

# ------------------------------------------------------------ 3. bloco novo no NCM
NCM_TITULO = "Descrição a partir de imagem ou catálogo em PDF"
NCM_TEXTO  = ("Quando o produto chega só com código e foto, a plataforma lê a imagem ou o catálogo do "
              "fornecedor em PDF e monta a descrição que alimenta a classificação, em vez de alguém "
              "escrever item por item.")

def ncm_bloco(html):
    if NCM_TITULO in html:
        return html
    i = html.find("Reclassificação em lote")
    start, end, bloco = block_at(html, i, must_contain="<svg")
    novo = bloco.replace("Reclassificação em lote", NCM_TITULO)
    novo = re.sub(r'(data-widget_type="text-editor.default">\s*).*?(\s*</div>)',
                  lambda m: m.group(1) + NCM_TEXTO + m.group(2), novo, count=1, flags=re.S)
    return html[:end] + "\n\t\t" + novo + html[end:]

NCM_CARD_HOME = [
    ("Um agente especializado sugere a NCM com score de confiança e base legal. De 3–4 horas para 5 minutos por produto.",
     "Um agente especializado sugere a NCM com score de confiança e base legal, e monta a descrição do produto a partir de imagem ou catálogo em PDF. De 3–4 horas para 5 minutos por produto."),
]

def main():
    os.chdir(REPO)
    for p in sorted(glob.glob("*.html")):
        h = rd(p)
        orig = h
        h = menus(h)
        if p == "index.html":
            h = home_cards(h)
            for old, new in CONTAGEM + NCM_CARD_HOME:
                if old in h: h = h.replace(old, new)
        if p == "ncm.html":
            h = ncm_bloco(h)
            for old, new in CONTAGEM:
                if old in h: h = h.replace(old, new)
        if p in ("cadastro-de-produtos.html", "duimp.html", "lpco.html", "du-e.html",
                 "nfe.html", "integracoes.html", "extrator-di.html", "ex-tarifario.html", "sobre.html"):
            for old, new in CONTAGEM:
                if old in h: h = h.replace(old, new)
        if h != orig:
            wr(p, h); print("atualizado", p)

main()
