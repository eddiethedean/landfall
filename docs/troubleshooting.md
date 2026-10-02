# Troubleshooting

[Documentation index](README.md) · [API reference](api.md)

Most plotting problems come down to one of three things: coordinate order,
tile access, or an optional package installed into a different environment.
Use this table to get from symptom to the next check quickly.

| Symptom | What to check |
| --- | --- |
| The marker appears in the wrong place | Native pairs use `(latitude, longitude)`; GeoJSON and Shapely use `(longitude, latitude)`. Use `flip_coords=True` only for native inputs supplied longitude first. |
| Tiles fail to download or appear blank | The default OpenStreetMap provider needs network access. Check connectivity, provider availability, and tile-provider terms. Pass another py-staticmaps provider with `tile_provider` if needed. |
| `ImportError: GeoPandas not installed` | Install `landfall[geo]` in the same Python environment that runs your script. |
| `ValueError` about array lengths or colors | Separate latitude/longitude/radius arrays and `ids` must match object count. `colors` must be a palette name, one color in a list, or one color per object. |
| `ValueError` about coordinates or radius | Latitude must be −90..90, longitude −180..180; values must be finite. Circle radii must be finite and non-negative. |
| An empty GeoJSON or geometry list cannot render | Supply at least one plottable geometry; null and empty geometries are skipped. |
| A GeoDataFrame plots in an unexpected location | Set its CRS before plotting so Landfall can reproject to WGS84. Without a CRS, values are treated as WGS84 longitude/latitude. |
| A circle is much larger or smaller than intended | Radius defaults to meters. Pass `radius_unit="kilometers"` only if your radius values are kilometers. |
| SVG output is needed | Add shapes to `landfall.Context`, then call `context.render_svg(width, height).saveas("map.svg")`. |

If the issue persists, open a [GitHub issue](https://github.com/eddiethedean/landfall/issues)
with a small runnable example, Python and Landfall versions, and the full error.
