![Landfall Logo](https://raw.githubusercontent.com/eddiethedean/landfall/main/docs/landfall_logo.png)

# Landfall

[![PyPI](https://img.shields.io/pypi/v/landfall.svg)](https://pypi.org/project/landfall/)
[![Tests](https://github.com/eddiethedean/landfall/actions/workflows/tests.yml/badge.svg)](https://github.com/eddiethedean/landfall/actions/workflows/tests.yml)
[![Python](https://img.shields.io/pypi/pyversions/landfall.svg)](https://pypi.org/project/landfall/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Plot geographic data on static maps with a small Python API. Landfall wraps
[py-staticmaps](https://github.com/flopp/py-staticmaps) and returns Pillow images
that you can save, display in a notebook, or use in a report.

- Plot points, lines, polygons, and circles.
- Generate distinct, random, or color-wheel palettes, with optional ID grouping.
- Read GeoJSON features and geometry collections, including multipart shapes and polygon holes.
- Plot Shapely geometries and GeoDataFrames with the optional `geo` extra.
- Combine shapes with `Context` and render with Pillow or SVG.

## Install

Requires Python 3.8 or newer. The release test matrix covers Python 3.8–3.13
on Linux, Windows, and macOS, plus current macOS ARM64 on Python 3.13.

```sh
pip install landfall
# Optional GeoPandas and Shapely support
pip install 'landfall[geo]'
```

Map tiles use OpenStreetMap by default and require network access. You can
supply another py-staticmaps tile provider or configure a context for offline
rendering.

## Quick start

```python
import landfall

image = landfall.plot_points(
    [27.88, 27.92, 27.94],
    [-82.49, -82.46, -82.44],
    colors="distinct",
    window_size=(800, 600),
)
image.save("points.png")
```

Landfall's coordinate pairs use **(latitude, longitude)**. GeoJSON and Shapely
use **(longitude, latitude)** and are converted automatically. For native
functions receiving longitude first, set `flip_coords=True`.

```python
# Coordinate pairs are also accepted by plot_points.
image = landfall.plot_points([(27.88, -82.49), (27.92, -82.46)])

route = [(27.88, -82.49), (27.92, -82.46), (27.94, -82.44)]
image = landfall.plot_line(route, color="red", width=3)

polygon = [(27.88, -82.49), (27.92, -82.49), (27.92, -82.44), (27.88, -82.44)]
image = landfall.plot_polygon(polygon, color="red", fill_color="#0000ff64")

# Radius is in meters by default; this is a one-kilometer circle.
image = landfall.plot_circle(27.88, -82.49, 1000, fill_color="#0000ff64")
```

## Colors and grouped data

For batch functions, `colors` accepts `"distinct"`, `"random"`, `"wheel"`, or a
list of color names, hex strings, RGB/RGBA tuples, or `staticmaps.Color` objects.
A single-item list applies to every shape. Otherwise, provide one color per
shape; mismatched lists raise `ValueError` instead of omitting data.

```python
image = landfall.plot_points(
    [27.88, 27.92, 27.94], [-82.49, -82.46, -82.44],
    ids=["north", "south", "north"],
    id_colors={"north": "blue", "south": "red"},
)
```

Polygons and circles also accept `fill_colors`, `fill_same=True`, and
`fill_transparency` (alpha from 0 for transparent to 255 for opaque).
Coordinate arrays, IDs, and radius arrays must have matching lengths.
Coordinates must be finite and within latitude −90..90 and longitude −180..180;
radii must be finite and non-negative.

## Combine shapes

```python
context = landfall.Context()
context.add_points([27.88, 27.92], [-82.49, -82.46], colors="distinct")
context.add_line([(27.88, -82.49), (27.92, -82.46)], color="red", width=2)
context.add_polygon(
    [(27.88, -82.49), (27.92, -82.49), (27.92, -82.44), (27.88, -82.44)],
    fill_color="#0000ff64",
)
context.add_circles([27.88], [-82.49], [1000], fill_color="yellow")
context.render_pillow(800, 600).save("combined.png")
context.render_svg(800, 600).saveas("combined.svg")
```

`Context` supports singular and plural `add_point`, `add_line`, `add_polygon`,
and `add_circle` methods. Native polygons close their last edge automatically.
`Context.add_polygon(..., holes=[...])` accepts interior rings.

## GeoJSON

```python
feature = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [-82.49, 27.88]},
    "properties": {"marker-color": "red", "marker-size": 12},
}
image = landfall.plot_geojson(feature)
# Or read a UTF-8 GeoJSON file:
# image = landfall.plot_geojson_file("data.geojson")
```

GeoJSON can be a dictionary or JSON string. Point, MultiPoint, LineString,
MultiLineString, Polygon, MultiPolygon, and nested GeometryCollection objects
are supported, along with Feature and FeatureCollection wrappers. Null
geometries are skipped and null properties are accepted. Altitude is ignored
when plotting positions. Empty input with no geometries raises `ValueError`.
Styling supports `stroke`, `stroke-width`, `fill`, `fill-opacity`,
`marker-color`, and `marker-size`.

## GeoPandas and Shapely

```python
import geopandas as gpd
from shapely.geometry import Point

frame = gpd.GeoDataFrame(
    {"color": ["red", "blue"], "size": [10, 15]},
    geometry=[Point(-82.49, 27.88), Point(-82.46, 27.92)],
    crs="EPSG:4326",
    index=["A", "B"],
)
image = landfall.plot_geodataframe(frame, color_column="color", size_column="size")
image = landfall.plot_geometries(list(frame.geometry), colors="distinct")
image = landfall.plot_geometry(frame.geometry.iloc[0])
```

GeoDataFrames with a CRS are reprojected to WGS84 automatically, including
when selecting another `geometry_column`. A frame without a CRS is assumed
to contain longitude/latitude values. Raw Shapely geometries must already
use WGS84 coordinates. `color_column` contains color names or hex values;
use `colors="distinct"` to generate a palette. Styling follows row order,
including duplicate or string index labels. Null and empty geometries are
skipped; an entirely empty input raises `ValueError`.

## API

| Function | Input |
| --- | --- |
| `plot_points` | Latitude/longitude arrays or coordinate pairs |
| `plot_points_data` | Mapping with named latitude/longitude columns |
| `plot_line`, `plot_lines` | One route or a sequence of routes |
| `plot_polygon`, `plot_polygons` | One polygon or a sequence of polygons |
| `plot_circle`, `plot_circles` | Center coordinates and radius/radii |
| `plot_geojson`, `plot_geojson_file` | GeoJSON data or a file path |
| `plot_geometry`, `plot_geometries` | Shapely geometry/geometries; requires `geo` |
| `plot_geodataframe` | GeoDataFrame; requires `geo` |
| `random_color(rng=None)` | Optional seed; leaves global random state unchanged |
| `Context` | Add shapes and configure rendering |

Plotting functions return `PIL.Image.Image`. They accept `window_size`,
`tile_provider`, and an optional existing `context`. Points, lines, circles,
GeoJSON, and GeoPandas functions also accept `zoom` (an adjustment) and
`set_zoom` (an explicit override).

## What's changed in 0.4.2

- Correct circle radii: 1,000 meters now renders as one kilometer.
- Correct coordinate flipping for batch lines and polygons.
- Preserve every part of multipart geometries and transparent polygon holes.
- Support nested geometry collections, null properties, and positions with altitude.
- Fix GeoDataFrame indexes, palettes, selected geometry columns, and projected CRS handling.
- Reject mismatched arrays and invalid coordinates with clear errors.
- Preserve fully transparent fills and avoid modifying global random state or Pillow on import.
- Exercise optional dependencies and validate release distributions in CI.

See [CHANGELOG.md](CHANGELOG.md) for release history.

## Development

```sh
git clone https://github.com/eddiethedean/landfall.git
cd landfall
python -m venv .venv
# Activate the environment, then:
pip install -e '.[dev,geo]'
pytest
ruff check src tests
ruff format --check src tests
mypy src

# Core tests across Python 3.8–3.13 (requires those interpreters):
tox -e py38,py39,py310,py311,py312,py313
# Optional integrations, quality checks, and release packaging:
tox -e geo,ruff,mypy,package
```

Tests use an offline tile downloader. The `geo` environment enforces at least
85% total coverage. Tox tests installed wheels. The `package` environment
builds the source distribution and wheel and checks their metadata with Twine.
Contributions should include regression tests for behavior changes and pass
the relevant environments above.

## License and support

MIT license; see [LICENSE](LICENSE). Report bugs through
[GitHub Issues](https://github.com/eddiethedean/landfall/issues).
