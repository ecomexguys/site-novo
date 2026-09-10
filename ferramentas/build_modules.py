#!/usr/bin/env python3
"""Gera as paginas dos modulos novos a partir de ncm.html (mesmo markup Elementor)."""
import re, sys, time

REPO = "/Users/nicolasrocha/Library/CloudStorage/OneDrive-CommexTech/Marketing - Documentos/Site Institucional/site-novo"

def rd(p):
    for _ in range(8):
        try: return open(p, encoding="utf-8", errors="ignore").read()
        except OSError: time.sleep(1)
    raise SystemExit("nao consegui ler " + p)

def wr(p, s):
    for _ in range(8):
        try:
            open(p, "w", encoding="utf-8").write(s); return
        except OSError: time.sleep(1)
    raise SystemExit("nao consegui escrever " + p)

def strip_widget(html, needle):
    """Remove a <div class="elementor-element ..."> que contem needle (div balanceada)."""
    i = html.find(needle)
    if i < 0: raise SystemExit("nao achei para remover: " + needle[:60])
    start = html.rfind('<div class="elementor-element', 0, i)
    tag = re.compile(r"<(/?)div\b[^>]*>", re.I)
    depth, pos = 0, start
    while True:
        m = tag.search(html, pos)
        if not m: raise SystemExit("div desbalanceada")
        depth += -1 if m.group(1) else 1
        pos = m.end()
        if depth == 0: break
    return html[:start] + html[pos:]


def drop_empty_containers(html):
    """Remove containers Elementor que ficaram sem conteudo visivel."""
    tag = re.compile(r"<(/?)div\b[^>]*>", re.I)
    changed = True
    while changed:
        changed = False
        for m in re.finditer(r'<div class="elementor-element[^"]*"[^>]*>', html):
            start, depth, pos = m.start(), 0, m.start()
            while True:
                t = tag.search(html, pos)
                if not t: break
                depth += -1 if t.group(1) else 1
                pos = t.end()
                if depth == 0: break
            inner = html[m.end():pos - len("</div>")]
            visible = re.sub(r"<[^>]+>", "", inner).strip()
            if not visible and "<img" not in inner and "<svg" not in inner and "<a " not in inner:
                html = html[:start] + html[pos:]
                changed = True
                break
    return html

def apply(html, pairs):
    for old, new in pairs:
        n = html.count(old)
        if n != 1:
            raise SystemExit(f"esperava 1 ocorrencia, achei {n}: {old[:70]!r}")
        html = html.replace(old, new)
    return html

BASE = rd(f"{REPO}/ncm.html")

