#!/usr/bin/env python3
"""
IllusionFun — Kitaoka Diagonal Bevel Illusion Generator
========================================================
A fun CLI tool that generates Kitaoka-style optical illusion patterns
as SVG files with random colour schemes every run.

Usage:
    python illusion_fun.py                          # defaults: 8x8 grid, 3584px
    python illusion_fun.py --grid 6 --size 2048     # 6x6 grid, 2048px canvas
    python illusion_fun.py --grid 16 --size 4096    # 16x16 grid, 4096px canvas

Author: Charis Tsevis & Claude (Anthropic)
"""

import argparse
import random
import os
import sys
from datetime import datetime

# ── Curated colour schemes ───────────────────────────────────────────
# (name, tile_hex, background_hex)
COLOUR_SCHEMES = [
    ("Green & Orange",      "#00a651", "#f7941d"),
    ("Blue & Yellow",       "#3366cc", "#ffcc00"),
    ("Red & Cyan",          "#cc3333", "#33cccc"),
    ("Magenta & Lime",      "#cc33aa", "#66cc33"),
    ("Purple & Gold",       "#6633cc", "#ffaa00"),
    ("Teal & Coral",        "#009999", "#ff6655"),
    ("Navy & Peach",        "#223366", "#ffaa88"),
    ("Forest & Rose",       "#336633", "#ff6688"),
    ("Indigo & Amber",      "#4433aa", "#ffbb33"),
    ("Wine & Mint",         "#882244", "#55ddaa"),
    ("Slate & Tangerine",   "#445566", "#ff8833"),
    ("Cobalt & Lemon",      "#0044aa", "#eedd33"),
]

# ── Bevel pairs ──────────────────────────────────────────────────────
# (shadow_hex, highlight_hex)
BEVEL_PAIRS = [
    ("#000000", "#ffffff"),
    ("#1a1a2e", "#f0ece2"),
    ("#2d2d3d", "#e8e0d0"),
    ("#0c0f38", "#f0d264"),
]

# ── Rotation states ──────────────────────────────────────────────────
STATES = ["A", "B", "C", "D"]


def build_module_svg(ox, oy, state, module_size, bevel,
                     tile_color, shadow_color, highlight_color):
    """Generate SVG elements for one beveled module."""
    s, b = module_size, bevel
    ib = s - b
    interior = s - 2 * b
    ix, iy = ox + b, oy + b

    # Interior rectangle
    rect = f'    <rect fill="{tile_color}" x="{ix}" y="{iy}" width="{interior}" height="{interior}"/>'

    # Shadow L-bevel
    if state == "A":
        sp = f"{ox},{oy} {ox+b},{oy+b} {ox+b},{oy+ib} {ox+ib},{oy+ib} {ox+s},{oy+s} {ox},{oy+s}"
    elif state == "B":
        sp = f"{ox},{oy+s} {ox+b},{oy+ib} {ox+ib},{oy+ib} {ox+ib},{oy+b} {ox+s},{oy} {ox+s},{oy+s}"
    elif state == "C":
        sp = f"{ox+s},{oy+s} {ox+ib},{oy+ib} {ox+ib},{oy+b} {ox+b},{oy+b} {ox},{oy} {ox+s},{oy}"
    else:  # D
        sp = f"{ox+s},{oy} {ox+ib},{oy+b} {ox+b},{oy+b} {ox+b},{oy+ib} {ox},{oy+s} {ox},{oy}"
    shadow = f'    <polygon fill="{shadow_color}" points="{sp}"/>'

    # Highlight L-bevel
    if state == "A":
        hp = f"{ox+s},{oy} {ox},{oy} {ox+b},{oy+b} {ox+ib},{oy+b} {ox+ib},{oy+ib} {ox+s},{oy+s}"
    elif state == "B":
        hp = f"{ox},{oy} {ox},{oy+s} {ox+b},{oy+ib} {ox+b},{oy+b} {ox+ib},{oy+b} {ox+s},{oy}"
    elif state == "C":
        hp = f"{ox},{oy+s} {ox+s},{oy+s} {ox+ib},{oy+ib} {ox+b},{oy+ib} {ox+b},{oy+b} {ox},{oy}"
    else:  # D
        hp = f"{ox+s},{oy+s} {ox+s},{oy} {ox+ib},{oy+b} {ox+ib},{oy+ib} {ox+b},{oy+ib} {ox},{oy+s}"
    highlight = f'    <polygon fill="{highlight_color}" points="{hp}"/>'

    return f"  <g>\n{rect}\n{shadow}\n{highlight}\n  </g>"


