"""
Legacy test file converted to pytest format.
"""

import pytest
from PIL import Image

from landfall.context import Context
from landfall.points import plot_points, points_to_lats_lons
from tests.mock_tile_downloader import MockTileDownloader


@pytest.fixture
def context():
    """Create a context with mock tile downloader for testing."""
    context = Context()
    context.set_tile_downloader(MockTileDownloader())
    return context


def test_plot_points(context):
    """Test basic point plotting functionality."""
    img = plot_points([0, 1, 2], [0, 1, 2], context=context)
    assert isinstance(img, Image.Image)
    assert img.size == (500, 400)


def test_plot_points_accepts_numpy_coordinate_rows(context):
    numpy = pytest.importorskip("numpy")
    points = numpy.array([[27.88, -82.49], [27.92, -82.46]])

    assert points_to_lats_lons(points) == ([27.88, 27.92], [-82.49, -82.46])
    image = plot_points(points, context=context)
    assert isinstance(image, Image.Image)
