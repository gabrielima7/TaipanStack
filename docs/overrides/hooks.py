"""
MkDocs hook: inject accessibility attributes into generated HTML.

Fixes:
- Adds aria-label to md-toggle checkbox inputs (search & drawer)
  that lack accessible labels (WCAG 2.1 Form Labels requirement).
"""

from __future__ import annotations

import re


def on_post_page(output: str, **kwargs: object) -> str:
    """Post-process every page's full HTML output to inject missing aria-labels."""
    # Fix: <input class="md-toggle" ... id="__drawer" ...>
    # Add aria-label="Open navigation" to the drawer toggle
    output = re.sub(
        r'(<input\s[^>]*class="md-toggle"[^>]*id="__drawer"[^>]*)(>)',
        r'\1 aria-label="Open navigation"\2',
        output,
    )
    # Fix: <input class="md-toggle" ... id="__search" ...>
    # Add aria-label="Open search" to the search toggle
    output = re.sub(
        r'(<input\s[^>]*class="md-toggle"[^>]*id="__search"[^>]*)(>)',
        r'\1 aria-label="Open search"\2',
        output,
    )
    return output