# ------------------------------------------------------------------ Extrator de DI
DI = [
    # <head>
    ("<title>Classificador de NCM — Commex Tech</title>",
     "<title>Extrator de DI — Commex Tech</title>"),
    ('content="Agente especializado em classificação fiscal: sugere a NCM com score de confiança e base legal, e gera a descrição do produto a partir de imagem ou catálogo em PDF."',
     'content="O extrator busca as declarações de importação do período, abre cada DI por adição e item e transforma o que já foi declarado em produto no catálogo."'),
    # hero
    ('De 4 horas para <span style="color:#FF5905">5 minutos por produto</span>, com a base legal registrada',
     'O histórico de importação vira <span style="color:#FF5905">catálogo de produtos</span>, sem redigitação'),
    ("Um SKU novo toma de 3 a 4 horas de pesquisa de um analista sênior. A Commex Tech criou um agente especializado em classificação fiscal de NCM: ele sugere a NCM, mede a confiança de cada sugestão e registra a fundamentação, para o seu especialista revisar apenas os itens de menor confiança.",
     "Cada DI registrada guarda descrição, NCM, exportador e fabricante de itens que a sua empresa já importou. O extrator busca essas declarações por período, abre cada uma adição por adição e leva o que já foi declarado para o catálogo."),
    # secao "o custo"
    ('O custo da rotina <span style="color:#FF5905">manual.</span>',
     'O custo de recomeçar <span style="color:#FF5905">do zero.</span>'),
    ("Na rotina manual, cada SKU novo consome de 3 a 4 horas de um analista<br>sênior entre NCM, TIPI e NESH. Quanto mais itens entram no catálogo, mais<br>tempo da equipe fica alocado em pesquisa.",
     "O dado que falta no cadastro quase sempre já foi declarado alguma vez.<br>Ele só está preso no PDF do despachante, no e-mail e em planilhas<br>paralelas que ninguém consegue manter."),
    ("Horas de analista<br>sênior por item", "Histórico de importação<br>fora de alcance"),
    ("São 3 a 4 horas de pesquisa em NCM, TIPI e NESH para cada item novo. Em catálogos que recebem SKUs todo mês, esse tempo pesa na folha de pagamento e no prazo do desembaraço.",
     "As DIs dos últimos anos ficam com o despachante e em arquivos soltos. Consultar declaração por declaração, item a item, não é rotina que uma equipe de comex consiga sustentar."),
    ("Multa sem provisão<br>no balanço", "Redigitação<br>adição por adição"),
    ("Uma classificação incorreta gera multa, retenção na aduana e passivo contábil sem provisão. Em muitas operações, não há registro de quem decidiu cada código nem da fundamentação usada.",
     "Para montar o catálogo, alguém copia de cada declaração a NCM, a descrição, a unidade de medida, o exportador e o fabricante. É trabalho manual que volta a cada novo período."),
    ("Atualização da TIPI reabre<br>o catálogo", "Cadastro que não bate<br>com o declarado"),
    ("Cada mudança na TIPI ou novo entendimento da Receita obriga a revisar o catálogo item por item, repetindo boa parte da pesquisa já feita.",
     "Quando o dado é redigitado, o produto do catálogo deixa de corresponder ao que foi declarado. A diferença só aparece na conferência ou na fiscalização."),
    # secao "o que o modulo faz"
    ("A plataforma assume a parte braçal da pesquisa em NCM, TIPI e NESH. Para o seu time ficam só os itens em que a experiência do classificador faz diferença.",
     "O extrator assume a busca e a organização das declarações. Para o seu time fica a decisão do que entra no catálogo."),
    ("Agente especializado em classificação fiscal", "Extração por período e por CNPJ"),
    ("O agente foi treinado com milhões de classificações de NCM e analisa descrição, composição e uso do produto antes de propor o código.",
     "Você informa o CNPJ do importador e o intervalo de datas. O extrator consulta as declarações do período e mostra o progresso de cada execução, importação a importação."),
    ("Score de confiança por item", "Retentativa automática"),
    ("Cada sugestão sai com um score de confiança. Em vez de conferir tudo, o analista revisa apenas os itens abaixo do limiar, e a decisão dele fica registrada.",
     "Se a consulta falhar, o sistema tenta de novo a cada 5 minutos, por até 10 tentativas, e segue reprocessando até concluir as importações pendentes do período."),
    ("Base legal registrada por SKU", "Adição e item destrinchados"),
    ("Cada código fica registrado com as RGI e NESH aplicadas, o responsável e a data da decisão. O registro fica vinculado ao SKU e disponível para consulta e auditoria.",
     "Cada declaração chega aberta por adição e item, com NCM, descrição, unidade de medida, exportador e fabricante — e com o part number editável antes de catalogar."),
    ("Reclassificação em lote", "Do extrato ao produto"),
    ("Quando uma parte do catálogo precisa ser reprocessada, a reclassificação em lote refaz o conjunto de uma vez. Cada item mantém o mesmo registro de responsável e fundamentação de uma classificação individual.",
     "Da lista de declarações, os itens selecionados vão para o catálogo: dá para catalogar direto ou gerar o produto com IA, aproveitando a descrição que já foi declarada."),
    # secao da captura de tela
    ('Detalhes <span style="color:#FF5905">de classificação</span>',
     'Declarações <span style="color:#FF5905">abertas por item</span>'),
    ("Cada NCM sugerida aparece com justificativa técnica, regras gerais aplicadas<br>(RGI), candidatos alternativos e as abas de auditoria e evidências. Tudo<br>exportável em PDF.",
     "Cada DI aparece com adição, item, NCM, descrição, exportador e fabricante,<br>pronta para virar produto no catálogo ou para alimentar o relatório de DI."),
    # numeros
    ('O histórico do catálogo<br><span style="color:#FF5905">fica na empresa.</span>',
     'O que já foi declarado<br><span style="color:#FF5905">fica com você.</span>'),
    ("Tempo por produto medido, risco documentado e um dossiê por SKU que pode ser<br>apresentado à fiscalização, mesmo depois da saída de quem classificou.",
     "Histórico de importação recuperado por período, aberto item a item e disponível<br>para o cadastro de produtos e para os relatórios de DI."),
    (">5 min<", ">5 min<"),
    ("por produto novo, contra as 3–4 horas do processo manual",
     "entre uma tentativa e outra, quando a consulta de uma DI falha"),
    (">100 mil<", ">10 tentativas<"),
    ("produtos classificados na plataforma para a XCMG Brasil",
     "automáticas por execução antes de o período ser sinalizado como pendente"),
    # FAQ
    ("O agente substitui o analista fiscal?", "De onde vêm as declarações?"),
    ("<p>Não. O objetivo é tirar do analista as 3–4 horas de pesquisa por item, não a decisão. O agente pesquisa, sugere a NCM e monta a fundamentação; o score de confiança indica quais casos precisam passar pelo especialista, e é ele quem os valida. Na prática, o analista troca a pesquisa repetitiva pela revisão e pelo compliance da operação.</p>",
     "<p>Das declarações já registradas pelo CNPJ que você informar, consultadas com o certificado da empresa. Não é preciso subir PDF nem pedir arquivo ao despachante: você define o período e o extrator busca as DIs daquele intervalo.</p>"),
    ("E se a sugestão estiver errada?", "E se uma DI falhar na consulta?"),
    ("<p>Sugestões com score abaixo do limiar entram na fila de revisão humana antes de valer para a operação. Toda classificação, automática ou revisada, entra no audit log com a fundamentação completa em RGI e NESH. Se um código precisar de correção depois, o histórico mostra o que foi decidido, quando e por quê.</p>",
     "<p>A execução continua. O sistema repete a consulta a cada 5 minutos, por até 10 tentativas, e a tela mostra o progresso do período: quantas importações já concluíram e quantas seguem aguardando reprocessamento.</p>"),
    ("Funciona para o meu segmento?", "Os itens da DI viram produto automaticamente?"),
    # modulos relacionados
    ('Os módulos que recebem<br>a <span style="color:#FF5905">NCM classificada.</span>',
     'Os módulos que trabalham<br>com <span style="color:#FF5905">o que a DI trouxe.</span>'),
    ("Integrações ERP", "Classificador de NCM"),
    ("SAP, TOTVS, Oracle, OSGT e sistemas próprios conectados por API REST ou SFTP, com OAuth e ambiente multi-tenant isolado.",
     "Um agente especializado sugere a NCM com score de confiança e base legal, útil quando a DI traz item sem classificação confiável."),
    ('<a href="integracoes.html">Conhecer a base →</a>', '<a href="ncm.html">Conhecer o módulo →</a>'),
    # CTA final
    ('O próximo SKU do seu catálogo <span style="color:#FF5905">pode levar 5 minutos.</span>',
     'Quanto do seu catálogo <span style="color:#FF5905">já passou por uma DI?</span>'),
    ("Fale com um especialista e avalie, com o seu próprio catálogo, o que a plataforma resolve e o que não vale a pena automatizar.",
     "Fale com um especialista e avalie, com o seu próprio histórico de importação, quanto do catálogo já pode ser montado a partir do que você declarou."),
]

