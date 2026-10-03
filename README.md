<p>
  <img src="https://landfall.readthedocs.io/en/latest/landfall_logo.png" width="144" height="144" alt="Landfall coastal location pin logo">
</p>

# Landfall

[![PyPI](https://img.shields.io/pypi/v/landfall.svg)](https://pypi.org/project/landfall/)
[![Tests](https://github.com/eddiethedean/landfall/actions/workflows/tests.yml/badge.svg)](https://github.com/eddiethedean/landfall/actions/workflows/tests.yml)
[![Python](https://img.shields.io/pypi/pyversions/landfall.svg)](https://pypi.org/project/landfall/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Documentation](https://readthedocs.org/projects/landfall/badge/?version=latest)](https://landfall.readthedocs.io/en/latest/)

Landfall turns geographic data into static map images with a small Python API.
Plot points, routes, polygons, and circles; combine layers; or read GeoJSON and
GeoPandas data. It uses [py-staticmaps](https://github.com/flopp/py-staticmaps)
for map tiles and returns [Pillow](https://pillow.readthedocs.io/) images.
For geohash or H3 heatmaps from point observations, see the companion
[Heatfall documentation](https://heatfall.readthedocs.io/en/latest/index.html).

![Three points plotted on a real map of Tampa Bay](https://landfall.readthedocs.io/en/latest/images/points.png)

<p align="center">
  <a href="https://landfall.readthedocs.io/en/latest/shapes-and-styling/"><img src="https://landfall.readthedocs.io/en/latest/images/route.png" width="31%" alt="A styled route across Tampa Bay"></a>
  <a href="https://landfall.readthedocs.io/en/latest/shapes-and-styling/"><img src="https://landfall.readthedocs.io/en/latest/images/polygon.png" width="31%" alt="A translucent polygon on a map"></a>
  <a href="https://landfall.readthedocs.io/en/latest/shapes-and-styling/"><img src="https://landfall.readthedocs.io/en/latest/images/layers.png" width="31%" alt="A layered map with points, a route, and polygon"></a>
</p>
<p align="center"><sub>Routes · translucent areas · layered maps</sub></p>

## Install

Landfall supports Python 3.8–3.13. Install the optional `geo` extra for
GeoPandas and Shapely integration.

```sh
python -m pip install landfall
python -m pip install 'landfall[geo]'  # optional
```

The default OpenStreetMap tile provider needs network access when rendering.
If you use a different tile provider, pass a py-staticmaps provider through
`tile_provider` or configure a `Context` directly.

## Make a map

```python
import landfall

image = landfall.plot_points(
    [(27.88, -82.49), (27.92, -82.46), (27.94, -82.44)],
    colors="distinct",
    point_size=14,
    window_size=(640, 440),
    zoom=-1,
)
image.save("tampa-points.png")
```

Native coordinate pairs are **(latitude, longitude)**. GeoJSON and Shapely
positions are **(longitude, latitude)**; Landfall converts them. For native
inputs already in longitude/latitude order, use `flip_coords=True`.

Every `plot_*` function returns a `PIL.Image.Image`. Use `Context` when a map
needs multiple kinds of shapes or an SVG result:

```python
map_context = landfall.Context()
map_context.add_points([27.88, 27.92], [-82.49, -82.46], colors="distinct")
map_context.add_line([(27.88, -82.49), (27.92, -82.46)], color="red")
map_context.add_circle(27.88, -82.49, 1000, fill_color="#ff000064")
map_context.render_pillow(800, 600).save("combined.png")
map_context.render_svg(800, 600).saveas("combined.svg")
```

## More maps you can run

```python
route = [(27.88, -82.49), (27.90, -82.47),
         (27.92, -82.46), (27.94, -82.44)]
landfall.plot_line(
    route, color="#d12c31", width=5, window_size=(640, 440), zoom=-1
).save("route.png")
```

![A red route on a real map of Tampa Bay](https://landfall.readthedocs.io/en/latest/images/route.png)

```python
landfall.plot_circle(
    27.88, -82.49, 1000,
    color="#9b2727", fill_color="#d12c3155", width=3,
    window_size=(640, 440),
).save("coverage.png")
```

![A one-kilometer radius rendered on a real map](https://landfall.readthedocs.io/en/latest/images/circle.png)

Circle radii are in **meters** by default; set `radius_unit="kilometers"` for
kilometers. Colors can be names, hex values, RGB/RGBA tuples, or
`staticmaps.Color` objects. Batch functions also accept the `"distinct"`,
`"random"`, and `"wheel"` palettes.
The checked-in images above were generated with
[`examples/generate_doc_maps.py`](examples/generate_doc_maps.py) using real
OpenStreetMap tiles; tile attribution appears in each image.

## Documentation

Read the [full documentation on Read the Docs](https://landfall.readthedocs.io/en/latest/).

| Start here | What you will find |
| --- | --- |
| [Getting started](https://landfall.readthedocs.io/en/latest/getting-started/) | Installation, coordinates, first maps, and image output |
| [Working with shapes](https://landfall.readthedocs.io/en/latest/shapes-and-styling/) | Layers, colors, groups, polygon holes, and circles |
| [GeoJSON and GeoPandas](https://landfall.readthedocs.io/en/latest/geospatial-data/) | Files, features, coordinate systems, and styling |
| [API reference](https://landfall.readthedocs.io/en/latest/api/) | Public functions, parameters, defaults, and return values |
| [Troubleshooting](https://landfall.readthedocs.io/en/latest/troubleshooting/) | Common errors, tile access, and optional dependencies |
| [Contributing](https://landfall.readthedocs.io/en/latest/contributing/) | Local setup, checks, and release validation |

The [documentation index](https://landfall.readthedocs.io/en/latest/) also
links to example notebooks. For release history, see the
[changelog](CHANGELOG.md).

## Support and license

Report bugs or request features through
[GitHub Issues](https://github.com/eddiethedean/landfall/issues).
Landfall is released under the [MIT license](LICENSE).
