# Regenerates assets/banner.svg and assets/stack.svg.
# Pure-SVG animated cards (SMIL + declarative animation only - works inside
# GitHub's <img>/camo pipeline; no JS, no external requests).
# Icons are pulled from the simpleicons CDN and embedded as white paths.
# Run: python3 assets/generate.py

import base64
import random
import re
import urllib.request

W = 800
ICON_CDN = "https://cdn.simpleicons.org/{slug}"
AVATAR = "https://avatars.githubusercontent.com/u/224149905?size=128"

NAME = "reddux"
ROLE = "security researcher"
LINES = [
    "- offensive security & penetration testing",
    "- bug bounty hunting - hackerone & private programs",
    "- founder & engineer @ meridian safety",
]
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
GLYPHS = "!<>-_\\/[]{}=+*^?#@$"

# logo-loop marquee rows
ROW_A = ["cplusplus", "dotnet", "python", "go", "rust", "typescript",
         "javascript", "lua", "kalilinux", "burpsuite", "metasploit",
         "wireshark", "owasp", "hackthebox", "hackerone", "tryhackme"]
ROW_B = ["nodedotjs", "bun", "react", "nextdotjs", "express", "fastapi",
         "flask", "electron", "tailwindcss", "vite", "pytorch", "tensorflow",
         "opencv", "postgresql", "redis", "docker", "kubernetes", "nginx",
         "cloudflare", "vercel", "git", "githubactions", "linux", "neovim"]

NAMES = {
    "cplusplus": "c++", "dotnet": ".net", "python": "python", "go": "go",
    "rust": "rust", "typescript": "typescript", "javascript": "javascript",
    "lua": "lua", "kalilinux": "kali", "burpsuite": "burp suite",
    "metasploit": "metasploit", "wireshark": "wireshark", "owasp": "owasp",
    "hackthebox": "hackthebox", "hackerone": "hackerone",
    "tryhackme": "tryhackme", "nodedotjs": "node.js", "bun": "bun",
    "react": "react", "nextdotjs": "next.js", "express": "express",
    "fastapi": "fastapi", "flask": "flask", "electron": "electron",
    "tailwindcss": "tailwind", "vite": "vite", "pytorch": "pytorch",
    "tensorflow": "tensorflow", "opencv": "opencv", "postgresql": "postgres",
    "redis": "redis", "docker": "docker", "kubernetes": "k8s",
    "nginx": "nginx", "cloudflare": "cloudflare", "vercel": "vercel",
    "git": "git", "githubactions": "actions", "linux": "linux",
    "neovim": "neovim",
}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as r:
        return r.read()


def icon_paths(slug):
    svg = fetch(ICON_CDN.format(slug=slug)).decode()
    return re.findall(r'<path d="([^"]+)"', svg)


def icon(path_d, x, y, size, opacity=1.0):
    s = size / 24.0
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.3f})" '
            f'opacity="{opacity}"><path d="{path_d}" fill="#ffffff"/></g>')


def decrypt_frames(x, y, text, font_size, weight, fill,
                   frame_ms=70, resolve_ms=110):
    """Overlaid scramble frames that resolve left->right onto the static text."""
    def esc(s):
        return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    rng = random.Random(7)
    n = len(text)
    frames = []
    for i in range(n + 1):
        resolved = esc(text[:i])
        scramble = esc("".join(rng.choice(GLYPHS) for _ in range(n - i)))
        begin = i * frame_ms / 1000.0
        dur = (frame_ms + resolve_ms) / 1000.0
        frames.append(
            f'<text x="{x}" y="{y}" font-size="{font_size}" font-weight="{weight}" '
            f'fill="{fill}" font-family="{MONO}" display="none">'
            f'{resolved}<tspan fill="#6e7681">{scramble}</tspan>'
            f'<set attributeName="display" to="inline" begin="{begin:.2f}s" '
            f'dur="{dur:.2f}s"/></text>'
        )
    return "".join(frames)


