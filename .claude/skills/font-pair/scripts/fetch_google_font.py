#!/usr/bin/env python3
"""Download a single weight/style of a Google Font as a woff2 file.

Usage:
    fetch_google_font.py "<Family Name>" <weight> <style> <out.woff2>

    style is "normal" or "italic".

Exits non-zero with a message on stderr if the family/weight/style isn't
found on Google Fonts, so the caller can surface a clear error instead of
silently producing a broken font-face.
"""
import re
import sys
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")


def fail(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)


def main():
    if len(sys.argv) != 5:
        fail("usage: fetch_google_font.py \"<Family Name>\" <weight> <normal|italic> <out.woff2>")
    family, weight, style, out_path = sys.argv[1:5]

    if style not in ("normal", "italic"):
        fail(f"style must be 'normal' or 'italic', got: {style!r}")

    family_param = family.strip().replace(" ", "+")
    ital = "1" if style == "italic" else "0"
    css_url = (f"https://fonts.googleapis.com/css2"
               f"?family={family_param}:ital,wght@{ital},{weight}&display=swap")

    req = urllib.request.Request(css_url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            css = resp.read().decode("utf-8")
    except Exception as e:
        fail(f"could not reach Google Fonts for family {family!r}: {e}")

    if not css.strip():
        fail(f"Google Fonts returned nothing for family {family!r} -- "
             f"check the spelling (family names are case-sensitive on the API).")

    # The CSS lists one @font-face block per language subset, each preceded
    # by a comment like "/* latin */". We want the plain "latin" subset, not
    # "latin-ext" or any other script.
    blocks = re.split(r"/\*\s*([\w-]+)\s*\*/", css)
    # re.split with a capturing group yields: [pre, tag1, block1, tag2, block2, ...]
    latin_block = None
    for i in range(1, len(blocks), 2):
        tag, block = blocks[i], blocks[i + 1]
        if tag == "latin":
            style_ok = (style in block)
            if style_ok:
                latin_block = block
                break

    if latin_block is None:
        fail(f"no {style} weight {weight} found for family {family!r} on Google Fonts "
             f"(the family may not support this weight/style, or the name is misspelled).")

    m = re.search(r"url\(([^)]+)\)\s*format\('woff2'\)", latin_block)
    if not m:
        fail(f"couldn't find a woff2 URL in the Google Fonts response for {family!r}.")
    font_url = m.group(1)

    try:
        req2 = urllib.request.Request(font_url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req2, timeout=20) as resp:
            data = resp.read()
    except Exception as e:
        fail(f"could not download the font file for {family!r}: {e}")

    with open(out_path, "wb") as f:
        f.write(data)

    print(f"saved {family!r} ({style} {weight}) -> {out_path} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
