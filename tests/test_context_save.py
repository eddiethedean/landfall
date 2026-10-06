"""Tests for shared context image export."""

from pathlib import Path
from typing import Any, List, Tuple

import pytest

from landfall.context import Context


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
