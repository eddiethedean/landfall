![Landfall Logo](https://raw.githubusercontent.com/eddiethedean/landfall/main/docs/landfall_logo.png)
-----------------

# Landfall: Easy to use functions for plotting geographic data on static maps
[![PyPI Latest Release](https://img.shields.io/pypi/v/landfall.svg)](https://pypi.org/project/landfall/)
![Tests](https://github.com/eddiethedean/landfall/actions/workflows/tests.yml/badge.svg)
[![Python Support](https://img.shields.io/pypi/pyversions/landfall.svg)](https://pypi.org/project/landfall/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What is it?

**Landfall** is a modern, well-tested Python package with easy-to-use functions for plotting geographic data on static maps. Built with type safety, comprehensive testing, and cross-platform compatibility in mind.

## ✨ Features

- 🗺️ **Easy geospatial plotting** - Plot points, polygons, lines, and circles on static maps
- 🎨 **Smart color generation** - Automatic distinct color generation for data visualization
- 📍 **GeoJSON support** - Plot industry-standard GeoJSON data directly
- 🐼 **GeoPandas integration** - Optional integration with GeoDataFrames and Shapely geometries
- 🔧 **Type-safe** - Full type annotations with mypy support
- 🧪 **Well-tested** - 182+ tests with comprehensive coverage across Python 3.8-3.13
- 🚀 **Modern packaging** - Built with modern `pyproject.toml` standards
- 🔄 **Cross-platform** - Works on Windows, macOS, and Linux
- 📦 **Minimal dependencies** - Only essential packages required

## 🆕 What's New in v0.4.0

**Major feature expansion with 4 new plotting capabilities:**

- 🛣️ **Line/Polyline Plotting** - Plot routes, paths, and linear features with `plot_line()` and `plot_lines()`
- ⭕ **Circle/Buffer Plotting** - Create coverage areas and buffer zones with `plot_circle()` and `plot_circles()`
- 📄 **GeoJSON Support** - Plot industry-standard GeoJSON data directly with `plot_geojson()` and `plot_geojson_file()`
- 🐼 **GeoPandas Integration** - Optional GeoDataFrame support with `plot_geodataframe()`, `plot_geometry()`, and `plot_geometries()`

**Plus enhanced Context class with new methods:**
- `add_line()`, `add_lines()` - Add lines to existing maps
- `add_circle()`, `add_circles()` - Add circles to existing maps

**Installation for GeoPandas support:**
```bash
pip install landfall[geo]
```

## Requirements

- **Python 3.8-3.13** (comprehensive version support)
- **Pillow >=10.0.0** (image processing)
- **py-staticmaps** (map rendering)
- **distinctipy** (color generation)

## Installation

### From PyPI
```sh
pip install landfall
```

### Development Installation
```sh
pip install -e .[dev]
```

### With GeoPandas Support
```sh
pip install landfall[geo]
```

This installs the package in editable mode with development dependencies including:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `mypy` - Type checking
- `flake8` - Linting
- `tox` - Multi-environment testing

**GeoPandas extras include:**
- `geopandas>=0.14.0` - GeoDataFrame support
- `shapely>=2.0.0` - Geometry operations

## Quick Start

### Basic Point Plotting
```python
import landfall

# Plot points on a map
lats = [27.88, 27.92, 27.94]
lons = [-82.49, -82.49, -82.46]

landfall.plot_points(lats, lons)
```

### Advanced Plotting with Colors
```python
import landfall

# Plot points with distinct colors
lats = [27.88, 27.92, 27.94, 27.96]
lons = [-82.49, -82.49, -82.46, -82.44]

# Use distinct colors for each point
landfall.plot_points(lats, lons, colors="distinct")

# Or use custom colors
landfall.plot_points(lats, lons, colors=["red", "blue", "green", "yellow"])
```

### Polygon Plotting
```python
import landfall

# Define polygon coordinates
polygon = [
    (27.88, -82.49),
    (27.92, -82.49), 
    (27.94, -82.46),
    (27.88, -82.46)
]

# Plot polygon with fill
landfall.plot_polygon(polygon, fill_color="blue", color="red")
```

### Using the Enhanced Context
```python
import landfall

# Create a context for complex maps
context = landfall.Context()

# Add multiple elements
context.add_points([27.88, 27.92], [-82.49, -82.46], colors="distinct")
context.add_polygon(polygon, fill_color="blue", color="red", width=2)

# Render the map
image = context.render_pillow(800, 600)
```

### Line Plotting
```python
import landfall

# Plot lines/routes on a map
lines = [
    [(27.88, -82.49), (27.92, -82.46), (27.94, -82.44)],  # Route 1
    [(27.90, -82.50), (27.95, -82.45), (27.98, -82.42)]   # Route 2
]

# Plot multiple lines with distinct colors
landfall.plot_lines(lines, colors="distinct", width=3)

# Plot single line
line = [(27.88, -82.49), (27.92, -82.46), (27.94, -82.44)]
landfall.plot_line(line, color="red", width=2)
```

### Circle/Buffer Plotting
```python
import landfall

# Plot circles for coverage areas
lats = [27.88, 27.92, 27.94]
lons = [-82.49, -82.46, -82.44]
radii = [1000, 2000, 1500]  # meters

# Plot circles with fill colors
landfall.plot_circles(lats, lons, radii, 
                     fill_colors="distinct", 
                     radius_unit="meters")

# Plot single circle
landfall.plot_circle(27.88, -82.49, 1000, 
                    fill_color="blue", 
                    color="red", 
                    radius_unit="meters")
```

### GeoJSON Support
```python
import landfall

# Plot GeoJSON data directly
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-82.49, 27.88]
            },
            "properties": {
                "name": "Location 1",
                "marker-color": "red"
            }
        }
    ]
}

# Plot GeoJSON from dict
landfall.plot_geojson(geojson_data)

# Plot GeoJSON from file
landfall.plot_geojson_file("data.geojson")
```

### GeoPandas Integration (Optional)
```python
import landfall
import geopandas as gpd
from shapely.geometry import Point

# Create GeoDataFrame
data = {'name': ['A', 'B', 'C'], 'value': [10, 20, 30]}
geometry = [Point(-82.49, 27.88), Point(-82.46, 27.92), Point(-82.44, 27.96)]
gdf = gpd.GeoDataFrame(data, geometry=geometry)

# Plot GeoDataFrame directly
landfall.plot_geodataframe(gdf, color_column="value")

# Plot individual Shapely geometries
point = Point(-82.49, 27.88)
landfall.plot_geometry(point)
```

### Using the Enhanced Context
```python
import landfall

# Create a context for complex maps
context = landfall.Context()

# Add multiple elements
context.add_points([27.88, 27.92], [-82.49, -82.46], colors="distinct")
context.add_polygon(polygon, fill_color="blue", color="red", width=2)
context.add_lines(lines, colors="random", width=2)
context.add_circles([27.88], [-82.49], [1000], fill_color="yellow")

# Render the map
image = context.render_pillow(800, 600)
```

## API Reference

### Core Functions

- `plot_points(lats, lons, **kwargs)` - Plot points on a map
- `plot_polygon(polygon, **kwargs)` - Plot a single polygon
- `plot_polygons(polygons, **kwargs)` - Plot multiple polygons
- `plot_line(line, **kwargs)` - Plot a single line/polyline
- `plot_lines(lines, **kwargs)` - Plot multiple lines/polylines
- `plot_circle(lat, lon, radius, **kwargs)` - Plot a single circle
- `plot_circles(lats, lons, radii, **kwargs)` - Plot multiple circles
- `plot_geojson(geojson_data, **kwargs)` - Plot GeoJSON data
- `plot_geojson_file(filepath, **kwargs)` - Plot GeoJSON from file
- `random_color(rng=None)` - Generate a random color
- `Context()` - Enhanced context for complex maps

### GeoPandas Functions (Optional)

- `plot_geodataframe(gdf, **kwargs)` - Plot GeoDataFrame
- `plot_geometry(geometry, **kwargs)` - Plot Shapely geometry
- `plot_geometries(geometries, **kwargs)` - Plot multiple geometries

### Color Options

- `"random"` - Generate random colors
- `"distinct"` - Generate visually distinct colors
- `"wheel"` - Generate colors from HSV color wheel
- Custom color list: `["red", "blue", "green"]`
- RGB tuples: `[(255, 0, 0), (0, 255, 0)]`

## Development

### Setup Development Environment
```sh
git clone https://github.com/eddiethedean/landfall.git
cd landfall
pip install -e .[dev]
```

### Running Tests
```sh
# Run all tests
pytest

# Run with coverage
pytest --cov=landfall

# Run specific test categories
pytest tests/test_colors.py      # Color-related tests
pytest tests/test_plotting.py    # Plotting tests
pytest tests/test_comprehensive.py  # Comprehensive tests

# Run tests excluding slow tests
pytest -m "not slow"

# Run tests across all Python versions
tox
```

### Code Quality
```sh
# Linting
flake8 src tests

# Type checking
mypy src

# Formatting
ruff format src tests

# All quality checks
tox -e flake8,mypy
```

### Multi-Version Testing
```sh
# Test across all supported Python versions (3.8-3.13)
tox

# Test specific Python versions
tox -e py38,py311,py313
```

## Dependencies

- **[py-staticmaps](https://github.com/flopp/py-staticmaps)** - Static map image generation
- **[distinctipy](https://github.com/alan-turing-institute/distinctipy)** - Visually distinct color generation
- **[Pillow](https://python-pillow.org/)** - Python Imaging Library

## Changelog

### v0.3.6 (Latest)
- ✅ **Full modernization** - Migrated to modern `pyproject.toml` packaging
- ✅ **Enhanced testing** - 105+ tests with 80% coverage across Python 3.8-3.13
- ✅ **Type safety** - Complete type annotations with mypy support
- ✅ **Bug fixes** - Fixed critical color scaling bug in `distinctipy` integration
- ✅ **Cross-platform** - Verified compatibility across Windows, macOS, and Linux
- ✅ **Modern CI/CD** - Updated GitHub Actions with pip caching and separate linting
- ✅ **Compatibility patches** - Automatic fixes for Pillow compatibility issues

### Previous Versions
- v0.3.5 - Initial modernization and bug fixes
- v0.3.4 and earlier - Legacy versions

## Contributing

We welcome contributions! Please see our development guidelines:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature-name`
3. **Make your changes** with tests
4. **Run quality checks**: `tox -e flake8,mypy`
5. **Run tests**: `tox`
6. **Submit a pull request**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📖 **Documentation**: [GitHub README](https://github.com/eddiethedean/landfall#readme)
- 🐛 **Issues**: [GitHub Issues](https://github.com/eddiethedean/landfall/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/eddiethedean/landfall/discussions)

---

**Made with ❤️ for the geospatial Python community**