import random
import os

svg = """<svg width="850" height="180" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .graph { pointer-events: all; cursor: crosshair; }
      .sq { transition: all 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275); rx: 2; }
      .bg { fill: transparent; }
"""

# Generate 50 different explosion patterns for chaos
for i in range(1, 51):
    dx = random.randint(-300, 300)
    dy = random.randint(-150, 150)
    rot = random.randint(-180, 180)
    scl = random.uniform(0.2, 2.5)
    color = random.choice(["#ff003c", "#00F2FF", "#00FF9D", "#F7768E", "#7000FF"])
    svg += f"""
      .graph:hover .sq.g{i} {{
         transform: translate({dx}px, {dy}px) rotate({rot}deg) scale({scl});
         fill: {color};
         opacity: {random.uniform(0.6, 1)};
      }}
"""

svg += """
      .hidden-text {
        font-family: monospace, sans-serif;
        font-size: 32px;
        fill: #ff003c;
        text-anchor: middle;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.5s ease-in 0.3s;
        filter: drop-shadow(0 0 10px #ff003c);
      }
      .graph:hover ~ .hidden-text {
        opacity: 1;
      }
    </style>
  </defs>

  <!-- Invisible background to catch hover over the whole area -->
  <rect class="graph bg" width="850" height="180" />
  
  <g class="graph" transform="translate(40, 30)">
"""

# GitHub colors
# Heavily weighted towards empty/low activity for realism, with some streaks
colors = ["#161B22"] * 10 + ["#0E4429"] * 4 + ["#006D32"] * 2 + ["#26A641", "#39D353"]

for col in range(53):
    for row in range(7):
        x = col * 14
        y = row * 14
        color = random.choice(colors)
        group = random.randint(1, 50)
        # transform-origin for individual rotation/scaling
        origin_x = x + 5
        origin_y = y + 5
        svg += f'    <rect class="sq g{group}" x="{x}" y="{y}" width="10" height="10" fill="{color}" style="transform-origin: {origin_x}px {origin_y}px;" />\n'

svg += """
  </g>
  
  <text x="425" y="100" class="hidden-text">
    ⚠️ NEURAL CORE BREACHED // KIEN234 ⚠️
  </text>
</svg>
"""

os.makedirs('assets', exist_ok=True)
with open('assets/fake_graph.svg', 'w', encoding='utf-8') as f:
    f.write(svg)
