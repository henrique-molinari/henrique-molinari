<!--
=====================================================================
  TUTORIAL: COMO CRIAR UM README DE PERFIL DO GITHUB COMO ESTE
=====================================================================

  Este arquivo (README.md) fica em um repositório com o MESMO NOME do seu
  usuário do GitHub (ex.: github.com/henrique-molinari/henrique-molinari).
  O GitHub mostra esse README no topo do seu perfil. Tudo o que você lê
  neste bloco é comentário HTML: não aparece na página, só no código.

  VISÃO GERAL DAS PEÇAS (na ordem em que aparecem no perfil)
    1. Cabeçalho animado           -> header.svg / header-light.svg
    2. Painel principal (terminal) -> dark.svg / light.svg
    3. Card de streak              -> serviço externo streak-stats
    4. Cards de stats e linguagens -> serviço externo github-readme-stats
    5. Jogo space shooter          -> game.gif (gerado por uma GitHub Action)
    6. Botões de contato           -> shields.io

  PASSO 0 - PREPARAÇÃO (faça uma vez)
    a) Crie um repositório PÚBLICO chamado exatamente como o seu usuário
       e marque "Add a README file".
    b) No seu perfil, clique em "Contribution settings" (menu ao lado do
       gráfico de contribuições) e deixe MARCADO "Private contributions".
       Sem isso, commits em repositórios privados não aparecem no jogo
       nem nos cards (a API não os enxerga).
    c) Em Settings > Actions > General do repositório, em "Workflow
       permissions", escolha "Read and write permissions". Isso permite
       que as automações salvem os arquivos gerados (GIF).

  TÉCNICAS QUE SE REPETEM NO ARQUIVO
    * picture + source media="(prefers-color-scheme: dark)":
      o GitHub troca a imagem automaticamente entre tema escuro e claro.
      A tag img dentro do picture é a imagem do tema claro (e o fallback).
    * div align="center": centraliza o conteúdo (o GitHub não aceita CSS).
    * width="100%": a imagem ocupa toda a largura do README.
    * br: quebra de linha; usado para criar espaço entre os blocos,
      já que o GitHub também não aceita margin nem padding.
    * URLs raw.githubusercontent.com/USUARIO/REPO/main/ARQUIVO apontam
      para arquivos do próprio repositório. Trocar "henrique-molinari"
      pelo seu usuário é o principal ajuste que você precisa fazer.
-->

<!-- ===== 1) CABEÇALHO ANIMADO =====
  PASSO 1 - Coloque no repositório dois arquivos SVG animados:
    header.svg        -> versão escura (fundo preto, letras verdes)
    header-light.svg  -> versão clara  (fundo branco, letras verde escuro)
  São SVGs de 1180x150 com animação SMIL (tags animate), que o GitHub
  reproduz normalmente quando carregados por img. Para o seu, copie um
  SVG e altere o texto e as cores (#00FF66 = verde neon do tema escuro,
  #15803D = verde do tema claro).
  A tag picture escolhe o arquivo conforme o tema do visitante.
  alt="..." é o texto para leitores de tela e para quando a imagem falha.
-->
<div align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/henrique-molinari/henrique-molinari/main/header.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/henrique-molinari/henrique-molinari/main/header-light.svg">
  <img alt="Wake up, HRK... Java enthusiast. Henrique Molinari" src="https://raw.githubusercontent.com/henrique-molinari/henrique-molinari/main/header-light.svg" width="100%"/>
</picture>
</div>

<br/>

<!-- ===== 2) PAINEL PRINCIPAL (estilo terminal) =====
  PASSO 2 - Mesmo esquema do cabeçalho, agora com dark.svg e light.svg
  (1180x610). É o "cartão de visita": arte ASCII, dados sobre você e
  animações. Cores de fundo usadas:
    tema escuro -> #000000 (preto)      tema claro -> #FFFFFF (branco)
  Para personalizar, abra o SVG num editor de texto e troque os textos
  e as cores. Mantenha a largura 1180 para alinhar com os cards abaixo.
-->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/henrique-molinari/henrique-molinari/main/dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/henrique-molinari/henrique-molinari/main/light.svg">
  <img alt="Henrique Molinari" src="https://raw.githubusercontent.com/henrique-molinari/henrique-molinari/main/light.svg">
</picture>

<br/>
<br/>

<!-- ===== 3) e 4) CARDS DE ESTATÍSTICAS =====
  Todos os cards abaixo são imagens geradas por serviços gratuitos: você só
  monta a URL com o seu usuário e as cores. Nada precisa ser instalado.
  Cores são hexadecimais SEM o "#". Padrão do tema escuro: fundo 060B08,
  destaque 00FF66. Padrão do tema claro: fundo FFFFFF, destaque 15803D/16A34A.
  Para ter o MESMO visual em todos os cards, repetimos em cada URL:
  borda verde visível + cantos arredondados (raio 18, igual ao painel).
-->

<div align="center">

