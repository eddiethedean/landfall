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

- 🗺️ **Easy geospatial plotting** - Plot points and polygons on static maps
- 🎨 **Smart color generation** - Automatic distinct color generation for data visualization
- 🔧 **Type-safe** - Full type annotations with mypy support
- 🧪 **Well-tested** - 105+ tests with 80% coverage across Python 3.8-3.13
- 🚀 **Modern packaging** - Built with modern `pyproject.toml` standards
- 🔄 **Cross-platform** - Works on Windows, macOS, and Linux
- 📦 **Minimal dependencies** - Only essential packages required

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

This installs the package in editable mode with development dependencies including:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `mypy` - Type checking
- `flake8` - Linting
- `tox` - Multi-environment testing

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

## API Reference

### Core Functions

- `plot_points(lats, lons, **kwargs)` - Plot points on a map
- `plot_polygon(polygon, **kwargs)` - Plot a single polygon
- `plot_polygons(polygons, **kwargs)` - Plot multiple polygons
- `random_color(rng=None)` - Generate a random color
- `Context()` - Enhanced context for complex maps

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