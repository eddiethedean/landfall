![Landfall Logo](https://raw.githubusercontent.com/eddiethedean/landfall/main/docs/landfall_logo.png)
-----------------

# Landfall: Easy to use functions for plotting geographic data on static maps
[![PyPI Latest Release](https://img.shields.io/pypi/v/landfall.svg)](https://pypi.org/project/landfall/)
![Tests](https://github.com/eddiethedean/landfall/actions/workflows/tests.yml/badge.svg)

## What is it?

**Landfall** is a Python package with easy to use functions for plotting geographic data on a static map.

## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/eddiethedean/landfall

```sh
# PyPI
pip install landfall
```

## Dependencies
- [py-staticmaps - A python module to create static map images (PNG, SVG) with markers, geodesic lines, etc.](https://github.com/flopp/py-staticmaps)
- [distinctipy - A lightweight package for generating visually distinct colours.](https://github.com/alan-turing-institute/distinctipy)


## Example
```sh
import landfall


lats = [27.88, 27.92, 27.94]
lons = [-82.49, -82.49, -82.46]

landfall.plot_points(lats, lons)
```
![](https://raw.githubusercontent.com/eddiethedean/landfall/main/docs/example_map.png)