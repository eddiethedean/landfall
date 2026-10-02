"""Regression tests for errors that previously produced plausible but wrong maps."""

import random
import subprocess
import sys
import xml.etree.ElementTree as ET

import pytest
import staticmaps
from geographiclib.geodesic import Geodesic

import landfall
from landfall.circles import add_circle, add_circles
from landfall.color import convert_color, map_id_colors, process_colors
from landfall.geojson import extract_geometries, parse_geojson
from landfall.lines import add_line, add_lines
from landfall.plot import plot_fill_colors
from landfall.points import add_points, points_to_lats_lons
from landfall.polygons import add_polygon, add_polygons


def coordinate(point):
    return point.lat().degrees, point.lng().degrees


@pytest.mark.parametrize(
    "add,shape",
    [
        (add_lines, [(-82.49, 27.88), (-82.46, 27.92)]),
        (add_polygons, [(-82.49, 27.88), (-82.46, 27.92), (-82.44, 27.88)]),
    ],
)
def test_batch_flips_coordinates_once(mock_context, add, shape):
    add(mock_context, [shape], flip_coords=True)
    assert coordinate(mock_context._objects[0]._latlngs[0]) == pytest.approx(
        (27.88, -82.49)
    )


def test_point_pairs_and_flip(mock_context):
    add_points(mock_context, [(-82.49, 27.88), (-82.46, 27.92)], flip_coords=True)
    assert [coordinate(obj.latlng()) for obj in mock_context._objects] == pytest.approx(
        [(27.88, -82.49), (27.92, -82.46)]
    )
    assert points_to_lats_lons([]) == ([], [])


@pytest.mark.parametrize("points", [[27.88, 27.92], [(27.88,)], [(27.88, -82.49, 3)]])
def test_invalid_point_pairs(points, mock_context):
    with pytest.raises(ValueError, match="pairs"):
        add_points(mock_context, points)
    assert not mock_context._objects


@pytest.mark.parametrize(
    "add,args",
    [
        (add_points, ([1, 2], [1])),
        (add_circles, ([1, 2], [1, 2], [100])),
        (add_circles, ([1], [1, 2], [100])),
    ],
)
def test_mismatched_coordinate_lengths_fail_before_adding(mock_context, add, args):
    with pytest.raises(ValueError, match="same length"):
        add(mock_context, *args)
    assert not mock_context._objects


@pytest.mark.parametrize(
    "add,args",
    [
        (add_points, ([27, 28], [-82, -83])),
        (add_lines, ([[(27, -82), (28, -83)]] * 2,)),
        (add_polygons, ([[(27, -82), (28, -83), (28, -82)]] * 2,)),
        (add_circles, ([27, 28], [-82, -83], [100, 200])),
    ],
)
def test_one_color_applies_to_every_object(mock_context, add, args):
    add(mock_context, *args, colors=["green"])
    assert len(mock_context._objects) == 2
    assert all(obj.color().int_rgb() == (0, 255, 0) for obj in mock_context._objects)


@pytest.mark.parametrize(
    "colors,count", [([], 1), (["red", "blue"], 3), (["red", "blue"], 1)]
)
def test_short_or_excess_color_lists_are_rejected(colors, count):
    with pytest.raises(ValueError, match="one color or match"):
        process_colors(colors, count)


def test_ids_length_is_validated(mock_context):
    with pytest.raises(ValueError, match="ids must match"):
        add_points(mock_context, [27, 28], [-82, -83], ids=["a"], id_colors="wheel")
    assert not mock_context._objects


def test_fill_alpha_zero_is_preserved(mock_context):
    add_polygons(mock_context, [[(27, -82), (28, -83), (28, -82)]], fill_transparency=0)
    assert mock_context._objects[0].fill_color().int_rgba()[3] == 0
    assert (
        plot_fill_colors(1, [staticmaps.RED], fill_same=True, fill_transparency=0)[
            0
        ].int_rgba()[3]
        == 0
    )


def test_color_randomness_is_local_and_reproducible():
    state = random.getstate()
    colors = process_colors("random", 5, rng=42)
    assert len({color.int_rgb() for color in colors}) == 5
    assert [color.int_rgb() for color in colors] == [
        color.int_rgb() for color in process_colors("random", 5, rng=42)
    ]
    landfall.random_color(42)
    assert random.getstate() == state


def test_id_palette_uses_first_seen_unique_ids():
    palette = map_id_colors(["b", "a", "b", "c"], "wheel")
    assert list(palette) == ["b", "a", "c"]
    assert [c.int_rgb() for c in palette.values()] == [
        c.int_rgb() for c in process_colors("wheel", 3)
    ]


@pytest.mark.parametrize("value", [None, 5, object()])
def test_invalid_color_types_give_value_error(value):
    with pytest.raises(ValueError, match="convert_color requires"):
        convert_color(value)


