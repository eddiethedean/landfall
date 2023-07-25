import unittest

from PIL import ImageChops

from landfall.points import plot_points, plot_points_data
from landfall.context import Context

from tests.mock_tile_downloader import MockTileDownloader

context = Context()
context.set_tile_downloader(MockTileDownloader())


class TestPoints(unittest.TestCase):
    def test_plot_points(self):
        img = plot_points([0, 1, 2], [0, 1, 2], context=context)
        self.assertEqual(img.size, (500, 400))