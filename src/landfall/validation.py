"""Validation shared by geometry entry points."""

import math
from numbers import Real
from typing import Any

import staticmaps


def create_latlng(latitude: Any, longitude: Any) -> Any:
    """Create a coordinate, rejecting invalid values before rendering."""
    if (
        not isinstance(latitude, Real)
        or not isinstance(longitude, Real)
        or not math.isfinite(latitude)
        or not math.isfinite(longitude)
        or not -90 <= float(latitude) <= 90
        or not -180 <= float(longitude) <= 180
    ):
        raise ValueError(
            "coordinates must be finite: latitude -90..90, longitude -180..180"
        )
    return staticmaps.create_latlng(latitude, longitude)
