#!/usr/bin/env python3
"""
TUTORIAL - Gráfico de commits do ano para o README do perfil
============================================================

O que este script faz
    1. Consulta a API GraphQL do GitHub e pega o calendário de contribuições
       do ano ATUAL (1º de janeiro até 31 de dezembro).
    2. Desenha esse calendário como um SVG no estilo do gráfico do GitHub:
       uma coluna por semana, uma linha por dia da semana, um quadradinho por dia.
    3. Salva dois arquivos, um para cada tema do GitHub:
           commits-dark.svg   (tema escuro)
           commits-light.svg  (tema claro)
       O README escolhe qual mostrar usando <picture> (veja o README.md).

Como usar (passo a passo)
    1. Copie este arquivo para .github/scripts/generate_commits.py no seu repositório.
    2. Troque o usuário padrão em USER (ou defina a variável de ambiente GH_USER).
    3. Copie o workflow .github/workflows/commits-graph.yml, que roda o script
       automaticamente e faz commit dos SVGs gerados.
    4. No seu perfil, deixe marcada a opção "Private contributions"
       (Contribution settings), para que commits privados sejam contados.
    5. Para testar localmente:
           GITHUB_TOKEN=<seu token> python .github/scripts/generate_commits.py
       (o token pode ser obtido com "gh auth token" se você usa o GitHub CLI)

Não precisa instalar nada: só usa a biblioteca padrão do Python 3.
"""
import datetime, json, os, sys, urllib.request

# ---------------------------------------------------------------------------
# PASSO 1 - Configuração
# ---------------------------------------------------------------------------
# Usuário do GitHub que será consultado. Pode ser trocado por variável de ambiente.
USER = os.environ.get("GH_USER", "henrique-molinari")
# Token de acesso. No GitHub Actions ele vem de secrets.GITHUB_TOKEN (veja o workflow).
TOKEN = os.environ.get("GITHUB_TOKEN", "")
# Ano atual: o gráfico sempre mostra de janeiro a dezembro deste ano.
YEAR = datetime.date.today().year

# Consulta GraphQL. Pedimos, para o período $from..$to, o total de contribuições
# e, semana a semana, a data e a quantidade de contribuições de cada dia.
QUERY = """query($u:String!,$from:DateTime!,$to:DateTime!){user(login:$u){contributionsCollection(from:$from,to:$to){contributionCalendar{
totalContributions weeks{contributionDays{date contributionCount}}}}}}"""

# ---------------------------------------------------------------------------
# PASSO 2 - Temas de cor
# ---------------------------------------------------------------------------
# bg      = fundo do cartão            border = contorno do cartão
# title   = cor do título              text   = cor dos textos pequenos (meses, legenda)
# levels  = 5 cores, da menor atividade (0 commits) até a maior (nível 4)
THEMES = {
    "dark":  dict(bg="#060B08", border="#00FF66", title="#00FF66", text="#8FBF9F",
                  levels=["#1A2A21", "#12A044", "#00A843", "#00D452", "#00FF66"]),
    "light": dict(bg="#FFFFFF", border="#16A34A", title="#15803D", text="#3F5C4A",
                  levels=["#E8F1EB", "#86E0A6", "#4CCB79", "#16A34A", "#14532D"]),
}


# ---------------------------------------------------------------------------
# PASSO 3 - Buscar os dados na API do GitHub
# ---------------------------------------------------------------------------
def fetch():
    """Retorna o calendário de contribuições (total + semanas/dias) do ano atual."""
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {
            "u": USER,
            "from": f"{YEAR}-01-01T00:00:00Z",   # início do ano
            "to": f"{YEAR}-12-31T23:59:59Z",     # fim do ano
        }}).encode(),
        headers={"Authorization": f"Bearer {TOKEN}", "User-Agent": "commit-graph"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)["data"]["user"]["contributionsCollection"]["contributionCalendar"]


