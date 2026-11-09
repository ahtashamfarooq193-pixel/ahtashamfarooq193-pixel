# -*- coding: utf-8 -*-
"""Build an aurora arcade / quest-style GitHub contribution card."""
from __future__ import annotations

import re
import urllib.request
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
USERNAME = "ahtashamfarooq193-pixel"
FONT = "ui-sans-serif, system-ui, Segoe UI, Helvetica, Arial, sans-serif"
LEVELS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
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


def shell(inner_h: int) -> tuple[str, str]:
    h = inner_h + 20
    return f'''<svg width="880" height="{h}" viewBox="0 0 880 {h}" fill="none" xmlns="http://www.w3.org/2000/svg" role="img">
  <rect x="10.5" y="10.5" width="859" height="{inner_h - 1}" rx="14" fill="#0d1117" stroke="#30363d"/>
''', "</svg>\n"


def build() -> str:
    days = fetch_days()
    total = sum(c for _d, _l, c in days)
    active = sum(1 for _d, _l, c in days if c > 0)
    current, best = streaks(days)

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

    inner_h = 220
    open_, close = shell(inner_h)

    cell, gap = 11.0, 3.0
    grid_w = len(weeks) * (cell + gap) - gap
    origin_x = 42 + (796 - grid_w) / 2
    origin_y = 106

    cells = []
    month_at: dict[int, str] = {}
    prev_month = None
    for wi, week in enumerate(weeks):
        x = origin_x + wi * (cell + gap)
        for di, (d, lv, count) in enumerate(week):
            y = origin_y + di * (cell + gap)
            color = LEVELS[min(lv, 4)]
            cells.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{cell}" height="{cell}" rx="2.5" fill="{color}">'
                f'<title>{count} contributions on {d.isoformat()}</title></rect>'
            )
        month = week[0][0].strftime("%b")
        if month != prev_month and week[0][0].day <= 13:
            month_at[wi] = month
            prev_month = month

    months = []
    for wi, label in month_at.items():
        x = origin_x + wi * (cell + gap)
        months.append(
            f'<text x="{x:.1f}" y="96" fill="#8b949e" font-family="{FONT}" font-size="10">{label}</text>'
        )

    legend_y = 220
    legend_x = 680
    legend = f'<text x="42" y="{legend_y:.1f}" fill="#8b949e" font-family="{FONT}" font-size="10">{active} active days · {current}-day current streak · {best}-day best</text>'
    legend += f'<text x="{legend_x:.1f}" y="{legend_y:.1f}" fill="#8b949e" font-family="{FONT}" font-size="10">Less</text>'
    for i, color in enumerate(LEVELS):
        lx = legend_x + 34 + i * 14
        ly = legend_y - 10
        legend += f'<rect x="{lx:.1f}" y="{ly:.1f}" width="10" height="10" rx="2" fill="{color}"/>'
    legend += f'<text x="{legend_x + 34 + 5 * 14 + 4:.1f}" y="{legend_y:.1f}" fill="#8b949e" font-family="{FONT}" font-size="10">More</text>'

    body = f'''
  <text x="42" y="48" fill="#e6edf3" font-family="{FONT}" font-size="20" font-weight="600">Contribution activity</text>
  <text x="838" y="43" text-anchor="end" fill="#e6edf3" font-family="{FONT}" font-size="18" font-weight="600">{total:,}</text>
  <text x="838" y="61" text-anchor="end" fill="#8b949e" font-family="{FONT}" font-size="10">contributions in the last year</text>
{''.join(months)}
{''.join(cells)}
{legend}
'''
    return open_ + body + close


def main() -> None:
    svg = build()
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT.name} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
