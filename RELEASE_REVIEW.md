# Release reviews

## 0.4.3 release review

Released on October 3, 2026. The annotated
[`v0.4.3` tag](https://github.com/eddiethedean/landfall/tree/v0.4.3) points to
commit `8b59bfaedff9a82c402c6916f333ff60ca724d14`. The source distribution and
wheel were published to [PyPI](https://pypi.org/project/landfall/0.4.3/) through
Trusted Publishing. Both files are available and are not yanked.

This release introduces the coastal location-pin logo in the README,
documentation header, and favicon. Package metadata, the runtime version,
packaging checks, and the version regression test now use `0.4.3`.

### Validation

| Check | Result |
| --- | --- |
| Release workflow for tag `v0.4.3` | **Passed**; distribution build and PyPI publication both succeeded in the [release run](https://github.com/eddiethedean/landfall/actions/runs/37095073002). |
| Hosted CI for tag `v0.4.3` | **31 jobs passed** in the [tag test run](https://github.com/eddiethedean/landfall/actions/runs/37095072999). |
| Hosted CI for the matching `main` commit | **31 jobs passed** in the [main test run](https://github.com/eddiethedean/landfall/actions/runs/37095061438). |
| PyPI files | Confirmed `landfall-0.4.3-py3-none-any.whl` and `landfall-0.4.3.tar.gz`; uploaded at 04:02:18 and 04:02:20 UTC on October 3, 2026. |
| Fresh install from PyPI, Python 3.11 | Passed: distribution metadata and `landfall.__version__` both report `0.4.3`; core import does not eagerly load GeoPandas; offline point rendering returns a 320 × 240 Pillow image. |
| Local release checks | Installed-wheel Python 3.11 tests, Ruff lint and formatting, mypy, sdist/wheel builds, strict Twine validation, and strict MkDocs build passed. |

Install the published release with:

```sh
python -m pip install landfall==0.4.3
```

## 0.4.2 release review

Reviewed on October 2, 2026. The annotated `v0.4.2` tag points to commit
`23307420168a9d82b03cf9196e1b2adcdbfb240b` on `main`. The release-tag CI run
completed successfully with all 31 jobs passing. The source distribution and
wheel were published to PyPI through Trusted Publishing on October 2, 2026.
This review records the tag, CI result, and published artifacts; a GitHub
Release page has not been created.

### Findings resolved

| Impact | Finding | Resolution and evidence |
| --- | --- | --- |
| High | Circles were 1,000 times too large | Convert meters to renderer kilometers; regression tests measure the actual WGS84 distance for both unit options. |
| High | Batch lines/polygons flipped coordinates twice | Flip once in the singular helper; test asymmetric coordinates at real locations. |
| High | Short color lists silently omitted shapes | Broadcast one color, validate other lengths; inspect counts for points, lines, polygons, circles, and multipart geometries. |
| High | Polygon interior rings were filled as separate polygons | Preserve holes in Pillow, SVG, and Cairo; verify pixels, underlying objects, and SVG paths. |
| High | GeoDataFrame indexes were treated as array positions | Use row order; test integer, string, duplicate indexes, and null rows. |
| High | Projected CRS values were plotted as geographic coordinates | Reproject the selected geometry series to WGS84; test both active and alternate geometry columns. |
| Medium | Point pairs were unpacked incorrectly | Handle coordinate pairs directly, including longitude-first input. |
| Medium | Shapely MultiPoint and palette names failed | Use a shared geometry dispatcher and resolve palettes once per input. |
| Medium | GeometryCollections were skipped and null properties crashed | Traverse nested collections and normalize null properties; accept altitude for 2D plots. |
| Medium | Invalid inputs failed deep in rendering | Validate array lengths, colors, IDs, coordinate bounds, and finite non-negative radii with ValueError. |
| Medium | Fully transparent fills were ignored | Check alpha against None, preserving zero. |
| Medium | Random colors changed global state and repeated seeded colors | Use a local generator for each palette; preserve first-seen ID order. |
| Medium | Importing Landfall patched Pillow globally | Require py-staticmaps 0.5.0+, which uses textbbox; leave compatibility helpers explicit and load GeoPandas only when used. |
| Medium | CI skipped optional integrations and tested editable installs | Test wheels, optional extras, coverage, and distribution metadata; isolate coverage files per tox environment. |
| Low | Documentation and notebooks used stale APIs and providers | Refresh README/changelog, replace obsolete tile endpoint and parameter, execute all notebook cells offline. |

The baseline had **4 failing tests out of 202** when GeoPandas was installed.
Several other defects passed the old suite because it checked only that an
image was returned.

### Validation

| Check | Result |
| --- | --- |
| Complete suite, Python 3.11 with GeoPandas and Cairo | **292 passed**, **93.32% statement coverage** |
| Installed-wheel core tests, Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13 | All six environments passed; 258 tests per environment, optional GeoPandas module and two Cairo cases skipped |
| GeoPandas tests on Python 3.8, 3.9, 3.11, 3.13 | **290 passed**, 2 Cairo cases skipped; **90.57% coverage** |
| Standard virtualenv/pip tox runner, Python 3.11 core and geo | Both passed |
| Ruff lint and formatting | Passed |
| mypy | Passed for all 16 source modules |
| Build source distribution, then wheel from that source distribution | Passed |
| Twine strict metadata validation | Both distributions passed |
| Wheel contents | Includes all new modules, `py.typed`, and MIT license |
| Notebook examples | All **45 code cells** across four notebooks passed offline |
| Git whitespace/error check | Passed |
| Hosted CI for tag `v0.4.2` | **31 jobs passed**; [workflow run](https://github.com/eddiethedean/landfall/actions/runs/37056795159) |
| PyPI publication | **Passed**; sdist and wheel uploaded by [release workflow](https://github.com/eddiethedean/landfall/actions/runs/37061723829) |

Python 3.9 was rerun with managed CPython 3.9.25 after the macOS system
interpreter's LibreSSL triggered urllib3's OpenSSL warning. For the local
multi-version run, tox-uv avoided a copied-interpreter bootstrap problem with
standalone Python. Standard tox was also verified independently. These local
workarounds are not repository requirements.

### Release behavior changes to communicate

- Circle distances now match the documented units. Remove any manual factor-of-1,000
  workaround in downstream code.
- Mismatched color lists/arrays and invalid coordinates/radii now raise ValueError.
  A single-item color list broadcasts to all input objects.
- Entirely empty Shapely inputs raise ValueError. GeoDataFrames without a CRS
  continue to assume longitude/latitude coordinates.
- Optional plotting functions remain importable without GeoPandas and give an
  installation hint when called without the extra.
- The minimum renderer version is py-staticmaps 0.5.0. Python 3.8 development and
  optional dependencies use compatible version markers.

### Remaining release steps

The package release is complete. Create a GitHub Release page for `v0.4.2` if
you want release notes to appear in the GitHub Releases tab as well.

Tests deliberately use offline tiles; live tile services were not exercised.
Setuptools emits deprecation notices for the existing license-table/classifier
format. Distribution metadata validates successfully; the format is retained
for source-build compatibility with Python 3.8.

Geometry behavior was checked against [GeoJSON RFC 7946](https://datatracker.ietf.org/doc/html/rfc7946).
Runner labels were checked against [GitHub's hosted runner documentation](https://docs.github.com/en/actions/reference/runners/github-hosted-runners).
