"""Builds the static header and section-title SVGs into assets/. Run once: python scripts/build_assets.py"""
from pathlib import Path
from svgtext import path, width

OUT = Path(__file__).resolve().parent.parent / "assets"
RED, DEEP, WHITE, GREY = "#e63946", "#3a0000", "#ffffff", "#8b949e"


def header():
    W, H = 1000, 270
    name = path("THIRUMURUGAN KUMAR", 54, W / 2, 118, spacing=3, anchor="middle")
    sub = path("DATA ANALYST  /  DATA SCIENTIST  /  PHOTOGRAPHER", 15, W / 2, 158,
               weight="Medium", spacing=3, anchor="middle")
    lines = [
        "DATA SCIENCE & ANALYTICS @ EPITA PARIS",
        "TURNING RAW DATA INTO BUSINESS DECISIONS",
        "SQL  /  PYTHON  /  POWER BI  /  MACHINE LEARNING",
        "OPEN TO INTERNSHIPS FROM JANUARY 2027",
    ]
    n = len(lines)
    tag_paths = "".join(
        f'<path class="t t{i}" d="{path(t, 13, W / 2, 205, weight="Medium", spacing=2, anchor="middle")}"/>'
        for i, t in enumerate(lines))
    per = 3  # seconds per line
    total = per * n
    keyframes = f"""
@keyframes cycle {{
  0% {{ opacity:0; transform:translateY(8px) }}
  {100/n*0.12:.2f}% {{ opacity:1; transform:translateY(0) }}
  {100/n*0.88:.2f}% {{ opacity:1; transform:translateY(0) }}
  {100/n:.2f}% {{ opacity:0; transform:translateY(-8px) }}
  100% {{ opacity:0 }}
}}"""
    delays = "".join(f".t{i}{{animation-delay:{i*per}s}}" for i in range(n))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#000000"/><stop offset=".55" stop-color="#1a0003"/><stop offset="1" stop-color="#5a0a10"/>
  </linearGradient>
  <linearGradient id="nameg" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#ffffff"/><stop offset=".5" stop-color="#ffd6d9"/><stop offset="1" stop-color="#ffffff"/>
  </linearGradient>
  <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <filter id="glow" x="-20%" y="-50%" width="140%" height="200%">
    <feGaussianBlur stdDeviation="6" result="b"/><feFlood flood-color="{RED}" flood-opacity=".75"/>
    <feComposite in2="b" operator="in"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
  <clipPath id="nameclip"><path d="{name}"/></clipPath>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="14"/></clipPath>
</defs>
<style>
  .w1{{animation:drift 9s ease-in-out infinite alternate}}
  .w2{{animation:drift 13s ease-in-out infinite alternate-reverse}}
  @keyframes drift{{from{{transform:translateX(0)}}to{{transform:translateX(-140px)}}}}
  .sweep{{animation:sweep 5s ease-in-out infinite}}
  @keyframes sweep{{0%{{transform:translateX(-400px)}}60%,100%{{transform:translateX(1100px)}}}}
  .t{{fill:{RED};opacity:0;animation:cycle {total}s linear infinite}}
  {keyframes}
  {delays}
  .dot{{animation:blink 2.4s ease-in-out infinite}}
  @keyframes blink{{0%,100%{{opacity:.25}}50%{{opacity:1}}}}
</style>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <path class="w1" fill="{RED}" fill-opacity=".14" d="M0 210 C 150 170 300 250 450 215 S 750 175 900 215 S 1100 240 1200 205 V {H} H 0 Z"/>
  <path class="w2" fill="{RED}" fill-opacity=".22" d="M0 235 C 180 205 330 270 500 240 S 800 205 960 238 S 1120 255 1200 232 V {H} H 0 Z"/>
  <rect x="0" y="0" width="{W}" height="3" fill="{RED}"/>
</g>
<g filter="url(#glow)"><path d="{name}" fill="url(#nameg)"/></g>
<g clip-path="url(#nameclip)"><rect class="sweep" x="0" y="40" width="160" height="100" fill="url(#shine)"/></g>
<path d="{sub}" fill="{WHITE}" fill-opacity=".85"/>
<rect x="{W/2-60}" y="174" width="120" height="2" fill="{RED}"/>
{tag_paths}
<circle class="dot" cx="{W-40}" cy="30" r="5" fill="{RED}"/>
<circle class="dot" cx="40" cy="30" r="5" fill="{RED}" style="animation-delay:1.2s"/>
</svg>'''


def title(text, size=26):
    W, H = 1000, 80
    tw = width(text, size, spacing=4)
    d = path(text, size, W / 2, 46, spacing=4, anchor="middle")
    gap = 26
    lx, rx = W / 2 - tw / 2 - gap, W / 2 + tw / 2 + gap
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
  <linearGradient id="g" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{RED}" stop-opacity="0"/><stop offset=".5" stop-color="{RED}"/><stop offset="1" stop-color="{RED}" stop-opacity="0"/>
  </linearGradient>
  <filter id="glow" x="-10%" y="-60%" width="120%" height="220%">
    <feGaussianBlur stdDeviation="4" result="b"/><feFlood flood-color="{RED}" flood-opacity=".6"/>
    <feComposite in2="b" operator="in"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<style>
  .line{{animation:pulse 3s ease-in-out infinite}}
  @keyframes pulse{{0%,100%{{opacity:.45}}50%{{opacity:1}}}}
  .spark{{animation:run 3.5s linear infinite}}
  @keyframes run{{from{{transform:translateX(0)}}to{{transform:translateX(860px)}}}}
  .dia{{transform:rotate(45deg);animation:spin 6s linear infinite}}
  @keyframes spin{{from{{transform:rotate(45deg)}}to{{transform:rotate(405deg)}}}}
</style>
<g filter="url(#glow)"><path d="{d}" fill="#ffffff"/></g>
<g transform="translate({lx} 35)"><rect class="dia" x="-6" y="-6" width="12" height="12" fill="{RED}"/></g>
<g transform="translate({rx} 35)"><rect class="dia" x="-6" y="-6" width="12" height="12" fill="{RED}"/></g>
<rect class="line" x="70" y="66" width="860" height="2" fill="url(#g)"/>
<circle class="spark" cx="70" cy="67" r="2.5" fill="#ffffff"/>
</svg>'''


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (OUT / "header.svg").write_text(header())
    for name, text in [("welcome", "WELCOME - I'M THIRU"), ("about", "ABOUT ME"), ("knowledge", "KNOWLEDGE"),
                       ("projects", "PROJECTS"), ("stats", "STATS"), ("socials", "SOCIALS")]:
        (OUT / f"title-{name}.svg").write_text(title(text))
    print("built", sorted(p.name for p in OUT.glob("*.svg")))
