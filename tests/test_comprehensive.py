"""
Comprehensive pytest test suite for landfall package.

Tests all major functionality including the recent bug fixes and improvements.
"""

import warnings

import pytest
import staticmaps
from PIL import Image

from landfall import (
    plot_points,
    plot_points_data,
    plot_polygons,
    plot_polygon,
    random_color,
    Context,
)
from landfall.color import (
    process_colors,
    convert_color,
    process_id_colors,
    map_id_colors,
)
from landfall.distinctipy import get_distinct_colors, get_distict_colors
from landfall.colorsys import hsvt_to_rgb, get_wheel_colors
from landfall.points import add_points, add_point, points_to_lats_lons
from landfall.polygons import (
    create_polygon_points,
    flip_polygon_coords,
    add_polygons,
    add_polygon,
)

from tests.mock_tile_downloader import MockTileDownloader


@pytest.fixture
def mock_context():
    """Create a context with mock tile downloader for testing."""
    context = Context()
    context.set_tile_downloader(MockTileDownloader())
    return context


@pytest.fixture
def mock_staticmaps_context():
    """Create a staticmaps context with mock tile downloader for testing."""
    context = staticmaps.Context()
    context.set_tile_downloader(MockTileDownloader())
    return context


class TestMockTileDownloader:
    """Test the mock tile downloader functionality."""

    def test_mock_tile_downloader_creation(self):
        """Test that mock tile downloader can be created."""
        downloader = MockTileDownloader()
        assert isinstance(downloader, staticmaps.TileDownloader)

    def test_mock_tile_downloader_get(self):
        """Test that mock tile downloader returns None."""
        downloader = MockTileDownloader()
        result = downloader.get(staticmaps.tile_provider_OSM, "/tmp", 10, 100, 200)
        assert result is None


