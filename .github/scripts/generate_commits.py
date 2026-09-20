#!/usr/bin/env python3
"""Generate commits-dark.svg and commits-light.svg (green contribution calendar)."""
import datetime, json, os, sys, urllib.request

USER = os.environ.get("GH_USER", "henrique-molinari")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
QUERY = """query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{
totalContributions weeks{contributionDays{date contributionCount}}}}}}"""

THEMES = {
    "dark":  dict(bg="#060B08", title="#00FF66", text="#8FBF9F", levels=["#0F1F16", "#0B5A2A", "#00993A", "#00CC44", "#00FF66"]),
    "light": dict(bg="#FFFFFF", title="#15803D", text="#3F5C4A", levels=["#E8F1EB", "#A7E9BF", "#5FD68A", "#16A34A", "#14532D"]),
}

def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"u": USER}}).encode(),
        headers={"Authorization": f"Bearer {TOKEN}", "User-Agent": "commit-graph"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)["data"]["user"]["contributionsCollection"]["contributionCalendar"]

def level(n, mx):
    if n == 0: return 0
    return min(4, 1 + int(3 * (n - 1) / max(mx, 1)) + (1 if n == mx else 0)) if mx > 1 else 4

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
         f'<text x="{W-24}" y="34" font-size="12" text-anchor="end" fill="{t["text"]}">{cal["totalContributions"]} contributions in the last year</text>']
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
