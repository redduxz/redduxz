# Generates dist/top-langs.svg: a dark "Top Languages" card with a stacked
# percentage bar + legend, styled to match the profile's cyan theme.
# Reads public repo language bytes via the GitHub REST API — no extra scopes.

import json
import os
import urllib.request

USER = "redduxz"
OUT = "dist/top-langs.svg"

LANG_COLORS = {
    "C++": "#f34b7d", "C#": "#178600", "Python": "#3572A5", "Rust": "#dea584",
    "Go": "#00ADD8", "TypeScript": "#3178c6", "JavaScript": "#f1e05a",
    "HTML": "#e34c26", "CSS": "#563d7c", "Lua": "#000080", "Shell": "#89e051",
    "PowerShell": "#012456", "Batchfile": "#C1F12E", "Dockerfile": "#384d54",
    "Kotlin": "#A97BFF", "Java": "#b07219", "Swift": "#F05138",
}
FALLBACK = "#36BCF7"


def api(path):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "redduxz-langs",
            **({"Authorization": f"Bearer {os.environ['GH_TOKEN']}"} if os.environ.get("GH_TOKEN") else {}),
        },
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def main():
    totals = {}
    page = 1
    while True:
        repos = api(f"/users/{USER}/repos?per_page=100&page={page}&type=owner")
        if not repos:
            break
        for repo in repos:
            if repo.get("fork"):
                continue
            for lang, b in api(f"/repos/{USER}/{repo['name']}/languages").items():
                totals[lang] = totals.get(lang, 0) + b
        page += 1

    top = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)[:6]
    total = sum(v for _, v in top) or 1
    langs = [(n, v / total * 100) for n, v in top]

    width, height = 340, 40 + 24 + 20 * len(langs) + 16
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">',
        f'<rect width="{width}" height="{height}" rx="6" fill="#0d1117" stroke="#30363d"/>',
        f'<text x="16" y="26" fill="#c9d1d9" font-family="Segoe UI,Helvetica,Arial,sans-serif" '
        f'font-size="14" font-weight="600">Top Languages</text>',
    ]

    # stacked percentage bar
    x = 16.0
    bar_y, bar_h, bar_w = 36, 8, width - 32
    for name, pct in langs:
        w = max(bar_w * pct / 100, 0.0)
        svg.append(f'<rect x="{x:.2f}" y="{bar_y}" width="{w:.2f}" height="{bar_h}" '
                   f'fill="{LANG_COLORS.get(name, FALLBACK)}"/>')
        x += w
    svg.append(f'<rect x="16" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="4" '
               f'fill="none" stroke="#30363d"/>')

    # legend
    y = 60
    for i, (name, pct) in enumerate(langs):
        col = i % 2
        lx = 16 + col * 160
        ly = y + (i // 2) * 20
        svg.append(f'<circle cx="{lx + 4}" cy="{ly - 4}" r="4" '
                   f'fill="{LANG_COLORS.get(name, FALLBACK)}"/>')
        svg.append(f'<text x="{lx + 14}" y="{ly}" fill="#c9d1d9" '
                   f'font-family="Segoe UI,Helvetica,Arial,sans-serif" font-size="12">'
                   f'{name} <tspan fill="#8b949e">{pct:.1f}%</tspan></text>')

    svg.append("</svg>")
    os.makedirs("dist", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"wrote {OUT}: {langs}")


if __name__ == "__main__":
    main()
