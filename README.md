# site-novo

Site institucional da **Commex Tech**. É o site que o designer montou em WordPress/Elementor
(`commex.eltonpedroso.com.br`), trazido para cá como HTML estático: sem build, sem WordPress.
Para ver, é só abrir `index.html` no navegador.

## Estrutura

- `*.html` — as 12 páginas
- `assets/css/` — CSS do tema Hello Elementor, do Elementor e o CSS por página (`post-*.css`)
- `assets/js/` — jQuery, runtime do Elementor e o slider de depoimentos
- `assets/elementor/js/`, `assets/pro-elements/js/` — chunks que o Elementor carrega sob demanda
  (accordion do FAQ, menu, text-editor). **Não renomear estas pastas**: o caminho está no
  `elementorFrontendConfig` de cada página.
- `assets/css/commex-static.css` — o que é só da versão estática (botão de WhatsApp e dois ajustes)
- `assets/img/` — imagens e capturas de tela
- `ferramentas/` — scripts usados para gerar o site (ver abaixo)

## Páginas

| Arquivo | Página |
|---|---|
| `index.html` | Home |
| `sobre.html` | Sobre nós |
| `cadastro-de-produtos.html` | Catálogo de produtos (base da plataforma) |
| `ncm.html` | Classificador de NCM |
| `extrator-di.html` | Extrator de DI |
| `ex-tarifario.html` | Sugestão de Ex-Tarifário |
| `duimp.html` · `lpco.html` · `du-e.html` · `nfe.html` · `integracoes.html` | Demais módulos |
| `contato.html` | Fale Conosco |

## Como mexer

O markup é o que o Elementor gerou, então o estilo vem de `assets/css/post-<id>.css` casando com
as classes `elementor-element-<id>` de cada bloco. Para criar um módulo novo, o caminho curto é
copiar uma página de módulo existente (`ncm.html` é a mais completa) **mantendo as classes**, e
trocar só os textos — foi assim que `extrator-di.html` e `ex-tarifario.html` nasceram.
Header e rodapé são iguais em todas as páginas: mudança de menu tem que ser replicada em todas.

`ferramentas/` guarda os scripts dessa geração: `convert.py` (baixa e converte o site do
WordPress), `build_modules.py` (gera as páginas de módulo novas a partir de `ncm.html`) e
`nav_home_ncm.py` (menu, cards da home e o bloco extra do NCM).

## Pendências

- `extrator-di.html` e `ex-tarifario.html` têm a copy marcada com `<!-- REVISAR -->` no topo e
  ainda não têm captura de tela do módulo (as demais páginas usam `assets/img/<modulo>.png`).
- Política de Privacidade: o link do rodapé continua sem destino, como no site do designer.
- Em telas estreitas o layout estoura horizontalmente — o mesmo acontece no site do designer,
  então é um ajuste a fazer no CSS do Elementor.
