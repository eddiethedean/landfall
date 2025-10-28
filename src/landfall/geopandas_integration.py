"""
Functions for plotting GeoPandas and Shapely geometries.
"""

from typing import Any, List, Optional, Sequence, Tuple, Union
import staticmaps
from PIL.Image import Image

from landfall.plot import plot_zoom
from landfall.points import add_points
from landfall.lines import add_lines
from landfall.polygons import add_polygons

tp = staticmaps.tile_provider_OSM

# Import guard for optional dependencies
try:
    import geopandas as gpd  # noqa: F401
    import shapely.geometry as geom  # noqa: F401

    GEOPANDAS_AVAILABLE = True
except ImportError:
    GEOPANDAS_AVAILABLE = False


def _check_geopandas_available() -> None:
    """Check if GeoPandas is available and raise helpful error if not."""
    if not GEOPANDAS_AVAILABLE:
        raise ImportError(
            "GeoPandas not installed. Install with: pip install landfall[geo]"
        )


def _geometry_to_coords(geometry: Any) -> Tuple[str, Any]:
    """Convert shapely geometry to landfall format.

    Args:
        geometry: Shapely geometry object

    Returns:
        Tuple of (geometry_type, coordinates)

    Raises:
        ValueError: If geometry type is unsupported
    """
    geom_type = geometry.geom_type

    if geom_type == "Point":
        coords = geometry.coords[0]  # (lon, lat)
        return "Point", coords
    elif geom_type == "MultiPoint":
        coords = list(geometry.coords)  # [(lon, lat), ...]
        return "MultiPoint", coords
    elif geom_type == "LineString":
        coords = list(geometry.coords)  # [(lon, lat), ...]
        return "LineString", coords
    elif geom_type == "MultiLineString":
        coords = [
            list(line.coords) for line in geometry.geoms
        ]  # [[(lon, lat), ...], ...]
        return "MultiLineString", coords
    elif geom_type == "Polygon":
        coords = [
            list(ring.coords) for ring in geometry.interiors
        ]  # [[(lon, lat), ...], ...]
        coords.insert(0, list(geometry.exterior.coords))  # Add exterior ring first
        return "Polygon", coords
    elif geom_type == "MultiPolygon":
        coords = []
        for polygon in geometry.geoms:
            polygon_coords = [list(ring.coords) for ring in polygon.interiors]
            polygon_coords.insert(0, list(polygon.exterior.coords))
            coords.append(polygon_coords)
        return "MultiPolygon", coords
    else:
        raise ValueError(f"Unsupported geometry type: {geom_type}")


def _extract_gdf_colors(
    gdf: Any, color_column: Optional[str] = None
) -> Optional[List[str]]:
    """Extract colors from GeoDataFrame column.

    Args:
        gdf: GeoDataFrame
        color_column: Name of color column

    Returns:
        List of colors or None
    """
    if color_column is None or color_column not in gdf.columns:
        return None

    try:
        colors: List[str] = gdf[color_column].astype(str).tolist()
        return colors
    except Exception:
        return None


def _extract_gdf_sizes(
    gdf: Any, size_column: Optional[str] = None
) -> Optional[List[int]]:
    """Extract sizes from GeoDataFrame column.

    Args:
        gdf: GeoDataFrame
        size_column: Name of size column

    Returns:
        List of sizes or None
    """
    if size_column is None or size_column not in gdf.columns:
        return None

    try:
        sizes: List[int] = gdf[size_column].astype(int).tolist()
        return sizes
    except Exception:
        return None


