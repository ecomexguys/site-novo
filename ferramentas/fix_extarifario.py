#!/usr/bin/env python3
"""Reescreve ex-tarifario.html conforme a spec do vault (Sugestão de Ex-Tarifário por IA)."""
import re, time

REPO = "/Users/nicolasrocha/Library/CloudStorage/OneDrive-CommexTech/Marketing - Documentos/Site Institucional/site-novo"
P = f"{REPO}/ex-tarifario.html"

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

PARES = [
    ('content="A plataforma varre o catálogo, aponta os itens candidatos a ex-tarifário a partir da NCM e da descrição técnica e organiza a documentação do pleito."',
     'content="Para cada produto do catálogo, a plataforma avalia os ex-tarifários vigentes da NCM e indica qual descreve aquele item, com a evidência do que casou e do que não casou."'),

    ('Onde o seu catálogo <span style="color:#FF5905">pode pagar menos imposto</span>',
     'Qual ex-tarifário <span style="color:#FF5905">descreve o seu produto</span>'),
    ("O ex-tarifário reduz o imposto de importação de bens de capital e de informática sem produção nacional equivalente. O módulo varre o catálogo que você já tem, aponta os itens com chance de enquadramento e organiza a fundamentação do pleito.",
     "A base de ex-tarifários vigentes é sincronizada todo dia com o MDIC. Para cada produto do catálogo, a plataforma avalia os ex vigentes da NCM dele e indica qual descreve aquele item — ou registra que nenhum descreve. Quem aceita é o seu time."),

    ('O custo de deixar <span style="color:#FF5905">passar.</span>',
     'O custo de deixar <span style="color:#FF5905">passar.</span>'),
    ("O benefício existe e é conhecido. O que não existe é tempo para revisar,<br>item a item, um catálogo que cresce todo mês e uma lista de<br>enquadramentos que muda junto.",
     "O ex-tarifário reduz o Imposto de Importação, mas depende de comparar a<br>redação da legislação com a descrição técnica de cada item — e a lista de<br>ex vigentes muda sem avisar."),
    ("Oportunidade que<br>ninguém procura", "Ex vigente muda,<br>catálogo não acompanha"),
    ("Achar candidatos exige ler a descrição técnica de cada item e comparar com os enquadramentos vigentes. Entre um despacho e outro, isso não acontece.",
     "A lista de ex-tarifários vigentes é publicada e revista pelo MDIC. Sem acompanhar a mudança, a empresa perde enquadramento novo e continua com ex já revogado."),
    ("Lista que muda,<br>catálogo que não", "Comparação técnica,<br>não busca por palavra"),
    ("Enquadramentos entram e saem, e um item que não servia passa a servir. Sem revisão periódica do catálogo, a empresa segue pagando a alíquota cheia.",
     "“Motor de 5,2 kW” e “potência de 7 cv” são a mesma coisa, e a legislação raramente usa o vocabulário do seu catálogo. Procurar por palavra descarta o ex certo sem ninguém perceber."),
    ("Pleito sem<br>memória técnica", "Enquadramento errado<br>vira auto de infração"),
    ("Quando o pleito é montado do zero, a descrição técnica e os documentos ficam espalhados em e-mails. Na renovação, o trabalho é refeito inteiro.",
     "Ex aplicado indevidamente faz o importador recolher o Imposto de Importação a menor e gera multa. Sem ver o que casou e o que não casou, conferir vira aposta."),

    ("A plataforma faz a varredura e a triagem. Para o seu time, ou para a consultoria que acompanha a empresa, fica a decisão sobre quais pleitos vale a pena entrar.",
     "A plataforma faz a comparação e apresenta a evidência. A decisão de aplicar o ex ao produto continua sendo do seu time."),
    ("Varredura do catálogo", "Base de ex vigentes atualizada todo dia"),
    ("A plataforma percorre os produtos já cadastrados e separa os que estão em NCM de bem de capital (BK) e de informática e telecomunicação (BIT), onde o ex-tarifário se aplica.",
     "Uma sincronização diária traz os ex-tarifários vigentes do MDIC. Se o volume vier abaixo do esperado, a foto anterior é preservada em vez de sobrescrita por dado incompleto."),
    ("Sugestão com justificativa", "Todos os candidatos da NCM avaliados"),
    ("Para cada candidato, o módulo indica o enquadramento provável a partir da descrição técnica e da NCM classificada, junto da fundamentação que sustenta a análise.",
     "Não há pré-filtro por palavra: todos os ex vigentes da NCM do produto entram na avaliação, em blocos, com uma rodada de desempate quando mais de um candidato sobrevive."),
    ("Prioridade por impacto", "Evidência item a item"),
    ("Os candidatos aparecem ordenados pelo que representam em imposto, para o time começar pelos itens que pagam o esforço do pleito.",
     "Cada sugestão mostra o que casou, o que não casou e o que o catálogo não informa. Quando falta dado, o módulo devolve a lista do que preencher em vez de um “não”."),
    ("Dossiê do pleito", "Reavaliação quando algo muda"),
    ("Descrição técnica, NCM, base do enquadramento e responsável ficam registrados no mesmo padrão de auditoria do catálogo, prontos para o pleito e para a renovação.",
     "Produto ativado, sincronizado do Portal Único ou ex novo publicado dispara nova avaliação. O que já foi julgado não volta para a fila, e sugestão pendente não é sobrescrita."),

    ('Candidatos <span style="color:#FF5905">com fundamentação</span>',
     'A decisão <span style="color:#FF5905">continua sendo humana</span>'),
    ("Cada item candidato aparece com a NCM classificada, a descrição técnica que<br>sustenta o enquadramento e o registro de quem revisou a análise.",
     "Nada é aplicado ao produto automaticamente. A sugestão fica pendente até alguém<br>aceitar ou descartar, e o ex só entra no cadastro depois do aceite."),

    ('A economia possível<br><span style="color:#FF5905">deixa de ser palpite.</span>',
     'O enquadramento<br><span style="color:#FF5905">fica documentado.</span>'),
    ("Catálogo varrido por inteiro, candidatos priorizados por impacto e a<br>fundamentação de cada análise registrada junto do produto.",
     "Ex vigente conferido contra a descrição técnica do produto, evidência registrada<br>e aviso quando o que já foi aceito perde a validade."),
    (">BK e BIT<", ">500 ex<"),
    ("as duas famílias de NCM em que o ex-tarifário se aplica",
     "na NCM com mais candidatos: todos são avaliados, sem corte por palavra-chave"),
    (">100 mil<", ">todo dia<"),
    ("produtos já cadastrados na plataforma para a XCMG Brasil",
     "a base de ex-tarifários vigentes é sincronizada com o MDIC pela manhã"),

    ("O módulo entra com o pleito por mim?", "O módulo pede ex-tarifário novo ao MDIC?"),
    ("<p>Não. O módulo encontra os candidatos no seu catálogo e organiza a documentação técnica. O pleito e a decisão de entrar com ele seguem com a sua equipe ou com a consultoria que acompanha a empresa.</p>",
     "<p>Não. Ele trabalha com os ex-tarifários que já estão vigentes: procura, entre os ex da NCM do seu produto, qual descreve aquele item. Pleito de ex novo é outro caminho, fora da plataforma.</p>"),
    ("Preciso ter a NCM classificada na plataforma?", "O que a plataforma usa para comparar?"),
    ("<p>Ajuda, mas não é obrigatório. A varredura usa a NCM e a descrição técnica que estiverem no catálogo, e quanto melhor a descrição, mais preciso é o candidato. Produtos classificados pelo módulo de NCM já chegam com essa base pronta.</p>",
     "<p>A denominação, a descrição técnica e os atributos Siscomex já preenchidos, com o nome legível de cada atributo resolvido. A NCM precisa estar correta, porque é ela que delimita quais ex entram na avaliação. Quanto mais completo o produto, melhor a indicação — e, quando falta informação, o módulo diz qual atributo preencher.</p>"),
    ("Funciona para o meu segmento?", "A IA pode aplicar um ex errado no meu produto?"),
    ("<p>O módulo atende quem importa bens de capital e itens de informática e telecomunicação — indústrias com linha de produção, importadores diretos e tradings que trazem máquinas e equipamentos. Se o seu catálogo não tem itens em NCM de BK ou BIT, o ex-tarifário não se aplica, e a gente diz isso na primeira conversa.</p>",
     "<p>A sugestão não altera o produto: ela fica pendente até alguém aceitar, e vem com a evidência do que casou e do que não casou. Sugestão abaixo do piso de confiança é marcada como tal em vez de ser escondida, e ex que não estava entre os candidatos daquela NCM é descartado automaticamente.</p>"),

    ('Os módulos que sustentam<br>a <span style="color:#FF5905">análise de enquadramento.</span>',
     'Os módulos que alimentam<br>a <span style="color:#FF5905">avaliação de ex.</span>'),
    ("A NCM classificada com score e base legal é o ponto de partida da varredura de candidatos a ex-tarifário.",
     "A NCM correta delimita quais ex-tarifários entram na avaliação — é o ponto de partida do módulo."),
    ("Fale com um especialista e avalie, com uma amostra do seu catálogo, quantos itens têm chance real de enquadramento.",
     "Fale com um especialista e avalie, com uma amostra do seu catálogo, quantos itens têm um ex-tarifário vigente que os descreve."),
]