def banner_svg(avatar_b64):
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="0.7" fill="#ffffff" opacity="0.05"/>'
        for x in range(24, W, 28) for y in range(24, 236, 28)
    )
    particles = "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffffff" opacity="0">'
        f'<animate attributeName="cy" values="{y};{y - 55}" dur="{d}s" '
        f'repeatCount="indefinite" begin="{b}s"/>'
        f'<animate attributeName="opacity" values="0;0.45;0" dur="{d}s" '
        f'repeatCount="indefinite" begin="{b}s"/></circle>'
        for x, y, r, d, b in [
            (60, 220, 1.2, 7, 0), (180, 235, 0.9, 9, 1.2), (330, 225, 1.4, 8, 2.5),
            (480, 238, 1.0, 10, 0.6), (620, 228, 1.3, 7.5, 3.1),
            (720, 232, 1.1, 9.5, 1.8), (750, 90, 0.9, 8.5, 4.0),
            (30, 100, 1.0, 11, 2.0), (560, 60, 0.8, 8, 0.9), (250, 55, 0.9, 9, 3.4),
        ]
    )
    bullets = "".join(
        f'<text x="180" y="{154 + i * 26}" fill="#8b949e" font-size="14" '
        f'font-family="{MONO}">{line.replace("&", "&amp;")}</text>'
        for i, line in enumerate(LINES)
    )
    caret_x = 180 + len(NAME) * 18 + 6
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{W}" height="240" viewBox="0 0 {W} 240" role="img"
     aria-label="reddux - security researcher">
  <defs>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
    <clipPath id="av"><circle cx="112" cy="120" r="44"/></clipPath>
  </defs>
  <rect width="{W}" height="240" rx="14" fill="#000000" stroke="#30363d"/>
  <rect x="0.6" y="0.6" width="{W - 1.2}" height="238.8" rx="14" fill="none"
        stroke="#ffffff" stroke-width="1.4" pathLength="2080"
        stroke-dasharray="70 2010" stroke-dashoffset="0" stroke-linecap="round"
        opacity="0.9">
    <animate attributeName="stroke-dashoffset" from="0" to="-2080"
             dur="7.5s" repeatCount="indefinite"/>
  </rect>
  {dots}
  <ellipse cx="400" cy="200" rx="260" ry="90" fill="url(#glow)">
    <animate attributeName="cx" values="300;500;300" dur="16s" repeatCount="indefinite"/>
  </ellipse>
  {particles}
  <circle cx="112" cy="120" r="45.5" fill="none" stroke="#ffffff"
          stroke-opacity="0.6" stroke-width="1.2"/>
  <image x="68" y="76" width="88" height="88" clip-path="url(#av)"
         xlink:href="data:image/jpeg;base64,{avatar_b64}"
         href="data:image/jpeg;base64,{avatar_b64}"/>
  <text x="180" y="80" fill="#ffffff" font-size="30" font-weight="600"
        font-family="{MONO}">{NAME}</text>
  {decrypt_frames(180, 80, NAME, 30, 600, "#ffffff")}
  <rect x="{caret_x}" y="62" width="10" height="21" fill="#ffffff">
    <animate attributeName="opacity" values="1;1;0;0;1" dur="1.1s" repeatCount="indefinite"/>
  </rect>
  <text x="180" y="110" fill="#ffffff" font-size="15" font-weight="600"
        letter-spacing="2" font-family="{MONO}">{ROLE.upper()}</text>
  <line x1="180" y1="124" x2="620" y2="124" stroke="#21262d" stroke-width="1"/>
  {bullets}
</svg>
'''


def marquee_row(slugs, y, icon_size, pitch, dur_s, reverse):
    """One infinite icon strip. Content duplicated; translates -pitch*n."""
    strip_w = len(slugs) * pitch
    items = "".join(
        "".join(icon(d, i * pitch, 0, icon_size) for d in icon_paths(slug))
        + f'<text x="{i * pitch + icon_size / 2:.1f}" y="{icon_size + 14}" '
        f'text-anchor="middle" fill="#6e7681" font-size="8.5" '
        f'font-family="{MONO}">{NAMES.get(slug, slug)}</text>'
        for i, slug in enumerate(slugs)
    )
    doubled = f'<g>{items}</g><g transform="translate({strip_w},0)">{items}</g>'
    x0, x1 = (-strip_w, 0) if reverse else (0, -strip_w)
    return (
        f'<g transform="translate(0,{y})"><g>'
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="{x0} 0" to="{x1} 0" dur="{dur_s}s" repeatCount="indefinite"/>'
        f'{doubled}</g></g>'
    )


def stack_svg():
    icon_size, pitch = 30, 62
    h = 216
    card_inset = 14
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}"
     viewBox="0 0 {W} {h}" role="img" aria-label="stack">
  <defs>
    <linearGradient id="fadeL" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#000000" stop-opacity="1"/>
      <stop offset="1" stop-color="#000000" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="fadeR" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#000000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000000" stop-opacity="1"/>
    </linearGradient>
    <clipPath id="view"><rect x="{card_inset}" y="0" width="{W - 2 * card_inset}" height="{h}"/></clipPath>
  </defs>
  <rect width="{W}" height="{h}" rx="14" fill="#000000" stroke="#30363d"/>
  <text x="{W / 2}" y="34" text-anchor="middle" fill="#6e7681" font-size="11"
        letter-spacing="4" font-family="{MONO}">STACK</text>
  <g clip-path="url(#view)">
    {marquee_row(ROW_A, 56, icon_size, pitch, 26, False)}
    {marquee_row(ROW_B, 132, icon_size, pitch, 36, True)}
  </g>
  <rect x="{card_inset}" y="40" width="70" height="{h - 46}" fill="url(#fadeL)"/>
  <rect x="{W - card_inset - 70}" y="40" width="70" height="{h - 46}" fill="url(#fadeR)"/>
</svg>
'''


def main():
    avatar_b64 = base64.b64encode(fetch(AVATAR)).decode()
    with open("assets/banner.svg", "w") as f:
        f.write(banner_svg(avatar_b64))
    with open("assets/stack.svg", "w") as f:
        f.write(stack_svg())
    print("wrote assets/banner.svg, assets/stack.svg")


if __name__ == "__main__":
    main()
