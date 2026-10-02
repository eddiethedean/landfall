"""
Test GeoPandas integration functionality.
"""

import pytest
from PIL import Image

from tests.mock_tile_downloader import MockTileDownloader

# Skip tests if geopandas is not available
geopandas = pytest.importorskip("geopandas")
shapely = pytest.importorskip("shapely")


@pytest.fixture
def mock_context():
    """Create a context with mock tile downloader for testing."""
    from landfall.context import Context

    context = Context()
    context.set_tile_downloader(MockTileDownloader())
    return context


@pytest.fixture
def sample_point_geometry():
    """Sample Point geometry."""
    return shapely.geometry.Point(-82.49, 27.88)


@pytest.fixture
def sample_linestring_geometry():
    """Sample LineString geometry."""
    return shapely.geometry.LineString(
        [(-82.49, 27.88), (-82.46, 27.92), (-82.44, 27.96)]
    )


@pytest.fixture
def sample_polygon_geometry():
    """Sample Polygon geometry."""
    return shapely.geometry.Polygon(
        [
            (-82.49, 27.88),
            (-82.46, 27.88),
            (-82.46, 27.92),
            (-82.49, 27.92),
            (-82.49, 27.88),
        ]
    )


@pytest.fixture
def sample_geodataframe():
    """Sample GeoDataFrame."""
    import pandas as pd  # noqa: F401
    from shapely.geometry import Point

    data = {
        "name": ["Point 1", "Point 2", "Point 3"],
        "value": [10, 20, 30],
        "color": ["red", "green", "blue"],
    }
    geometry = [Point(-82.49, 27.88), Point(-82.46, 27.92), Point(-82.44, 27.96)]

    return geopandas.GeoDataFrame(data, geometry=geometry)


@pytest.fixture
def sample_mixed_geodataframe():
    """Sample GeoDataFrame with mixed geometry types."""
    from shapely.geometry import LineString, Point, Polygon

    data = {"name": ["Point", "Line", "Polygon"], "type": ["point", "line", "polygon"]}
    geometry = [
        Point(-82.49, 27.88),
        LineString([(-82.46, 27.92), (-82.44, 27.96)]),
        Polygon(
            [
                (-82.44, 27.96),
                (-82.41, 27.96),
                (-82.41, 28.00),
                (-82.44, 28.00),
                (-82.44, 27.96),
            ]
        ),
    ]

    return geopandas.GeoDataFrame(data, geometry=geometry)


