"""
Test color functionality specifically.
"""

import warnings

import pytest
import staticmaps

from landfall.color import process_colors, convert_color
from landfall.distinctipy import get_distinct_colors, get_distict_colors
from landfall.colorsys import hsvt_to_rgb, get_wheel_colors


class TestColorBugFix:
    """Test the critical color bug fix."""

    def test_distinct_colors_proper_scaling(self):
        """Test that distinct colors are properly scaled to 0-255 range."""
        colors = get_distinct_colors(10)

        for color in colors:
            r, g, b = color
            # All components should be in 0-255 range
            assert 0 <= r <= 255
            assert 0 <= g <= 255
            assert 0 <= b <= 255

            # At least some colors should have values > 1 (proving the bug is fixed)
            if r > 1 or g > 1 or b > 1:
                break
        else:
            pytest.fail(
                "All color components are <= 1, indicating the bug is not fixed"
            )

    def test_deprecated_function_still_works(self):
        """Test that the deprecated function still works."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            colors = get_distict_colors(5)

            # Should work the same as the new function
            assert len(colors) == 5
            assert isinstance(colors, list)

            # Should emit deprecation warning
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "deprecated" in str(w[0].message)


@pytest.mark.parametrize(
    "h,s,v,expected",
    [
        (0.0, 1.0, 1.0, (255, 0, 0)),  # Pure red
        (0.33, 1.0, 1.0, (0, 255, 0)),  # Pure green (approximate)
        (0.67, 1.0, 1.0, (0, 0, 255)),  # Pure blue (approximate)
        (0.0, 0.0, 1.0, (255, 255, 255)),  # White
        (0.0, 0.0, 0.0, (0, 0, 0)),  # Black
    ],
)
def test_hsv_to_rgb_conversion(h, s, v, expected):
    """Test HSV to RGB conversion with known values."""
    result = hsvt_to_rgb(h, s, v)
    # Allow for small rounding differences in HSV conversion
    if h in (0.33, 0.67):  # Approximate values for green and blue
        assert abs(result[0] - expected[0]) <= 5
        assert abs(result[1] - expected[1]) <= 5
        assert abs(result[2] - expected[2]) <= 5
    else:
        assert result == expected


@pytest.mark.parametrize(
    "color_input,expected_type",
    [
        ("red", staticmaps.Color),
        ("#FF0000", staticmaps.Color),
        ((255, 0, 0), staticmaps.Color),
        ((255, 0, 0, 128), staticmaps.Color),
    ],
)
def test_convert_color_types(color_input, expected_type):
    """Test color conversion with different input types."""
    result = convert_color(color_input)
    assert isinstance(result, expected_type)


@pytest.mark.parametrize(
    "invalid_input",
    [
        (1, 2),  # Too few components
        (1, 2, 3, 4, 5),  # Too many components
        "invalid_color",  # Invalid color name
    ],
)
def test_convert_color_invalid(invalid_input):
    """Test color conversion with invalid inputs."""
    with pytest.raises(ValueError):
        convert_color(invalid_input)


@pytest.mark.parametrize(
    "color_type,count",
    [
        ("random", 1),
        ("random", 10),
        ("distinct", 3),
        ("distinct", 15),
        ("wheel", 2),
        ("wheel", 8),
    ],
)
def test_process_colors_scales(color_type, count):
    """Test color processing with different scales."""
    colors = process_colors(color_type, count)
    assert len(colors) == count
    assert all(isinstance(c, staticmaps.Color) for c in colors)


def test_wheel_colors_uniqueness():
    """Test that wheel colors are unique."""
    colors = get_wheel_colors(5)
    assert len(colors) == 5
    assert len(colors) == len(set(colors))  # All colors should be unique


def test_wheel_colors_large_number():
    """Test that wheel colors can handle large numbers."""
    colors = get_wheel_colors(100)
    assert len(colors) == 100
    assert isinstance(colors, set)
