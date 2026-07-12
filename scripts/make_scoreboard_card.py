"""
Build a "match scoreboard" style info card SVG (sits to the RIGHT of
boot-log.svg): a LIVE scoreboard header, then rows grouped into LINEUP
(current roles/edu), STACK, and MATCH STATS (highlights) -- a sports-card
skin on the classic key/value info-panel idea, not a terminal / neofetch look.

Static content, hand-authored in ROWS below. Rows slide in on a stagger.
STATIC=1 emits the frozen state for previews.
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "scoreboard-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W, H = 490, 430
PAD = 20
HEAD_H = 34
KEY_X = PAD
VAL_X = PAD + 96
LINE_H = 20.5

BG = "#0b1220"
BG2 = "#0f1830"
FRAME = "#22314f"
MUTED = "#8290ab"
INK = "#dbe4f5"
KEY = "#f2c14e"      # gold keys
SECTION = "#22d3ee"  # cyan section headers
GREEN = "#3fd67a"
LIVE_RED = "#ff5c5c"

HOST = "Jay Machhi"
KICKER = "B.Tech IT &#183; GCET, CVM University &#183; Sem 7"

ROWS = [
    ("sec", "Lineup"),
    ("kv", "Now", "Summer Intern @ OptimAI (PHP/SaaS)"),
    ("kv", "Guide", "Er. Diyesh Patel (external)"),
    ("kv", "HoD", "Prof. Nikhil Gondaliya"),
    ("kv", "Target", "6-mo internship, PPO potential"),
    ("gap",),
    ("sec", "Stack"),
    ("kv", "Languages", "Python, Java, C/C++, JavaScript"),
    ("kv", "Web/App", "React, PHP, Node.js, Express"),
    ("kv", "Data/ML", "TensorFlow, Keras, scikit-learn"),
    ("kv", "Data stores", "MySQL, PostgreSQL, MongoDB"),
    ("gap",),
    ("sec", "Match stats"),
    ("bul", "Built OptimAI: PHP SaaS for SEO/GEO audits + file gen"),
    ("bul", "Led ML backend for YATRIKA, a Gujarat travel platform"),
    ("bul", "YOLOv8 + ByteTrack traffic monitoring on Colab T4"),
    ("bul", "Prepping for GATE while sprinting on placements"),
]


def esc(s):
    return html.escape(s)


def rise(inner, i):
    if STATIC:
        return f"<g>{inner}</g>"
    d = 0.18 + i * 0.055
    return (f'<g opacity="0" transform="translate(0,5)">{inner}'
            f'<animate attributeName="opacity" from="0" to="1" begin="{d:.2f}s" dur="0.4s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" '
            f'begin="{d:.2f}s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></g>')


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>'
    f'<linearGradient id="sbg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#sbg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<rect x="0" y="0" width="{W}" height="{HEAD_H}" rx="12" fill="{BG2}"/>',
    f'<rect x="0" y="{HEAD_H/2}" width="{W}" height="{HEAD_H/2}" fill="{BG2}"/>',
    f'<line x1="0" y1="{HEAD_H}" x2="{W}" y2="{HEAD_H}" stroke="{FRAME}"/>',
    f'<circle cx="{PAD}" cy="{HEAD_H/2}" r="4" fill="{LIVE_RED}">'
    f'<animate attributeName="opacity" values="1;0.35;1" dur="1.4s" repeatCount="indefinite"/></circle>',
    f'<text x="{PAD+12}" y="{HEAD_H/2+4}" fill="{LIVE_RED}" font-size="11" font-weight="700">LIVE</text>',
    f'<text x="{W/2}" y="{HEAD_H/2+4}" fill="{MUTED}" font-size="12" text-anchor="middle">profile scoreboard</text>',
    f'<text x="{W-PAD}" y="{HEAD_H/2+4}" fill="{MUTED}" font-size="11" text-anchor="end">SEM 7</text>',
]

y = HEAD_H + 26
parts.append(rise(f'<text x="{KEY_X}" y="{y}" fill="{INK}" font-size="15" font-weight="700">{esc(HOST)}</text>', 0))
y += 17
parts.append(rise(f'<text x="{KEY_X}" y="{y}" fill="{MUTED}" font-size="11">{KICKER}</text>', 1))
y += LINE_H

for i, row in enumerate(ROWS, start=2):
    kind = row[0]
    if kind == "gap":
        y += LINE_H * 0.5
        continue
    if kind == "sec":
        title = esc(row[1])
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" fill="{SECTION}" font-size="12.5" font-weight="700">'
                 f'&#9654; {title}</text>'
                 f'<line x1="{KEY_X + 18 + len(row[1])*8}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" '
                 f'stroke="{FRAME}" stroke-opacity="0.8"/>')
    elif kind == "kv":
        key, val = esc(row[1]), esc(row[2])
        inner = (f'<text x="{KEY_X}" y="{y:.1f}" fill="{KEY}" font-size="12.5" font-weight="700">{key}</text>'
                 f'<text x="{VAL_X}" y="{y:.1f}" fill="{INK}" font-size="12.5">{val}</text>')
    elif kind == "bul":
        txt = esc(row[1])
        inner = (f'<circle cx="{KEY_X+3}" cy="{y-4:.1f}" r="2.5" fill="{GREEN}"/>'
                 f'<text x="{KEY_X+14}" y="{y:.1f}" fill="{INK}" font-size="12.5">{txt}</text>')
    else:
        continue
    parts.append(rise(inner, i))
    y += LINE_H

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print("wrote", OUT, len(svg), "bytes;", W, "x", H, "content_bottom", round(y))
