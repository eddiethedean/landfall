"""Tests for shared context image export."""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, List, Tuple

import pytest
from PIL import Image

from landfall.context import Context
from tests.mock_tile_downloader import MockTileDownloader


class _RenderedOutput:
    def __init__(self, calls: List[Tuple[Any, ...]]) -> None:
        self.calls = calls

    def save(self, path: str) -> None:
        self.calls.append(("save", path))

    def saveas(self, path: str) -> None:
        self.calls.append(("saveas", path))

    def write_to_png(self, path: str) -> None:
        self.calls.append(("write_to_png", path))


@pytest.mark.parametrize(
    "path,renderer,render_method,write_method",
    [
        (Path("map.png"), None, "render_pillow", "save"),
        ("map.svg", None, "render_svg", "saveas"),
        ("map.png", "cairo", "render_cairo", "write_to_png"),
    ],
)
def test_save_selects_renderer_and_writes_output(
    monkeypatch, path, renderer, render_method, write_method
):
    calls = []
    context = Context()

    def render(width, height):
        calls.append((render_method, width, height))
        return _RenderedOutput(calls)

    monkeypatch.setattr(context, render_method, render)

    result = context.save(path, 640, 440, renderer=renderer)

    assert result is None
    assert calls == [
        (render_method, 640, 440),
        (write_method, str(path)),
    ]


def test_save_uses_subclass_render_hook():
    calls = []

    class HookContext(Context):
        def render_pillow(self, width, height):
            calls.append(("hook", width, height))
            return _RenderedOutput(calls)

    HookContext().save("hook.png", 320, 240)

    assert calls == [("hook", 320, 240), ("save", "hook.png")]


def _local_map_context() -> Context:
    context = Context()
    context.set_tile_downloader(MockTileDownloader())
    context.add_point(27.88, -82.49)
    return context


def test_save_writes_real_png_from_local_map(tmp_path):
    output = tmp_path / "local-map.png"

    _local_map_context().save(output, 320, 240)

    with Image.open(output) as image:
        assert image.format == "PNG"
        assert image.size == (320, 240)


def test_save_writes_real_svg_from_local_map(tmp_path):
    output = tmp_path / "local-map.svg"

    _local_map_context().save(output, 320, 240)

    root = ET.parse(output).getroot()
    assert root.tag.endswith("svg")
    assert root.attrib["width"] == "320px"
    assert root.attrib["height"] == "240px"


@pytest.mark.parametrize(
    "path,renderer,message",
    [
        ("map.jpg", None, "Output path must end in .png or .svg"),
        ("map.svg", "pillow", "Pillow renderer requires a .png"),
        ("map.png", "svg", "SVG renderer requires a .svg"),
        ("map.svg", "cairo", "Cairo renderer requires a .png"),
        ("map.png", "unknown", "renderer must be"),
    ],
)
def test_save_rejects_invalid_renderer_or_extension(
    monkeypatch, path, renderer, message
):
    context = Context()
    calls = []
    monkeypatch.setattr(context, "render_pillow", lambda *args: calls.append(args))
    monkeypatch.setattr(context, "render_svg", lambda *args: calls.append(args))

    with pytest.raises(ValueError, match=message):
        context.save(path, 320, 240, renderer=renderer)

    assert calls == []