def generate_illusion(grid_n, canvas_size, cell_size=32):
    """Generate a complete Kitaoka illusion SVG string."""

    # Pick random colours
    scheme_name, tile_color, bg_color = random.choice(COLOUR_SCHEMES)
    shadow_color, highlight_color = random.choice(BEVEL_PAIRS)

    # 50% chance to swap tile/bg for variety
    if random.random() < 0.5:
        tile_color, bg_color = bg_color, tile_color

    # Derived geometry
    module_size = grid_n * cell_size
    bevel = cell_size
    step = (grid_n - 1) * cell_size

    # Grid range
    max_idx = canvas_size // step + 2

    # Collect even-parity modules sorted for z-order
    modules = []
    for col in range(max_idx):
        for row in range(max_idx):
            if (col + row) % 2 != 0:
                continue
            ox = col * step
            oy = row * step
            if ox >= canvas_size or oy >= canvas_size:
                continue
            d = col - row
            state = STATES[((d + 2) // 4) % 4]
            modules.append((col + row, col, ox, oy, state))

    modules.sort(key=lambda m: (m[0], m[1]))

    # Build SVG
    lines = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_size} {canvas_size}">',
        f'  <!-- IllusionFun — {scheme_name} | grid {grid_n}x{grid_n} -->',
        f'  <rect fill="{bg_color}" width="{canvas_size}" height="{canvas_size}"/>',
    ]

    for _, _, ox, oy, state in modules:
        lines.append(build_module_svg(
            ox, oy, state, module_size, bevel,
            tile_color, shadow_color, highlight_color,
        ))

    lines.append("</svg>")
    return "\n".join(lines), scheme_name


def write_info_file(output_path):
    """Write a short info text about the Kitaoka illusion."""
    info = """Kitaoka Illusion — Quick Facts
==============================

What is this?
  This is a variant of the "optical illusion of diagonal beveled tiles"
  popularised by Professor Akiyoshi Kitaoka of Ritsumeikan University, Japan.
  The perfectly straight diagonal lines appear to curve or tilt because of the
  asymmetric light/shadow bevels that rotate in an AA BB CC DD sequence.

How does it work?
  Each square tile has a raised-button bevel (shadow on one side, highlight
  on the other). When the bevel direction shifts every two tiles along a
  diagonal, your brain interprets the straight lines as bending. The
  checkerboard colouring amplifies the effect.

Who is Akiyoshi Kitaoka?
  A Japanese Professor of Psychology at Ritsumeikan University, Kyoto.
  He is one of the world's leading researchers on visual illusions and has
  created hundreds of remarkable optical illusion designs.

Want to know more?
  Read the full story of how this pattern was decoded and implemented:
  https://tsevis.com/blog/dear-claude-you-were-wrong-so-was-i-lets-talk

Generated by IllusionFun — Charis Tsevis & Claude (Anthropic)
"""
    with open(output_path, "w") as f:
        f.write(info)


def main():
    parser = argparse.ArgumentParser(
        prog="IllusionFun",
        description="Generate Kitaoka diagonal bevel optical illusion SVGs",
    )
    parser.add_argument(
        "--grid", type=int, default=8, choices=[6, 8, 10, 12, 16],
        help="Module grid size NxN (default: 8)",
    )
    parser.add_argument(
        "--size", type=int, default=3584,
        help="Canvas size in pixels (default: 3584)",
    )
    parser.add_argument(
        "--cell", type=int, default=32,
        help="Cell size in pixels (default: 32)",
    )
    parser.add_argument(
        "--output", "-o", type=str, default=None,
        help="Output SVG filename (default: auto-generated)",
    )
    args = parser.parse_args()

    # Generate
    svg_content, scheme_name = generate_illusion(args.grid, args.size, args.cell)

    # Output filename
    if args.output:
        svg_path = args.output
    else:
        timestamp = datetime.now().strftime("%H%M%S")
        svg_path = f"illusion_{args.grid}x{args.grid}_{timestamp}.svg"

    # Write SVG
    with open(svg_path, "w") as f:
        f.write(svg_content)

    # Write info file (once, beside the SVG)
    info_path = os.path.join(os.path.dirname(svg_path) or ".", "kitaoka_illusion_info.txt")
    if not os.path.exists(info_path):
        write_info_file(info_path)

    print(f"IllusionFun!")
    print(f"  Grid:    {args.grid}x{args.grid}")
    print(f"  Canvas:  {args.size}x{args.size}px")
    print(f"  Colours: {scheme_name}")
    print(f"  Output:  {svg_path}")
    print(f"  Info:    {info_path}")


if __name__ == "__main__":
    main()