class TestGeoPandasIntegration:
    """Test GeoPandas integration functionality."""

    def test_plot_geometry_point(self, mock_context, sample_point_geometry):
        """Test plotting Point geometry."""
        from landfall.geopandas_integration import plot_geometry

        img = plot_geometry(sample_point_geometry, context=mock_context)
        assert isinstance(img, Image.Image)
        assert img.size == (500, 400)

    def test_plot_geometry_linestring(self, mock_context, sample_linestring_geometry):
        """Test plotting LineString geometry."""
        from landfall.geopandas_integration import plot_geometry

        img = plot_geometry(sample_linestring_geometry, context=mock_context)
        assert isinstance(img, Image.Image)
        assert img.size == (500, 400)

    def test_plot_geometry_polygon(self, mock_context, sample_polygon_geometry):
        """Test plotting Polygon geometry."""
        from landfall.geopandas_integration import plot_geometry

        img = plot_geometry(sample_polygon_geometry, context=mock_context)
        assert isinstance(img, Image.Image)
        assert img.size == (500, 400)

    def test_plot_geometries_multiple(
        self, mock_context, sample_point_geometry, sample_linestring_geometry
    ):
        """Test plotting multiple geometries."""
        from landfall.geopandas_integration import plot_geometries

        geometries = [sample_point_geometry, sample_linestring_geometry]
        img = plot_geometries(geometries, context=mock_context)
        assert isinstance(img, Image.Image)
        assert img.size == (500, 400)

    def test_plot_geometries_with_colors(
        self, mock_context, sample_point_geometry, sample_linestring_geometry
    ):
        """Test plotting multiple geometries with colors."""
        from landfall.geopandas_integration import plot_geometries

        geometries = [sample_point_geometry, sample_linestring_geometry]
        colors = ["red", "blue"]
        img = plot_geometries(geometries, colors=colors, context=mock_context)
        assert isinstance(img, Image.Image)

    def test_plot_geodataframe_basic(self, mock_context, sample_geodataframe):
        """Test plotting basic GeoDataFrame."""
        from landfall.geopandas_integration import plot_geodataframe

        img = plot_geodataframe(sample_geodataframe, context=mock_context)
        assert isinstance(img, Image.Image)
        assert img.size == (500, 400)

    def test_plot_geodataframe_with_color_column(
        self, mock_context, sample_geodataframe
    ):
        """Test plotting GeoDataFrame with color column."""
        from landfall.geopandas_integration import plot_geodataframe

        img = plot_geodataframe(
            sample_geodataframe, color_column="color", context=mock_context
        )
        assert isinstance(img, Image.Image)

    def test_plot_geodataframe_with_size_column(
        self, mock_context, sample_geodataframe
    ):
        """Test plotting GeoDataFrame with size column."""
        from landfall.geopandas_integration import plot_geodataframe

        img = plot_geodataframe(
            sample_geodataframe, size_column="value", context=mock_context
        )
        assert isinstance(img, Image.Image)

    def test_plot_geodataframe_mixed_geometries(
        self, mock_context, sample_mixed_geodataframe
    ):
        """Test plotting GeoDataFrame with mixed geometry types."""
        from landfall.geopandas_integration import plot_geodataframe

        img = plot_geodataframe(sample_mixed_geodataframe, context=mock_context)
        assert isinstance(img, Image.Image)

    def test_plot_geodataframe_custom_size(self, mock_context, sample_geodataframe):
        """Test plotting GeoDataFrame with custom window size."""
        from landfall.geopandas_integration import plot_geodataframe

        img = plot_geodataframe(
            sample_geodataframe, window_size=(800, 600), context=mock_context
        )
        assert isinstance(img, Image.Image)
        assert img.size == (800, 600)

    def test_plot_geodataframe_with_colors(self, mock_context, sample_geodataframe):
        """Test plotting GeoDataFrame with custom colors."""
        from landfall.geopandas_integration import plot_geodataframe

        colors = ["red", "green", "blue"]
        img = plot_geodataframe(
            sample_geodataframe, colors=colors, context=mock_context
        )
        assert isinstance(img, Image.Image)

    def test_plot_geodataframe_color_string(self, mock_context, sample_geodataframe):
        """Test plotting GeoDataFrame with color string."""
        from landfall.geopandas_integration import plot_geodataframe

        img = plot_geodataframe(
            sample_geodataframe, colors="distinct", context=mock_context
        )
        assert isinstance(img, Image.Image)


class TestErrorHandling:
    """Test error handling for GeoPandas integration."""

    def test_plot_geometry_collection(self, mock_context):
        """Test plotting geometry collections."""
        from landfall.geopandas_integration import plot_geometry

        # Create a GeometryCollection
        geom_collection = shapely.geometry.GeometryCollection(
            [shapely.geometry.Point(-82.49, 27.88)]
        )

        img = plot_geometry(geom_collection, context=mock_context)
        assert isinstance(img, Image.Image)
        assert len(mock_context._objects) == 1

    def test_plot_geodataframe_no_geometry_column(self, mock_context):
        """Test plotting GeoDataFrame without geometry column."""
        import pandas as pd

        from landfall.geopandas_integration import plot_geodataframe

        # Create regular DataFrame without geometry
        df = pd.DataFrame({"name": ["A", "B"], "value": [1, 2]})
        gdf = geopandas.GeoDataFrame(df)

        with pytest.raises(ValueError, match="GeoDataFrame has no geometry column"):
            plot_geodataframe(gdf, context=mock_context)

    def test_plot_geodataframe_invalid_geometry_column(
        self, mock_context, sample_geodataframe
    ):
        """Test plotting GeoDataFrame with invalid geometry column name."""
        from landfall.geopandas_integration import plot_geodataframe

        with pytest.raises(ValueError, match="Geometry column 'invalid' not found"):
            plot_geodataframe(
                sample_geodataframe, geometry_column="invalid", context=mock_context
            )

    def test_plot_geodataframe_empty(self, mock_context):
        """Test plotting empty GeoDataFrame."""
        from landfall.geopandas_integration import plot_geodataframe

        # Create empty GeoDataFrame
        gdf = geopandas.GeoDataFrame()

        with pytest.raises(ValueError, match="GeoDataFrame has no geometry column"):
            plot_geodataframe(gdf, context=mock_context)


