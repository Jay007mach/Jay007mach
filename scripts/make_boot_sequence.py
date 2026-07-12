"""
Build a self-hosted, self-contained "boot log" SVG: a terminal window that
types itself out line by line via a clip-path width animation (true typewriter,
not just fade-in), then blinks a cursor forever on the last line.

This stands in for a photo-based ASCII portrait -- no image required, and it
fits the "GATE prep / IT undergrad" framing better than a face render would.
Edit LINES below; everything re-lays-out and re-times itself.
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "boot-log.svg")
STATIC = bool(os.environ.get("STATIC"))

W, H = 370, 430
PAD = 18
TITLEBAR_H = 30
LINE_H = 19
CHAR_W = 7.35   # approx monospace advance at font-size 12.5
CPS = 38        # characters typed per second

BG = "#0a0e14"
BG2 = "#0d1420"
FRAME = "#1f6feb"
MUTED = "#7d8590"
INK = "#c9d1d9"
PROMPT = "#39d353"
ACCENT = "#22d3ee"
GOLD = "#f2cc60"

# ===========================================================================
#  EDIT THIS -- each line is (prefix_color, prefix_text, rest_text).
#  prefix_text is optional (pass "" to skip); rest_text is typed out.
# ===========================================================================
LINES = [
    (PROMPT, "jay@gcet", ":~$ whoami"),
    (None, "", "Jay Machhi -- B.Tech IT, Sem 7 @ GCET (CVM University)"),
    (PROMPT, "jay@gcet", ":~$ cat focus.txt"),
    (None, "", "> GATE 2027 prep -- DSA, CN, OS, DBMS, COA"),
    (None, "", "> Placement-ready: 6-mo internship w/ PPO target"),
    (None, "", "> Summer intern @ OptimAI (PHP / SaaS SEO tooling)"),
    (PROMPT, "jay@gcet", ":~$ cat traits.txt"),
    (None, "", "> Sports background -> discipline, resilience, teamwork"),
    (None, "", "> Breaks down hard problems, ships, iterates"),
    (PROMPT, "jay@gcet", ":~$ echo $STATUS"),
    (GOLD, "", "Open to any technical / analytical challenge."),
]


def esc(s):
    return html.escape(s)


def text_width(prefix, rest):
    return (len(prefix) + len(rest)) * CHAR_W


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>'
    f'<linearGradient id="tbg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#tbg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
             f'text-anchor="middle">jay@gcet: ~$ boot.log</text>')

y = TITLEBAR_H + 28
clip_id = 0
delay = 0.25
for prefix_color, prefix, rest in LINES:
    tw = text_width(prefix, rest)
    dur = max(0.15, len(prefix + rest) / CPS)
    clip_id += 1
    cid = f"clip{clip_id}"

    inner = ""
    x = PAD
    if prefix:
        inner += f'<text x="{x}" y="{y}" fill="{prefix_color}" font-size="12.5" font-weight="700">{esc(prefix)}</text>'
        x += len(prefix) * CHAR_W
    rest_color = prefix_color if (prefix_color and not prefix) else INK
    if rest:
        inner += f'<text x="{x}" y="{y}" fill="{rest_color}" font-size="12.5">{esc(rest)}</text>'

    if STATIC:
        parts.append(f'<g>{inner}</g>')
    else:
        parts.append(
            f'<clipPath id="{cid}"><rect x="0" y="{y-14}" width="0" height="18">'
            f'<animate attributeName="width" from="0" to="{tw+6:.1f}" begin="{delay:.2f}s" '
            f'dur="{dur:.2f}s" fill="freeze"/></rect></clipPath>'
            f'<g clip-path="url(#{cid})">{inner}</g>'
        )
    delay += dur + 0.12
    y += LINE_H

# blinking cursor after the last line finishes typing
if not STATIC:
    cursor_x = PAD
    parts.append(
        f'<rect x="{cursor_x}" y="{y-14}" width="7" height="14" fill="{ACCENT}" opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.01s" fill="freeze"/>'
        f'<animate attributeName="opacity" values="1;0;1" begin="{delay:.2f}s" dur="1s" repeatCount="indefinite"/>'
        f'</rect>'
    )

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print("wrote", OUT, len(svg), "bytes;", W, "x", H, "content_bottom", round(y))
