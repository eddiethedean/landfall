<section class="lf-hero" markdown="1">
<div class="lf-hero__copy" markdown="1">

<p class="lf-kicker">Landfall · Python map plotting</p>

# Maps from the data you already have

Turn coordinates, GeoJSON, Shapely shapes, and GeoDataFrames into clear static
maps. Start with a few points, then add routes, boundaries, and layers as your
project grows.

[Make your first map →](getting-started.md){ .lf-button }
[Explore the examples](shapes-and-styling.md){ .lf-button .lf-button--quiet }

</div>
<div class="lf-hero__visual" markdown="1">

![Three points plotted across Tampa Bay](images/points.png)

</div>
</section>

## Find your path

<div class="lf-card-grid" markdown="1">
<div class="lf-card" markdown="1">
<span class="lf-card__label">01 · Start here</span>

<p class="lf-card__title">Build a first map</p>

Install Landfall, learn coordinate order, and save your first Pillow image.

[Open the quick start →](getting-started.md)
</div>
<div class="lf-card" markdown="1">
<span class="lf-card__label">02 · Style it</span>

<p class="lf-card__title">Add shape and meaning</p>

Explore route styling, translucent polygons, circles, color groups, and layers.

[Browse shapes and styling →](shapes-and-styling.md)
</div>
<div class="lf-card" markdown="1">
<span class="lf-card__label">03 · Bring your data</span>

<p class="lf-card__title">Plot geospatial files</p>

Read GeoJSON, reproject GeoDataFrames, or plot Shapely geometry directly.

[Work with geospatial data →](geospatial-data.md)
</div>
</div>

Need a different basemap? See [how to connect a custom tile service](custom-tile-service.md)
and render it behind Landfall's shapes. For specialized objects or advanced
rendering, see the [py-staticmaps interoperability guide](py-staticmaps.md) to
use the native API directly through `landfall.Context`.

Working with point observations and want geohash or H3 heat layers? See the
[Heatfall documentation](https://heatfall.readthedocs.io/en/latest/index.html)
for gridding, styling, and combining heat cells with Landfall shapes.

## A few things you can make

These examples use real OpenStreetMap tiles and the same public API described
in the guides.

<div class="lf-image-grid" markdown="1">
<div markdown="1">

![Colored point markers over Tampa Bay](images/points.png)
<span class="lf-image-caption">Plot coordinate pairs with a generated palette.</span>

</div>
<div markdown="1">

![A red route across Tampa Bay](images/route.png)
<span class="lf-image-caption">Give a route a clear color and line weight.</span>

</div>
<div markdown="1">

![A translucent coverage circle on the map](images/circle.png)
<span class="lf-image-caption">Show distance or coverage with a radius in meters.</span>

</div>
</div>

## Learn by running an example

The examples share a small set of Tampa Bay coordinates, so you can compare
the output while changing one option at a time.

<div class="lf-card-grid" markdown="1">
<div class="lf-card" markdown="1">

<p class="lf-card__title">Public API reference</p>

Find function choices, parameter defaults, coordinate rules, and `Context`
methods.

[Look up an option →](api.md)
</div>
<div class="lf-card" markdown="1">

<p class="lf-card__title">py-staticmaps interoperability</p>

Use native map objects, tile providers, context controls, and renderers with
Landfall's `Context`.

[Go beyond the helpers →](py-staticmaps.md)
</div>
<div class="lf-card" markdown="1">

<p class="lf-card__title">Jupyter notebooks</p>

Run the [points notebook](https://github.com/eddiethedean/landfall/blob/main/examples/plot_points_function.ipynb),
[lines notebook](https://github.com/eddiethedean/landfall/blob/main/examples/plot_lines_function.ipynb),
or [polygons notebook](https://github.com/eddiethedean/landfall/blob/main/examples/plot_polygons_function.ipynb).

</div>
<div class="lf-card" markdown="1">

<p class="lf-card__title">Need a hand?</p>

Check common tile, input, and optional dependency issues before opening an issue.

[Troubleshoot a map →](troubleshooting.md)
</div>
</div>

!!! tip "One coordinate rule to remember"
    Landfall's native points use `(latitude, longitude)`. GeoJSON and Shapely
    use `(longitude, latitude)`; Landfall converts those formats for you.

See the [repository README](https://github.com/eddiethedean/landfall#readme)
for a concise overview and the
[changelog](https://github.com/eddiethedean/landfall/blob/main/CHANGELOG.md)
for release history.
