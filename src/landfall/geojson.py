"""
Functions for plotting GeoJSON data.
"""

import json
from typing import Any, Dict, List, Optional, Tuple, Union
import staticmaps
from PIL.Image import Image

from landfall.plot import plot_zoom
from landfall.points import add_points
from landfall.lines import add_lines
from landfall.polygons import add_polygons

tp = staticmaps.tile_provider_OSM


def parse_geojson(data: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Parse GeoJSON data from string or dict.

    Args:
        data: GeoJSON as string or dict

    Returns:
        Parsed GeoJSON dict

    Raises:
        ValueError: If GeoJSON is invalid or unsupported
    """
    if isinstance(data, str):
        try:
            geojson: Dict[str, Any] = json.loads(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
    elif isinstance(data, dict):
        geojson = data
    else:
        raise ValueError("GeoJSON data must be string or dict")

    # Validate basic GeoJSON structure
    if "type" not in geojson:
        raise ValueError("GeoJSON must have 'type' field")

    if geojson["type"] not in [
        "Feature",
        "FeatureCollection",
        "Point",
        "LineString",
        "Polygon",
        "MultiPoint",
        "MultiLineString",
        "MultiPolygon",
    ]:
        raise ValueError(f"Unsupported GeoJSON type: {geojson['type']}")

    return geojson


def extract_geometries(
    geojson: Dict[str, Any],
) -> List[Tuple[str, Any, Dict[str, Any]]]:
    """Extract geometries from GeoJSON.

    Args:
        geojson: Parsed GeoJSON dict

    Returns:
        List of (geometry_type, coordinates, properties) tuples
    """
    geometries = []

    if geojson["type"] == "Feature":
        geom = geojson.get("geometry", {})
        if geom and geom.get("type") != "GeometryCollection":
            geometries.append(
                (geom["type"], geom["coordinates"], geojson.get("properties", {}))
            )
    elif geojson["type"] == "FeatureCollection":
        features = geojson.get("features", [])
        for feature in features:
            geom = feature.get("geometry", {})
            if geom and geom.get("type") != "GeometryCollection":
                geometries.append(
                    (geom["type"], geom["coordinates"], feature.get("properties", {}))
                )
    else:
        # Direct geometry (not GeometryCollection)
        if geojson["type"] != "GeometryCollection":
            geometries.append((geojson["type"], geojson["coordinates"], {}))

    return geometries


def _extract_color_from_properties(
    properties: Dict[str, Any], default_color: str = "blue"
) -> str:
    """Extract color from GeoJSON properties.

    Args:
        properties: GeoJSON properties dict
        default_color: Default color if none found

    Returns:
        Color string
    """
    # Common GeoJSON styling properties
    color_keys = ["stroke", "marker-color", "color", "fill"]
    for key in color_keys:
        if key in properties:
            return str(properties[key])
    return default_color


def _extract_width_from_properties(
    properties: Dict[str, Any], default_width: int = 2
) -> int:
    """Extract width from GeoJSON properties.

    Args:
        properties: GeoJSON properties dict
        default_width: Default width if none found

    Returns:
        Width value
    """
    width_keys = ["stroke-width", "width", "line-width"]
    for key in width_keys:
        if key in properties:
            try:
                return int(properties[key])
            except (ValueError, TypeError):
                pass
    return default_width


def _extract_size_from_properties(
    properties: Dict[str, Any], default_size: int = 10
) -> int:
    """Extract marker size from GeoJSON properties.

    Args:
        properties: GeoJSON properties dict
        default_size: Default size if none found

    Returns:
        Size value
    """
    size_keys = ["marker-size", "size", "point-size"]
    for key in size_keys:
        if key in properties:
            try:
                return int(properties[key])
            except (ValueError, TypeError):
                pass
    return default_size


def _plot_point_geometry(
    coords: List[float], properties: Dict[str, Any], context: staticmaps.Context
) -> None:
    """Plot Point geometry."""
    if len(coords) != 2:
        raise ValueError("Point coordinates must have exactly 2 values")

    # GeoJSON uses lon, lat order
    lon, lat = coords
    color = _extract_color_from_properties(properties)
    size = _extract_size_from_properties(properties)

    add_points(context, [lat], [lon], colors=[color], point_size=size)


def _plot_multipoint_geometry(
    coords: List[List[float]], properties: Dict[str, Any], context: staticmaps.Context
) -> None:
    """Plot MultiPoint geometry."""
    lats = []
    lons = []
    for coord in coords:
        if len(coord) != 2:
            raise ValueError("Point coordinates must have exactly 2 values")
        lons.append(coord[0])
        lats.append(coord[1])

    color = _extract_color_from_properties(properties)
    size = _extract_size_from_properties(properties)

    add_points(context, lats, lons, colors=[color], point_size=size)


def _plot_linestring_geometry(
    coords: List[List[float]], properties: Dict[str, Any], context: staticmaps.Context
) -> None:
    """Plot LineString geometry."""
    # Convert lon, lat to lat, lon tuples
    line = [(coord[1], coord[0]) for coord in coords]

    color = _extract_color_from_properties(properties)
    width = _extract_width_from_properties(properties)

    add_lines(context, [line], colors=[color], width=width)


def _plot_multilinestring_geometry(
    coords: List[List[List[float]]],
    properties: Dict[str, Any],
    context: staticmaps.Context,
) -> None:
    """Plot MultiLineString geometry."""
    lines = []
    for line_coords in coords:
        # Convert lon, lat to lat, lon tuples
        line = [(coord[1], coord[0]) for coord in line_coords]
        lines.append(line)

    color = _extract_color_from_properties(properties)
    width = _extract_width_from_properties(properties)

    add_lines(context, lines, colors=[color], width=width)


def _plot_polygon_geometry(
    coords: List[List[List[float]]],
    properties: Dict[str, Any],
    context: staticmaps.Context,
) -> None:
    """Plot Polygon geometry."""
    polygons = []
    for ring in coords:
        # Convert lon, lat to lat, lon tuples
        polygon = [(coord[1], coord[0]) for coord in ring]
        polygons.append(polygon)

    color = _extract_color_from_properties(properties)
    width = _extract_width_from_properties(properties)

    add_polygons(context, polygons, colors=[color], width=width)


def _plot_multipolygon_geometry(
    coords: List[List[List[List[float]]]],
    properties: Dict[str, Any],
    context: staticmaps.Context,
) -> None:
    """Plot MultiPolygon geometry."""
    polygons = []
    for polygon_coords in coords:
        for ring in polygon_coords:
            # Convert lon, lat to lat, lon tuples
            polygon = [(coord[1], coord[0]) for coord in ring]
            polygons.append(polygon)

    color = _extract_color_from_properties(properties)
    width = _extract_width_from_properties(properties)

    add_polygons(context, polygons, colors=[color], width=width)


def plot_geojson(
    geojson_data: Union[str, Dict[str, Any]],
    tile_provider: Any = tp,
    window_size: Tuple[int, int] = (500, 400),
    zoom: int = 0,
    set_zoom: Optional[int] = None,
    context: Optional[staticmaps.Context] = None,
) -> Image:
    """Plot GeoJSON data on a map.

    Args:
        geojson_data: GeoJSON as string, dict, or file path
        tile_provider: Map tile provider
        window_size: Output image size (width, height)
        zoom: Zoom level adjustment
        set_zoom: Override automatic zoom level
        context: Optional existing staticmaps context

    Returns:
        PIL Image with plotted GeoJSON data

    Raises:
        ValueError: If GeoJSON is invalid or contains unsupported geometry types
    """
    if context is None:
        context = staticmaps.Context()

    context.set_tile_provider(tile_provider)

    # Parse GeoJSON
    geojson = parse_geojson(geojson_data)

    # Extract geometries
    geometries = extract_geometries(geojson)

    if not geometries:
        raise ValueError("No geometries found in GeoJSON")

    # Plot each geometry
    for geom_type, coords, properties in geometries:
        if geom_type == "Point":
            _plot_point_geometry(coords, properties, context)
        elif geom_type == "MultiPoint":
            _plot_multipoint_geometry(coords, properties, context)
        elif geom_type == "LineString":
            _plot_linestring_geometry(coords, properties, context)
        elif geom_type == "MultiLineString":
            _plot_multilinestring_geometry(coords, properties, context)
        elif geom_type == "Polygon":
            _plot_polygon_geometry(coords, properties, context)
        elif geom_type == "MultiPolygon":
            _plot_multipolygon_geometry(coords, properties, context)
        else:
            raise ValueError(f"Unsupported geometry type: {geom_type}")

    zoom = plot_zoom(context, window_size, zoom, set_zoom)
    context.set_zoom(zoom)

    return context.render_pillow(*window_size)  # type: ignore


def plot_geojson_file(
    filepath: str,
    tile_provider: Any = tp,
    window_size: Tuple[int, int] = (500, 400),
    zoom: int = 0,
    set_zoom: Optional[int] = None,
    context: Optional[staticmaps.Context] = None,
) -> Image:
    """Plot GeoJSON data from a file.

    Args:
        filepath: Path to GeoJSON file
        tile_provider: Map tile provider
        window_size: Output image size (width, height)
        zoom: Zoom level adjustment
        set_zoom: Override automatic zoom level
        context: Optional existing staticmaps context

    Returns:
        PIL Image with plotted GeoJSON data

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If GeoJSON is invalid
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            geojson_data = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"GeoJSON file not found: {filepath}")

    return plot_geojson(
        geojson_data,
        tile_provider=tile_provider,
        window_size=window_size,
        zoom=zoom,
        set_zoom=set_zoom,
        context=context,
    )
