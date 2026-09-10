#!/usr/bin/env python3
"""Converte o mirror do WP/Elementor em site estatico no repo site-novo."""
import os, re, shutil, json, sys

SRC  = os.path.dirname(os.path.abspath(__file__)) + "/mirror"
REPO = "/Users/nicolasrocha/Library/CloudStorage/OneDrive-CommexTech/Marketing - Documentos/Site Institucional/site-novo"
DOM  = "https://commex.eltonpedroso.com.br"

PAGES = {                      # arquivo mirror -> arquivo final
    "page-home.html": "index.html",
    "page-65.html":   "sobre.html",
    "page-150.html":  "cadastro-de-produtos.html",
    "page-116.html":  "ncm.html",
    "page-136.html":  "duimp.html",
    "page-152.html":  "lpco.html",
    "page-146.html":  "du-e.html",
    "page-154.html":  "nfe.html",
    "page-148.html":  "integracoes.html",
    "page-275.html":  "contato.html",
}
PAGEID = {  # page_id -> arquivo
    "16": "index.html", "13": "index.html", "65": "sobre.html",
    "150": "cadastro-de-produtos.html", "116": "ncm.html", "136": "duimp.html",
    "152": "lpco.html", "146": "du-e.html", "154": "nfe.html",
    "148": "integracoes.html", "275": "contato.html",
}
TITLES = {  # arquivo -> (title, description)
    "index.html": ("Commex Tech — Governança e automação para o comércio exterior",
        "Plataforma de governança para comércio exterior: cadastro de produtos em massa, classificação NCM por agente especializado e integração com o Portal Único."),
    "sobre.html": ("Sobre nós — Commex Tech",
        "Quem é a Commex Tech: tecnologia de governança para operações de comércio exterior em escala."),
    "cadastro-de-produtos.html": ("Catálogo de Produtos — Commex Tech",
        "Cadastro de produtos em massa, atributos do Portal Único validados antes do envio e trilha de auditoria por SKU."),
    "ncm.html": ("Classificador de NCM — Commex Tech",
        "Agente especializado em classificação fiscal: sugere a NCM com score de confiança e base legal, e gera a descrição do produto a partir de imagem ou catálogo em PDF."),
    "duimp.html": ("DUIMP — Commex Tech",
        "Prontidão para a DUIMP: medimos quanto do seu catálogo atende às exigências e organizamos o preenchimento do que falta."),
    "lpco.html": ("LPCO — Commex Tech",
        "Licenças e anuências acompanhadas dentro do fluxo, com o prazo de cada órgão anuente visível para o time."),
    "du-e.html": ("DU-E — Commex Tech",
        "Dados do ERP direto para a DU-E, com o histórico de cada envio registrado."),
    "nfe.html": ("NFe — Commex Tech",
        "Integração fiscal alinhada à operação de comex, sem divergência entre sistemas."),
    "integracoes.html": ("Integração ERP — Commex Tech",
        "SAP, TOTVS, Oracle, OSGT e sistemas próprios conectados por API REST ou SFTP, com OAuth e ambiente multi-tenant isolado."),
    "contato.html": ("Fale Conosco — Commex Tech",
        "Fale com um especialista da Commex Tech e veja onde a sua operação de comex está exposta."),
}

# ---------------------------------------------------------------- assets
def target_for(path):
    """wp-path -> caminho no repo (ou None se deve sumir)."""
    # chunks lazy-loaded do Elementor: precisam manter a estrutura <plugin>/js/
    m = re.match(r"wp-content/plugins/(elementor|pro-elements)/assets/js/(.+\.bundle\.min\.js)$", path)
    if m:
        return f"assets/{m.group(1)}/js/{m.group(2)}"
    if re.match(r"wp-content/uploads/\d{4}/\d{2}/", path):
        return "assets/img/" + os.path.basename(path)
    if path.startswith("wp-content/uploads/elementor/css/"):
        return "assets/css/" + os.path.basename(path)
    if path == "wp-content/plugins/elementor/assets/images/placeholder.png":
        return "assets/img/placeholder.png"
    if path.startswith("wp-content/plugins/elementor/assets/css/"):
        return "assets/css/elementor-" + os.path.basename(path)
    if path.startswith("wp-content/plugins/elementor/assets/js/"):
        return "assets/js/elementor-" + os.path.basename(path)
    if path.startswith("wp-content/plugins/pro-elements/assets/lib/"):
        return "assets/js/" + os.path.basename(path)
    if path.startswith("wp-content/plugins/pro-elements/assets/css/"):
        return "assets/css/pro-" + os.path.basename(path)
    if path.startswith("wp-content/plugins/pro-elements/assets/js/"):
        return "assets/js/pro-" + os.path.basename(path)
    if path.startswith("wp-content/plugins/depoimentos-commex-tech/assets/css/"):
        return "assets/css/" + os.path.basename(path)
    if path.startswith("wp-content/plugins/depoimentos-commex-tech/assets/js/"):
        return "assets/js/" + os.path.basename(path)
    if path.startswith("wp-content/themes/hello-elementor/assets/css/"):
        return "assets/css/hello-" + os.path.basename(path)
    if path.startswith("wp-content/themes/hello-elementor/assets/js/"):
        return "assets/js/" + os.path.basename(path)
    if path.startswith("wp-includes/js/"):
        return "assets/js/" + os.path.basename(path)
    return None