class TestEdgeCases:
    """Test edge cases for GeoPandas integration."""

    def test_plot_geometry_empty(self, mock_context):
        """Test plotting empty geometry."""
        from landfall.geopandas_integration import plot_geometry

        empty_point = shapely.geometry.Point()
        with pytest.raises(ValueError, match="No non-empty geometries"):
            plot_geometry(empty_point, context=mock_context)

    def test_plot_geodataframe_with_none_geometries(self, mock_context):
        """Test plotting GeoDataFrame with None geometries."""
        import pandas as pd  # noqa: F401
        from shapely.geometry import Point

        from landfall.geopandas_integration import plot_geodataframe

        data = {"name": ["A", "B"], "value": [1, 2]}
        geometry = [Point(-82.49, 27.88), None]  # One None geometry

        gdf = geopandas.GeoDataFrame(data, geometry=geometry)
        img = plot_geodataframe(gdf, context=mock_context)
        assert isinstance(img, Image.Image)

    def test_plot_geodataframe_invalid_color_column(
        self, mock_context, sample_geodataframe
    ):
        """Test plotting GeoDataFrame with invalid color column."""
        from landfall.geopandas_integration import plot_geodataframe

        # Should not raise error, just ignore invalid column
        img = plot_geodataframe(
            sample_geodataframe, color_column="invalid", context=mock_context
        )
        assert isinstance(img, Image.Image)

    def test_plot_geodataframe_invalid_size_column(
        self, mock_context, sample_geodataframe
    ):
        """Test plotting GeoDataFrame with invalid size column."""
        from landfall.geopandas_integration import plot_geodataframe

        # Should not raise error, just ignore invalid column
        img = plot_geodataframe(
            sample_geodataframe, size_column="invalid", context=mock_context
        )
        assert isinstance(img, Image.Image)


@pytest.mark.parametrize("index", [[10, 20, 30], ["a", "b", "c"], ["a", "a", "b"]])
def test_styles_follow_row_position(mock_context, sample_geodataframe, index):
    from landfall import plot_geodataframe

    sample_geodataframe.index = index
    plot_geodataframe(
        sample_geodataframe,
        color_column="color",
        size_column="value",
        context=mock_context,
    )
    assert [obj.color().int_rgb() for obj in mock_context._objects] == [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
    ]
    assert [obj.size() for obj in mock_context._objects] == [10, 20, 30]


def test_projected_crs_is_converted(mock_context, sample_geodataframe):
    from landfall import plot_geodataframe

    projected = sample_geodataframe.set_crs(epsg=4326).to_crs(epsg=3857)
    plot_geodataframe(projected, context=mock_context)
    point = mock_context._objects[0].latlng()
    assert (point.lat().degrees, point.lng().degrees) == pytest.approx((27.88, -82.49))
    assert projected.crs.to_epsg() == 3857


def test_selected_geometry_column_uses_its_own_crs(mock_context, sample_geodataframe):
    from landfall import plot_geodataframe

    sample_geodataframe["projected"] = sample_geodataframe.geometry.set_crs(
        epsg=4326
    ).to_crs(epsg=3857)
    plot_geodataframe(
        sample_geodataframe, geometry_column="projected", context=mock_context
    )
    point = mock_context._objects[0].latlng()
    assert (point.lat().degrees, point.lng().degrees) == pytest.approx((27.88, -82.49))