class TestColorFunctions:
    """Test color generation and processing functions."""

    def test_random_color(self):
        """Test random color generation."""
        color = random_color()
        assert isinstance(color, staticmaps.Color)
        assert 0 <= color.int_rgb()[0] <= 255

    def test_random_color_with_seed(self):
        """Test random color generation with seed."""
        color1 = random_color(42)
        color2 = random_color(42)
        assert color1.int_rgb() == color2.int_rgb()

    def test_get_distinct_colors(self):
        """Test the fixed distinct colors function."""
        colors = get_distinct_colors(3)
        assert len(colors) == 3
        assert isinstance(colors, list)

        # Test that colors are properly scaled to 0-255 range
        for color in colors:
            assert isinstance(color, tuple)
            assert len(color) == 3
            for component in color:
                assert 0 <= component <= 255

    def test_get_distict_colors_deprecated(self):
        """Test that the deprecated function still works and warns."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            colors = get_distict_colors(3)

            # Should work the same as the new function
            assert len(colors) == 3
            assert isinstance(colors, list)

            # Should emit deprecation warning
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "deprecated" in str(w[0].message)

    def test_hsvt_to_rgb(self):
        """Test HSV to RGB conversion."""
        # Test known HSV values
        rgb = hsvt_to_rgb(0.0, 1.0, 1.0)  # Pure red
        assert rgb == (255, 0, 0)

        rgb = hsvt_to_rgb(0.33, 1.0, 1.0)  # Pure green
        # Allow for small rounding differences
        assert abs(rgb[0] - 0) <= 5
        assert rgb[1] == 255
        assert abs(rgb[2] - 0) <= 5

        rgb = hsvt_to_rgb(0.67, 1.0, 1.0)  # Pure blue
        # Allow for small rounding differences
        assert abs(rgb[0] - 0) <= 5
        assert abs(rgb[1] - 0) <= 5
        assert rgb[2] == 255

    def test_get_wheel_colors(self):
        """Test color wheel generation."""
        colors = get_wheel_colors(5)
        assert len(colors) == 5
        assert isinstance(colors, set)

        for color in colors:
            assert isinstance(color, tuple)
            assert len(color) == 3
            for component in color:
                assert 0 <= component <= 255

    def test_get_wheel_colors_too_many(self):
        """Test wheel colors with large number."""
        # The function doesn't actually raise an error for large numbers
        colors = get_wheel_colors(100)
        assert len(colors) == 100

    def test_convert_color_string(self):
        """Test color conversion from string."""
        color = convert_color("red")
        assert isinstance(color, staticmaps.Color)

    def test_convert_color_rgb_tuple(self):
        """Test color conversion from RGB tuple."""
        color = convert_color((255, 0, 0))
        assert isinstance(color, staticmaps.Color)
        assert color.int_rgb() == (255, 0, 0)

    def test_convert_color_rgba_tuple(self):
        """Test color conversion from RGBA tuple."""
        color = convert_color((255, 0, 0, 128))
        assert isinstance(color, staticmaps.Color)
        assert color.int_rgb() == (255, 0, 0)

    def test_convert_color_invalid(self):
        """Test color conversion with invalid input."""
        with pytest.raises(ValueError):
            convert_color((1, 2))  # Too few components

        with pytest.raises(ValueError):
            convert_color((1, 2, 3, 4, 5))  # Too many components

    @pytest.mark.parametrize("color_type", ["random", "distinct", "wheel"])
    def test_process_colors_types(self, color_type):
        """Test processing different color types."""
        colors = process_colors(color_type, 3)
        assert len(colors) == 3
        assert isinstance(colors, list)

    def test_process_colors_invalid_string(self):
        """Test processing colors with invalid string."""
        with pytest.raises(ValueError):
            process_colors("invalid", 3)

    def test_process_id_colors(self):
        """Test processing ID-based colors."""
        ids = ["A", "B", "C"]
        id_colors = {"A": "red", "B": "green", "C": "blue"}
        colors = process_id_colors(ids, id_colors)
        assert len(colors) == 3
        assert isinstance(colors, list)

    def test_map_id_colors(self):
        """Test mapping colors to IDs."""
        ids = ["A", "B", "C"]
        color_map = map_id_colors(ids, "distinct")
        assert isinstance(color_map, dict)
        assert len(color_map) == 3


class TestPoints:
    """Test point plotting functionality."""

    def test_plot_points_basic(self, mock_context):
        """Test basic point plotting."""
        img = plot_points([0, 1, 2], [0, 1, 2], context=mock_context)
        assert isinstance(img, Image.Image)
        assert img.size == (500, 400)

    def test_plot_points_with_colors(self, mock_context):
        """Test point plotting with custom colors."""
        img = plot_points(
            [0, 1, 2], [0, 1, 2], colors=["red", "green", "blue"], context=mock_context
        )
        assert isinstance(img, Image.Image)

    def test_plot_points_with_color_string(self, mock_context):
        """Test point plotting with color string."""
        img = plot_points([0, 1, 2], [0, 1, 2], colors="distinct", context=mock_context)
        assert isinstance(img, Image.Image)

    def test_plot_points_data(self, mock_context):
        """Test plotting points from data dictionary."""
        data = {"lat": [0, 1, 2], "lon": [0, 1, 2], "color": ["red", "green", "blue"]}
        img = plot_points_data(
            data, "lat", "lon", color_name="color", context=mock_context
        )
        assert isinstance(img, Image.Image)

    def test_add_points(self, mock_staticmaps_context):
        """Test adding points to context."""
        add_points(mock_staticmaps_context, [0, 1, 2], [0, 1, 2])
        # Context should have objects added
        assert len(mock_staticmaps_context._objects) > 0

    def test_add_point(self, mock_staticmaps_context):
        """Test adding single point to context."""
        add_point(mock_staticmaps_context, 0, 0, staticmaps.Color(255, 0, 0), 10)
        # Context should have objects added
        assert len(mock_staticmaps_context._objects) > 0

    def test_points_to_lats_lons(self):
        """Test converting points to lat/lon tuples."""
        points = [(0, 1), (2, 3), (4, 5)]
        lats, lons = points_to_lats_lons(points)
        assert lats == [0, 2, 4]
        assert lons == [1, 3, 5]


class TestPolygons:
    """Test polygon plotting functionality."""

    def test_plot_polygons_basic(self, mock_context):
        """Test basic polygon plotting."""
        polygons = [[(0, 0), (1, 0), (1, 1), (0, 1)], [(2, 2), (3, 2), (3, 3), (2, 3)]]
        img = plot_polygons(polygons, context=mock_context)
        assert isinstance(img, Image.Image)
        assert img.size == (500, 400)

    def test_plot_polygon_single(self, mock_context):
        """Test plotting single polygon."""
        polygon = [(0, 0), (1, 0), (1, 1), (0, 1)]
        img = plot_polygon(polygon, context=mock_context)
        assert isinstance(img, Image.Image)

    def test_create_polygon_points(self):
        """Test creating polygon points."""
        polygon = [(0, 0), (1, 0), (1, 1), (0, 1)]
        points = create_polygon_points(polygon)
        assert len(points) == 4
        # Check if it's a LatLng object (from s2sphere)
        assert hasattr(points[0], "lat") and hasattr(points[0], "lng")

    def test_flip_polygon_coords(self):
        """Test flipping polygon coordinates."""
        polygon = [(0, 1), (2, 3), (4, 5)]
        flipped = flip_polygon_coords(polygon)
        assert flipped == [(1, 0), (3, 2), (5, 4)]

    def test_add_polygons(self, mock_staticmaps_context):
        """Test adding polygons to context."""
        polygons = [[(0, 0), (1, 0), (1, 1), (0, 1)]]
        add_polygons(mock_staticmaps_context, polygons)
        # Context should have objects added
        assert len(mock_staticmaps_context._objects) > 0

    def test_add_polygon(self, mock_staticmaps_context):
        """Test adding single polygon to context."""
        polygon = [(0, 0), (1, 0), (1, 1), (0, 1)]
        add_polygon(
            mock_staticmaps_context,
            polygon,
            staticmaps.Color(255, 0, 0, 100),
            2,
            staticmaps.Color(255, 0, 0),
        )
        # Context should have objects added
        assert len(mock_staticmaps_context._objects) > 0


class TestContext:
    """Test the enhanced Context class."""

    def test_context_creation(self):
        """Test creating context."""
        context = Context()
        assert isinstance(context, staticmaps.Context)

    def test_context_add_points(self, mock_context):
        """Test adding points through context."""
        mock_context.add_points([0, 1, 2], [0, 1, 2])
        # Context should have objects added
        assert len(mock_context._objects) > 0

    def test_context_add_point(self, mock_context):
        """Test adding single point through context."""
        mock_context.add_point(0, 0, staticmaps.Color(255, 0, 0), 10)
        # Context should have objects added
        assert len(mock_context._objects) > 0

    def test_context_add_polygons(self, mock_context):
        """Test adding polygons through context."""
        polygons = [[(0, 0), (1, 0), (1, 1), (0, 1)]]
        mock_context.add_polygons(polygons)
        # Context should have objects added
        assert len(mock_context._objects) > 0

    def test_context_add_polygon(self, mock_context):
        """Test adding single polygon through context."""
        polygon = [(0, 0), (1, 0), (1, 1), (0, 1)]
        fill_color = staticmaps.Color(255, 0, 0, 100)
        color = staticmaps.RED
        width = 2
        mock_context.add_polygon(polygon, fill_color, width, color)
        # Context should have objects added
        assert len(mock_context._objects) > 0


class TestIntegration:
    """Integration tests for the complete package."""

    def test_full_workflow_points(self, mock_context):
        """Test complete workflow for plotting points."""
        # Test data
        lats = [27.88, 27.92, 27.94]
        lons = [-82.49, -82.49, -82.46]

        # Plot points
        img = plot_points(lats, lons, context=mock_context)
        assert isinstance(img, Image.Image)
        assert img.size == (500, 400)

    def test_full_workflow_polygons(self, mock_context):
        """Test complete workflow for plotting polygons."""
        # Test data
        polygons = [
            [(27.88, -82.49), (27.92, -82.49), (27.94, -82.46), (27.88, -82.49)],
            [(28.0, -82.5), (28.1, -82.5), (28.1, -82.4), (28.0, -82.4)],
        ]

        # Plot polygons
        img = plot_polygons(polygons, context=mock_context)
        assert isinstance(img, Image.Image)
        assert img.size == (500, 400)

    def test_color_bug_fix_verification(self):
        """Verify that the critical color bug is fixed."""
        # This test specifically verifies the integer conversion bug fix
        colors = get_distinct_colors(5)

        for color in colors:
            r, g, b = color
            # All components should be in 0-255 range
            assert 0 <= r <= 255
            assert 0 <= g <= 255
            assert 0 <= b <= 255

            # At least some colors should have values > 1 (proving the bug is fixed)
            if r > 1 or g > 1 or b > 1:
                break
        else:
            pytest.fail(
                "All color components are <= 1, indicating the bug is not fixed"
            )


class TestErrorHandling:
    """Test error handling and edge cases."""

    def test_empty_points(self, mock_context):
        """Test handling empty point lists."""
        # Should raise error with empty lists
        with pytest.raises(RuntimeError, match="Cannot render map without center/zoom"):
            plot_points([], [], context=mock_context)

    def test_empty_polygons(self, mock_context):
        """Test handling empty polygon lists."""
        # Should raise error with empty lists
        with pytest.raises(RuntimeError, match="Cannot render map without center/zoom"):
            plot_polygons([], context=mock_context)

    def test_invalid_coordinates(self, mock_context):
        """Test handling invalid coordinates."""
        # Should raise error with invalid coordinates
        with pytest.raises(AssertionError):
            plot_points([1000, -1000], [1000, -1000], context=mock_context)


# Parametrized tests for comprehensive coverage
@pytest.mark.parametrize(
    "color_type,count",
    [
        ("random", 1),
        ("random", 5),
        ("distinct", 3),
        ("distinct", 10),
        ("wheel", 2),
        ("wheel", 7),
    ],
)
def test_color_generation_scales(color_type, count):
    """Test color generation with different scales."""
    colors = process_colors(color_type, count)
    assert len(colors) == count
    assert all(isinstance(c, staticmaps.Color) for c in colors)


@pytest.mark.parametrize(
    "lat,lon",
    [
        ([0, 1, 2], [0, 1, 2]),
        ([27.88, 27.92], [-82.49, -82.46]),
        ([0], [0]),
    ],
)
def test_plot_points_coordinates(lat, lon, mock_context):
    """Test plotting points with various coordinate sets."""
    img = plot_points(lat, lon, context=mock_context)
    assert isinstance(img, Image.Image)
    assert img.size == (500, 400)


@pytest.mark.parametrize(
    "window_size",
    [
        (500, 400),
        (800, 600),
        (1000, 800),
    ],
)
def test_plot_points_window_sizes(window_size, mock_context):
    """Test plotting points with different window sizes."""
    img = plot_points([0, 1], [0, 1], window_size=window_size, context=mock_context)
    assert isinstance(img, Image.Image)
    assert img.size == window_size


# Performance tests
@pytest.mark.slow
def test_large_dataset_performance(mock_context):
    """Test performance with larger datasets."""
    import time

    # Generate larger dataset with valid coordinates
    lats = [i * 0.01 for i in range(0, 100)]  # Valid latitude range
    lons = [i * 0.01 for i in range(0, 100)]  # Valid longitude range

    start_time = time.time()
    img = plot_points(lats, lons, context=mock_context)
    end_time = time.time()

    assert isinstance(img, Image.Image)
    # Should complete within reasonable time (adjust threshold as needed)
    assert (end_time - start_time) < 5.0  # 5 seconds max


# Fixture for test data
@pytest.fixture
def sample_data():
    """Sample data for testing."""
    return {
        "lats": [27.88, 27.92, 27.94],
        "lons": [-82.49, -82.49, -82.46],
        "polygons": [
            [(27.88, -82.49), (27.92, -82.49), (27.94, -82.46)],
            [(28.0, -82.5), (28.1, -82.5), (28.1, -82.4)],
        ],
    }


def test_sample_data_usage(sample_data, mock_context):
    """Test using sample data fixture."""
    img = plot_points(sample_data["lats"], sample_data["lons"], context=mock_context)
    assert isinstance(img, Image.Image)

    img = plot_polygons(sample_data["polygons"], context=mock_context)
    assert isinstance(img, Image.Image)