def plot_geometry(
    geometry: Any,
    tile_provider: Any = tp,
    window_size: Tuple[int, int] = (500, 400),
    zoom: int = 0,
    set_zoom: Optional[int] = None,
    context: Optional[staticmaps.Context] = None,
) -> Image:
    """Plot a single shapely geometry on a map.

    Args:
        geometry: Shapely geometry object
        tile_provider: Map tile provider
        window_size: Output image size (width, height)
        zoom: Zoom level adjustment
        set_zoom: Override automatic zoom level
        context: Optional existing staticmaps context

    Returns:
        PIL Image with plotted geometry

    Raises:
        ImportError: If GeoPandas/Shapely not installed
        ValueError: If geometry type is unsupported
    """
    _check_geopandas_available()

    if context is None:
        context = staticmaps.Context()

    context.set_tile_provider(tile_provider)

    geom_type, coords = _geometry_to_coords(geometry)

    # Plot based on geometry type
    if geom_type == "Point":
        lon, lat = coords
        add_points(context, [lat], [lon])
    elif geom_type == "MultiPoint":
        lats = [coord[1] for coord in coords]
        lons = [coord[0] for coord in coords]
        add_points(context, lats, lons)
    elif geom_type == "LineString":
        line = [(coord[1], coord[0]) for coord in coords]  # Convert to lat, lon
        add_lines(context, [line])
    elif geom_type == "MultiLineString":
        lines = [[(coord[1], coord[0]) for coord in line] for line in coords]
        add_lines(context, lines)
    elif geom_type == "Polygon":
        polygons = [[(coord[1], coord[0]) for coord in ring] for ring in coords]
        add_polygons(context, polygons)
    elif geom_type == "MultiPolygon":
        polygons = []
        for polygon_coords in coords:
            for ring in polygon_coords:
                ring_coords = [(coord[1], coord[0]) for coord in ring]
                polygons.append(ring_coords)
        add_polygons(context, polygons)

    zoom = plot_zoom(context, window_size, zoom, set_zoom)
    context.set_zoom(zoom)

    return context.render_pillow(*window_size)  # type: ignore


def plot_geometries(
    geometries: Sequence[Any],
    tile_provider: Any = tp,
    colors: Optional[Union[Sequence[Any], str]] = None,
    window_size: Tuple[int, int] = (500, 400),
    zoom: int = 0,
    set_zoom: Optional[int] = None,
    context: Optional[staticmaps.Context] = None,
) -> Image:
    """Plot multiple shapely geometries on a map.

    Args:
        geometries: Sequence of shapely geometry objects
        tile_provider: Map tile provider
        colors: Colors for geometries
        window_size: Output image size (width, height)
        zoom: Zoom level adjustment
        set_zoom: Override automatic zoom level
        context: Optional existing staticmaps context

    Returns:
        PIL Image with plotted geometries

    Raises:
        ImportError: If GeoPandas/Shapely not installed
        ValueError: If any geometry type is unsupported
    """
    _check_geopandas_available()

    if context is None:
        context = staticmaps.Context()

    context.set_tile_provider(tile_provider)

    # Process each geometry
    for i, geometry in enumerate(geometries):
        geom_type, coords = _geometry_to_coords(geometry)

        # Get color for this geometry
        if colors is not None:
            if isinstance(colors, str):
                color = colors
            else:
                color = colors[i] if i < len(colors) else colors[0]
        else:
            color = "blue"

        # Plot based on geometry type
        if geom_type == "Point":
            lon, lat = coords
            add_points(context, [lat], [lon], colors=[color])
        elif geom_type == "MultiPoint":
            lats = [coord[1] for coord in coords]
            lons = [coord[0] for coord in coords]
            add_points(context, lats, lons, colors=[color])
        elif geom_type == "LineString":
            line = [(coord[1], coord[0]) for coord in coords]
            add_lines(context, [line], colors=[color])
        elif geom_type == "MultiLineString":
            lines = [[(coord[1], coord[0]) for coord in line] for line in coords]
            add_lines(context, lines, colors=[color])
        elif geom_type == "Polygon":
            polygons = [[(coord[1], coord[0]) for coord in ring] for ring in coords]
            add_polygons(context, polygons, colors=[color])
        elif geom_type == "MultiPolygon":
            polygons = []
            for polygon_coords in coords:
                for ring in polygon_coords:
                    ring_coords = [(coord[1], coord[0]) for coord in ring]
                    polygons.append(ring_coords)
            add_polygons(context, polygons, colors=[color])

    zoom = plot_zoom(context, window_size, zoom, set_zoom)
    context.set_zoom(zoom)

    return context.render_pillow(*window_size)  # type: ignore


