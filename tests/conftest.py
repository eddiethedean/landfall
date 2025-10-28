"""
Shared pytest fixtures and configuration for landfall tests.
"""

import pytest
import staticmaps

from landfall.context import Context


@pytest.fixture
def mock_context():
    """Create a landfall context with mock tile downloader."""
    from tests.mock_tile_downloader import MockTileDownloader

    context = Context()
    context.set_tile_downloader(MockTileDownloader())
    return context


@pytest.fixture
def mock_staticmaps_context():
    """Create a staticmaps context with mock tile downloader."""
    from tests.mock_tile_downloader import MockTileDownloader

    context = staticmaps.Context()
    context.set_tile_downloader(MockTileDownloader())
    return context


@pytest.fixture
def sample_coordinates():
    """Sample coordinate data for testing."""
    return {
        "lats": [27.88, 27.92, 27.94],
        "lons": [-82.49, -82.49, -82.46],
        "points": [(27.88, -82.49), (27.92, -82.49), (27.94, -82.46)],
    }


@pytest.fixture
def sample_polygons():
    """Sample polygon data for testing."""
    return [
        [(27.88, -82.49), (27.92, -82.49), (27.94, -82.46), (27.88, -82.49)],
        [(28.0, -82.5), (28.1, -82.5), (28.1, -82.4), (28.0, -82.4)],
    ]


@pytest.fixture
def sample_data_dict():
    """Sample data dictionary for testing."""
    return {
        "lat": [0, 1, 2],
        "lon": [0, 1, 2],
        "color": ["red", "green", "blue"],
        "id": ["A", "B", "C"],
    }
