"""
Compatibility fixes for py-staticmaps with newer Pillow versions.

This module provides patches for compatibility issues between py-staticmaps
and newer versions of Pillow (11.0+) where textsize was removed.
"""

import warnings
from typing import Any, Optional, Tuple

try:
    from PIL import ImageDraw

    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False


def patch_textsize_compatibility() -> None:
    """
    Patch ImageDraw.textsize method for compatibility with newer Pillow versions.

    In Pillow 11.0+, textsize was removed and replaced with textbbox.
    This function adds a textsize method that uses textbbox internally.
    """
    if not PILLOW_AVAILABLE:
        return

    if hasattr(ImageDraw.ImageDraw, "textsize"):
        # Already patched or old Pillow version
        return

    def textsize(self: Any, text: str, font: Optional[Any] = None) -> Tuple[int, int]:
        """
        Compatibility method for textsize using textbbox.

        Args:
            text: Text to measure
            font: Font to use (optional)

        Returns:
            Tuple of (width, height)
        """
        try:
            # Use textbbox to get the bounding box
            bbox = self.textbbox((0, 0), text, font=font)
            if bbox:
                width = bbox[2] - bbox[0]  # right - left
                height = bbox[3] - bbox[1]  # bottom - top
                return (width, height)
            else:
                return (0, 0)
        except Exception:
            # Fallback for any issues
            return (0, 0)

    # Add the method to ImageDraw class
    setattr(ImageDraw.ImageDraw, "textsize", textsize)

    # Only show warning if not in test environment
    import sys

    if "pytest" not in sys.modules:
        warnings.warn(
            "Patched ImageDraw.textsize for Pillow compatibility. "
            "Consider updating py-staticmaps to a newer version.",
            UserWarning,
            stacklevel=2,
        )


def apply_compatibility_patches() -> None:
    """Apply all compatibility patches."""
    patch_textsize_compatibility()


# Auto-apply patches when module is imported
if PILLOW_AVAILABLE:
    apply_compatibility_patches()