FAQ3_DI = ("<p>O agente foi treinado em milhões de classificações de NCM e a plataforma atende importadores diretos",
           "Os itens da DI viram produto automaticamente?")

# ------------------------------------------------------------------ Ex-tarifario
EX = [
    ("<title>Classificador de NCM — Commex Tech</title>",
     "<title>Sugestão de Ex-Tarifário — Commex Tech</title>"),
    ('content="Agente especializado em classificação fiscal: sugere a NCM com score de confiança e base legal, e gera a descrição do produto a partir de imagem ou catálogo em PDF."',
     'content="A plataforma varre o catálogo, aponta os itens candidatos a ex-tarifário a partir da NCM e da descrição técnica e organiza a documentação do pleito."'),
    ('De 4 horas para <span style="color:#FF5905">5 minutos por produto</span>, com a base legal registrada',
     'Onde o seu catálogo <span style="color:#FF5905">pode pagar menos imposto</span>'),
    ("Um SKU novo toma de 3 a 4 horas de pesquisa de um analista sênior. A Commex Tech criou um agente especializado em classificação fiscal de NCM: ele sugere a NCM, mede a confiança de cada sugestão e registra a fundamentação, para o seu especialista revisar apenas os itens de menor confiança.",
     "O ex-tarifário reduz o imposto de importação de bens de capital e de informática sem produção nacional equivalente. O módulo varre o catálogo que você já tem, aponta os itens com chance de enquadramento e organiza a fundamentação do pleito."),
    ('O custo da rotina <span style="color:#FF5905">manual.</span>',
     'O custo de deixar <span style="color:#FF5905">passar.</span>'),
    ("Na rotina manual, cada SKU novo consome de 3 a 4 horas de um analista<br>sênior entre NCM, TIPI e NESH. Quanto mais itens entram no catálogo, mais<br>tempo da equipe fica alocado em pesquisa.",
     "O benefício existe e é conhecido. O que não existe é tempo para revisar,<br>item a item, um catálogo que cresce todo mês e uma lista de<br>enquadramentos que muda junto."),
    ("Horas de analista<br>sênior por item", "Oportunidade que<br>ninguém procura"),
    ("São 3 a 4 horas de pesquisa em NCM, TIPI e NESH para cada item novo. Em catálogos que recebem SKUs todo mês, esse tempo pesa na folha de pagamento e no prazo do desembaraço.",
     "Achar candidatos exige ler a descrição técnica de cada item e comparar com os enquadramentos vigentes. Entre um despacho e outro, isso não acontece."),
    ("Multa sem provisão<br>no balanço", "Lista que muda,<br>catálogo que não"),
    ("Uma classificação incorreta gera multa, retenção na aduana e passivo contábil sem provisão. Em muitas operações, não há registro de quem decidiu cada código nem da fundamentação usada.",
     "Enquadramentos entram e saem, e um item que não servia passa a servir. Sem revisão periódica do catálogo, a empresa segue pagando a alíquota cheia."),
    ("Atualização da TIPI reabre<br>o catálogo", "Pleito sem<br>memória técnica"),
    ("Cada mudança na TIPI ou novo entendimento da Receita obriga a revisar o catálogo item por item, repetindo boa parte da pesquisa já feita.",
     "Quando o pleito é montado do zero, a descrição técnica e os documentos ficam espalhados em e-mails. Na renovação, o trabalho é refeito inteiro."),
    ("A plataforma assume a parte braçal da pesquisa em NCM, TIPI e NESH. Para o seu time ficam só os itens em que a experiência do classificador faz diferença.",
     "A plataforma faz a varredura e a triagem. Para o seu time, ou para a consultoria que acompanha a empresa, fica a decisão sobre quais pleitos vale a pena entrar."),
    ("Agente especializado em classificação fiscal", "Varredura do catálogo"),
    ("O agente foi treinado com milhões de classificações de NCM e analisa descrição, composição e uso do produto antes de propor o código.",
     "A plataforma percorre os produtos já cadastrados e separa os que estão em NCM de bem de capital (BK) e de informática e telecomunicação (BIT), onde o ex-tarifário se aplica."),
    ("Score de confiança por item", "Sugestão com justificativa"),
    ("Cada sugestão sai com um score de confiança. Em vez de conferir tudo, o analista revisa apenas os itens abaixo do limiar, e a decisão dele fica registrada.",
     "Para cada candidato, o módulo indica o enquadramento provável a partir da descrição técnica e da NCM classificada, junto da fundamentação que sustenta a análise."),
    ("Base legal registrada por SKU", "Prioridade por impacto"),
    ("Cada código fica registrado com as RGI e NESH aplicadas, o responsável e a data da decisão. O registro fica vinculado ao SKU e disponível para consulta e auditoria.",
     "Os candidatos aparecem ordenados pelo que representam em imposto, para o time começar pelos itens que pagam o esforço do pleito."),
    ("Reclassificação em lote", "Dossiê do pleito"),
    ("Quando uma parte do catálogo precisa ser reprocessada, a reclassificação em lote refaz o conjunto de uma vez. Cada item mantém o mesmo registro de responsável e fundamentação de uma classificação individual.",
     "Descrição técnica, NCM, base do enquadramento e responsável ficam registrados no mesmo padrão de auditoria do catálogo, prontos para o pleito e para a renovação."),
    ('Detalhes <span style="color:#FF5905">de classificação</span>',
     'Candidatos <span style="color:#FF5905">com fundamentação</span>'),
    ("Cada NCM sugerida aparece com justificativa técnica, regras gerais aplicadas<br>(RGI), candidatos alternativos e as abas de auditoria e evidências. Tudo<br>exportável em PDF.",
     "Cada item candidato aparece com a NCM classificada, a descrição técnica que<br>sustenta o enquadramento e o registro de quem revisou a análise."),
    ('O histórico do catálogo<br><span style="color:#FF5905">fica na empresa.</span>',
     'A economia possível<br><span style="color:#FF5905">deixa de ser palpite.</span>'),
    ("Tempo por produto medido, risco documentado e um dossiê por SKU que pode ser<br>apresentado à fiscalização, mesmo depois da saída de quem classificou.",
     "Catálogo varrido por inteiro, candidatos priorizados por impacto e a<br>fundamentação de cada análise registrada junto do produto."),
    (">5 min<", ">BK e BIT<"),
    ("por produto novo, contra as 3–4 horas do processo manual",
     "as duas famílias de NCM em que o ex-tarifário se aplica"),
    (">100 mil<", ">100 mil<"),
    ("produtos classificados na plataforma para a XCMG Brasil",
     "produtos já cadastrados na plataforma para a XCMG Brasil"),
    ("O agente substitui o analista fiscal?", "O módulo entra com o pleito por mim?"),
    ("<p>Não. O objetivo é tirar do analista as 3–4 horas de pesquisa por item, não a decisão. O agente pesquisa, sugere a NCM e monta a fundamentação; o score de confiança indica quais casos precisam passar pelo especialista, e é ele quem os valida. Na prática, o analista troca a pesquisa repetitiva pela revisão e pelo compliance da operação.</p>",
     "<p>Não. O módulo encontra os candidatos no seu catálogo e organiza a documentação técnica. O pleito e a decisão de entrar com ele seguem com a sua equipe ou com a consultoria que acompanha a empresa.</p>"),
    ("E se a sugestão estiver errada?", "Preciso ter a NCM classificada na plataforma?"),
    ("<p>Sugestões com score abaixo do limiar entram na fila de revisão humana antes de valer para a operação. Toda classificação, automática ou revisada, entra no audit log com a fundamentação completa em RGI e NESH. Se um código precisar de correção depois, o histórico mostra o que foi decidido, quando e por quê.</p>",
     "<p>Ajuda, mas não é obrigatório. A varredura usa a NCM e a descrição técnica que estiverem no catálogo, e quanto melhor a descrição, mais preciso é o candidato. Produtos classificados pelo módulo de NCM já chegam com essa base pronta.</p>"),
    ("Funciona para o meu segmento?", "Funciona para o meu segmento?"),
    ('Os módulos que recebem<br>a <span style="color:#FF5905">NCM classificada.</span>',
     'Os módulos que sustentam<br>a <span style="color:#FF5905">análise de enquadramento.</span>'),
    ("Integrações ERP", "Classificador de NCM"),
    ("SAP, TOTVS, Oracle, OSGT e sistemas próprios conectados por API REST ou SFTP, com OAuth e ambiente multi-tenant isolado.",
     "A NCM classificada com score e base legal é o ponto de partida da varredura de candidatos a ex-tarifário."),
    ('<a href="integracoes.html">Conhecer a base →</a>', '<a href="ncm.html">Conhecer o módulo →</a>'),
    ('O próximo SKU do seu catálogo <span style="color:#FF5905">pode levar 5 minutos.</span>',
     'Quanto do seu catálogo <span style="color:#FF5905">pode pagar menos?</span>'),
    ("Fale com um especialista e avalie, com o seu próprio catálogo, o que a plataforma resolve e o que não vale a pena automatizar.",
     "Fale com um especialista e avalie, com uma amostra do seu catálogo, quantos itens têm chance real de enquadramento."),
]

