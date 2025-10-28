__version__ = "0.4.0"

# Apply compatibility patches first
import landfall.compatibility  # noqa: F401

from landfall.color import random_color
from landfall.points import plot_points, plot_points_data
from landfall.polygons import plot_polygons, plot_polygon
from landfall.lines import plot_line, plot_lines
from landfall.circles import plot_circle, plot_circles
from landfall.geojson import plot_geojson, plot_geojson_file
from landfall.context import Context

# Conditional import for geopandas
try:
    from landfall.geopandas_integration import (
        plot_geodataframe,  # noqa: F401
        plot_geometry,  # noqa: F401
        plot_geometries,  # noqa: F401
    )

    _geopandas_available = True
except ImportError:
    # GeoPandas not available, skip
    _geopandas_available = False

__all__ = [
    "plot_points",
    "plot_points_data",
    "plot_polygons",
    "plot_polygon",
    "plot_line",
    "plot_lines",
    "plot_circle",
    "plot_circles",
    "plot_geojson",
    "plot_geojson_file",
    "random_color",
    "Context",
]

# Add geopandas functions to __all__ if available
if _geopandas_available:
    __all__.extend(["plot_geodataframe", "plot_geometry", "plot_geometries"])