<!-- 3) STREAK (sequência de dias com contribuição), largura total
  PASSO 3 - Serviço: streak-stats.demolab.com
  (projeto DenverCoder1/github-readme-streak-stats)
  Parâmetros usados na URL:
    user=SEU_USUARIO        quem será analisado
    hide_border=false       mostra a borda do card
    border_radius=18        cantos arredondados
    border=COR              cor da borda
    background=COR          cor de fundo do card
    stroke=COR              cor das linhas divisórias entre as 3 colunas
    ring=COR                cor do círculo da sequência atual
    fire=COR                cor do ícone de fogo
    currStreakLabel, sideLabels, currStreakNum, sideNums, dates
                            cores dos textos (rótulos, números e datas)
    titleColor=COR          cor de títulos
    card_width=1180         largura do card em pixels (igual ao painel principal)
  O source (tema escuro) usa cores neon; o img (tema claro) usa cores escuras.
-->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://streak-stats.demolab.com/?user=henrique-molinari&hide_border=false&border_radius=18&border=00FF66&background=060B08&stroke=00FF66&ring=00CC44&fire=00FF66&currStreakLabel=00FF66&sideLabels=8FBF9F&currStreakNum=F8FAFC&sideNums=F8FAFC&dates=3A5A45&titleColor=00FF66&card_width=1180" />
  <img width="100%" src="https://streak-stats.demolab.com/?user=henrique-molinari&hide_border=false&border_radius=18&border=16A34A&background=FFFFFF&stroke=15803D&ring=16A34A&fire=15803D&currStreakLabel=15803D&sideLabels=3F5C4A&currStreakNum=0F172A&sideNums=0F172A&dates=8FBF9F&titleColor=15803D&card_width=1180" alt="Henrique's streak" />
</picture>

<br/>
<br/>

<!-- 4) STATS + LINGUAGENS lado a lado
  PASSO 4 - Serviço: github-readme-stats (projeto anuraghazra/github-readme-stats).
  IMPORTANTE: o serviço público costuma estourar o limite de requisições.
  Aqui usamos uma cópia PRÓPRIA hospedada na Vercel (URL ...vercel.app).
  Para ter a sua: faça fork do projeto, importe na Vercel e adicione a
  variável de ambiente PAT_1 com um token do GitHub (read:user e repo).
  Parâmetros do card de stats (/api):
    username=USUARIO           show_icons=true  mostra ícones
    count_private=true         inclui contribuições privadas
    include_all_commits=true   conta commits de todos os anos, não só o atual
    hide_rank=true             esconde o círculo de nota (rank)
    line_height=24             espaço entre linhas (ajustado para o card ficar
                               com a mesma altura do card de linguagens)
    hide_border=false, border_radius=18, border_color=COR   borda igual aos outros
    title_color, icon_color, text_color, bg_color           cores
    card_width=580             cada card mede metade da largura do painel
  Parâmetros do card de linguagens (/api/top-langs/):
    layout=compact             barra única com legenda em colunas
    langs_count=8              quantidade de linguagens exibidas
  Largura: cada imagem usa width="49.2%" e há só UM espaço (a quebra de linha
  entre as tags) entre elas. 49,2% + 49,2% + esse espaço cabem na linha mesmo
  em telas de celular. Com um espaço maior (ex.: dois &nbsp;) a soma passa de
  100% no celular e o segundo card cai para baixo do primeiro.
-->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats-sigma-rosy-28.vercel.app/api?username=henrique-molinari&show_icons=true&count_private=true&include_all_commits=true&hide_rank=true&line_height=24&hide_border=false&border_radius=18&title_color=00FF66&icon_color=00CC44&text_color=8FBF9F&bg_color=060B08&card_width=580&border_color=00FF66" />
  <img width="49.2%" src="https://github-readme-stats-sigma-rosy-28.vercel.app/api?username=henrique-molinari&show_icons=true&count_private=true&include_all_commits=true&hide_rank=true&line_height=24&hide_border=false&border_radius=18&title_color=15803D&icon_color=16A34A&text_color=0F172A&bg_color=FFFFFF&card_width=580&border_color=16A34A" alt="Henrique's GitHub stats" />
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github-readme-stats-sigma-rosy-28.vercel.app/api/top-langs/?username=henrique-molinari&layout=compact&langs_count=8&hide_border=false&border_radius=18&title_color=00FF66&text_color=8FBF9F&bg_color=060B08&card_width=580&border_color=00FF66" />
  <img width="49.2%" src="https://github-readme-stats-sigma-rosy-28.vercel.app/api/top-langs/?username=henrique-molinari&layout=compact&langs_count=8&hide_border=false&border_radius=18&title_color=15803D&text_color=0F172A&bg_color=FFFFFF&card_width=580&border_color=16A34A" alt="Top languages" />
</picture>

<br/>

</div>

<br/>

