# IllusionFun Manual

## 1. Overview

IllusionFun generates SVG optical illusions inspired by the Kitaoka diagonal bevel pattern.  
It is a standalone script with no third-party packages.

Main file:

- `illusion_fun.py`

## 2. Installation

No installation step is required beyond Python.

Check Python:

```bash
python3 --version
```

## 3. Running the Program

Basic usage:

```bash
python3 illusion_fun.py [options]
```

Help:

```bash
python3 illusion_fun.py --help
```

## 4. Command-Line Reference

### `--grid {6,8,10,12,16}`

- Controls module size as an `N x N` logical grid.
- Default: `8`

### `--size SIZE`

- Canvas width/height in pixels.
- Default: `3584`

### `--cell CELL`

- Base cell size (pixels) used to derive geometry and bevel width.
- Default: `32`

### `--output PATH` or `-o PATH`

- Output SVG file path.
- If omitted, auto filename format is:
  - `illusion_<grid>x<grid>_<HHMMSS>.svg`

## 5. Output Files

### SVG file

- Written to current directory unless `--output` points elsewhere.
- Contains:
  - Background rectangle
  - Ordered beveled tile modules for the illusion pattern
  - Metadata comment with selected color scheme and grid size

### `kitaoka_illusion_info.txt`

- Written beside the SVG.
- Created only if it does not already exist in that output directory.
- Contains background context on the illusion and references.

## 6. How Rendering Works (Technical Summary)

1. A random tile/background color scheme is selected from a curated list.
2. A random bevel shadow/highlight pair is selected.
3. With 50% probability, tile and background colors are swapped.
4. Geometry is derived from:
   - `module_size = grid * cell`
   - `bevel = cell`
   - `step = (grid - 1) * cell`
5. Tiles are placed on even checkerboard parity and assigned one of four states (`A`, `B`, `C`, `D`) based on diagonal offset.
6. Modules are sorted for deterministic z-order and emitted as SVG groups containing:
   - interior rectangle
   - shadow bevel polygon
   - highlight bevel polygon

## 7. Practical Presets

Small/fast preview:

```bash
python3 illusion_fun.py --grid 6 --size 1024
```

Balanced default look:

```bash
python3 illusion_fun.py --grid 8 --size 3584
```

High-detail output:

```bash
python3 illusion_fun.py --grid 16 --size 4096
```

## 8. Troubleshooting

### Command not found for Python

Use `python` instead of `python3` if your environment maps Python 3 that way.

### Permission error when writing output

- Choose a writable path with `-o`, for example:

```bash
python3 illusion_fun.py -o /tmp/illusion.svg
```

### Output looks too dense or too sparse

- Increase/decrease `--grid`
- Increase/decrease `--cell`
- Increase/decrease `--size` to change total canvas extent

## 9. Repo Contents

- `illusion_fun.py`: generator script
- `kitaoka_illusion_info.txt`: reference text sample
- `illusion_6x6_sample.svg`: sample output
- `illusion_8x8_sample.svg`: sample output
- `illusion_16x16_sample.svg`: sample output