def copy_assets():
    n = 0
    for root, _, files in os.walk(SRC):
        for f in files:
            full = os.path.join(root, f)
            rel  = os.path.relpath(full, SRC)
            if not (rel.startswith("wp-content/") or rel.startswith("wp-includes/")):
                continue
            tgt = target_for(rel)
            if not tgt:
                print("  ignorado:", rel); continue
            dst = os.path.join(REPO, tgt)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if tgt.endswith(".css"):
                css = open(full, encoding="utf-8", errors="ignore").read()
                css = re.sub(DOM + r"/wp-content/uploads/\d{4}/\d{2}/([^)\"']+)", r"../img/\1", css)
                open(dst, "w", encoding="utf-8").write(css)
            else:
                shutil.copy2(full, dst)
            n += 1
    print(f"  {n} assets copiados")

# ---------------------------------------------------------------- html
DROP_STYLE_IDS  = {"wp-emoji-styles-inline-css", "joinchat-button-style-inline-css",
                   "cookieadmin-style-inline-css"}
DROP_SCRIPT_PAT = re.compile(r"cookieadmin|joinchat|wp-emoji", re.I)


def strip_divs(html, pattern):
    """Remove <div> balanceadas cujo start tag casa com pattern."""
    rx = re.compile(pattern)
    tag = re.compile(r"<(/?)div\b[^>]*>", re.I)
    while True:
        m = rx.search(html)
        if not m:
            return html
        start = html.rfind("<div", 0, m.end())
        depth, pos = 0, start
        while True:
            t = tag.search(html, pos)
            if not t:
                return html
            depth += -1 if t.group(1) else 1
            pos = t.end()
            if depth == 0:
                break
        html = html[:start] + html[pos:]