<!-- ===== 5) JOGO SPACE SHOOTER =====
  PASSO 5 - Um GIF animado em que uma nave "destrói" o seu gráfico de
  contribuições. É gerado pela Action czl9707/gh-space-shooter,
  configurada em .github/workflows/space-shooter.yml (roda todo dia à
  meia-noite UTC) e salva o resultado como game.gif na raiz do repositório.
  Para usar: copie o workflow, rode-o uma vez em Actions > Update Space
  Shooter Game > Run workflow, e depois referencie o game.gif com a img abaixo.
  O GitHub não aceita CSS (nem borda) em imagens do README, então o
  retângulo com contorno verde e cantos arredondados é desenhado dentro do
  próprio GIF pelo script .github/scripts/frame_game.py, que o workflow
  executa logo depois de gerar o jogo.
-->

<div align="center">

<img alt="Space shooter clearing my contribution graph" src="https://raw.githubusercontent.com/henrique-molinari/henrique-molinari/main/game.gif" width="100%"/>

</div>

<!-- ===== END SPACE SHOOTER ===== -->
<br/>

<!--
  ===== PAINEL DE PROJETOS (desativado por enquanto) =====
  O template original listava os PROJETOS DO ARIF (repositórios e logos dele).
  Removi essa seção para não exibir projetos que não são seus.
  Quando quiser reativar, edite projects.json com seus próprios repositórios
  e descomente o bloco abaixo.

<br/>
<div align="center">
<img width="100%" src="https://raw.githubusercontent.com/henrique-molinari/henrique-molinari/projects/projects.svg" alt="Projects" />
</div>
-->

<!-- ===== 6) BOTÕES DE CONTATO =====
  PASSO 6 - Badges do shields.io. O formato da URL é:
    https://img.shields.io/badge/TEXTO-COR_FUNDO?style=for-the-badge&logo=NOME&logoColor=COR&labelColor=COR
  O LinkedIn usa um ícone SVG embutido em base64 (logo=data:image/svg+xml;base64,...)
  porque o nome "linkedin" não está disponível em todas as versões do shields.
  Cada badge está dentro de um link (a href) para virar botão clicável
  (perfil do LinkedIn, GitHub e e-mail via mailto:).
  Troque os links pelos seus. O "&nbsp;&nbsp;" separa os botões.
-->
<br/>
<div align="center">

<a href="https://www.linkedin.com/in/henrique-molinari">
  <img src="https://img.shields.io/badge/LinkedIn-060B08?style=for-the-badge&logoColor=white&labelColor=060B08&logo=data:image/svg+xml;base64,PHN2ZyByb2xlPSJpbWciIHZpZXdCb3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiBmaWxsPSJ3aGl0ZSI+PHBhdGggZD0iTTIwLjQ0NyAyMC40NTJoLTMuNTU0di01LjU2OWMwLTEuMzI4LS4wMjctMy4wMzctMS44NTItMy4wMzctMS44NTMgMC0yLjEzNiAxLjQ0NS0yLjEzNiAyLjkzOXY1LjY2N0g5LjM1MVY5aDMuNDE0djEuNTYxaC4wNDZjLjQ3Ny0uOSAxLjYzNy0xLjg1IDMuMzctMS44NSAzLjYwMSAwIDQuMjY3IDIuMzcgNC4yNjcgNS40NTV2Ni4yODZ6TTUuMzM3IDcuNDMzYy0xLjE0NCAwLTIuMDYzLS45MjYtMi4wNjMtMi4wNjUgMC0xLjEzOC45Mi0yLjA2MyAyLjA2My0yLjA2MyAxLjE0IDAgMi4wNjQuOTI1IDIuMDY0IDIuMDYzIDAgMS4xMzktLjkyNSAyLjA2NS0yLjA2NCAyLjA2NXptMS43ODIgMTMuMDE5SDMuNTU1VjloMy41NjR2MTEuNDUyek0yMi4yMjUgMEgxLjc3MUMuNzkyIDAgMCAuNzc0IDAgMS43Mjl2MjAuNTQyQzAgMjMuMjI3Ljc5MiAyNCAxLjc3MSAyNGgyMC40NTFDMjMuMiAyNCAyNCAyMy4yMjcgMjQgMjIuMjcxVjEuNzI5QzI0IC43NzQgMjMuMiAwIDIyLjIyNSAweiIvPjwvc3ZnPg==" alt="LinkedIn" />
</a>
&nbsp;&nbsp;
<a href="https://github.com/henrique-molinari">
  <img src="https://img.shields.io/badge/GitHub-060B08?style=for-the-badge&logo=github&logoColor=00FF66&labelColor=060B08" alt="GitHub" />
</a>
&nbsp;&nbsp;
<a href="mailto:henriquee.molinari@gmail.com">
  <img src="https://img.shields.io/badge/Gmail-060B08?style=for-the-badge&logo=gmail&logoColor=00FF66&labelColor=060B08" alt="Email" />
</a>
&nbsp;&nbsp;
</div>

<!-- ===== END SOCIAL BADGES ===== -->


<!-- =================================== -->
