# Contributing

[Documentation index](README.md) · [Repository](https://github.com/eddiethedean/landfall)

## Development setup

```sh
git clone https://github.com/eddiethedean/landfall.git
cd landfall
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python -m pip install -e '.[dev,geo]'
```

Run the checks relevant to your change before opening a pull request:

```sh
python -m pytest
ruff check src tests
ruff format --check src tests
mypy src
```

!!! tip "One command for the complete matrix"
    `tox -p auto` runs the configured Python, geospatial, lint, typing, and
    packaging environments in parallel. Install the matching interpreters
    first if you want the full Python 3.8–3.13 matrix locally.

The tests use an offline tile downloader. `tox` runs tests against installed
wheels for Python 3.8–3.13 and has separate `geo`, `ruff`, `mypy`, and
`package` environments. The `geo` environment enforces at least 85% total
coverage. The `package` environment builds the sdist and wheel and runs
Twine's strict metadata check. To run every environment locally, install the
required Python interpreters and use:

```sh
tox -p auto
```

## Documentation

The site uses MkDocs Material and builds on Read the Docs. Install its build
requirements and check links/navigation locally:

```sh
python -m pip install -r docs/requirements.txt
python -m mkdocs build --strict
python -m mkdocs serve
```

The map screenshots use real OpenStreetMap tiles. To regenerate them, install
the project, connect to the network, then run:

```sh
python examples/generate_doc_maps.py
```

Keep examples executable and include a screenshot when a new visual feature
needs one. Preserve the tile attribution visible in generated images.
Changes in behavior should include a regression test and a changelog entry.

!!! info "Before changing a screenshot"
    The documentation images use real OpenStreetMap tiles. Regenerate them
    from the checked-in examples so the code and visual output stay aligned.

## Publish on Read the Docs

The repository root contains `.readthedocs.yaml`, which builds `mkdocs.yml`
with the pinned packages in `docs/requirements.txt`. Import
`eddiethedean/landfall` in Read the Docs and choose the project slug
`landfall` to match the README and package metadata URLs. The `latest`
version normally follows the repository's default branch, so merge the docs
changes there before publishing `latest`. Alternatively, activate the
`codex/release-0.4.2` branch as a separate version while reviewing it.
If a different slug is required, update the hosted links and `site_url`
before publishing.
