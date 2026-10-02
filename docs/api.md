# API reference

[Documentation index](README.md) · [Getting started](getting-started.md)

The names below are exported by `import landfall`. All `plot_*` functions
return `PIL.Image.Image`. `Context` holds shapes for a combined map and can
render Pillow or SVG output. Examples and pictures are in
[shapes and styling](shapes-and-styling.md) and
[geospatial data](geospatial-data.md).

<div class="lf-card-grid" markdown="1">
<div class="lf-card" markdown="1">

<p class="lf-card__title">Core plotting</p>

Points, lines, polygons, and circles are available after `pip install landfall`.

</div>
<div class="lf-card" markdown="1">

<p class="lf-card__title">GIS inputs</p>

GeoJSON is built in. Shapely and GeoPandas functions use the `landfall[geo]`
extra.

</div>
<div class="lf-card" markdown="1">

<p class="lf-card__title">Combined maps</p>

Use `Context` to layer different shape types and export Pillow or SVG output.

</div>
</div>

!!! note "Function names are import-ready"
    The table lists names from `landfall.*`, so you can call them directly
    after `import landfall`.

## Choose a function

| Function | Required input | Main options |
| --- | --- | --- |
| `plot_points(latitudes, longitudes=None)` | Two coordinate arrays, or `(lat, lon)` pairs | `colors`, `ids`, `id_colors`, `point_size`, `color`, `flip_coords` |
| `plot_points_data(data, latitude_name, longitude_name)` | Mapping with named coordinate arrays | `color_name`, `ids_name`, `id_colors`, `colors`, `point_size` |
| `plot_line(line)` | One sequence of `(lat, lon)` pairs | `color`, `width`, `flip_coords` |
| `plot_lines(lines)` | Sequence of lines | `colors`, `ids`, `id_colors`, `width`, `flip_coords` |
| `plot_polygon(polygon)` | One sequence of at least three `(lat, lon)` pairs | `color`, `fill_color`, `width`, `flip_coords` |
| `plot_polygons(polygons)` | Sequence of polygons | `colors`, `fill_colors`, `fill_same`, `fill_transparency`, `ids`, `id_colors`, `id_fill_colors` |
| `plot_circle(latitude, longitude, radius)` | Center and radius | `color`, `fill_color`, `width`, `radius_unit`, `flip_coords` |
| `plot_circles(latitudes, longitudes, radii)` | Equal-length arrays of centers and radii | `colors`, `fill_colors`, `fill_same`, `fill_transparency`, `ids`, `id_colors`, `id_fill_colors`, `radius_unit` |
| `plot_geojson(geojson_data)` | GeoJSON dictionary or JSON string | `zoom`, `set_zoom` |
| `plot_geojson_file(filepath)` | UTF-8 GeoJSON file path | `zoom`, `set_zoom` |
| `plot_geometry(geometry)` | One Shapely geometry | `zoom`, `set_zoom` |
| `plot_geometries(geometries)` | Sequence of Shapely geometries | `colors`, `zoom`, `set_zoom` |
| `plot_geodataframe(gdf)` | GeoDataFrame | `geometry_column`, `color_column`, `size_column`, `colors`, `zoom`, `set_zoom` |

`plot_geometry`, `plot_geometries`, and `plot_geodataframe` require the
`landfall[geo]` extra. Their imports are available without it, but calling
them raises a helpful `ImportError`.
For `plot_geometries` and `plot_geodataframe`, `colors="red"` applies that
literal color to every geometry; the palette names `"distinct"`, `"random"`,
and `"wheel"` generate palettes.

## Shared plotting options

All `plot_*` functions accept:

| Option | Default | Meaning |
| --- | --- | --- |
| `tile_provider` | OpenStreetMap provider | A py-staticmaps tile provider |
| `window_size` | `(500, 400)` | Output `(width, height)` in pixels |
| `context` | `None` | Existing py-staticmaps or Landfall context to add shapes to |

Points, lines, circles, GeoJSON, and GeoPandas/Shapely functions also accept
`zoom=0` (offset from the automatically determined zoom) and `set_zoom=None`
(an explicit zoom override). The polygon plotting functions do not accept
these zoom options. Rendering may download tiles from the selected provider.

## Coordinates and sizing

Native point pairs, line vertices, polygon vertices, and circle centers are
`(latitude, longitude)`. Use `flip_coords=True` for native inputs supplied as
`(longitude, latitude)`. GeoJSON and Shapely already use longitude first;
do not flip them. `plot_points_data` uses the columns named by
`latitude_name` and `longitude_name`. All coordinates must be finite and in
their valid geographic ranges.

`point_size` defaults to 10 pixels. Line and border `width` defaults to 2
pixels. `radius_unit` is `"meters"` by default and can be `"kilometers"`.
Radius values must be finite and non-negative. Native polygon rings close
automatically; add holes through `Context.add_polygon(..., holes=[ring, ...])`
or through GeoJSON/Shapely polygons.

## Colors and grouping

The singular `color` and `fill_color` options take a color name, hex string,
RGB/RGBA tuple, or `staticmaps.Color`. Batch `colors` and `fill_colors` take
a sequence of these values or one of `"distinct"`, `"random"`, `"wheel"`.
One color in a sequence broadcasts to every object. Otherwise, the number
of colors must equal the number of objects. For a single named color on a
batch, use `color="red"` or `colors=["red"]`, not `colors="red"`.

`ids` assigns a group to each object. `id_colors` maps each ID to a color or
uses a palette name to generate a color per unique ID. It requires `ids` to
have the same length as the objects and takes precedence over `colors`.
For batch polygons and circles, `id_fill_colors` does the same for fills.
`fill_same=True` copies border colors into fills. `fill_transparency` replaces
fill alpha with a value from 0 to 255; 0 means fully transparent.

`plot_points_data` accepts `color_name` for a column of literal colors,
`ids_name` for a grouping column, and `colors` for a palette name when no
color column is supplied. `color_name` takes precedence over `colors`.

## `Context`

`landfall.Context` extends `staticmaps.Context` with:

| Method | Input |
| --- | --- |
| `add_point`, `add_points` | One point or arrays/pairs of points |
| `add_line`, `add_lines` | One line or a sequence of lines |
| `add_polygon`, `add_polygons` | One polygon or a sequence of polygons |
| `add_circle`, `add_circles` | One circle or arrays of circles |

`Context.add_polygon` supports `holes`, a sequence of interior rings. Use
py-staticmaps methods such as `set_tile_provider`, `set_zoom`,
`render_pillow(width, height)`, and `render_svg(width, height)` to control
output. `render_svg` returns a drawing whose `saveas(path)` method writes an
SVG file.

## `random_color(rng=None)`

Returns a `staticmaps.Color`. Pass an integer seed as `rng` for a reproducible
result. Calling it does not change Python's global random state.
