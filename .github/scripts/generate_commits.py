#!/usr/bin/env python3
"""Generate commits-dark.svg and commits-light.svg (green contribution calendar)."""
import datetime, json, os, sys, urllib.request

USER = os.environ.get("GH_USER", "henrique-molinari")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
YEAR = datetime.date.today().year
QUERY = """query($u:String!,$from:DateTime!,$to:DateTime!){user(login:$u){contributionsCollection(from:$from,to:$to){contributionCalendar{
totalContributions weeks{contributionDays{date contributionCount}}}}}}"""

THEMES = {
    "dark":  dict(bg="#060B08", title="#00FF66", text="#8FBF9F", levels=["#16241B", "#0E7A38", "#00A843", "#00D452", "#00FF66"]),
    "light": dict(bg="#FFFFFF", title="#15803D", text="#3F5C4A", levels=["#E8F1EB", "#86E0A6", "#4CCB79", "#16A34A", "#14532D"]),
}

def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"u": USER, "from": f"{YEAR}-01-01T00:00:00Z", "to": f"{YEAR}-12-31T23:59:59Z"}}).encode(),
        headers={"Authorization": f"Bearer {TOKEN}", "User-Agent": "commit-graph"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)["data"]["user"]["contributionsCollection"]["contributionCalendar"]

def level(n, mx):
    # any day with a commit is clearly visible (level >= 1)
    if n == 0: return 0
    if n == 1 or mx <= 1: return 1
    return min(4, 1 + max(1, round(3 * (n - 1) / (mx - 1))))

def render(cal, t):
    weeks = cal["weeks"]
    cell, gap, left, top = 12, 3, 44, 62
    step = cell + gap
    W = left + len(weeks) * step + 24
    H = top + 7 * step + 46
    mx = max(d["contributionCount"] for w in weeks for d in w["contributionDays"])
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" role="img" aria-label="Commit activity">',
         f'<rect width="{W}" height="{H}" rx="12" fill="{t["bg"]}"/>',
         f'<text x="24" y="34" font-size="16" font-weight="700" fill="{t["title"]}">Commit Activity</text>',
         f'<text x="{W-24}" y="34" font-size="12" text-anchor="end" fill="{t["text"]}">{cal["totalContributions"]} contributions in {YEAR}</text>']
    last_m = -1
    for i, w in enumerate(weeks):
        d0 = w["contributionDays"][0]["date"]
        m = int(d0[5:7])
        if m != last_m and i < len(weeks) - 2:
            o.append(f'<text x="{left+i*step}" y="{top-10}" font-size="10" fill="{t["text"]}">{datetime.date.fromisoformat(d0).strftime("%b")}</text>')
            last_m = m
        for j, d in enumerate(w["contributionDays"]):
            c = d["contributionCount"]
            o.append(f'<rect x="{left+i*step}" y="{top+j*step}" width="{cell}" height="{cell}" rx="2" fill="{t["levels"][level(c, mx)]}"><title>{d["date"]}: {c}</title></rect>')
    for j, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        o.append(f'<text x="24" y="{top+j*step+10}" font-size="10" text-anchor="middle" fill="{t["text"]}">{name[0]}</text>')
    ly = H - 22
    lx = W - 24 - 5 * step - 60
    o.append(f'<text x="{lx}" y="{ly+10}" font-size="10" fill="{t["text"]}">Less</text>')
    for k, col in enumerate(t["levels"]):
        o.append(f'<rect x="{lx+34+k*step}" y="{ly}" width="{cell}" height="{cell}" rx="2" fill="{col}"/>')
    o.append(f'<text x="{lx+34+5*step+4}" y="{ly+10}" font-size="10" fill="{t["text"]}">More</text></svg>')
    return "".join(o)

def main():
    cal = fetch()
    for name, t in THEMES.items():
        with open(f"commits-{name}.svg", "w", encoding="utf8") as f:
            f.write(render(cal, t))
    print("ok", cal["totalContributions"])

if __name__ == "__main__":
    main()
