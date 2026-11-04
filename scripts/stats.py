"""Generates dist/stats.svg: total contributions, total repos and streaks. Run by GitHub Actions."""
import datetime as dt
import json
import os
import sys
import urllib.request
from pathlib import Path

from svgtext import path

RED, WHITE, GREY = "#e63946", "#ffffff", "#8b949e"


def gql(query, variables, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "profile-stats"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(f"GitHub API error: {data['errors']}")
    return data["data"]


def fetch(user, token):
    base = gql("""query($u:String!){ user(login:$u){ createdAt
        repositories(ownerAffiliations:OWNER, privacy:PUBLIC){ totalCount } } }""", {"u": user}, token)["user"]
    days = {}
    start = int(base["createdAt"][:4])
    now = dt.datetime.now(dt.timezone.utc)
    for year in range(start, now.year + 1):
        frm = f"{year}-01-01T00:00:00Z"
        to = f"{year}-12-31T23:59:59Z" if year < now.year else now.strftime("%Y-%m-%dT%H:%M:%SZ")
        cal = gql("""query($u:String!,$f:DateTime!,$t:DateTime!){ user(login:$u){
            contributionsCollection(from:$f,to:$t){ contributionCalendar{ weeks{ contributionDays{ date contributionCount } } } } } }""",
                  {"u": user, "f": frm, "t": to}, token)
        for w in cal["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]:
            for d in w["contributionDays"]:
                days[d["date"]] = d["contributionCount"]
    return base["repositories"]["totalCount"], days


def streaks(days):
    dates = sorted(days)
    total = sum(days.values())
    longest = run = 0
    for d in dates:
        run = run + 1 if days[d] > 0 else 0
        longest = max(longest, run)
    today = dt.date.today()
    cur, day = 0, today
    if days.get(day.isoformat(), 0) == 0:
        day -= dt.timedelta(days=1)  # today not counted yet -> streak still alive
    while days.get(day.isoformat(), 0) > 0:
        cur += 1
        day -= dt.timedelta(days=1)
    active = [d for d in dates if days[d] > 0]
    return total, cur, longest, active[0] if active else today.isoformat()


def fmt(n):
    return f"{n:,}"


def card(total, repos, cur, longest, since):
    W, H = 1000, 210
    cols = [W / 6, W / 2, W * 5 / 6]
    since_txt = dt.date.fromisoformat(since).strftime("SINCE %b %Y").upper()
    blocks = [
        (fmt(total), "TOTAL CONTRIBUTIONS", since_txt),
        (fmt(repos), "PUBLIC REPOSITORIES", "PROJECTS ON GITHUB"),
        (fmt(cur), "CURRENT STREAK", f"LONGEST: {longest} DAYS"),
    ]
    parts = []
    for i, (x, (num, label, small)) in enumerate(zip(cols, blocks)):
        delay = i * 0.25
        if i == 2:
            parts.append(f'''<g class="pop" style="animation-delay:{delay}s">
  <circle cx="{x}" cy="88" r="46" fill="none" stroke="#2a0a0d" stroke-width="6"/>
  <circle class="ring" cx="{x}" cy="88" r="46" fill="none" stroke="{RED}" stroke-width="6" stroke-linecap="round"
          stroke-dasharray="289" transform="rotate(-90 {x} 88)"/>
  <path d="{path(num, 34, x, 101, anchor='middle')}" fill="{WHITE}"/></g>''')
        else:
            parts.append(f'<g class="pop" style="animation-delay:{delay}s"><path d="{path(num, 40, x, 104, anchor="middle")}" fill="{WHITE}"/></g>')
        parts.append(f'<path class="pop" style="animation-delay:{delay+.1}s" d="{path(label, 12, x, 162, weight="Medium", spacing=1.5, anchor="middle")}" fill="{RED}"/>')
        parts.append(f'<path class="pop" style="animation-delay:{delay+.2}s" d="{path(small, 10, x, 184, weight="Medium", spacing=1.2, anchor="middle")}" fill="{GREY}"/>')
    seps = "".join(f'<rect x="{x}" y="40" width="1.5" height="140" fill="#30363d"/>' for x in (W / 3, W * 2 / 3))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>
  .pop{{opacity:0;animation:in .8s ease-out forwards}}
  @keyframes in{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:translateY(0)}}}}
  .ring{{stroke-dashoffset:289;animation:draw 1.6s ease-out .6s forwards}}
  @keyframes draw{{to{{stroke-dashoffset:0}}}}
</style>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="#0d1117" stroke="#30363d"/>
<rect x="40" y="1" width="{W-80}" height="3" rx="1.5" fill="{RED}"/>
{seps}
{"".join(parts)}
</svg>'''


if __name__ == "__main__":
    user = os.environ.get("GITHUB_USER") or (sys.argv[1] if len(sys.argv) > 1 else "thirurishi")
    token = os.environ["GITHUB_TOKEN"]
    repos, days = fetch(user, token)
    total, cur, longest, since = streaks(days)
    out = Path("dist")
    out.mkdir(exist_ok=True)
    (out / "stats.svg").write_text(card(total, repos, cur, longest, since))
    print(f"total={total} repos={repos} current={cur} longest={longest} since={since}")
