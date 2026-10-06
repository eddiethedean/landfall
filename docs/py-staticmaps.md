# py-staticmaps interoperability

[Documentation index](README.md) · [API reference](api.md) ·
[Custom tile services](custom-tile-service.md)

Landfall is built on [py-staticmaps](https://github.com/flopp/py-staticmaps),
created by Florian Pigorsch. The library handles map framing, tile composition,
and Pillow, SVG, and optional Cairo rendering. Landfall adds convenient
functions for common geographic inputs while keeping the native
py-staticmaps API available.

`landfall.Context` subclasses `staticmaps.Context`. You can pass it anywhere a
py-staticmaps context is accepted, configure it with py-staticmaps methods, and
add any native py-staticmaps map object with `add_object`. Landfall's helpers
cover common points, lines, polygons, and circles; they do not limit which
objects or context features you can use.

## Add native map objects

For example, use py-staticmaps' `ImageMarker` alongside Landfall shapes. It
places a PNG at a geographic coordinate; `origin_x` and `origin_y` locate the
anchor point within the image.

```python
import landfall
import staticmaps

context = landfall.Context()
context.add_line([(27.88, -82.49), (27.92, -82.46)], color="#d12c31", width=4)
context.add_object(
    staticmaps.ImageMarker(
        staticmaps.create_latlng(27.88, -82.49),
        "harbor-pin.png",
        origin_x=16,
        origin_y=32,
    )
)
context.render_pillow(640, 440).save("harbor.png")
```

Native objects include `staticmaps.Marker`, `ImageMarker`, `Line`, `Area`, and
`Circle`. You can also implement a custom `staticmaps.Object` and add it with
`context.add_object(...)`. A custom object supplies geographic bounds and
pixel padding, plus a rendering method for each output format you want to
support.

## Configure the underlying context

Use py-staticmaps controls directly for a fixed center and zoom, tile cache,
provider, downloader, geographic bounds, and pixel padding. `add_bounds` takes
an `s2sphere.LatLngRect`.

```python
import landfall
import s2sphere
import staticmaps

context = landfall.Context()
context.set_tile_provider(staticmaps.tile_provider_CartoDark)
context.set_cache_dir("./map-tile-cache")
context.set_center(staticmaps.create_latlng(27.91, -82.47))
context.set_zoom(12)
context.add_bounds(
    s2sphere.LatLngRect.from_point_pair(
        staticmaps.create_latlng(27.85, -82.55),
        staticmaps.create_latlng(27.97, -82.39),
    ),
    extra_pixel_bounds=(16, 16, 16, 16),
)
context.add_points([(27.88, -82.49), (27.92, -82.46)], colors="distinct")
context.render_pillow(640, 440).save("bounded-map.png")
```

The [custom tile service guide](custom-tile-service.md) shows custom URL
templates, keyed providers, and provider attribution. py-staticmaps also
provides several built-in tile providers; use any provider exposed by your
installed version.

## Choose a renderer

Render the same context to Pillow or SVG with the base installation. Cairo
produces anti-aliased PNG output and is available after installing the
`cairo` extra and the system Cairo library.

```python
context.render_pillow(640, 440).save("map.png")
context.render_svg(640, 440).saveas("map.svg")
context.render_cairo(640, 440).write_to_png("map-antialiased.png")
```

`landfall.Context.save()` provides the same exports through one method. It
infers Pillow for `.png` and SVG for `.svg`; select Cairo explicitly when the
`cairo` extra and system Cairo library are installed. Width and height are in
pixels. The method returns `None`.

```python
context.save("map.png", 640, 440)
context.save("map.svg", 640, 440)
context.save("map-antialiased.png", 640, 440, renderer="cairo")
```

The explicit renderer must match the output extension: Pillow and Cairo write
PNG, while SVG writes SVG. The method dispatches to the context instance's
`render_pillow()`, `render_svg()`, or `render_cairo()` method, preserving
rendering hooks supplied by subclasses. For example, a Pillow hook can
decorate the rendered image before saving:

```python
from PIL import ImageDraw


class LabeledContext(landfall.Context):
    def render_pillow(self, width, height):
        image = super().render_pillow(width, height)
        ImageDraw.Draw(image).text((8, 8), "Example", fill="red")
        return image


LabeledContext().save("labeled.png", 640, 440)
```

```sh
python -m pip install 'landfall[cairo]'
```

See the [py-staticmaps project](https://github.com/flopp/py-staticmaps) for
its full API, current features, and upstream documentation. py-staticmaps is
MIT licensed; see its [license](https://github.com/flopp/py-staticmaps/blob/master/LICENSE).
