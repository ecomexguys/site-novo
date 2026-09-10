#!/usr/bin/env python3
"""Acrescenta ao Catálogo de Produtos: operadores estrangeiros, carga do Portal Único,
operações em massa e aviso de mudança de atributo (webhook do Portal Único)."""
import re, time

REPO = "/Users/nicolasrocha/Library/CloudStorage/OneDrive-CommexTech/Marketing - Documentos/Site Institucional/site-novo"
P = f"{REPO}/cadastro-de-produtos.html"

def rd(p):
    for _ in range(8):
        try: return open(p, encoding="utf-8", errors="ignore").read()
        except OSError: time.sleep(1)
    raise SystemExit("leitura falhou")

def wr(p, s):
    for _ in range(8):
        try:
            open(p, "w", encoding="utf-8").write(s); return
        except OSError: time.sleep(1)
    raise SystemExit("escrita falhou")

def block_at(html, idx, must_contain=None):
    tagre = re.compile(r"<(/?)div\b[^>]*>", re.I)
    search_from = idx
    while True:
        start = html.rfind('<div class="elementor-element', 0, search_from)
        depth, pos = 0, start
        while True:
            m = tagre.search(html, pos)
            depth += -1 if m.group(1) else 1
            pos = m.end()
            if depth == 0: break
        if pos > idx and (must_contain is None or must_contain in html[start:pos]):
            return start, pos, html[start:pos]
        search_from = start

NOVOS = [
    ("Operadores estrangeiros vinculados ao produto",
     "Fabricante, produtor e fornecedor de fora do Brasil ficam cadastrados com TIN e país de "
     "origem, e vinculados aos produtos que abastecem. O vínculo que o Portal Único exige sai do "
     "mesmo cadastro, sem planilha paralela."),
    ("Carga do que já está no Portal Único",
     "Produtos, operadores estrangeiros e os vínculos entre eles que já estão registrados no "
     "Portal Único entram por sincronização — com atributos ou para complementar depois. "
     "Ninguém recadastra o que a empresa já declarou."),
    ("Ações em massa sobre a seleção",
     "Selecione os itens e edite atributos, ative, desative, envie ao OSGT ou exclua rascunhos em "
     "bloco. A edição de atributo é merge: preenche o que falta sem apagar o que cada produto já "
     "tinha, e o resultado mostra item a item o que passou e o que ficou pendente."),
    ("Aviso quando o Portal Único muda o produto",
     "Quando uma mudança de atributo da NCM desativa um item no Portal Único, a notificação chega "
     "na plataforma e o produto aparece marcado. Em vez de descobrir no registro, o time reativa "
     "a nova versão em massa."),
]

html = rd(P)
if NOVOS[0][0] in html:
    raise SystemExit("ja aplicado")

# clona o 4o card de "o que o modulo faz" (container 1a4836ed)
i = html.find('elementor-element-1a4836ed e-con-full')
start, end, modelo = block_at(html, i + 50, must_contain="Histórico e versões por produto")
assert modelo.count("<h3") == 1, "o modelo pegou mais de um card"

novos_html = []
for titulo, texto in NOVOS:
    b = modelo.replace("Histórico e versões por produto", titulo)
    b = re.sub(r'(data-widget_type="text-editor.default">\s*).*?(\s*</div>)',
               lambda m: m.group(1) + texto + m.group(2), b, count=1, flags=re.S)
    novos_html.append(b)

html = html[:end] + "\n\t\t" + "\n\t\t".join(novos_html) + html[end:]

# o titulo da secao agora cobre mais que preenchimento
html = html.replace("Levantamento, preenchimento,<br>validação e histórico",
                    "Levantamento, preenchimento,<br>validação e acompanhamento")

wr(P, html)
print("4 blocos adicionados ao catalogo de produtos")
