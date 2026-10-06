# Getting started

[Documentation index](README.md) · [API reference](api.md)

Install Landfall with Python 3.8–3.13:

```sh
python -m pip install landfall
```

The default map uses OpenStreetMap tiles, so rendering needs network access.
Tile usage is subject to the provider's terms. To use another py-staticmaps
provider, pass it as `tile_provider` to a plotting function or set it on a
`Context`. See [how to configure a custom tile service](custom-tile-service.md)
for URL templates, API keys, and a rendered example.
Landfall builds on py-staticmaps and keeps its native context API available;
see [using the full py-staticmaps API](py-staticmaps.md) for custom objects,
advanced context controls, and renderer choices.

!!! info "What you get"
    Every `plot_*` call returns a Pillow image. Landfall handles the map
    framing and tile composition; you decide what to draw and where to save it.

## Plot and save your first map

```python
import landfall

places = [
    (27.88, -82.49),
    (27.92, -82.46),
    (27.94, -82.44),
]
image = landfall.plot_points(
    places, colors="distinct", point_size=14, window_size=(640, 440), zoom=-1
)
image.save("places.png")
```

![Three differently colored points rendered on a real map](images/points.png)

`image` is a Pillow `Image`. You can display it in a notebook by leaving
`image` as the last expression in a cell, or save it in any format Pillow
supports. `window_size` is `(width, height)` in pixels and defaults to
`(500, 400)`.

## Coordinate order

!!! warning "Native pairs start with latitude"
    Landfall's native pair format is `(latitude, longitude)`. GeoJSON and
    Shapely use the reverse order, `(longitude, latitude)`.

| Input | Order | Example for Tampa |
| --- | --- | --- |
| Landfall coordinate pair | `(latitude, longitude)` | `(27.88, -82.49)` |
| Landfall separate arrays | latitudes, then longitudes | `[27.88], [-82.49]` |
| GeoJSON or Shapely | `(longitude, latitude)` | `[-82.49, 27.88]` |

Landfall converts GeoJSON and Shapely positions automatically. If a native
point, line, polygon, or circle input is already in longitude/latitude order,
pass `flip_coords=True`. For example:

```python
image = landfall.plot_points(
    [(-82.49, 27.88), (-82.46, 27.92)],
    flip_coords=True,
)
```

Coordinates must be finite; latitude must be between −90 and 90, longitude
between −180 and 180. Swapping coordinates can still produce a valid but
incorrect location, so check the order before plotting.

## Choose a workflow

<div class="lf-card-grid" markdown="1">
<div class="lf-card" markdown="1">

<p class="lf-card__title">Draw shapes</p>

Build routes, boundaries, circles, and multi-layer maps.

[See shape examples →](shapes-and-styling.md)
</div>
<div class="lf-card" markdown="1">

<p class="lf-card__title">Use existing GIS data</p>

Plot GeoJSON, Shapely, or GeoPandas, including projected data.

[Open the geospatial guide →](geospatial-data.md)
</div>
<div class="lf-card" markdown="1">

<p class="lf-card__title">Find exact options</p>

Compare public functions, shared arguments, and defaults.

[Browse the API →](api.md)
</div>
</div>
