#!/usr/bin/env python3
"""Revisao de copy + remocao de tells de IA na copy nova."""
import time

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

EDICOES = {
"extrator-di.html": [
 # travessao fora, ritmo mais curto
 ("Cada DI registrada guarda descrição, NCM, exportador e fabricante de itens que a sua empresa já importou. O extrator busca essas declarações por período, abre cada uma adição por adição e leva o que já foi declarado para o catálogo.",
  "Cada DI registrada guarda descrição, NCM, exportador e fabricante de itens que a sua empresa já importou. O extrator busca essas declarações por período e abre cada uma, adição por adição, para o catálogo."),
 ("O dado que falta no cadastro quase sempre já foi declarado alguma vez.<br>Ele só está preso no PDF do despachante, no e-mail e em planilhas<br>paralelas que ninguém consegue manter.",
  "O dado que falta no cadastro quase sempre já foi declarado alguma vez.<br>Ele só está preso no PDF do despachante, no e-mail e em planilhas paralelas."),
 ("As DIs dos últimos anos ficam com o despachante e em arquivos soltos. Consultar declaração por declaração, item a item, não é rotina que uma equipe de comex consiga sustentar.",
  "As DIs dos últimos anos ficam com o despachante e em arquivos soltos. Consultar uma a uma, item a item, não cabe na rotina de quem despacha."),
 ("Cada declaração chega aberta por adição e item, com NCM, descrição, unidade de medida, exportador e fabricante — e com o part number editável antes de catalogar.",
  "Cada declaração chega aberta por adição e item, com NCM, descrição, unidade de medida, exportador e fabricante. O part number fica editável antes de catalogar."),
 ("Da lista de declarações, os itens selecionados vão para o catálogo: dá para catalogar direto ou gerar o produto com IA, aproveitando a descrição que já foi declarada.",
  "Da lista de declarações, os itens selecionados vão para o catálogo. Dá para catalogar direto ou gerar o produto com IA, aproveitando a descrição declarada na DI."),
 ("<p>Das declarações já registradas pelo CNPJ que você informar, consultadas com o certificado da empresa. Não é preciso subir PDF nem pedir arquivo ao despachante: você define o período e o extrator busca as DIs daquele intervalo.</p>",
  "<p>Das declarações registradas no CNPJ que você informar, consultadas com o certificado da empresa. Você define o período e o extrator busca as DIs daquele intervalo. Não é preciso subir PDF nem pedir arquivo ao despachante.</p>"),
 ("quantas importações já concluíram e quantas seguem aguardando reprocessamento",
  "quantas importações concluíram e quantas seguem aguardando reprocessamento"),
 ("Fale com um especialista e avalie, com o seu próprio histórico de importação, quanto do catálogo já pode ser montado a partir do que você declarou.",
  "Fale com um especialista e avalie, com o seu próprio histórico de importação, quanto do catálogo dá para montar a partir do que você já declarou."),
],
"ex-tarifario.html": [
 ("indica qual descreve aquele item — ou registra que nenhum descreve",
  "indica qual descreve aquele item, ou registra que nenhum descreve"),
 ("redação da legislação com a descrição técnica de cada item — e a lista de<br>ex vigentes muda sem avisar.",
  "redação da legislação com a descrição técnica de cada item.<br>E a lista de ex vigentes muda sem avisar."),
 ("Uma sincronização diária traz os ex-tarifários vigentes do MDIC. Se o volume vier abaixo do esperado, a foto anterior é preservada em vez de sobrescrita por dado incompleto.",
  "Uma sincronização diária traz os ex-tarifários vigentes do MDIC. Se o volume vier abaixo do esperado, a sincronização é abortada e a lista anterior continua valendo."),
 ("está a 30, 15 e 5 dias de vencer — antes de a alíquota mudar sem ninguém ver.",
  "está a 30, 15 e 5 dias de vencer. Antes de a alíquota mudar sem ninguém ver."),
 ("A NCM correta delimita quais ex-tarifários entram na avaliação — é o ponto de partida do módulo.",
  "A NCM correta delimita quais ex-tarifários entram na avaliação. É o ponto de partida do módulo."),
 ("<p>Não. Ele trabalha com os ex-tarifários que já estão vigentes: procura, entre os ex da NCM do seu produto, qual descreve aquele item.",
  "<p>Não. Ele trabalha com os ex-tarifários vigentes: procura, entre os ex da NCM do seu produto, qual descreve aquele item."),
 ("<p>A denominação, a descrição técnica e os atributos Siscomex já preenchidos, com o nome legível de cada atributo resolvido. A NCM precisa estar correta, porque é ela que delimita quais ex entram na avaliação. Quanto mais completo o produto, melhor a indicação — e, quando falta informação, o módulo diz qual atributo preencher.</p>",
  "<p>A denominação, a descrição técnica e os atributos Siscomex preenchidos, com o nome legível de cada atributo resolvido. A NCM precisa estar correta, porque é ela que delimita quais ex entram na avaliação. Quanto mais completo o produto, melhor a indicação. Quando falta informação, o módulo diz qual atributo preencher.</p>"),
],
"cadastro-de-produtos.html": [
 ("Fabricante, produtor e fornecedor de fora do Brasil ficam cadastrados com TIN e país de origem, e vinculados aos produtos que abastecem. O vínculo que o Portal Único exige sai do mesmo cadastro, sem planilha paralela.",
  "Fabricante, produtor e fornecedor de fora do Brasil ficam cadastrados com TIN e país de origem, vinculados aos produtos que abastecem. O vínculo que o Portal Único exige sai daí, sem planilha paralela."),
 ("Produtos, operadores estrangeiros e os vínculos entre eles que já estão registrados no Portal Único entram por sincronização — com atributos ou para complementar depois. Ninguém recadastra o que a empresa já declarou.",
  "Produtos, operadores estrangeiros e os vínculos entre eles já registrados no Portal Único entram por sincronização, com atributos ou para completar depois. Ninguém recadastra o que a empresa já declarou."),
 ("Selecione os itens e edite atributos, ative, desative, envie ao OSGT ou exclua rascunhos em bloco. A edição de atributo é merge: preenche o que falta sem apagar o que cada produto já tinha, e o resultado mostra item a item o que passou e o que ficou pendente.",
  "Selecione os itens e edite atributos, ative, desative, envie ao OSGT ou exclua rascunhos em bloco. A edição de atributo preenche o que falta sem apagar o que cada produto já tinha. No fim, o resultado mostra item a item o que passou e o que ficou pendente."),
 ("Quando uma mudança de atributo da NCM desativa um item no Portal Único, a notificação chega na plataforma e o produto aparece marcado. Em vez de descobrir no registro, o time reativa a nova versão em massa.",
  "Quando uma mudança de atributo da NCM desativa um item no Portal Único, a notificação chega na plataforma e o produto aparece marcado. O time reativa a nova versão em massa, sem descobrir a pendência na hora do registro."),
],
"ncm.html": [
 ("Quando o produto chega só com código e foto, a plataforma lê a imagem ou o catálogo do fornecedor em PDF e monta a descrição que alimenta a classificação, em vez de alguém escrever item por item.",
  "Quando o produto chega só com código e foto, a plataforma lê a imagem ou o catálogo do fornecedor em PDF e monta a descrição que alimenta a classificação, sem alguém escrever item por item."),
],
}

total = 0
for arq, pares in EDICOES.items():
    p = f"{REPO}/{arq}"
    s = rd(p)
    n = 0
    for old, new in pares:
        c = s.count(old)
        if c == 0:
            print(f"  !! nao achei em {arq}: {old[:60]!r}"); continue
        if c > 1:
            raise SystemExit(f"{arq}: {c} ocorrencias de {old[:40]!r}")
        s = s.replace(old, new); n += 1
    wr(p, s); total += n
    print(f"  {arq}: {n} edicoes")
print(f"{total} edicoes no total")
