"""Convenient helpers for plotting geographic data on static maps."""

from landfall.circles import plot_circle, plot_circles
from landfall.color import random_color
from landfall.context import Context
from landfall.geojson import plot_geojson, plot_geojson_file
from landfall.geopandas_integration import (
    plot_geodataframe,
    plot_geometries,
    plot_geometry,
)
from landfall.lines import plot_line, plot_lines
from landfall.points import plot_points, plot_points_data
from landfall.polygons import plot_polygon, plot_polygons

__version__ = "0.5.0"

__all__ = [
    "Context",
    "plot_circle",
    "plot_circles",
    "plot_geodataframe",
    "plot_geojson",
    "plot_geojson_file",
    "plot_geometries",
    "plot_geometry",
    "plot_line",
    "plot_lines",
    "plot_points",
    "plot_points_data",
    "plot_polygon",
    "plot_polygons",
    "random_color",
]