def test_multipoint_preserves_all_points(mock_context):
    from landfall import plot_geometry

    geometry = shapely.geometry.MultiPoint([(-82.49, 27.88), (-82.46, 27.92)])
    plot_geometry(geometry, context=mock_context)
    assert len(mock_context._objects) == 2


def test_geometries_palette_applies_to_every_part(mock_context):
    from landfall import plot_geometries

    geometries = [
        shapely.geometry.MultiPoint([(-82.49, 27.88), (-82.46, 27.92)]),
        shapely.geometry.MultiLineString(
            [[(-82.49, 27.88), (-82.46, 27.92)], [(-82.44, 27.94), (-82.40, 27.96)]]
        ),
    ]
    plot_geometries(geometries, colors=["green", "red"], context=mock_context)
    assert len(mock_context._objects) == 4
    assert [obj.color().int_rgb() for obj in mock_context._objects] == [
        (0, 255, 0)
    ] * 2 + [(255, 0, 0)] * 2


def test_geometry_helpers_accept_literal_color_strings(mock_context):
    from landfall import plot_geodataframe, plot_geometries

    points = [shapely.geometry.Point(-82, 27), shapely.geometry.Point(-83, 28)]
    plot_geometries(points, colors="red", context=mock_context)
    assert [obj.color().int_rgb() for obj in mock_context._objects] == [
        (255, 0, 0),
        (255, 0, 0),
    ]

    frame = geopandas.GeoDataFrame(geometry=points)
    mock_context._objects.clear()
    plot_geodataframe(frame, colors="red", context=mock_context)
    assert [obj.color().int_rgb() for obj in mock_context._objects] == [
        (255, 0, 0),
        (255, 0, 0),
    ]


def test_empty_geometry_rows_can_have_null_styles(mock_context):
    from landfall import plot_geodataframe, plot_geometries

    points = [shapely.geometry.Point(-82, 27), None, shapely.geometry.Point(-83, 28)]
    plot_geometries(points, colors=["red", None, "blue"], context=mock_context)
    assert [obj.color().int_rgb() for obj in mock_context._objects] == [
        (255, 0, 0),
        (0, 0, 255),
    ]

    frame = geopandas.GeoDataFrame(
        {"color": ["red", None, "blue"], "size": [10, None, 12]},
        geometry=points,
    )
    mock_context._objects.clear()
    plot_geodataframe(
        frame,
        color_column="color",
        size_column="size",
        context=mock_context,
    )
    assert [obj.color().int_rgb() for obj in mock_context._objects] == [
        (255, 0, 0),
        (0, 0, 255),
    ]
    assert [obj.size() for obj in mock_context._objects] == [10, 12]


def test_null_rows_keep_style_alignment(mock_context):
    from landfall import plot_geodataframe

    gdf = geopandas.GeoDataFrame(
        {"color": ["red", "green", "blue"]},
        geometry=[
            shapely.geometry.Point(-82, 27),
            None,
            shapely.geometry.Point(-83, 28),
        ],
        index=["x", "y", "z"],
    )
    plot_geodataframe(gdf, color_column="color", context=mock_context)
    assert [obj.color().int_rgb() for obj in mock_context._objects] == [
        (255, 0, 0),
        (0, 0, 255),
    ]


def test_shapely_holes_render_transparently(mock_context):
    from landfall import plot_geometry
    from tests.test_release_regressions import donut

    rings = donut()
    geometry = shapely.geometry.Polygon(rings[0], rings[1:])
    image = plot_geometry(
        geometry, context=mock_context, set_zoom=11, window_size=(400, 400)
    )
    assert len(mock_context._objects) == 1
    assert image.getpixel((200, 200)) != image.getpixel((290, 200))


@pytest.mark.parametrize("geometry", [[], [None], [shapely.geometry.Point()]])
def test_empty_geometries_raise_clear_error(mock_context, geometry):
    from landfall import plot_geometries

    with pytest.raises(ValueError, match="No non-empty geometries"):
        plot_geometries(geometry, context=mock_context)