REVISAR = ("<!-- REVISAR: copy rascunhada a partir do modelo das outras paginas de modulo. "
           "Validar numeros, funcionamento e enquadramento com o time de produto antes de publicar. "
           "Falta tambem a captura de tela do modulo (as demais paginas usam assets/img/<modulo>.png). -->\n")

def build(pairs, out, faq3_q, faq3_a):
    html = BASE
    html = apply(html, pairs)
    # a 3a pergunta do FAQ tem texto proprio
    old_a = re.search(r"<p>O agente foi treinado em milhões de classificações de NCM.*?</p>", html, re.S).group(0)
    html = html.replace(old_a, faq3_a)
    if faq3_q:
        html = html.replace("Funciona para o meu segmento?", faq3_q)
    # tira as capturas de tela do modulo de NCM (nao servem para estes modulos)
    html = strip_widget(html, 'src="assets/img/NCM-comex-2.png"')
    html = strip_widget(html, 'src="assets/img/NCM2.gif"')
    html = drop_empty_containers(html)
    html = html.replace("<body ", REVISAR + "<body ", 1)
    html = re.sub(r'(<body[^>]*class=")', r'\1commex-sem-captura ', html, count=1)
    wr(f"{REPO}/{out}", html)
    print("gerado", out, len(html), "bytes")

build(DI, "extrator-di.html", None,
      "<p>Não sem alguém decidir. Da lista de declarações você seleciona os itens e escolhe catalogar ou gerar o produto com IA. A descrição declarada e a NCM da DI vão junto, e o produto entra no catálogo com a mesma trilha de auditoria dos demais.</p>")
build(EX, "ex-tarifario.html", None,
      "<p>O módulo atende quem importa bens de capital e itens de informática e telecomunicação — indústrias com linha de produção, importadores diretos e tradings que trazem máquinas e equipamentos. Se o seu catálogo não tem itens em NCM de BK ou BIT, o ex-tarifário não se aplica, e a gente diz isso na primeira conversa.</p>")