BLOCO_TITULO = "Aviso de vencimento e revogação"
BLOCO_TEXTO = ("Um acompanhamento diário avisa os administradores quando um ex aceito é revogado, "
               "vence, ou está a 30, 15 e 5 dias de vencer — antes de a alíquota mudar sem ninguém ver.")

html = rd(P)
for old, new in PARES:
    n = html.count(old)
    if n != 1:
        raise SystemExit(f"esperava 1, achei {n}: {old[:60]!r}")
    html = html.replace(old, new)

# quinto bloco em "O que o módulo faz"
if BLOCO_TITULO not in html:
    i = html.find("Reavaliação quando algo muda")
    start, end, bloco = block_at(html, i, must_contain="<svg")
    novo = bloco.replace("Reavaliação quando algo muda", BLOCO_TITULO)
    novo = re.sub(r'(data-widget_type="text-editor.default">\s*).*?(\s*</div>)',
                  lambda m: m.group(1) + BLOCO_TEXTO + m.group(2), novo, count=1, flags=re.S)
    html = html[:end] + "\n\t\t" + novo + html[end:]

# nota de revisao atualizada
html = re.sub(r"<!-- REVISAR:.*?-->\n", "", html, flags=re.S)
html = html.replace("<body ", "<!-- Copy baseada na spec do vault (04 - Regras de Negócio/Sugestão de "
                    "Ex-Tarifário por IA). Falta a captura de tela do módulo. -->\n<body ", 1)
wr(P, html)
print("ex-tarifario.html reescrito")