def clean(html, outname):
    # <link> descartaveis
    html = re.sub(r"[ \t]*<link[^>]*(complianz-gdpr|cookieadmin|creame-whatsapp-me)[^>]*>\n?", "", html)
    html = re.sub(r"[ \t]*<link[^>]*rel=[\"']?(alternate|profile|canonical|EditURI|pingback|shortlink|https://api\.w\.org/)[\"']?[^>]*>\n?", "", html)
    html = re.sub(r"[ \t]*<meta[^>]*name=['\"](robots|generator)['\"][^>]*>\n?", "", html)
    # <style> descartaveis
    def style_sub(m):
        sid = re.search(r'id="([^"]+)"', m.group(1) or "")
        return "" if sid and sid.group(1) in DROP_STYLE_IDS else m.group(0)
    html = re.sub(r"<style([^>]*)>.*?</style>\s*", lambda m: style_sub(m), html, flags=re.S)
    # <script> descartaveis (com e sem src)
    def script_sub(m):
        return "" if DROP_SCRIPT_PAT.search(m.group(0)) else m.group(0)
    html = re.sub(r"<script\b[^>]*>.*?</script>\s*", script_sub, html, flags=re.S)
    html = re.sub(r"<script\b[^>]*/?>\s*(?=<)", lambda m: "" if DROP_SCRIPT_PAT.search(m.group(0)) else m.group(0), html)
    # markup do joinchat e do banner de cookies
    html = strip_divs(html, r"<div[^>]*\b(?:id|class)=\"[^\"]*joinchat[^\"]*\"[^>]*>")
    html = strip_divs(html, r"<div[^>]*\b(?:id|class)=\"[^\"]*cookieadmin[^\"]*\"[^>]*>")
    html = re.sub(r"<button[^>]*cookieadmin[^>]*>.*?</button>\s*", "", html, flags=re.S)
    # noscript do emoji / links wp
    html = html.replace(' data-rsssl=1', '')

    # URLs -> caminhos relativos
    def repl(m):
        path = m.group(1).split("?")[0].split("#")[0]
        tgt = target_for(path)
        return tgt if tgt else m.group(0)
    html = re.sub(re.escape(DOM) + r"/([A-Za-z0-9_\-./%]+(?:\?[^\"'\\ )]*)?)", repl, html)
    # URLs escapadas em JSON (https:\/\/...)
    def repl_esc(m):
        path = m.group(1).replace("\\/", "/").split("?")[0]
        tgt = target_for(path)
        return tgt.replace("/", "\\/") if tgt else m.group(0)
    html = re.sub(re.escape(DOM).replace("/", r"\\?/") + r"\\?/([A-Za-z0-9_\-.\\/%]+)", repl_esc, html)
    # links de pagina
    for pid, f in sorted(PAGEID.items(), key=lambda kv: -len(kv[0])):
        html = html.replace(f"{DOM}/?page_id={pid}", f)
        html = html.replace(f"{DOM}/index.php?rest_route=/wp/v2/pages/{pid}", f)
    # o Elementor carrega chunks de widget a partir de urls.assets
    html = html.replace(DOM.replace("/", "\\/") + "\\/wp-content\\/plugins\\/elementor\\/assets\\/",
                        "assets\\/elementor\\/")
    html = html.replace(DOM.replace("/", "\\/") + "\\/wp-content\\/plugins\\/pro-elements\\/assets\\/",
                        "assets\\/pro-elements\\/")
    html = html.replace(f'"{DOM}/"', '"index.html"').replace(f"'{DOM}/'", "'index.html'")
    # o que sobrar do dominio (ajaxurl, rest, uploads, lottie no config do Elementor)
    html = re.sub(re.escape(DOM).replace("/", r"\\/") + r"[A-Za-z0-9_\-.\\/%?=]*", "", html)
    html = re.sub(re.escape(DOM) + r"[A-Za-z0-9_\-./%?=]*", "", html)
    html = re.sub(r"\?ver=[0-9a-zA-Z.\-]+", "", html)
    html = re.sub(r"&#0?38;ver=[0-9a-zA-Z.\-]+", "", html)

    # o designer subiu o mesmo logo com dois nomes (Commex-Tech.svg / commex-tech.svg);
    # em host case-sensitive um deles quebra, entao normalizamos para um so
    html = html.replace("img/commex-tech.svg", "img/Commex-Tech.svg")
    # o CTA final das paginas internas aponta para o placeholder do Elementor
    html = re.sub(r'<img[^>]*src="assets/img/placeholder\.png"[^>]*/?>',
                  '<img decoding="async" width="515" height="717" src="assets/img/fale-com-a-commex.png" '
                  'class="attachment-full size-full wp-image-27" alt="" '
                  'srcset="assets/img/fale-com-a-commex.png 515w, assets/img/fale-com-a-commex-215x300.png 215w" '
                  'sizes="(max-width: 515px) 100vw, 515px" loading="lazy" />', html)

    # title + description
    title, desc = TITLES[outname]
    html = re.sub(r"<title>.*?</title>",
                  f"<title>{title}</title>\n<meta name=\"description\" content=\"{desc}\">",
                  html, count=1, flags=re.S)
    # botao flutuante de WhatsApp (substitui o Joinchat)
    wa = ('\n<a class="commex-wa" href="https://wa.me/5547999744290?text=Ol%C3%A1%2C%20vim%20do%20site%20da%20'
          'Commex%20Tech%20e%20gostaria%20de%20mais%20informa%C3%A7%C3%B5es" target="_blank" rel="noopener"'
          ' aria-label="Falar no WhatsApp">'
          '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M3.516 3.516c4.686-4.686 '
          '12.284-4.686 16.97 0s4.686 12.283 0 16.97a12 12 0 0 1-13.754 2.299l-5.814.735a.392.392 0 0 '
          '1-.438-.44l.748-5.788A12 12 0 0 1 3.517 3.517zm3.61 17.043.3.158a9.85 9.85 0 0 0 '
          '11.534-1.758c3.843-3.843 3.843-10.074 0-13.918s-10.075-3.843-13.918 0a9.85 9.85 0 0 0-1.747 '
          '11.554l.16.303-.51 3.942a.196.196 0 0 0 .219.22zm6.534-7.003-.933 1.164a9.84 9.84 0 0 '
          '1-3.497-3.495l1.166-.933a.79.79 0 0 0 .23-.94L9.561 6.96a.79.79 0 0 0-.924-.445l-2.023.524a.797.797 '
          '0 0 0-.588.88 11.754 11.754 0 0 0 10.005 10.005.797.797 0 0 0 .88-.587l.525-2.023a.79.79 0 0 '
          '0-.445-.923L14.6 13.327a.79.79 0 0 0-.94.23z"/></svg></a>\n')
    html = html.replace("</body>", wa + '<link rel="stylesheet" href="assets/css/commex-static.css">\n</body>')
    # limpa linhas em branco repetidas no head
    html = re.sub(r"\n{3,}", "\n\n", html)
    return html

def main():
    print("copiando assets...");  copy_assets()
    print("convertendo paginas...")
    for src, out in PAGES.items():
        html = open(os.path.join(SRC, src), encoding="utf-8").read()
        open(os.path.join(REPO, out), "w", encoding="utf-8").write(clean(html, out))
        print(f"  {src} -> {out}")

if __name__ == "__main__":
    main()
