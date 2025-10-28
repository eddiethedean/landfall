# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
