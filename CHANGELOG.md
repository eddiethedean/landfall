# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.3] - 2026-10-02

### Changed
- Replace the project artwork with a coastal location-pin logo in the README,
  documentation header, and favicon.

## [0.4.2] - 2026-10-02

### Fixed
- Circle radii now convert meters to the kilometers expected by py-staticmaps;
  a 1,000-meter radius no longer produces a 1,000-kilometer circle.
- Batch lines and polygons flip longitude/latitude coordinates exactly once.
- Point coordinate pairs are unpacked correctly when longitudes are omitted.
- Single-item color lists apply to all shapes instead of silently dropping data.
- Multipart GeoJSON and Shapely geometries retain every component.
- Polygon holes preserve the background and underlying objects in Pillow, SVG,
  and Cairo; native polygons close the final boundary edge.
- GeoDataFrame styling follows row position rather than index labels and respects
  the selected geometry column's CRS, reprojecting to WGS84 when available.
- GeoDataFrame palette names and missing geometry columns now behave consistently.
- Shapely and GeoDataFrame helpers accept literal `colors="red"` as well as
  generated palette names; styles for null or empty geometry rows are ignored.
- Transparent polygon outlines no longer erase the fill beneath them in Pillow.
- A fill alpha of zero remains fully transparent.
- Seeded random palettes generate a sequence of colors without changing global
  random state; ID palettes follow first appearance rather than set order.
- Singular Context geometry methods accept documented default styling and color names.

### Added
- Nested GeoJSON/Shapely GeometryCollection support, null Feature properties,
  and GeoJSON positions with altitude (ignored for two-dimensional plotting).
- Validation for mismatched coordinates, radii, colors, IDs, invalid coordinates,
  and non-finite or negative circle radii. These now raise ValueError.
- Regression tests checking object counts, actual coordinates, geodesic radius,
  styling, reprojection, and transparent holes in rendered images.
- Optional integration CI across platforms, installed-wheel tests, coverage floor,
  and source/wheel metadata validation with downloadable build artifacts.

### Changed
- Require py-staticmaps >=0.5.0 for native support of current Pillow APIs.
- Importing Landfall no longer patches Pillow globally or imports GeoPandas eagerly.
- Optional plotting APIs remain available without the geo extra and raise a helpful
  ImportError when called without it. Entirely empty Shapely inputs raise ValueError.
- Development dependency markers preserve installation on Python 3.8.
- Replace stale flake8 instructions with project-local Ruff configuration.
- Refresh README examples and release documentation to match the public API.
- Add a Read the Docs-ready MkDocs site with task-based guides, API reference,
  strict CI build, executable examples, and maps rendered from real tiles.

## [0.4.1] - 2025-01-27

### Fixed
- **CI/CD Pipeline** - Fixed GitHub Actions workflow compatibility issues
- **Linting** - Replaced flake8 with ruff for consistent code quality checks
- **Test Environment** - Fixed tox configuration for cross-platform compatibility
- **Python Paths** - Removed hardcoded local Python paths from tox.ini

### Technical Improvements
- Updated GitHub Actions workflow to use ruff instead of flake8
- Added ruff to dev dependencies for consistent linting
- Fixed tox.ini to use generic python3.x commands instead of absolute paths
- Ensured CI/CD works across all supported Python versions (3.8-3.13) and operating systems

## [0.4.0] - 2025-01-27

### Added
- **Line/Polyline plotting** - `plot_line()`, `plot_lines()` for routes and paths
- **Circle plotting** - `plot_circle()`, `plot_circles()` for buffer zones and coverage areas
- **GeoJSON support** - `plot_geojson()`, `plot_geojson_file()` for industry-standard format
- **GeoPandas integration** - Optional `plot_geodataframe()`, `plot_geometry()`, `plot_geometries()` for GeoDataFrame support
- New Context methods: `add_line()`, `add_lines()`, `add_circle()`, `add_circles()`
- Optional `[geo]` dependency group for GeoPandas/Shapely integration
- Comprehensive test coverage for all new features (77+ new tests)
- Support for radius units (meters/kilometers) in circle plotting
- GeoJSON property extraction for styling (stroke, fill, marker-color, etc.)
- Coordinate order handling (lat/lon vs lon/lat) across all new features

### Changed
- Expanded API surface with 8+ new functions
- Enhanced Context class with geometry methods
- Updated test count from 105+ to 180+ tests
- Improved error handling and validation

### Documentation
- Added comprehensive examples for all new features
- Updated API reference with new functions
- Added installation instructions for GeoPandas support
- Enhanced README with practical usage examples

## [0.3.6] - 2024-12-28

### Added
- **Comprehensive README upgrade** - Modern, feature-rich documentation with examples
- **Enhanced API documentation** - Complete function reference and usage examples
- **Development workflow documentation** - Detailed setup and testing instructions
- **Multi-version testing verification** - Confirmed compatibility across Python 3.8-3.13

### Changed
- **Version bump** - Updated to v0.3.6 reflecting full modernization completion
- **Documentation structure** - Reorganized README with clear sections and examples
- **Development instructions** - Added comprehensive development setup guide

## [0.3.5] - 2024-12-28
- Support for Python 3.9, 3.11, 3.12, and 3.13
- Comprehensive type hints throughout the codebase
- Modern pyproject.toml-only packaging configuration
- Development dependencies as optional extras
- Separate linting job in CI/CD pipeline
- CHANGELOG.md for tracking changes

### Changed
- Migrated from setup.cfg to modern pyproject.toml configuration
- Updated all development dependencies to latest versions:
  - pytest: 6.2.5 → 8.3.x
  - pytest-cov: 2.12.1 → 6.0.x
  - mypy: 0.910 → 1.13.x
  - flake8: 3.9.2 → 7.1.x
- Updated GitHub Actions to v4/v5 (from deprecated v2)
- Standardized parameter naming: `tileprovider` → `tile_provider`
- Improved error messages with actual type information
- Enhanced CI/CD with pip caching and separate linting job

### Fixed
- **Critical**: Fixed integer conversion bug in `distinctipy.py` that was severely muting colors
- **Security**: Removed Pillow version pin (was `<=9.5.0`, now `>=10.0.0`)
- Fixed typo: `get_distict_colors` → `get_distinct_colors` (with backward compatibility)
- Fixed wrong package name in metadata ("trashpandas" → "landfall")
- Replaced unsafe `type(x) is str` with `isinstance(x, str)` checks
- Removed trailing whitespace and improved code formatting

### Deprecated
- `get_distict_colors()` function (use `get_distinct_colors()` instead)

### Removed
- Legacy `setup.cfg` configuration file
- Obsolete requirements files (replaced with pyproject.toml extras)
- Debugging utilities and icecream dependency (simplified package)

## [0.3.5] - 2023-08-01

### Added
- Initial release with basic geospatial plotting functionality
- Support for plotting points and polygons on static maps
- Color generation utilities (random, distinct, wheel colors)
- Context wrapper for staticmaps integration

### Dependencies
- py-staticmaps
- distinctipy
- Pillow<=9.5.0
