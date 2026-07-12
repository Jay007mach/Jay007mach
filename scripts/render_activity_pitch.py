#!/usr/bin/env python3
"""
Render data/contributions.json as an "Activity Pitch" -- a 53x7 grid of commit
cells laid out on a football-pitch backdrop (touchlines, centre circle, penalty
arcs) instead of a plain GitHub-style heatmap. A small ball glyph sits on the
most recent active day, and a scoreboard strip along the bottom shows real
streak/total stats. One-shot reveal animation (sweeps on load, then freezes).

Run by .github/workflows/update-profile.yml after fetch_contributions.py.
"""
import datetime
import json
import os

HERE = os.path.dirname(__file__)
IN_PATH = os.path.join(HERE, "..", "data", "contributions.json")
OUT_PATH = os.path.join(HERE, "..", "activity-pitch.svg")

# turf-green ramp: empty -> brightest activity
PALETTE = ["#0f2417", "#154d2b", "#1f7a3f", "#2fae57", "#4fe08a"]

CELL = 11
GAP = 3
STEP = CELL + GAP
PAD_L = 34
PAD_R = 22
PAD_TOP = 46
SCORE_H = 58

PITCH = "#0c1f14"
PITCH_LINE = "#2c5c3c"
BG = "#081210"
FRAME = "#1e3a28"
TEXT = "#eafff0"
MUTED = "#7fa88f"
GOLD = "#f2c14e"
BALL = "#f4f1e8"

COL_T = 0.016
ROW_T = 0.04
CELL_DUR = 0.38


def level_for(count):
    if count == 0:
        return 0
    if count <= 3:
        return 1
    if count <= 8:
        return 2
    if count <= 15:
        return 3
    return 4


def build_grid(days):
    first = datetime.date.fromisoformat(days[0]["date"])
    lead_pad = (first.weekday() + 1) % 7  # sunday=0
    grid, col = [], [None] * lead_pad
    for d in days:
        date = datetime.date.fromisoformat(d["date"])
        weekday = (date.weekday() + 1) % 7
        while len(col) < weekday:
            col.append(None)
        col.append((d["date"], d["count"], level_for(d["count"])))
        if len(col) == 7:
            grid.append(col)
            col = []
    if col:
        while len(col) < 7:
            col.append(None)
        grid.append(col)
    return grid


