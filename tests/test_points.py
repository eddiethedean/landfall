import unittest

from PIL import ImageChops

from landfall.points import plot_points, plot_points_data


class TestPoints(unittest.TestCase):
    def test_plot_points(self):
        
        img = plot_points([0, 1, 2], [0, 1, 2])
        self.assertEqual(img.size, (500, 400))