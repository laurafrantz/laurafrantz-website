---
name: font-pair
description: Generate a small chat-visible tile previewing a heading font paired with a body font (lorem ipsum body copy). Use whenever the user asks to preview, demo, or compare a font pairing, or explicitly invokes /font-pair. Takes two font names as arguments (heading font, body font) and fetches them live from Google Fonts. Do not use this for elaborate multi-section type specimens unless the user asks for more than a simple tile.
---

# font-pair

Builds and publishes a small Artifact: a heading in one Google Font over a
lorem-ipsum paragraph in another, so the user can eyeball a pairing quickly.
Keep it to just the tile — this is a fast preview tool, not a full type
specimen. If the user wants weights, italics, an in-context mockup, etc.,
that's a bigger one-off job, not this skill.

## Steps

1. **Parse the two font names** from `args` (e.g. `Fraunces, Open Sans` or
   `Playfair Display / Inter`). First name is the heading font, second is the
   body font. If `args` is empty or only one name is given, ask the user for
   the missing name(s) rather than guessing.

2. **Fetch both fonts** using the bundled script, weight 400, style normal:
   ```
   python3 scripts/fetch_google_font.py "<heading font>" 400 normal /tmp/heading.woff2
   python3 scripts/fetch_google_font.py "<body font>" 400 normal /tmp/body.woff2
   ```
   Use paths under the scratchpad directory, not `/tmp` directly, if one is
   configured for this session. If either command fails, its stderr explains
   why (family not found, no matching weight, network issue) — report that to
   the user and stop instead of publishing a broken tile.

3. **Base64-encode both files** and build the tile from
   `assets/tile-template.html`, replacing:
   - `__HEADING_FONT_URI__` → `data:font/woff2;base64,<heading b64>`
   - `__BODY_FONT_URI__` → `data:font/woff2;base64,<body b64>`
   - `__HEADING_FONT_NAME__` / `__BODY_FONT_NAME__` → the two font names as
     given (used in the tile's own heading text, e.g. "Fraunces & Open Sans")

   A quick one-liner works well for the substitution, e.g.:
   ```python
   import base64
   heading_b64 = base64.b64encode(open('/tmp/heading.woff2','rb').read()).decode()
   body_b64 = base64.b64encode(open('/tmp/body.woff2','rb').read()).decode()
   html = open('assets/tile-template.html').read()
   html = (html.replace('__HEADING_FONT_URI__', f'data:font/woff2;base64,{heading_b64}')
               .replace('__BODY_FONT_URI__', f'data:font/woff2;base64,{body_b64}')
               .replace('__HEADING_FONT_NAME__', heading_name)
               .replace('__BODY_FONT_NAME__', body_name))
   open('/tmp/font-pair-tile.html', 'w').write(html)
   ```

4. **Publish** the filled file with the `Artifact` tool (favicon: 🔤, title
   e.g. "`<Heading> + <Body>`"). Redeploying under the same scratch path on a
   later invocation is fine — no need to preserve old tiles.

## Why base64 data URIs

Artifacts run under a CSP that blocks font CDN requests, so a normal
`@font-face { src: url("https://fonts.gstatic.com/...") }` fails silently.
Every font must be inlined as a `data:` URI instead — that's what the fetch
script and template are set up for.
