"""
MkDocs hook: inject accessibility attributes into generated HTML.

Fixes:
1. Adds aria-label to md-toggle checkbox inputs (drawer & search)
   that lack accessible labels (WCAG 2.1 Form Labels requirement).
   Covers both regular pages (on_post_page) and 404 (on_page_context).
2. Adds title attribute to icon-only badge links <a><img alt="..."></a>
   so linters recognize them as having discernible text.
"""

from __future__ import annotations

import re


def _patch_html(html: str) -> str:
    """Apply all accessibility patches to a full HTML page string."""
    # Patch 1: hidden checkbox toggle for drawer navigation
    html = re.sub(
        r'(<input\s[^>]*class="md-toggle"[^>]*id="__drawer"[^>]*)(>)',
        r'\1 aria-label="Open navigation" title="Open navigation"\2',
        html,
    )
    # Patch 2: hidden checkbox toggle for search overlay
    html = re.sub(
        r'(<input\s[^>]*class="md-toggle"[^>]*id="__search"[^>]*)(>)',
        r'\1 aria-label="Open search" title="Open search"\2',
        html,
    )
    # Patch 3: <a href="..."><img alt="TEXT" ...></a> badge links
    # The VS Code linter requires the <a> itself to have discernible text
    # or a title attribute — img alt alone is not recognized by some linters.
    # Inject title="TEXT" from the img's alt into the parent <a>.
    def _add_title_from_img_alt(match: re.Match[str]) -> str:
        a_open = match.group(1)
        img_tag = match.group(2)
        rest = match.group(3)
        # Only patch if <a> has no title yet
        if 'title=' in a_open:
            return match.group(0)
        # Extract alt from <img>
        alt_match = re.search(r'alt="([^"]*)"', img_tag)
        if alt_match and alt_match.group(1):
            alt_text = alt_match.group(1)
            a_open = a_open.rstrip('>') + f' title="{alt_text}">'
        return a_open + img_tag + rest

    html = re.sub(
        r'(<a\s[^>]*href=[^>]+>)(<img\s[^>]+>)(</a>)',
        _add_title_from_img_alt,
        html,
    )
    return html


def on_post_page(output: str, **kwargs: object) -> str:
    """Post-process every page's full HTML output."""
    return _patch_html(output)


def on_page_context(context: dict[str, object], **kwargs: object) -> None:  # type: ignore[return]
    """Called for 404 and special pages — patch them via the page object."""
    # on_post_page is NOT called for the 404 error page.
    # We use on_page_context as an opportunity to mark the page for patching.
    # The actual patching happens via a custom approach: we hook on_env instead.
    pass


def on_post_build(config: dict[str, object], **kwargs: object) -> None:
    """Post-build hook: patch the 404.html which on_post_page misses."""
    import pathlib

    site_dir = str(config.get("site_dir", "site"))
    error_page = pathlib.Path(site_dir) / "404.html"
    if error_page.exists():
        original = error_page.read_text(encoding="utf-8")
        patched = _patch_html(original)
        if patched != original:
            error_page.write_text(patched, encoding="utf-8")

