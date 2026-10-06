"""
Functions for plotting GeoJSON data.
"""

import json
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import staticmaps
from PIL.Image import Image

from landfall.lines import add_lines
from landfall.plot import plot_zoom, set_tile_provider
from landfall.points import add_points
from landfall.polygons import add_polygon
from landfall.validation import create_latlng

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
    if not isinstance(geojson, dict):
        raise ValueError("GeoJSON must be an object")
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
        "GeometryCollection",
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

    def extract(
        data: Any, properties: Dict[str, Any]
    ) -> List[Tuple[str, Any, Dict[str, Any]]]:
        data = parse_geojson(data)
        kind = data["type"]
        if kind == "Feature":
            props = data.get("properties")
            if props is None:
                props = {}
            if not isinstance(props, dict):
                raise ValueError("Feature properties must be an object or null")
            if "geometry" not in data:
                raise ValueError("Feature must have 'geometry' field")
            geometry = data["geometry"]
            if geometry is None:
                return []
            if not isinstance(geometry, dict) or geometry.get("type") in (
                "Feature",
                "FeatureCollection",
            ):
                raise ValueError("Feature geometry must be a geometry object or null")
            return extract(geometry, props)
        if kind in ("FeatureCollection", "GeometryCollection"):
            key = "features" if kind == "FeatureCollection" else "geometries"
            members = data.get(key)
            if not isinstance(members, (list, tuple)):
                raise ValueError(f"{kind} must have a '{key}' array")
            result = []
            for member in members:
                if kind == "FeatureCollection" and (
                    not isinstance(member, dict) or member.get("type") != "Feature"
                ):
                    raise ValueError("FeatureCollection members must be Features")
                if kind == "GeometryCollection" and (
                    not isinstance(member, dict)
                    or member.get("type") in ("Feature", "FeatureCollection")
                ):
                    raise ValueError("GeometryCollection members must be geometries")
                result.extend(extract(member, properties))
            return result
        if "coordinates" not in data:
            raise ValueError(f"{kind} must have 'coordinates' field")
        return [(kind, data["coordinates"], properties)]

    return extract(geojson, {})


def _extract_color_from_properties(
    properties: Dict[str, Any], default_color: str = "blue"
) -> Any:
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
            return properties[key]
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
    if not isinstance(coords, (list, tuple)) or len(coords) < 2:
        raise ValueError("Point coordinates must have at least 2 values")

    # GeoJSON uses lon, lat order
    lon, lat = coords[:2]
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
        if not isinstance(coord, (list, tuple)) or len(coord) < 2:
            raise ValueError("Point coordinates must have at least 2 values")
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
    line = _coordinate_pairs(coords)

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
        line = _coordinate_pairs(line_coords)
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
    if not isinstance(coords, (list, tuple)):
        raise ValueError("Polygon coordinates must be an array of rings")
    if not coords:
        return
    rings = [_coordinate_pairs(ring) for ring in coords]

    color = _extract_color_from_properties(properties)
    width = _extract_width_from_properties(properties)

    from landfall.color import convert_color

    fill_color = convert_color(properties.get("fill", "#ff000064"))
    opacity = properties.get("fill-opacity")
    if opacity is not None:
        try:
            alpha = float(opacity)
        except (ValueError, TypeError) as error:
            raise ValueError("fill-opacity must be between 0 and 1") from error
        if not 0 <= alpha <= 1:
            raise ValueError("fill-opacity must be between 0 and 1")
        fill_color = staticmaps.Color(*fill_color.int_rgb(), round(alpha * 255))
    add_polygon(
        context,
        rings[0],
        color=convert_color(color),
        fill_color=fill_color,
        width=width,
        holes=rings[1:],
    )


def _plot_multipolygon_geometry(
    coords: List[List[List[List[float]]]],
    properties: Dict[str, Any],
    context: staticmaps.Context,
) -> None:
    """Plot MultiPolygon geometry."""
    for polygon_coords in coords:
        _plot_polygon_geometry(polygon_coords, properties, context)


def _coordinate_pairs(coordinates: Any) -> List[Tuple[float, float]]:
    if not isinstance(coordinates, (list, tuple)):
        raise ValueError("coordinates must be an array of positions")
    pairs = []
    for position in coordinates:
        if not isinstance(position, (list, tuple)) or len(position) < 2:
            raise ValueError("positions must have at least 2 values")
        lon, lat = position[:2]
        create_latlng(lat, lon)
        pairs.append((lat, lon))
    return pairs


def add_geometry(
    context: staticmaps.Context,
    geometry_type: str,
    coordinates: Any,
    properties: Dict[str, Any],
) -> None:
    """Add a geometry, preserving multi-part shapes and polygon holes."""
    handlers: Dict[str, Callable[[Any, Dict[str, Any], staticmaps.Context], None]] = {
        "Point": _plot_point_geometry,
        "MultiPoint": _plot_multipoint_geometry,
        "LineString": _plot_linestring_geometry,
        "MultiLineString": _plot_multilinestring_geometry,
        "Polygon": _plot_polygon_geometry,
        "MultiPolygon": _plot_multipolygon_geometry,
    }
    if geometry_type not in handlers:
        raise ValueError(f"Unsupported geometry type: {geometry_type}")
    if not isinstance(coordinates, (list, tuple)):
        raise ValueError(f"{geometry_type} coordinates must be an array")
    handlers[geometry_type](coordinates, properties, context)


def plot_geojson(
    geojson_data: Union[str, Dict[str, Any]],
    tile_provider: Any = tp,
    window_size: Tuple[int, int] = (500, 400),
    zoom: int = 0,
    set_zoom: Optional[int] = None,
    context: Optional[staticmaps.Context] = None,
    api_key: Optional[str] = None,
) -> Image:
    """Plot GeoJSON data on a map.

    Args:
        geojson_data: GeoJSON as string or dict
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

    set_tile_provider(context, tile_provider, api_key)

    # Parse GeoJSON
    geojson = parse_geojson(geojson_data)

    # Extract geometries
    geometries = extract_geometries(geojson)

    if not geometries:
        raise ValueError("No geometries found in GeoJSON")

    for geom_type, coords, properties in geometries:
        add_geometry(context, geom_type, coords, properties)

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
    api_key: Optional[str] = None,
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
        api_key=api_key,
    )