def render(data):
    grid = build_grid(data["days"])
    weeks = len(grid)
    W = PAD_L + weeks * STEP + PAD_R
    H = PAD_TOP + 7 * STEP + 14 + SCORE_H

    # find most recent active day for the ball marker
    ball_pos = None
    for wi in range(weeks - 1, -1, -1):
        if ball_pos:
            break
        for di in range(6, -1, -1):
            cell = grid[wi][di]
            if cell and cell[1] > 0:
                ball_pos = (wi, di)
                break

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        '<defs>'
        f'<linearGradient id="pbg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{PITCH}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
        f'<rect width="{W}" height="{H}" rx="14" fill="url(#pbg)"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{FRAME}"/>',
        f'<text x="{PAD_L}" y="24" fill="{TEXT}" font-size="13" font-weight="700">Activity Pitch</text>',
        f'<text x="{W-PAD_R}" y="24" fill="{MUTED}" font-size="10.5" text-anchor="end">'
        f'last 12 months &#183; @{data["username"]}</text>',
    ]

    # pitch markings behind the grid
    grid_w, grid_h = weeks * STEP, 7 * STEP
    gx, gy = PAD_L - 8, PAD_TOP - 6
    parts.append(f'<rect x="{gx}" y="{gy}" width="{grid_w+16}" height="{grid_h+12}" rx="6" '
                 f'fill="none" stroke="{PITCH_LINE}" stroke-width="1.5"/>')
    midx = gx + (grid_w + 16) / 2
    parts.append(f'<line x1="{midx:.1f}" y1="{gy}" x2="{midx:.1f}" y2="{gy+grid_h+12}" '
                 f'stroke="{PITCH_LINE}" stroke-width="1.2"/>')
    parts.append(f'<circle cx="{midx:.1f}" cy="{gy+(grid_h+12)/2:.1f}" r="26" fill="none" '
                 f'stroke="{PITCH_LINE}" stroke-width="1.2"/>')

    # day-of-week labels
    for i, lbl in enumerate(["", "Mon", "", "Wed", "", "Fri", ""]):
        if lbl:
            parts.append(f'<text x="{PAD_L-8}" y="{PAD_TOP + i*STEP + 9}" fill="{MUTED}" '
                         f'font-size="9" text-anchor="end">{lbl}</text>')

    for wi, col in enumerate(grid):
        x = PAD_L + wi * STEP
        for di, cell in enumerate(col):
            y = PAD_TOP + di * STEP
            if cell is None:
                continue
            date, count, level = cell
            delay = 0.1 + wi * COL_T + di * ROW_T
            fill = PALETTE[level]
            rect = (f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{fill}" '
                    f'opacity="0"><title>{date}: {count} commit{"s" if count != 1 else ""}</title>'
                    f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" '
                    f'dur="{CELL_DUR}s" fill="freeze"/></rect>')
            parts.append(rect)

    if ball_pos:
        wi, di = ball_pos
        bx = PAD_L + wi * STEP + CELL / 2
        by = PAD_TOP + di * STEP + CELL / 2
        ball_delay = 0.1 + wi * COL_T + di * ROW_T + CELL_DUR + 0.15
        parts.append(
            f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="0" fill="{BALL}" stroke="{GOLD}" stroke-width="1">'
            f'<animate attributeName="r" from="0" to="6.5" begin="{ball_delay:.3f}s" dur="0.35s" '
            f'fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></circle>'
        )

    # legend
    leg_y = PAD_TOP + grid_h + 22
    parts.append(f'<text x="{PAD_L}" y="{leg_y}" fill="{MUTED}" font-size="9.5">Quiet</text>')
    lx = PAD_L + 42
    for lvl, col in enumerate(PALETTE):
        parts.append(f'<rect x="{lx + lvl*15}" y="{leg_y-9}" width="10" height="10" rx="2" fill="{col}"/>')
    parts.append(f'<text x="{lx + len(PALETTE)*15 + 6}" y="{leg_y}" fill="{MUTED}" font-size="9.5">Active</text>')

    # scoreboard strip
    sb_y = H - SCORE_H
    parts.append(f'<line x1="0" y1="{sb_y}" x2="{W}" y2="{sb_y}" stroke="{FRAME}"/>')
    parts.append(f'<rect x="0" y="{sb_y}" width="{W}" height="{SCORE_H}" fill="{BG}"/>')

    stats = [
        ("TOTAL", str(data["total_contributions"])),
        ("STREAK", f'{data["current_streak"]}d'),
        ("BEST STREAK", f'{data["longest_streak"]}d'),
        ("BEST DAY", str(data["best_day"]["count"])),
    ]
    col_w = W / len(stats)
    for i, (label, value) in enumerate(stats):
        cx = col_w * i + col_w / 2
        parts.append(f'<text x="{cx:.1f}" y="{sb_y+24}" fill="{GOLD}" font-size="16" '
                     f'font-weight="700" text-anchor="middle">{value}</text>')
        parts.append(f'<text x="{cx:.1f}" y="{sb_y+40}" fill="{MUTED}" font-size="8.5" '
                     f'letter-spacing="0.6" text-anchor="middle">{label}</text>')
        if i > 0:
            parts.append(f'<line x1="{col_w*i:.1f}" y1="{sb_y+12}" x2="{col_w*i:.1f}" y2="{sb_y+SCORE_H-12}" '
                         f'stroke="{FRAME}"/>')

    parts.append("</svg>")
    return "".join(parts), W, H


if __name__ == "__main__":
    with open(IN_PATH) as f:
        data = json.load(f)
    svg, w, h = render(data)
    with open(OUT_PATH, "w") as f:
        f.write(svg)
    print(f"wrote {OUT_PATH}: {w}x{h}, {len(svg)} bytes")
