"""Plot GeoPandas and Shapely geometries in geographic coordinates."""

from typing import Any, List, Optional, Sequence, Tuple, Union

import staticmaps
from PIL.Image import Image

from landfall.color import process_colors
from landfall.geojson import add_geometry, extract_geometries
from landfall.plot import plot_zoom

tp = staticmaps.tile_provider_OSM


def _check_geopandas_available() -> None:
    try:
        import geopandas  # noqa: F401
        import shapely  # noqa: F401
    except ImportError as error:
        raise ImportError(
            "GeoPandas not installed. Install with: pip install landfall[geo]"
        ) from error


def _add_geometry(
    context: staticmaps.Context, geometry: Any, color: Any, size: int = 10
) -> bool:
    if geometry is None or geometry.is_empty:
        return False
    for kind, coords, _ in extract_geometries(geometry.__geo_interface__):
        add_geometry(context, kind, coords, {"color": color, "marker-size": size})
    return True


def _render(
    context: staticmaps.Context,
    window_size: Tuple[int, int],
    zoom: int,
    set_zoom: Optional[int],
) -> Image:
    context.set_zoom(plot_zoom(context, window_size, zoom, set_zoom))
    return context.render_pillow(*window_size)  # type: ignore[no-any-return]


def plot_geometry(
    geometry: Any,
    tile_provider: Any = tp,
    window_size: Tuple[int, int] = (500, 400),
    zoom: int = 0,
    set_zoom: Optional[int] = None,
    context: Optional[staticmaps.Context] = None,
) -> Image:
    """Plot a Shapely geometry in WGS84 (longitude, latitude) coordinates.

    Polygon holes, multipart shapes, and GeometryCollections are preserved.
    Empty geometries raise ValueError.
    """
    _check_geopandas_available()
    if context is None:
        context = staticmaps.Context()
    context.set_tile_provider(tile_provider)
    if not _add_geometry(context, geometry, "blue"):
        raise ValueError("No non-empty geometries to plot")
    return _render(context, window_size, zoom, set_zoom)


def plot_geometries(
    geometries: Sequence[Any],
    tile_provider: Any = tp,
    colors: Optional[Union[Sequence[Any], str]] = None,
    window_size: Tuple[int, int] = (500, 400),
    zoom: int = 0,
    set_zoom: Optional[int] = None,
    context: Optional[staticmaps.Context] = None,
) -> Image:
    """Plot WGS84 Shapely geometries; skip null or empty entries.

    Colors may be a palette name, a single-item list to broadcast, or one
    color per input geometry. Empty inputs raise ValueError.
    """
    _check_geopandas_available()
    if context is None:
        context = staticmaps.Context()
    context.set_tile_provider(tile_provider)
    palette = process_colors(
        colors if colors is not None else ["blue"], len(geometries)
    )
    added = False
    for geometry, color in zip(geometries, palette):
        added = _add_geometry(context, geometry, color) or added
    if not added:
        raise ValueError("No non-empty geometries to plot")
    return _render(context, window_size, zoom, set_zoom)


def _extract_gdf_colors(
    gdf: Any, color_column: Optional[str] = None
) -> Optional[List[str]]:
    if color_column is None or color_column not in gdf.columns:
        return None
    return list(gdf[color_column].astype(str))


def _extract_gdf_sizes(
    gdf: Any, size_column: Optional[str] = None
) -> Optional[List[int]]:
    if size_column is None or size_column not in gdf.columns:
        return None
    try:
        return list(gdf[size_column].astype(int))
    except (ValueError, TypeError, OverflowError) as error:
        raise ValueError("size_column must contain integer marker sizes") from error


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
    """Plot a GeoDataFrame, reprojecting its selected geometry to WGS84.

    Frames without a CRS are assumed to contain longitude/latitude values.
    color_column contains color names or hex values; size_column controls
    marker sizes. Styling follows row position regardless of index labels.
    Empty geometries are skipped; an entirely empty frame raises ValueError.
    """
    _check_geopandas_available()
    if geometry_column is None:
        try:
            geometry_column = gdf.geometry.name
        except AttributeError as error:
            raise ValueError("GeoDataFrame has no geometry column") from error
    if geometry_column not in gdf.columns:
        raise ValueError(
            f"Geometry column '{geometry_column}' not found in GeoDataFrame"
        )
    import geopandas as gpd

    geometries = gpd.GeoSeries(gdf[geometry_column])
    if geometries.crs is not None:
        geometries = geometries.to_crs(epsg=4326)
    gdf_colors = _extract_gdf_colors(gdf, color_column)
    palette = process_colors(
        gdf_colors
        if gdf_colors is not None
        else colors
        if colors is not None
        else ["blue"],
        len(gdf),
    )
    sizes = _extract_gdf_sizes(gdf, size_column)
    if context is None:
        context = staticmaps.Context()
    context.set_tile_provider(tile_provider)
    added = False
    for position, geometry in enumerate(geometries):
        size = sizes[position] if sizes is not None else 10
        added = _add_geometry(context, geometry, palette[position], size) or added
    if not added:
        raise ValueError("No non-empty geometries to plot")
    return _render(context, window_size, zoom, set_zoom)
