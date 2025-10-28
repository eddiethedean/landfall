"""
Legacy test file converted to pytest format.
"""

import pytest
from PIL import Image

from landfall.points import plot_points
from landfall.context import Context
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
