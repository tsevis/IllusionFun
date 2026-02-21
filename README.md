# IllusionFun

IllusionFun is a Python CLI app that generates Kitaoka-style diagonal bevel optical illusion patterns as SVG files.

Each run picks a random curated color scheme, renders a tiled illusion grid, and writes an SVG you can open in any browser or vector editor.

## Requirements

- Python 3.8+ (no external dependencies)

## Quick Start

Run with defaults:

```bash
python3 illusion_fun.py
```

This generates:

- An SVG file named like `illusion_8x8_143210.svg`
- A `kitaoka_illusion_info.txt` file (created once per output directory)

## Common Examples

Generate a smaller image:

```bash
python3 illusion_fun.py --grid 6 --size 2048
```

Generate a larger image:

```bash
python3 illusion_fun.py --grid 16 --size 4096
```

Set output filename:

```bash
python3 illusion_fun.py --grid 8 --size 3584 -o my_illusion.svg
```

## CLI Options

```text
--grid {6,8,10,12,16}  Module grid size NxN (default: 8)
--size SIZE            Canvas size in pixels (default: 3584)
--cell CELL            Cell size in pixels (default: 32)
--output, -o PATH      Output SVG path (default: auto-generated)
```

## Notes

- Output is randomized per run (color scheme + possible tile/background swap).
- SVG is vector output, so it can be scaled without quality loss.
- Sample SVGs included in this repo:
  - `illusion_6x6_sample.svg`
  - `illusion_8x8_sample.svg`
  - `illusion_16x16_sample.svg`
