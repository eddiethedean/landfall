"""
Test plotting functionality.
"""

import pytest
from PIL import Image

from landfall import plot_points, plot_points_data, plot_polygons, plot_polygon
from landfall.points import add_points, add_point
from landfall.polygons import add_polygons, add_polygon
from tests.mock_tile_downloader import MockTileDownloader


@pytest.fixture
def mock_context():
    """Create a context with mock tile downloader for testing."""
    from landfall.context import Context

    context = Context()
    context.set_tile_downloader(MockTileDownloader())
    return context


@pytest.fixture
def mock_staticmaps_context():
    """Create a staticmaps context with mock tile downloader for testing."""
    import staticmaps

    context = staticmaps.Context()
    context.set_tile_downloader(MockTileDownloader())
    return context


class TestPointPlotting:
    """Test point plotting functionality."""

    def test_basic_point_plotting(self, mock_context):
        """Test basic point plotting."""
        img = plot_points([0, 1, 2], [0, 1, 2], context=mock_context)
        assert isinstance(img, Image.Image)
        assert img.size == (500, 400)

    def test_point_plotting_with_colors(self, mock_context):
        """Test point plotting with custom colors."""
        img = plot_points(
            [0, 1, 2], [0, 1, 2], colors=["red", "green", "blue"], context=mock_context
        )
        assert isinstance(img, Image.Image)

    def test_point_plotting_with_color_string(self, mock_context):
        """Test point plotting with color string."""
        img = plot_points([0, 1, 2], [0, 1, 2], colors="distinct", context=mock_context)
        assert isinstance(img, Image.Image)

    def test_point_plotting_custom_size(self, mock_context):
        """Test point plotting with custom window size."""
        img = plot_points(
            [0, 1, 2], [0, 1, 2], window_size=(800, 600), context=mock_context
        )
        assert isinstance(img, Image.Image)
        assert img.size == (800, 600)

    def test_point_plotting_data_dict(self, mock_context):
        """Test plotting points from data dictionary."""
        data = {"lat": [0, 1, 2], "lon": [0, 1, 2], "color": ["red", "green", "blue"]}
        img = plot_points_data(
            data, "lat", "lon", color_name="color", context=mock_context
        )
        assert isinstance(img, Image.Image)

    def test_add_points_to_context(self, mock_staticmaps_context):
        """Test adding points to context."""
        add_points(mock_staticmaps_context, [0, 1, 2], [0, 1, 2])
        assert len(mock_staticmaps_context._objects) > 0

    def test_add_single_point_to_context(self, mock_staticmaps_context):
        """Test adding single point to context."""
        import staticmaps

        add_point(mock_staticmaps_context, 0, 0, staticmaps.Color(255, 0, 0), 10)
        assert len(mock_staticmaps_context._objects) > 0


class TestPolygonPlotting:
    """Test polygon plotting functionality."""

    def test_basic_polygon_plotting(self, mock_context):
        """Test basic polygon plotting."""
        polygons = [[(0, 0), (1, 0), (1, 1), (0, 1)], [(2, 2), (3, 2), (3, 3), (2, 3)]]
        img = plot_polygons(polygons, context=mock_context)
        assert isinstance(img, Image.Image)
        assert img.size == (500, 400)

    def test_single_polygon_plotting(self, mock_context):
        """Test plotting single polygon."""
        polygon = [(0, 0), (1, 0), (1, 1), (0, 1)]
        img = plot_polygon(polygon, context=mock_context)
        assert isinstance(img, Image.Image)

    def test_polygon_plotting_with_fill(self, mock_context):
        """Test polygon plotting with fill colors."""
        polygons = [[(0, 0), (1, 0), (1, 1), (0, 1)]]
        img = plot_polygons(
            polygons,
            fill_color=(255, 0, 0, 100),
            color=(255, 0, 0),
            context=mock_context,
        )
        assert isinstance(img, Image.Image)

    def test_add_polygons_to_context(self, mock_staticmaps_context):
        """Test adding polygons to context."""
        polygons = [[(0, 0), (1, 0), (1, 1), (0, 1)]]
        add_polygons(mock_staticmaps_context, polygons)
        assert len(mock_staticmaps_context._objects) > 0

    def test_add_single_polygon_to_context(self, mock_staticmaps_context):
        """Test adding single polygon to context."""
        import staticmaps

        polygon = [(0, 0), (1, 0), (1, 1), (0, 1)]
        add_polygon(
            mock_staticmaps_context,
            polygon,
            staticmaps.Color(255, 0, 0, 100),
            2,
            staticmaps.Color(255, 0, 0),
        )
        assert len(mock_staticmaps_context._objects) > 0


@pytest.mark.parametrize(
    "coordinates",
    [
        ([0, 1, 2], [0, 1, 2]),
        ([27.88, 27.92], [-82.49, -82.46]),
        ([0], [0]),
        ([], []),  # Empty lists
    ],
)
def test_plot_points_coordinate_variations(coordinates, mock_context):
    """Test plotting points with various coordinate sets."""
    lats, lons = coordinates

    # Handle empty coordinates case
    if not lats or not lons:
        with pytest.raises(RuntimeError, match="Cannot render map without center/zoom"):
            plot_points(lats, lons, context=mock_context)
    else:
        img = plot_points(lats, lons, context=mock_context)
        assert isinstance(img, Image.Image)


@pytest.mark.parametrize(
    "window_size",
    [
        (500, 400),
        (800, 600),
        (1000, 800),
        (200, 200),
    ],
)
def test_plotting_window_sizes(window_size, mock_context):
    """Test plotting with different window sizes."""
    img = plot_points([0, 1], [0, 1], window_size=window_size, context=mock_context)
    assert isinstance(img, Image.Image)
    assert img.size == window_size


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_points(self, mock_context):
        """Test handling empty point lists."""
        with pytest.raises(RuntimeError, match="Cannot render map without center/zoom"):
            plot_points([], [], context=mock_context)

    def test_empty_polygons(self, mock_context):
        """Test handling empty polygon lists."""
        with pytest.raises(RuntimeError, match="Cannot render map without center/zoom"):
            plot_polygons([], context=mock_context)

    def test_extreme_coordinates(self, mock_context):
        """Test handling extreme coordinates."""
        with pytest.raises(AssertionError):
            plot_points([1000, -1000], [1000, -1000], context=mock_context)

    def test_single_point(self, mock_context):
        """Test plotting single point."""
        img = plot_points([0], [0], context=mock_context)
        assert isinstance(img, Image.Image)

    def test_single_polygon(self, mock_context):
        """Test plotting single polygon."""
        polygon = [(0, 0), (1, 0), (1, 1), (0, 1)]
        img = plot_polygon(polygon, context=mock_context)
        assert isinstance(img, Image.Image)
