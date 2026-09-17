# -*- coding: utf-8 -*-
"""Build an aurora arcade / quest-style GitHub contribution card."""
from __future__ import annotations

import math
import re
import urllib.request
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
USERNAME = "ahtashamfarooq193-pixel"
FONT = "ui-sans-serif, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
LEVELS = ["#1b2438", "#1d4e6a", "#0ea5b7", "#22d3ee", "#c4b5fd"]
OUT = ROOT / "contributions-quest.svg"


def fetch_days() -> list[tuple[date, int, int]]:
    url = f"https://github.com/users/{USERNAME}/contributions"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    dates = re.findall(r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*data-level="(\d+)"', html)
    tips = re.findall(r"<tool-tip[^>]*>([^<]+)</tool-tip>", html)
    days = []
    for i, (ds, level) in enumerate(dates):
        count = 0
        if i < len(tips):
            m = re.search(r"(\d+)\s+contribution", tips[i])
            count = int(m.group(1)) if m else 0
        days.append((date.fromisoformat(ds), int(level), count))
    days.sort(key=lambda x: x[0])
    return days


def streaks(days: list[tuple[date, int, int]]) -> tuple[int, int]:
    best = run = 0
    for _d, _level, count in days:
        if count > 0:
            run += 1
            best = max(best, run)
        else:
            run = 0
    idx = len(days) - 1
    if idx >= 0 and days[idx][2] == 0:
        idx -= 1
    current = 0
    while idx >= 0 and days[idx][2] > 0:
        current += 1
        idx -= 1
    return current, best


def rpg_level(total: int) -> tuple[int, int, int]:
    remaining = total
    level = 1
    needed = 12
    while remaining >= needed and level < 99:
        remaining -= needed
        level += 1
        needed = 10 + level * 3
    return level, remaining, needed


def shell(inner_h: int) -> tuple[str, str]:
    h = inner_h + 20
    return f'''<svg width="880" height="{h}" viewBox="0 0 880 {h}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img">
  <defs>
    <linearGradient id="q-bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#050914"/>
      <stop offset="42%" stop-color="#0a1224"/>
      <stop offset="100%" stop-color="#14081f"/>
    </linearGradient>
    <linearGradient id="q-shine" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.18"/>
      <stop offset="28%" stop-color="#ffffff" stop-opacity="0.04"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="q-stroke" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#67e8f9" stop-opacity="0.7"/>
      <stop offset="48%" stop-color="#a78bfa" stop-opacity="0.28"/>
      <stop offset="100%" stop-color="#f0abfc" stop-opacity="0.58"/>
    </linearGradient>
    <linearGradient id="q-edge" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#67e8f9"/>
      <stop offset="100%" stop-color="#c084fc"/>
    </linearGradient>
    <linearGradient id="q-xp" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#22d3ee"/>
      <stop offset="55%" stop-color="#818cf8"/>
      <stop offset="100%" stop-color="#e879f9"/>
    </linearGradient>
    <linearGradient id="q-title" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#a5f3fc"/>
      <stop offset="100%" stop-color="#d8b4fe"/>
    </linearGradient>
    <linearGradient id="q-tile" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#12203a" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#0b1224" stop-opacity="0.72"/>
    </linearGradient>
    <radialGradient id="q-orb-cyan" cx="18%" cy="12%" r="52%">
      <stop offset="0%" stop-color="#22d3ee" stop-opacity="0.42"/>
      <stop offset="100%" stop-color="#22d3ee" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="q-orb-violet" cx="90%" cy="8%" r="48%">
      <stop offset="0%" stop-color="#8b5cf6" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#8b5cf6" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="q-orb-pink" cx="70%" cy="100%" r="46%">
      <stop offset="0%" stop-color="#f472b6" stop-opacity="0.24"/>
      <stop offset="100%" stop-color="#f472b6" stop-opacity="0"/>
    </radialGradient>
    <filter id="q-glow">
      <feGaussianBlur stdDeviation="3.2" result="b"/>
      <feMerge>
        <feMergeNode in="b"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <pattern id="q-grid" width="28" height="28" patternUnits="userSpaceOnUse">
      <path d="M 28 0 L 0 0 0 28" fill="none" stroke="#ffffff" stroke-opacity="0.035" stroke-width="1"/>
    </pattern>
    <pattern id="q-scan" width="880" height="4" patternUnits="userSpaceOnUse">
      <rect width="880" height="1" fill="#67e8f9" fill-opacity="0.035"/>
    </pattern>
    <clipPath id="q-frame">
      <rect x="10" y="10" width="860" height="{inner_h}" rx="30"/>
    </clipPath>
  </defs>
  <g clip-path="url(#q-frame)">
    <rect x="10" y="10" width="860" height="{inner_h}" rx="30" fill="url(#q-bg)"/>
    <rect x="10" y="10" width="860" height="{inner_h}" fill="url(#q-grid)"/>
    <ellipse cx="150" cy="10" rx="250" ry="130" fill="url(#q-orb-cyan)"/>
    <ellipse cx="780" cy="20" rx="220" ry="140" fill="url(#q-orb-violet)"/>
    <ellipse cx="640" cy="{inner_h}" rx="260" ry="120" fill="url(#q-orb-pink)"/>
    <rect x="10" y="10" width="860" height="{inner_h}" rx="30" fill="url(#q-shine)"/>
    <rect x="10" y="10" width="860" height="{inner_h}" fill="url(#q-scan)"/>
    <rect x="10" y="10" width="5" height="{inner_h}" fill="url(#q-edge)"/>
  </g>
  <rect x="10.8" y="10.8" width="858.4" height="{inner_h - 1.6}" rx="29" fill="none" stroke="url(#q-stroke)" stroke-width="1.5"/>
''', "</svg>\n"


def pixel_hero(cx: float, cy: float) -> str:
    return f'''
  <g transform="translate({cx:.1f},{cy:.1f})">
    <ellipse cx="0" cy="26" rx="18" ry="5" fill="#22d3ee" fill-opacity="0.18"/>
    <rect x="-11" y="6" width="22" height="16" rx="6" fill="#1e293b" stroke="#67e8f9" stroke-width="1.2"/>
    <rect x="-16" y="10" width="7" height="5" rx="2" fill="#a78bfa"/>
    <rect x="9" y="10" width="7" height="5" rx="2" fill="#a78bfa"/>
    <circle cx="0" cy="-6" r="13" fill="#0f172a" stroke="#67e8f9" stroke-width="1.6"/>
    <circle cx="0" cy="-6" r="8.5" fill="#164e63"/>
    <path d="M -7 -8 Q 0 -14 7 -8 Q 4 -2 -7 -4 Z" fill="#67e8f9" fill-opacity="0.85"/>
    <circle cx="-3" cy="-8" r="1.6" fill="#ffffff" fill-opacity="0.7"/>
  </g>
'''


def build() -> str:
    days = fetch_days()
    total = sum(c for _d, _l, c in days)
    active = sum(1 for _d, _l, c in days if c > 0)
    current, best = streaks(days)
    max_day = max((c for _d, _l, c in days), default=0)
    level, xp_now, xp_need = rpg_level(total)
    xp_pct = 0 if xp_need == 0 else min(1.0, xp_now / xp_need)

    first = days[0][0]
    last = days[-1][0]
    start = first - timedelta(days=(first.weekday() + 1) % 7)
    lookup = {d: (level_, count) for d, level_, count in days}

    weeks: list[list[tuple[date, int, int]]] = []
    cursor = start
    while cursor <= last:
        week = []
        for i in range(7):
            d = cursor + timedelta(days=i)
            lv, count = lookup.get(d, (0, 0))
            week.append((d, lv, count))
        weeks.append(week)
        cursor += timedelta(days=7)
    weeks = weeks[-53:]

    inner_h = 338
    open_, close = shell(inner_h)

    cell, gap = 11.0, 3.0
    grid_w = len(weeks) * (cell + gap) - gap
    origin_x = 42 + (796 - grid_w) / 2
    origin_y = 198

    cells = []
    month_at: dict[int, str] = {}
    prev_month = None
    positions: dict[date, tuple[float, float]] = {}
    for wi, week in enumerate(weeks):
        x = origin_x + wi * (cell + gap)
        for di, (d, lv, count) in enumerate(week):
            y = origin_y + di * (cell + gap)
            color = LEVELS[min(lv, 4)]
            positions[d] = (x + cell / 2, y + cell / 2)
            glow = ' filter="url(#q-glow)"' if lv >= 4 else ""
            cells.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell}" height="{cell}" rx="2.6" fill="{color}"{glow}/>'
            )
            if lv >= 3:
                cells.append(
                    f'<rect x="{x + 2.2:.1f}" y="{y + 1.6:.1f}" width="{cell - 4.4:.1f}" height="2.2" rx="1" fill="#ffffff" fill-opacity="0.22"/>'
                )
        month = week[0][0].strftime("%b")
        if month != prev_month and week[0][0].day <= 13:
            month_at[wi] = month
            prev_month = month

    months = []
    for wi, label in month_at.items():
        x = origin_x + wi * (cell + gap)
        months.append(
            f'<text x="{x:.1f}" y="190" fill="#7dd3fc" font-family="{FONT}" font-size="10" font-weight="650">{label}</text>'
        )

    trail = [(d, c) for d, _l, c in days if c > 0][-28:]
    path_pts = []
    for d, _c in trail:
        if d in positions:
            px, py = positions[d]
            path_pts.append(f"{px:.1f},{py:.1f}")
    ship = ""
    if len(path_pts) >= 2:
        d_attr = "M " + " L ".join(path_pts)
        dur = max(12, min(22, len(path_pts) * 0.55))
        ship = f'''
  <path d="{d_attr}" fill="none" stroke="#67e8f9" stroke-opacity="0.18" stroke-width="2" stroke-linejoin="round"/>
  <g filter="url(#q-glow)">
    <polygon points="-6,0 8,0 1,-5" fill="#a5f3fc">
      <animateMotion dur="{dur:.1f}s" repeatCount="indefinite" rotate="auto" path="{d_attr}"/>
    </polygon>
    <circle r="3.2" fill="#e879f9" fill-opacity="0.95">
      <animateMotion dur="{dur:.1f}s" repeatCount="indefinite" path="{d_attr}"/>
    </circle>
  </g>
'''

    latest_pulse = ""
    for d, _l, c in reversed(days):
        if c > 0 and d in positions:
            px, py = positions[d]
            latest_pulse = f'''
  <circle cx="{px:.1f}" cy="{py:.1f}" r="8" fill="none" stroke="#f0abfc" stroke-width="1.4">
    <animate attributeName="r" values="6;12;6" dur="1.8s" repeatCount="indefinite"/>
    <animate attributeName="stroke-opacity" values="0.9;0.05;0.9" dur="1.8s" repeatCount="indefinite"/>
  </circle>
'''
            break

    legend_y = origin_y + 7 * (cell + gap) + 16
    legend_x = origin_x + grid_w - 168
    legend = f'<text x="{legend_x:.1f}" y="{legend_y:.1f}" fill="#94a3b8" font-family="{FONT}" font-size="10">idle</text>'
    for i, color in enumerate(LEVELS):
        lx = legend_x + 26 + i * 15
        ly = legend_y - 10
        legend += f'<rect x="{lx:.1f}" y="{ly:.1f}" width="11" height="11" rx="2.2" fill="{color}"/>'
    legend += f'<text x="{legend_x + 26 + 5 * 15 + 6:.1f}" y="{legend_y:.1f}" fill="#94a3b8" font-family="{FONT}" font-size="10">max</text>'

    tiles = [
        ("SCORE", str(total), "#a5f3fc"),
        ("COMBO", f"x{current}", "#67e8f9"),
        ("RECORD", str(best), "#c4b5fd"),
        ("STAGES", str(active), "#f0abfc"),
    ]
    tile_svg = ""
    for i, (label, value, color) in enumerate(tiles):
        x = 42 + i * 199
        tile_svg += f'''
  <rect x="{x}" y="118" width="188" height="52" rx="16" fill="url(#q-tile)" stroke="{color}" stroke-opacity="0.35"/>
  <text x="{x + 16}" y="138" fill="#94a3b8" font-family="{FONT}" font-size="10" font-weight="700" letter-spacing="1.8">{label}</text>
  <text x="{x + 16}" y="158" fill="{color}" font-family="{FONT}" font-size="22" font-weight="760">{value}</text>
'''

    badges = []
    if total >= 100:
        badges.append(("CENTURY", "#67e8f9"))
    if best >= 5:
        badges.append(("5-HIT COMBO", "#c4b5fd"))
    if active >= 30:
        badges.append(("MAP RUNNER", "#22d3ee"))
    if max_day >= 8:
        badges.append(("POWER HIT", "#f0abfc"))
    if current >= 2:
        badges.append(("ON FIRE", "#fb7185"))
    badges = badges[:4]

    next_quest = "NEXT: 10-DAY COMBO" if best < 10 else "NEXT: 200 SCORE"
    badge_svg = ""
    bx = 42.0
    for label, color in badges:
        w = round(22 + len(label) * 6.6, 1)
        badge_svg += f'''
  <rect x="{bx:.1f}" y="304" width="{w:.1f}" height="24" rx="12" fill="#0b1224" stroke="{color}" stroke-opacity="0.55"/>
  <circle cx="{bx + 12:.1f}" cy="316" r="3.2" fill="{color}"/>
  <text x="{bx + 20:.1f}" y="320" fill="{color}" font-family="{FONT}" font-size="10" font-weight="700" letter-spacing="0.6">{label}</text>
'''
        bx += w + 8
    badge_svg += f'''
  <text x="{bx + 6:.1f}" y="320" fill="#64748b" font-family="{FONT}" font-size="10.5" letter-spacing="0.6">{next_quest}</text>
'''

    bar_x, bar_y, bar_w, bar_h = 118, 86, 520, 12
    fill_w = max(8, bar_w * xp_pct)
    shimmer = bar_w * 0.22

    body = f'''
  <rect x="42" y="30" width="8" height="8" rx="2" fill="#67e8f9">
    <animate attributeName="fill-opacity" values="1;0.35;1" dur="1.4s" repeatCount="indefinite"/>
  </rect>
  <text x="56" y="38" fill="#7dd3fc" font-family="{FONT}" font-size="11" font-weight="700" letter-spacing="2.2">DEV QUEST</text>
  <text x="148" y="38" fill="#c4b5fd" font-family="{FONT}" font-size="11">player 01 · ahtasham</text>
  <text x="838" y="38" text-anchor="end" fill="#94a3b8" font-family="{FONT}" font-size="11" letter-spacing="1.4">STAGE {last.year}</text>

{pixel_hero(70, 78)}
  <text x="118" y="64" fill="url(#q-title)" font-family="{FONT}" font-size="22" font-weight="760">LEVEL {level}</text>
  <text x="232" y="64" fill="#e2e8f0" font-family="{FONT}" font-size="13">XP {xp_now} / {xp_need}</text>
  <text x="838" y="64" text-anchor="end" fill="#67e8f9" font-family="{FONT}" font-size="12" font-weight="700">COMBO x{current}</text>

  <rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_h}" rx="6" fill="#1b2438"/>
  <rect x="{bar_x}" y="{bar_y}" width="{fill_w:.1f}" height="{bar_h}" rx="6" fill="url(#q-xp)" filter="url(#q-glow)"/>
  <rect x="{bar_x}" y="{bar_y}" width="{shimmer:.1f}" height="{bar_h}" rx="6" fill="#ffffff" fill-opacity="0.18">
    <animate attributeName="x" values="{bar_x};{bar_x + fill_w - shimmer:.1f};{bar_x}" dur="2.8s" repeatCount="indefinite"/>
  </rect>
  <text x="{bar_x + bar_w + 14}" y="{bar_y + 11}" fill="#94a3b8" font-family="{FONT}" font-size="11">{math.floor(xp_pct * 100)}%</text>

{tile_svg}
{''.join(months)}
{''.join(cells)}
{ship}
{latest_pulse}
{legend}
{badge_svg}
'''
    return open_ + body + close


def main() -> None:
    svg = build()
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT.name} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