def plot_geodataframe(
    gdf: Any,
    geometry_column: Optional[str] = None,
    color_column: Optional[str] = None,
    size_column: Optional[str] = None,
    colors: Optional[Union[Sequence[Any], str]] = None,
    tile_provider: Any = tp,
    window_size: Tuple[int, int] = (500, 400),
    zoom: int = 0,
    set_zoom: Optional[int] = None,
    context: Optional[staticmaps.Context] = None,
) -> Image:
    """Plot a GeoDataFrame on a map.

    Args:
        gdf: GeoDataFrame
        geometry_column: Name of geometry column (auto-detect if None)
        color_column: Name of color column
        size_column: Name of size column
        colors: Colors for geometries
        tile_provider: Map tile provider
        window_size: Output image size (width, height)
        zoom: Zoom level adjustment
        set_zoom: Override automatic zoom level
        context: Optional existing staticmaps context

    Returns:
        PIL Image with plotted GeoDataFrame

    Raises:
        ImportError: If GeoPandas/Shapely not installed
        ValueError: If GeoDataFrame has no geometry column or unsupported geometries
    """
    _check_geopandas_available()

    if context is None:
        context = staticmaps.Context()

    context.set_tile_provider(tile_provider)

    # Auto-detect geometry column if not specified
    if geometry_column is None:
        geometry_column = gdf.geometry.name
        if geometry_column is None:
            raise ValueError("GeoDataFrame has no geometry column")

    if geometry_column not in gdf.columns:
        raise ValueError(
            f"Geometry column '{geometry_column}' not found in GeoDataFrame"
        )

    # Extract colors and sizes from columns if specified
    gdf_colors = _extract_gdf_colors(gdf, color_column)
    gdf_sizes = _extract_gdf_sizes(gdf, size_column)

    # Process each row
    for i, row in gdf.iterrows():
        geometry = row[geometry_column]

        if geometry is None or geometry.is_empty:
            continue

        geom_type, coords = _geometry_to_coords(geometry)

        # Get color for this geometry
        if gdf_colors is not None:
            color = gdf_colors[i]
        elif colors is not None:
            if isinstance(colors, str):
                color = colors
            else:
                color = colors[i] if i < len(colors) else colors[0]
        else:
            color = "blue"

        # Get size for points
        size = gdf_sizes[i] if gdf_sizes is not None else 10

        # Plot based on geometry type
        if geom_type == "Point":
            lon, lat = coords
            add_points(context, [lat], [lon], colors=[color], point_size=size)
        elif geom_type == "MultiPoint":
            lats = [coord[1] for coord in coords]
            lons = [coord[0] for coord in coords]
            add_points(context, lats, lons, colors=[color], point_size=size)
        elif geom_type == "LineString":
            line = [(coord[1], coord[0]) for coord in coords]
            add_lines(context, [line], colors=[color])
        elif geom_type == "MultiLineString":
            lines = [[(coord[1], coord[0]) for coord in line] for line in coords]
            add_lines(context, lines, colors=[color])
        elif geom_type == "Polygon":
            polygons = [[(coord[1], coord[0]) for coord in ring] for ring in coords]
            add_polygons(context, polygons, colors=[color])
        elif geom_type == "MultiPolygon":
            polygons = []
            for polygon_coords in coords:
                for ring in polygon_coords:
                    ring_coords = [(coord[1], coord[0]) for coord in ring]
                    polygons.append(ring_coords)
            add_polygons(context, polygons, colors=[color])

    zoom = plot_zoom(context, window_size, zoom, set_zoom)
    context.set_zoom(zoom)

    return context.render_pillow(*window_size)  # type: ignore
