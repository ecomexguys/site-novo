#!/usr/bin/env python3
"""Tira do snapshot os dados que nao podem ir para um site publico:
usuario logado, CNPJ do importador, numero de DI e nome de fornecedor real."""
import re, sys

# fornecedores reais -> genericos (a descricao do produto fica, ela e generica)
FORNECEDORES = {
    "RITRAMA S.A.": "FORNECEDOR ALFA LTD",
    "MINGBAI ENTERPRISE LTD": "FORNECEDOR BETA LTD",
}
# numeros de DI reais -> sequencia ficticia
DIS = {
    "21/0004540-6": "21/0000101-4",
    "21/0005728-5": "21/0000102-2",
    "21/0005848-6": "21/0000103-0",
}
CNPJ_DEMO = "00.000.000/0001-91"

def limpar(src, dst):
    s = open(src, encoding="utf-8", errors="ignore").read()
    # usuario logado
    s = s.replace("nicolas felippe da rocha", "Commex Tech")
    s = re.sub(r"\(\d{15,}\)\s*Commex Tech", "Commex Tech", s)
    s = re.sub(r"nicolas@commextech\.com", "usuario@commextech.com", s)
    s = re.sub(r'aria-label="Menu da conta: [^"]*"', 'aria-label="Menu da conta"', s)
    # dados do cliente
    s = re.sub(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}", CNPJ_DEMO, s)
    for real, falso in FORNECEDORES.items():
        s = s.replace(real, falso)
    for real, falso in DIS.items():
        s = s.replace(real, falso)
    # scripts fora, senao o Angular re-bootstrapa e limpa o DOM
    s = re.sub(r"<script[^>]*>.*?</script>", "", s, flags=re.S)
    s = re.sub(r"<script[^>]*/?>", "", s)
    open(dst, "w", encoding="utf-8").write(s)

    sobrou = {
        "nome do usuario": len(re.findall(r"nicolas", s, re.I)),
        "CNPJ real": len([c for c in re.findall(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}", s) if c != CNPJ_DEMO]),
        "fornecedor real": sum(s.count(k) for k in FORNECEDORES),
        "DI real": sum(s.count(k) for k in DIS),
    }
    print(f"{dst}: " + ", ".join(f"{k}={v}" for k, v in sobrou.items()))

if __name__ == "__main__":
    limpar(sys.argv[1], sys.argv[2])
