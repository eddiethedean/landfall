"""
Test line plotting functionality.
"""

import pytest
from PIL import Image

from landfall import plot_line, plot_lines
from landfall.lines import add_lines, add_line
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


class TestLinePlotting:
    """Test line plotting functionality."""

    def test_basic_line_plotting(self, mock_context):
        """Test basic line plotting."""
        line = [(0, 0), (1, 1), (2, 2)]
        img = plot_line(line, context=mock_context)
        assert isinstance(img, Image.Image)
        assert img.size == (500, 400)

    def test_multiple_lines_plotting(self, mock_context):
        """Test plotting multiple lines."""
        lines = [[(0, 0), (1, 1), (2, 2)], [(0, 1), (1, 2), (2, 3)]]
        img = plot_lines(lines, context=mock_context)
        assert isinstance(img, Image.Image)
        assert img.size == (500, 400)

    def test_line_plotting_with_colors(self, mock_context):
        """Test line plotting with custom colors."""
        lines = [[(0, 0), (1, 1)], [(0, 1), (1, 2)]]
        img = plot_lines(lines, colors=["red", "green"], context=mock_context)
        assert isinstance(img, Image.Image)

    def test_line_plotting_with_color_string(self, mock_context):
        """Test line plotting with color string."""
        lines = [[(0, 0), (1, 1)], [(0, 1), (1, 2)]]
        img = plot_lines(lines, colors="distinct", context=mock_context)
        assert isinstance(img, Image.Image)

    def test_line_plotting_custom_width(self, mock_context):
        """Test line plotting with custom width."""
        line = [(0, 0), (1, 1), (2, 2)]
        img = plot_line(line, width=5, context=mock_context)
        assert isinstance(img, Image.Image)

    def test_line_plotting_custom_size(self, mock_context):
        """Test line plotting with custom window size."""
        line = [(0, 0), (1, 1), (2, 2)]
        img = plot_line(line, window_size=(800, 600), context=mock_context)
        assert isinstance(img, Image.Image)
        assert img.size == (800, 600)

    def test_line_plotting_with_ids(self, mock_context):
        """Test line plotting with ID-based coloring."""
        lines = [[(0, 0), (1, 1)], [(0, 1), (1, 2)]]
        ids = [1, 2]
        img = plot_lines(lines, ids=ids, id_colors="wheel", context=mock_context)
        assert isinstance(img, Image.Image)

    def test_add_lines_to_context(self, mock_staticmaps_context):
        """Test adding lines to context."""
        lines = [[(0, 0), (1, 1), (2, 2)]]
        add_lines(mock_staticmaps_context, lines)
        assert len(mock_staticmaps_context._objects) > 0

    def test_add_single_line_to_context(self, mock_staticmaps_context):
        """Test adding single line to context."""
        import staticmaps

        line = [(0, 0), (1, 1), (2, 2)]
        add_line(mock_staticmaps_context, line, staticmaps.Color(255, 0, 0), 2)
        assert len(mock_staticmaps_context._objects) > 0

    def test_flip_coords(self, mock_context):
        """Test flip_coords functionality."""
        # Line in (lon, lat) order
        line = [(0, 0), (1, 1), (2, 2)]  # This would be (lat, lon) if flip_coords=True
        img = plot_line(line, flip_coords=True, context=mock_context)
        assert isinstance(img, Image.Image)

    def test_empty_line(self, mock_context):
        """Test handling empty line."""
        line = []
        with pytest.raises(
            ValueError, match="Trying to create line with less than 2 coordinates"
        ):
            plot_line(line, context=mock_context)

    def test_single_point_line(self, mock_context):
        """Test line with single point."""
        line = [(0, 0)]
        with pytest.raises(
            ValueError, match="Trying to create line with less than 2 coordinates"
        ):
            plot_line(line, context=mock_context)

    def test_empty_lines(self, mock_context):
        """Test handling empty lines list."""
        lines = []
        with pytest.raises(RuntimeError, match="Cannot render map without center/zoom"):
            plot_lines(lines, context=mock_context)


@pytest.mark.parametrize(
    "lines",
    [
        ([[(0, 0), (1, 1), (2, 2)]]),
        ([[(27.88, -82.49), (27.92, -82.46)]]),
        ([[(0, 0), (1, 1)], [(0, 1), (1, 2)]]),
    ],
)
def test_plot_lines_coordinate_variations(lines, mock_context):
    """Test plotting lines with various coordinate sets."""
    img = plot_lines(lines, context=mock_context)
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
def test_line_plotting_window_sizes(window_size, mock_context):
    """Test line plotting with different window sizes."""
    line = [(0, 0), (1, 1)]
    img = plot_line(line, window_size=window_size, context=mock_context)
    assert isinstance(img, Image.Image)
    assert img.size == window_size


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_extreme_coordinates(self, mock_context):
        """Test handling extreme coordinates."""
        with pytest.raises(ZeroDivisionError):
            plot_line([(1000, -1000), (1000, -1000)], context=mock_context)

    def test_line_width_zero(self, mock_context):
        """Test line with zero width."""
        line = [(0, 0), (1, 1)]
        img = plot_line(line, width=0, context=mock_context)
        assert isinstance(img, Image.Image)

    def test_line_width_large(self, mock_context):
        """Test line with large width."""
        line = [(0, 0), (1, 1)]
        img = plot_line(line, width=20, context=mock_context)
        assert isinstance(img, Image.Image)
