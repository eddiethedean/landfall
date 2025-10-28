"""
Test GeoJSON plotting functionality.
"""

import json
import pytest
from PIL import Image

from landfall import plot_geojson, plot_geojson_file
from landfall.geojson import parse_geojson, extract_geometries
from tests.mock_tile_downloader import MockTileDownloader


@pytest.fixture
def mock_context():
    """Create a context with mock tile downloader for testing."""
    from landfall.context import Context

    context = Context()
    context.set_tile_downloader(MockTileDownloader())
    return context


@pytest.fixture
def sample_point_geojson():
    """Sample Point GeoJSON."""
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [-82.49, 27.88]},
        "properties": {"name": "Test Point", "marker-color": "red"},
    }


@pytest.fixture
def sample_linestring_geojson():
    """Sample LineString GeoJSON."""
    return {
        "type": "Feature",
        "geometry": {
            "type": "LineString",
            "coordinates": [[-82.49, 27.88], [-82.46, 27.92], [-82.44, 27.96]],
        },
        "properties": {"name": "Test Line", "stroke": "blue", "stroke-width": 3},
    }


@pytest.fixture
def sample_polygon_geojson():
    """Sample Polygon GeoJSON."""
    return {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [-82.49, 27.88],
                    [-82.46, 27.88],
                    [-82.46, 27.92],
                    [-82.49, 27.92],
                    [-82.49, 27.88],
                ]
            ],
        },
        "properties": {"name": "Test Polygon", "fill": "green", "stroke": "red"},
    }


@pytest.fixture
def sample_featurecollection_geojson():
    """Sample FeatureCollection GeoJSON."""
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [-82.49, 27.88]},
                "properties": {"name": "Point 1"},
            },
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [-82.46, 27.92]},
                "properties": {"name": "Point 2"},
            },
        ],
    }


class TestGeoJSONParsing:
    """Test GeoJSON parsing functionality."""

    def test_parse_geojson_dict(self):
        """Test parsing GeoJSON from dict."""
        geojson = {"type": "Point", "coordinates": [-82.49, 27.88]}
        result = parse_geojson(geojson)
        assert result["type"] == "Point"
        assert result["coordinates"] == [-82.49, 27.88]

    def test_parse_geojson_string(self):
        """Test parsing GeoJSON from string."""
        geojson_str = '{"type": "Point", "coordinates": [-82.49, 27.88]}'
        result = parse_geojson(geojson_str)
        assert result["type"] == "Point"
        assert result["coordinates"] == [-82.49, 27.88]

    def test_parse_invalid_json(self):
        """Test parsing invalid JSON."""
        with pytest.raises(ValueError, match="Invalid JSON"):
            parse_geojson("invalid json")

    def test_parse_invalid_type(self):
        """Test parsing GeoJSON with invalid type."""
        geojson = {"type": "InvalidType", "coordinates": []}
        with pytest.raises(ValueError, match="Unsupported GeoJSON type"):
            parse_geojson(geojson)

    def test_parse_missing_type(self):
        """Test parsing GeoJSON without type field."""
        geojson = {"coordinates": []}
        with pytest.raises(ValueError, match="GeoJSON must have 'type' field"):
            parse_geojson(geojson)

    def test_extract_geometries_feature(self, sample_point_geojson):
        """Test extracting geometries from Feature."""
        geometries = extract_geometries(sample_point_geojson)
        assert len(geometries) == 1
        geom_type, coords, props = geometries[0]
        assert geom_type == "Point"
        assert coords == [-82.49, 27.88]
        assert props["name"] == "Test Point"

    def test_extract_geometries_featurecollection(
        self, sample_featurecollection_geojson
    ):
        """Test extracting geometries from FeatureCollection."""
        geometries = extract_geometries(sample_featurecollection_geojson)
        assert len(geometries) == 2
        assert geometries[0][0] == "Point"
        assert geometries[1][0] == "Point"

    def test_extract_geometries_direct_geometry(self):
        """Test extracting geometries from direct geometry."""
        geojson = {"type": "Point", "coordinates": [-82.49, 27.88]}
        geometries = extract_geometries(geojson)
        assert len(geometries) == 1
        assert geometries[0][0] == "Point"