@pytest.mark.parametrize("radius,unit", [(1000, "meters"), (1, "kilometers")])
def test_circle_radius_matches_geodesic_distance(mock_context, radius, unit):
    add_circle(mock_context, 27.88, -82.49, radius, radius_unit=unit)
    point = mock_context._objects[0]._latlngs[0]
    distance = Geodesic.WGS84.Inverse(27.88, -82.49, *coordinate(point))["s12"]
    assert distance == pytest.approx(1000, rel=1e-6)


@pytest.mark.parametrize("radius", [-1, float("nan"), float("inf")])
def test_invalid_radius(mock_context, radius):
    with pytest.raises(ValueError, match="finite and non-negative"):
        add_circle(mock_context, 27.88, -82.49, radius)


@pytest.mark.parametrize(
    "coords", [(91, 0), (0, 181), (float("nan"), 0), (0, float("inf")), ("27", -82)]
)
@pytest.mark.parametrize("kind", ["point", "line", "polygon", "circle"])
def test_invalid_coordinates_raise_value_error(mock_context, coords, kind):
    with pytest.raises(ValueError, match="coordinates must be finite"):
        if kind == "point":
            mock_context.add_point(*coords)
        elif kind == "line":
            add_line(mock_context, [coords, (27, -82)])
        elif kind == "polygon":
            add_polygon(mock_context, [coords, (27, -82), (28, -82)])
        else:
            add_circle(mock_context, *coords, 100)


def test_context_single_shape_defaults_accept_color_names(mock_context):
    mock_context.add_line([(27, -82), (28, -82)], color="green")
    mock_context.add_polygon([(27, -82), (28, -82), (28, -83)], fill_color="blue")
    mock_context.add_circle(27, -82, 100, fill_color="yellow")
    assert len(mock_context._objects) == 3
    polygon = mock_context._objects[1]
    assert coordinate(polygon._latlngs[0]) == coordinate(polygon._latlngs[-1])
    mock_context.render_pillow(300, 300)


@pytest.mark.parametrize("data", ["null", "123", "[]", '"Point"'])
def test_geojson_root_must_be_object(data):
    with pytest.raises(ValueError, match="must be an object"):
        parse_geojson(data)


def test_null_properties_altitude_and_nested_collections(mock_context):
    data = {
        "type": "Feature",
        "properties": None,
        "geometry": {
            "type": "GeometryCollection",
            "geometries": [
                {"type": "Point", "coordinates": [-82.49, 27.88, 10]},
                {
                    "type": "GeometryCollection",
                    "geometries": [
                        {
                            "type": "MultiPoint",
                            "coordinates": [[-82.46, 27.92, 20], [-82.44, 27.94, 30]],
                        }
                    ],
                },
            ],
        },
    }
    image = landfall.plot_geojson(data, context=mock_context)
    assert image.size == (500, 400)
    assert len(mock_context._objects) == 3
    assert coordinate(mock_context._objects[-1].latlng()) == pytest.approx(
        (27.94, -82.44)
    )


@pytest.mark.parametrize(
    "data",
    [
        {"type": "Feature", "geometry": {}, "properties": []},
        {"type": "FeatureCollection", "features": {}},
        {"type": "GeometryCollection", "geometries": None},
        {
            "type": "FeatureCollection",
            "features": [{"type": "Point", "coordinates": [0, 0]}],
        },
        {"type": "Feature", "geometry": {"type": "Feature", "geometry": None}},
        {
            "type": "GeometryCollection",
            "geometries": [{"type": "Feature", "geometry": None}],
        },
    ],
)
def test_malformed_geojson_structures(data):
    with pytest.raises(ValueError):
        extract_geometries(data)


def donut():
    return [
        [[-0.1, -0.1], [0.1, -0.1], [0.1, 0.1], [-0.1, 0.1], [-0.1, -0.1]],
        [[-0.03, -0.03], [-0.03, 0.03], [0.03, 0.03], [0.03, -0.03], [-0.03, -0.03]],
    ]


def test_polygon_holes_preserve_background_and_underlying_objects(mock_context):
    mock_context.set_background_color(staticmaps.WHITE)
    mock_context.add_polygon(
        [(-0.02, -0.02), (-0.02, 0.02), (0.02, 0.02), (0.02, -0.02)],
        fill_color="blue",
        width=0,
    )
    feature = {
        "type": "Feature",
        "geometry": {"type": "Polygon", "coordinates": donut()},
        "properties": {
            "fill": "green",
            "stroke": "red",
            "fill-opacity": 1,
            "stroke-width": 0,
        },
    }
    image = landfall.plot_geojson(
        feature, context=mock_context, set_zoom=11, window_size=(400, 400)
    )
    assert image.getpixel((200, 200)) == (0, 0, 255, 255)
    assert image.getpixel((290, 200)) == (0, 255, 0, 255)
    assert len(mock_context._objects) == 2
    svg = mock_context.render_svg(400, 400).tostring()
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert any(
        path.attrib.get("fill-rule") == "evenodd" and path.attrib["d"].count("M") == 2
        for path in paths
    )


