"""Regenerate the real-tile maps used by the documentation.

Requires network access to the default OpenStreetMap tile provider. Install
``landfall[geo]`` to include the GeoPandas example.
"""

from pathlib import Path

import landfall

OUTPUT = Path(__file__).resolve().parents[1] / "docs" / "images"
SIZE = (640, 440)
PLACES = [(27.88, -82.49), (27.92, -82.46), (27.94, -82.44)]
ROUTE = [(27.88, -82.49), (27.90, -82.47), (27.92, -82.46), (27.94, -82.44)]
BOUNDARY = [
    (27.87, -82.50),
    (27.93, -82.50),
    (27.93, -82.43),
    (27.87, -82.43),
]


def save(image, name):
    OUTPUT.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT / name, optimize=True)
    print(OUTPUT / name)


def main():
    save(
        landfall.plot_points(
            PLACES, colors="distinct", point_size=14, window_size=SIZE, zoom=-1
        ),
        "points.png",
    )
    save(
        landfall.plot_line(ROUTE, color="#d12c31", width=5, window_size=SIZE, zoom=-1),
        "route.png",
    )
    save(
        landfall.plot_polygon(
            BOUNDARY,
            color="#154e9e",
            fill_color="#154e9e55",
            width=3,
            window_size=SIZE,
        ),
        "polygon.png",
    )
    save(
        landfall.plot_circle(
            27.88,
            -82.49,
            1000,
            color="#9b2727",
            fill_color="#d12c3155",
            width=3,
            window_size=SIZE,
        ),
        "circle.png",
    )

    context = landfall.Context()
    context.add_points([27.88, 27.92], [-82.49, -82.46], colors=["blue", "red"])
    context.add_line(ROUTE, color="#d12c31", width=4)
    context.add_polygon(
        BOUNDARY,
        color="#154e9e",
        fill_color="#154e9e44",
        holes=[
            [
                (27.89, -82.48),
                (27.91, -82.48),
                (27.91, -82.46),
                (27.89, -82.46),
            ]
        ],
    )
    save(context.render_pillow(*SIZE), "layers.png")

    feature = {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": [[lon, lat] for lat, lon in ROUTE],
        },
        "properties": {"stroke": "#d12c31", "stroke-width": 5},
    }
    save(landfall.plot_geojson(feature, window_size=SIZE, zoom=-1), "geojson.png")

    try:
        import geopandas as gpd
        from shapely.geometry import Point
    except ImportError:
        print("Skipping GeoPandas map; install landfall[geo] to generate it")
    else:
        frame = gpd.GeoDataFrame(
            {"color": ["blue", "red", "green"], "size": [12, 16, 12]},
            geometry=[Point(lon, lat) for lat, lon in PLACES],
            crs="EPSG:4326",
        )
        save(
            landfall.plot_geodataframe(
                frame,
                color_column="color",
                size_column="size",
                window_size=SIZE,
                zoom=-1,
            ),
            "geodataframe.png",
        )


if __name__ == "__main__":
    main()