class TestGeoJSONPlotting:
    """Test GeoJSON plotting functionality."""

    def test_plot_point_geojson(self, mock_context, sample_point_geojson):
        """Test plotting Point GeoJSON."""
        img = plot_geojson(sample_point_geojson, context=mock_context)
        assert isinstance(img, Image.Image)
        assert img.size == (500, 400)

    def test_plot_linestring_geojson(self, mock_context, sample_linestring_geojson):
        """Test plotting LineString GeoJSON."""
        img = plot_geojson(sample_linestring_geojson, context=mock_context)
        assert isinstance(img, Image.Image)
        assert img.size == (500, 400)

    def test_plot_polygon_geojson(self, mock_context, sample_polygon_geojson):
        """Test plotting Polygon GeoJSON."""
        img = plot_geojson(sample_polygon_geojson, context=mock_context)
        assert isinstance(img, Image.Image)
        assert img.size == (500, 400)

    def test_plot_featurecollection_geojson(
        self, mock_context, sample_featurecollection_geojson
    ):
        """Test plotting FeatureCollection GeoJSON."""
        img = plot_geojson(sample_featurecollection_geojson, context=mock_context)
        assert isinstance(img, Image.Image)
        assert img.size == (500, 400)

    def test_plot_multipoint_geojson(self, mock_context):
        """Test plotting MultiPoint GeoJSON."""
        geojson = {
            "type": "Feature",
            "geometry": {
                "type": "MultiPoint",
                "coordinates": [[-82.49, 27.88], [-82.46, 27.92]],
            },
            "properties": {"marker-color": "blue"},
        }
        img = plot_geojson(geojson, context=mock_context)
        assert isinstance(img, Image.Image)

    def test_plot_multilinestring_geojson(self, mock_context):
        """Test plotting MultiLineString GeoJSON."""
        geojson = {
            "type": "Feature",
            "geometry": {
                "type": "MultiLineString",
                "coordinates": [
                    [[-82.49, 27.88], [-82.46, 27.92]],
                    [[-82.44, 27.96], [-82.41, 28.00]],
                ],
            },
            "properties": {"stroke": "red"},
        }
        img = plot_geojson(geojson, context=mock_context)
        assert isinstance(img, Image.Image)

    def test_plot_multipolygon_geojson(self, mock_context):
        """Test plotting MultiPolygon GeoJSON."""
        geojson = {
            "type": "Feature",
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [
                    [
                        [
                            [-82.49, 27.88],
                            [-82.46, 27.88],
                            [-82.46, 27.92],
                            [-82.49, 27.92],
                            [-82.49, 27.88],
                        ]
                    ],
                    [
                        [
                            [-82.44, 27.96],
                            [-82.41, 27.96],
                            [-82.41, 28.00],
                            [-82.44, 28.00],
                            [-82.44, 27.96],
                        ]
                    ],
                ],
            },
            "properties": {"fill": "yellow"},
        }
        img = plot_geojson(geojson, context=mock_context)
        assert isinstance(img, Image.Image)

    def test_plot_geojson_custom_size(self, mock_context, sample_point_geojson):
        """Test plotting GeoJSON with custom window size."""
        img = plot_geojson(
            sample_point_geojson, window_size=(800, 600), context=mock_context
        )
        assert isinstance(img, Image.Image)
        assert img.size == (800, 600)

    def test_plot_geojson_string_input(self, mock_context):
        """Test plotting GeoJSON from string."""
        geojson_str = '{"type": "Point", "coordinates": [-82.49, 27.88]}'
        img = plot_geojson(geojson_str, context=mock_context)
        assert isinstance(img, Image.Image)

    def test_plot_geojson_file(self, mock_context, tmp_path):
        """Test plotting GeoJSON from file."""
        geojson_data = {"type": "Point", "coordinates": [-82.49, 27.88]}

        file_path = tmp_path / "test.geojson"
        with open(file_path, "w") as f:
            json.dump(geojson_data, f)

        img = plot_geojson_file(str(file_path), context=mock_context)
        assert isinstance(img, Image.Image)

    def test_plot_geojson_file_not_found(self, mock_context):
        """Test plotting GeoJSON from non-existent file."""
        with pytest.raises(FileNotFoundError):
            plot_geojson_file("nonexistent.geojson", context=mock_context)

    def test_plot_empty_geojson(self, mock_context):
        """Test plotting GeoJSON with no geometries."""
        geojson = {"type": "FeatureCollection", "features": []}
        with pytest.raises(ValueError, match="No geometries found"):
            plot_geojson(geojson, context=mock_context)

    def test_plot_geojson_unsupported_geometry(self, mock_context):
        """Test plotting GeoJSON with unsupported geometry type."""
        geojson = {
            "type": "Feature",
            "geometry": {"type": "GeometryCollection", "geometries": []},
        }
        with pytest.raises(ValueError, match="No geometries found in GeoJSON"):
            plot_geojson(geojson, context=mock_context)


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_invalid_coordinate_format(self, mock_context):
        """Test handling invalid coordinate format."""
        geojson = {
            "type": "Point",
            "coordinates": "invalid",  # Should be [lon, lat]
        }
        with pytest.raises((ValueError, TypeError)):
            plot_geojson(geojson, context=mock_context)

    def test_missing_coordinates(self, mock_context):
        """Test handling missing coordinates."""
        geojson = {
            "type": "Point"
            # Missing coordinates
        }
        with pytest.raises((KeyError, ValueError)):
            plot_geojson(geojson, context=mock_context)

    def test_empty_coordinates(self, mock_context):
        """Test handling empty coordinates."""
        geojson = {"type": "Point", "coordinates": []}
        with pytest.raises((ValueError, IndexError)):
            plot_geojson(geojson, context=mock_context)

    def test_invalid_input_type(self, mock_context):
        """Test handling invalid input type."""
        with pytest.raises(ValueError, match="GeoJSON data must be string or dict"):
            plot_geojson(123, context=mock_context)
