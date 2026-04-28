"""
Generate a GitHub-style Contribution Graph SVG with a multi-color heart pattern.
"""
import os

# 53 columns x 7 rows (standard GitHub contribution graph)
COLS = 53
ROWS = 7
CELL = 11       # cell size
GAP = 3         # gap between cells
OFFSET_X = 45   # left offset for day labels
OFFSET_Y = 30   # top offset for month labels

# Heart pattern centered in the grid (defined as set of (row, col) offsets)
# We'll place TWO hearts: a big one center-left and a smaller one center-right

def make_heart(cx, cy, size=1):
    """Generate heart coordinates centered at (cx, cy)."""
    # Base heart shape (13 wide x 7 tall)
    pattern = [
        "..XX...XX..",
        ".XXXX.XXXX.",
        "XXXXXXXXXXX",
        "XXXXXXXXXXX",
        ".XXXXXXXXX.",
        "..XXXXXXX..",
        "...XXXXX...",
    ]
    if size == 0:  # small heart (7 wide x 7 tall)
        pattern = [
            ".X...X.",
            "XXX.XXX",
            "XXXXXXX",
            "XXXXXXX",
            ".XXXXX.",
            "..XXX..",
            "...X...",
        ]
    
    coords = set()
    h = len(pattern)
    w = len(pattern[0])
    for r, row in enumerate(pattern):
        for c, ch in enumerate(row):
            if ch == 'X':
                rr = cy - h // 2 + r
                cc = cx - w // 2 + c
                if 0 <= rr < ROWS and 0 <= cc < COLS:
                    coords.add((rr, cc))
    return coords

# Create hearts
heart1 = make_heart(cx=16, cy=3, size=1)   # Big heart left
heart2 = make_heart(cx=36, cy=3, size=1)   # Big heart right
heart3 = make_heart(cx=26, cy=3, size=0)   # Small heart center

all_hearts = heart1 | heart2 | heart3

# Color palettes for each heart (gradient feel)
heart1_colors = ["#FF6B9D", "#FF3C7A", "#FF1461", "#E8003A", "#C70039", "#FF6B9D", "#FF3C7A"]
heart2_colors = ["#00F2FF", "#00D4FF", "#00B4FF", "#0099FF", "#007AFF", "#00F2FF", "#00D4FF"]
heart3_colors = ["#FFD700", "#FFAA00", "#FF8C00", "#FF6600", "#FF4500", "#FFD700", "#FFAA00"]

def get_color(r, c):
    if (r, c) in heart1:
        return heart1_colors[r % len(heart1_colors)]
    if (r, c) in heart3:
        return heart3_colors[r % len(heart3_colors)]
    if (r, c) in heart2:
        return heart2_colors[r % len(heart2_colors)]
    return "#161B22"  # dark empty cell

# Month labels (approximate positions for a full year)
months = [
    (1, "Jan"), (5, "Feb"), (9, "Mar"), (14, "Apr"),
    (18, "May"), (23, "Jun"), (27, "Jul"), (31, "Aug"),
    (36, "Sep"), (40, "Oct"), (44, "Nov"), (48, "Dec")
]

# Day labels
days = [(1, "Mon"), (3, "Wed"), (5, "Fri")]

# Calculate total SVG dimensions
svg_w = OFFSET_X + COLS * (CELL + GAP) + 20
svg_h = OFFSET_Y + ROWS * (CELL + GAP) + 40

# Build SVG
svg = f'''<svg width="{svg_w}" height="{svg_h}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .cb {{ fill: #0D1117; }}
      .cb-border {{ stroke: #30363D; stroke-width: 1; fill: none; }}
      .month {{ font-family: monospace; font-size: 10px; fill: #555; }}
      .day {{ font-family: monospace; font-size: 10px; fill: #555; }}
      .cell {{
        rx: 2;
        ry: 2;
        stroke: rgba(255,255,255,0.03);
        stroke-width: 0.5;
      }}
      .heart-cell {{
        animation: heartbeat 2s ease-in-out infinite;
      }}
      @keyframes heartbeat {{
        0%, 100% {{ transform: scale(1); opacity: 1; }}
        15% {{ transform: scale(1.15); opacity: 0.9; }}
        30% {{ transform: scale(1); opacity: 1; }}
        45% {{ transform: scale(1.08); opacity: 0.95; }}
        60% {{ transform: scale(1); }}
      }}
      .title {{
        font-family: monospace;
        font-size: 11px;
        fill: #555;
      }}
      .legend-label {{
        font-family: monospace;
        font-size: 10px;
        fill: #555;
      }}
    </style>
  </defs>

  <!-- Background -->
  <rect class="cb" width="{svg_w}" height="{svg_h}" rx="10" />
  <rect class="cb-border" x="0.5" y="0.5" width="{svg_w - 1}" height="{svg_h - 1}" rx="10" />
'''

# Month labels
for col, label in months:
    x = OFFSET_X + col * (CELL + GAP)
    svg += f'  <text class="month" x="{x}" y="{OFFSET_Y - 8}">{label}</text>\n'

# Day labels
for row, label in days:
    y = OFFSET_Y + row * (CELL + GAP) + 9
    svg += f'  <text class="day" x="5" y="{y}">{label}</text>\n'

# Grid cells
for col in range(COLS):
    for row in range(ROWS):
        x = OFFSET_X + col * (CELL + GAP)
        y = OFFSET_Y + row * (CELL + GAP)
        color = get_color(row, col)
        is_heart = (row, col) in all_hearts
        
        ox = x + CELL / 2
        oy = y + CELL / 2
        
        if is_heart:
            # Stagger animation delay based on distance from center for wave effect
            dist = abs(col - 26) * 0.05
            svg += (
                f'  <rect class="cell heart-cell" x="{x}" y="{y}" '
                f'width="{CELL}" height="{CELL}" fill="{color}" '
                f'style="transform-origin: {ox}px {oy}px; animation-delay: {dist:.2f}s;" '
                f'filter="drop-shadow(0 0 3px {color})" />\n'
            )
        else:
            svg += (
                f'  <rect class="cell" x="{x}" y="{y}" '
                f'width="{CELL}" height="{CELL}" fill="{color}" />\n'
            )

# Legend
legend_x = svg_w - 180
legend_y = svg_h - 18

svg += f'\n  <text class="legend-label" x="{legend_x - 30}" y="{legend_y + 8}">Less</text>\n'

legend_colors = ["#161B22", "#FF6B9D55", "#FF6B9D99", "#FF6B9DCC", "#FF6B9D"]
for i, lc in enumerate(legend_colors):
    lx = legend_x + i * (CELL + 2)
    svg += f'  <rect class="cell" x="{lx}" y="{legend_y}" width="{CELL}" height="{CELL}" fill="{lc}" />\n'

svg += f'  <text class="legend-label" x="{legend_x + 5 * (CELL + 2) + 5}" y="{legend_y + 8}">More</text>\n'

svg += '</svg>\n'

# Write output
os.makedirs('assets', exist_ok=True)
with open('assets/contributions.svg', 'w', encoding='utf-8') as f:
    f.write(svg)

print(f"Generated assets/contributions.svg ({svg_w}x{svg_h})")