@pytest.mark.parametrize(
    "kind,coords,expected",
    [
        ("MultiPoint", [[-82, 27], [-82.1, 27.1], [-82.2, 27.2]], 3),
        (
            "MultiLineString",
            [[[-82, 27], [-82.1, 27.1]], [[-82.2, 27.2], [-82.3, 27.3]]],
            2,
        ),
        ("MultiPolygon", [donut(), donut()], 2),
    ],
)
def test_geojson_all_parts_are_added(mock_context, kind, coords, expected):
    landfall.plot_geojson({"type": kind, "coordinates": coords}, context=mock_context)
    assert len(mock_context._objects) == expected


def test_import_does_not_patch_pillow_or_load_geopandas():
    result = subprocess.run(
        [
            sys.executable,
            "-W",
            "error",
            "-c",
            'import sys; from PIL import ImageDraw; before = hasattr(ImageDraw.ImageDraw, "textsize"); '
            'import landfall; assert hasattr(ImageDraw.ImageDraw, "textsize") == before; '
            'assert "geopandas" not in sys.modules; assert landfall.__version__ == "0.4.2"',
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_version_matches_installed_distribution():
    from importlib.metadata import version

    assert landfall.__version__ == version("landfall")


def test_combined_plot_flips_points_and_polygons(monkeypatch, mock_context):
    from landfall import combos

    monkeypatch.setattr(combos, "Context", lambda: mock_context)
    image = combos.plot_points_and_polygons(
        [(-82.49, 27.88)],
        [[(-82.49, 27.88), (-82.46, 27.92), (-82.44, 27.88)]],
        flip_coords=True,
    )
    assert image.size == (800, 600)
    assert coordinate(mock_context._objects[0]._latlngs[0]) == pytest.approx(
        (27.88, -82.49)
    )
    assert coordinate(mock_context._objects[1].latlng()) == pytest.approx(
        (27.88, -82.49)
    )


def test_tuple_plot_wrapper(mock_context):
    from landfall.points import plot_points_tuples

    image = plot_points_tuples([(27.88, -82.49), (27.92, -82.46)], context=mock_context)
    assert image.size == (500, 400)
    assert len(mock_context._objects) == 2


def test_missing_optional_dependency_is_actionable(monkeypatch, mock_context):
    import builtins

    original_import = builtins.__import__

    def without_geopandas(name, *args, **kwargs):
        if name == "geopandas":
            raise ImportError("not installed")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", without_geopandas)
    with pytest.raises(ImportError, match=r"pip install landfall\[geo\]"):
        landfall.plot_geometries([], context=mock_context)


def test_legacy_pillow_helper_is_explicit_and_idempotent(monkeypatch):
    from types import SimpleNamespace

    from PIL import Image, ImageDraw

    from landfall import compatibility

    class LegacyDrawing(ImageDraw.ImageDraw):
        pass

    monkeypatch.setattr(
        compatibility, "ImageDraw", SimpleNamespace(ImageDraw=LegacyDrawing)
    )
    compatibility.apply_compatibility_patches()
    method = LegacyDrawing.textsize
    compatibility.apply_compatibility_patches()
    assert LegacyDrawing.textsize is method
    drawing = LegacyDrawing(Image.new("RGB", (100, 100)))
    width, height = drawing.textsize("Landfall")
    assert width > 0 and height > 0
    assert not hasattr(ImageDraw.ImageDraw, "textsize")


def test_invalid_geojson_fill_opacity(mock_context):
    feature = {
        "type": "Feature",
        "geometry": {"type": "Polygon", "coordinates": donut()},
        "properties": {"fill-opacity": 2},
    }
    with pytest.raises(ValueError, match="fill-opacity"):
        landfall.plot_geojson(feature, context=mock_context)


@pytest.mark.parametrize("width", [0, 2])
def test_cairo_polygon_holes_preserve_background(mock_context, width):
    from PIL import Image

    pytest.importorskip("cairo")
    mock_context.set_background_color(staticmaps.WHITE)
    rings = [[(lat, lon) for lon, lat in ring] for ring in donut()]
    mock_context.add_polygon(rings[0], holes=rings[1:], fill_color="green", width=width)
    mock_context.set_center(staticmaps.create_latlng(0, 0))
    mock_context.set_zoom(11)
    surface = mock_context.render_cairo(400, 400)
    surface.flush()
    image = Image.frombuffer(
        "RGBA",
        (400, 400),
        bytes(surface.get_data()),
        "raw",
        "BGRA",
        surface.get_stride(),
        1,
    )
    assert image.getpixel((200, 200)) == (255, 255, 255, 255)
    assert image.getpixel((290, 200)) == (0, 255, 0, 255)


@pytest.mark.parametrize(
    "kind,coords",
    [
        ("LineString", [[0], [1, 2]]),
        ("MultiLineString", [None]),
        ("Polygon", [None]),
        ("Polygon", [[[0], [1, 2], [2, 3]]]),
        ("MultiPolygon", [None]),
    ],
)
def test_malformed_nested_positions_raise_value_error(mock_context, kind, coords):
    with pytest.raises(ValueError, match="coordinates|positions"):
        landfall.plot_geojson(
            {"type": kind, "coordinates": coords}, context=mock_context
        )