# ---------------------------------------------------------------------------
# PASSO 4 - Converter quantidade de commits em cor
# ---------------------------------------------------------------------------
def level(n, mx):
    """Devolve o nível de cor (0 a 4) para um dia com n contribuições.

    n  = contribuições do dia
    mx = maior número de contribuições em um único dia do ano
    Regras:
      * 0 commits            -> nível 0 (quadrado apagado)
      * exatamente 1 commit  -> nível 1 (SEMPRE visível, mesmo que o ano
                                tenha dias com dezenas de commits)
      * acima disso          -> escala proporcional até o nível 4
    """
    if n == 0: return 0
    if n == 1 or mx <= 1: return 1
    return min(4, 1 + max(1, round(3 * (n - 1) / (mx - 1))))


# ---------------------------------------------------------------------------
# PASSO 5 - Desenhar o SVG
# ---------------------------------------------------------------------------
def render(cal, t):
    """Monta o texto do SVG para o calendário `cal` usando o tema `t`."""
    weeks = cal["weeks"]
    # Layout: 1180 px de largura (mesma do painel principal e do card de streak).
    left, top, W = 44, 62, 1180          # margem esquerda, margem superior, largura total
    step = (W - left - 24) / len(weeks)  # distância entre colunas (ajusta ao nº de semanas)
    cell = step - 3                      # tamanho do quadradinho (3 px de espaço entre eles)
    H = round(top + 7 * step + 46)       # altura total: cabeçalho + 7 dias + legenda
    mx = max(d["contributionCount"] for w in weeks for d in w["contributionDays"])

    # o = lista de pedaços do SVG; no final juntamos tudo em um texto só.
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" role="img" aria-label="Commit activity">',
         # fundo com cantos arredondados (raio 18, igual aos demais cards)
         f'<rect width="{W}" height="{H}" rx="18" fill="{t["bg"]}"/>',
         # contorno verde arredondado
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="17" fill="none" stroke="{t["border"]}" stroke-width="1"/>',
         # título e total de contribuições do ano
         f'<text x="24" y="34" font-size="16" font-weight="700" fill="{t["title"]}">Commit Activity</text>',
         f'<text x="{W-24}" y="34" font-size="12" text-anchor="end" fill="{t["text"]}">{cal["totalContributions"]} contributions in {YEAR}</text>']

    # Uma coluna por semana; dentro dela, um quadrado por dia (domingo a sábado).
    last_m = -1
    for i, w in enumerate(weeks):
        d0 = w["contributionDays"][0]["date"]
        m = int(d0[5:7])
        # escreve o nome do mês acima da primeira semana de cada mês
        if m != last_m and i < len(weeks) - 2:
            o.append(f'<text x="{left+i*step}" y="{top-10}" font-size="10" fill="{t["text"]}">{datetime.date.fromisoformat(d0).strftime("%b")}</text>')
            last_m = m
        for j, d in enumerate(w["contributionDays"]):
            c = d["contributionCount"]
            # <title> dentro do quadrado vira a dica ao passar o mouse: "data: quantidade"
            o.append(f'<rect x="{left+i*step}" y="{top+j*step}" width="{cell}" height="{cell}" rx="3" fill="{t["levels"][level(c, mx)]}"><title>{d["date"]}: {c}</title></rect>')

    # Letras dos dias da semana na lateral (M = segunda, W = quarta, F = sexta)
    for j, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        o.append(f'<text x="24" y="{top+j*step+10}" font-size="10" text-anchor="middle" fill="{t["text"]}">{name[0]}</text>')

    # Legenda "Less [cores] More" no canto inferior direito
    ly = H - 22
    lx = W - 24 - 5 * 15 - 60
    o.append(f'<text x="{lx}" y="{ly+10}" font-size="10" fill="{t["text"]}">Less</text>')
    for k, col in enumerate(t["levels"]):
        o.append(f'<rect x="{lx+34+k*15}" y="{ly}" width="12" height="12" rx="2" fill="{col}"/>')
    o.append(f'<text x="{lx+34+5*15+4}" y="{ly+10}" font-size="10" fill="{t["text"]}">More</text></svg>')
    return "".join(o)


# ---------------------------------------------------------------------------
# PASSO 6 - Executar: buscar dados e gravar um SVG por tema
# ---------------------------------------------------------------------------
def main():
    cal = fetch()
    for name, t in THEMES.items():
        with open(f"commits-{name}.svg", "w", encoding="utf8") as f:
            f.write(render(cal, t))
    print("ok", cal["totalContributions"])


if __name__ == "__main__":
    main()
