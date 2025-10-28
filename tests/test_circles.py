"""
Test circle plotting functionality.
"""

import pytest
from PIL import Image

from landfall import plot_circle, plot_circles
from landfall.circles import add_circles, add_circle
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


class TestCirclePlotting:
    """Test circle plotting functionality."""

    def test_basic_circle_plotting(self, mock_context):
        """Test basic circle plotting."""
        img = plot_circle(0, 0, 1000, context=mock_context)
        assert isinstance(img, Image.Image)
        assert img.size == (500, 400)

    def test_multiple_circles_plotting(self, mock_context):
        """Test plotting multiple circles."""
        lats = [0, 1]
        lons = [0, 1]
        radii = [1000, 2000]
        img = plot_circles(lats, lons, radii, context=mock_context)
        assert isinstance(img, Image.Image)
        assert img.size == (500, 400)

    def test_circle_plotting_with_colors(self, mock_context):
        """Test circle plotting with custom colors."""
        lats = [0, 1]
        lons = [0, 1]
        radii = [1000, 2000]
        img = plot_circles(
            lats, lons, radii, colors=["red", "green"], context=mock_context
        )
        assert isinstance(img, Image.Image)

    def test_circle_plotting_with_fill_colors(self, mock_context):
        """Test circle plotting with fill colors."""
        lats = [0, 1]
        lons = [0, 1]
        radii = [1000, 2000]
        img = plot_circles(
            lats, lons, radii, fill_colors=["blue", "yellow"], context=mock_context
        )
        assert isinstance(img, Image.Image)

    def test_circle_plotting_with_transparency(self, mock_context):
        """Test circle plotting with fill transparency."""
        lats = [0, 1]
        lons = [0, 1]
        radii = [1000, 2000]
        img = plot_circles(
            lats, lons, radii, fill_transparency=50, context=mock_context
        )
        assert isinstance(img, Image.Image)

    def test_circle_plotting_custom_width(self, mock_context):
        """Test circle plotting with custom border width."""
        img = plot_circle(0, 0, 1000, width=5, context=mock_context)
        assert isinstance(img, Image.Image)

    def test_circle_plotting_custom_size(self, mock_context):
        """Test circle plotting with custom window size."""
        img = plot_circle(0, 0, 1000, window_size=(800, 600), context=mock_context)
        assert isinstance(img, Image.Image)
        assert img.size == (800, 600)

    def test_circle_plotting_with_ids(self, mock_context):
        """Test circle plotting with ID-based coloring."""
        lats = [0, 1]
        lons = [0, 1]
        radii = [1000, 2000]
        ids = [1, 2]
        img = plot_circles(
            lats, lons, radii, ids=ids, id_colors="wheel", context=mock_context
        )
        assert isinstance(img, Image.Image)

    def test_circle_radius_units(self, mock_context):
        """Test circle plotting with different radius units."""
        # Test meters (default)
        img1 = plot_circle(0, 0, 1000, radius_unit="meters", context=mock_context)
        assert isinstance(img1, Image.Image)

        # Test kilometers
        img2 = plot_circle(0, 0, 1, radius_unit="kilometers", context=mock_context)
        assert isinstance(img2, Image.Image)

    def test_add_circles_to_context(self, mock_staticmaps_context):
        """Test adding circles to context."""
        lats = [0, 1]
        lons = [0, 1]
        radii = [1000, 2000]
        add_circles(mock_staticmaps_context, lats, lons, radii)
        assert len(mock_staticmaps_context._objects) > 0

    def test_add_single_circle_to_context(self, mock_staticmaps_context):
        """Test adding single circle to context."""
        import staticmaps

        add_circle(
            mock_staticmaps_context,
            0,
            0,
            1000,
            staticmaps.Color(255, 0, 0),
            staticmaps.Color(255, 0, 0, 100),
            2,
        )
        assert len(mock_staticmaps_context._objects) > 0

    def test_flip_coords(self, mock_context):
        """Test flip_coords functionality."""
        img = plot_circle(0, 0, 1000, flip_coords=True, context=mock_context)
        assert isinstance(img, Image.Image)

    def test_empty_circles(self, mock_context):
        """Test handling empty circles list."""
        lats = []
        lons = []
        radii = []
        with pytest.raises(RuntimeError, match="Cannot render map without center/zoom"):
            plot_circles(lats, lons, radii, context=mock_context)

    def test_zero_radius(self, mock_context):
        """Test circle with zero radius."""
        img = plot_circle(0, 0, 0, context=mock_context)
        assert isinstance(img, Image.Image)

    def test_large_radius(self, mock_context):
        """Test circle with large radius."""
        img = plot_circle(0, 0, 100000, context=mock_context)
        assert isinstance(img, Image.Image)

    def test_invalid_radius_unit(self, mock_context):
        """Test circle with invalid radius unit."""
        with pytest.raises(
            ValueError, match="radius_unit must be 'meters' or 'kilometers'"
        ):
            plot_circle(0, 0, 1000, radius_unit="invalid", context=mock_context)


@pytest.mark.parametrize(
    "coordinates",
    [
        ([0, 1], [0, 1], [1000, 2000]),
        ([27.88, 27.92], [-82.49, -82.46], [1000, 2000]),
        ([0], [0], [1000]),
    ],
)
def test_plot_circles_coordinate_variations(coordinates, mock_context):
    """Test plotting circles with various coordinate sets."""
    lats, lons, radii = coordinates
    img = plot_circles(lats, lons, radii, context=mock_context)
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
def test_circle_plotting_window_sizes(window_size, mock_context):
    """Test circle plotting with different window sizes."""
    img = plot_circle(0, 0, 1000, window_size=window_size, context=mock_context)
    assert isinstance(img, Image.Image)
    assert img.size == window_size


@pytest.mark.parametrize(
    "radius_unit",
    ["meters", "kilometers"],
)
def test_circle_radius_units(radius_unit, mock_context):
    """Test circle plotting with different radius units."""
    img = plot_circle(0, 0, 1000, radius_unit=radius_unit, context=mock_context)
    assert isinstance(img, Image.Image)


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_extreme_coordinates(self, mock_context):
        """Test handling extreme coordinates."""
        with pytest.raises(ValueError, match="cannot convert float NaN to integer"):
            plot_circle(1000, -1000, 1000, context=mock_context)

    def test_negative_radius(self, mock_context):
        """Test circle with negative radius."""
        img = plot_circle(0, 0, -1000, context=mock_context)
        assert isinstance(img, Image.Image)

    def test_circle_width_zero(self, mock_context):
        """Test circle with zero border width."""
        img = plot_circle(0, 0, 1000, width=0, context=mock_context)
        assert isinstance(img, Image.Image)

    def test_circle_width_large(self, mock_context):
        """Test circle with large border width."""
        img = plot_circle(0, 0, 1000, width=20, context=mock_context)
        assert isinstance(img, Image.Image)
