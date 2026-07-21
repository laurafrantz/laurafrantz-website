# Editing guide

How to add posts, images, and pages to the site. **You never build anything
yourself** — every commit auto-deploys in about a minute, and images are
automatically resized, converted to WebP, and served responsively during that
build.

The easiest way to edit (no software to install) is right on
**github.com/laurafrantz/laurafrantz-website**. Every step below is done there.
(You can also edit locally with Hugo for live preview — see the README.)

> **Protecting your originals:** the build optimizes what visitors see, but the
> *file you upload* is what lives in the public repo (and can be downloaded in
> bulk). So **shrink photos to ~1600px on the long edge before uploading** —
> that way your full-resolution masters never leave your computer.

---

## 1. New blog post with a featured image (shows on the cards)

The card / "featured" image is PaperMod's **cover**. Set it in front matter and
it appears on the home cards *and* at the top of the post.

1. **Add file → Create new file.**
2. Name it, including a new folder:
   `content/posts/my-post-title/index.md`
   (typing `/` creates the folder — this makes a "page bundle" that holds the
   post plus its images.)
3. Paste and edit:
   ```toml
   +++
   title = "My Post Title"
   date = 2026-07-20
   draft = false
   tags = ["Family", "Garden"]

   [cover]
     image = "cover.jpg"
     alt = "Short description of the photo"
     relative = true
   +++

   Write your post here. Add an inline image any time with:

   ![a caption or alt text](another-photo.jpg)
   ```
4. **Commit changes.**
5. Add the images: open the new `content/posts/my-post-title/` folder →
   **Add file → Upload files** → drag in `cover.jpg` (and any inline images) →
   **Commit.**

Live in ~1 minute.

- `draft = true` keeps a post hidden until you set it to `false`.
- To hide the featured image **only on the cards** (but keep it on the post),
  add `hiddenInList = true` inside the `[cover]` block.

> ⚠️ **The `[cover]` block must look exactly like the example above** — a
> `[cover]` line by itself, then an indented `image = "..."` line below it.
>
> **Never write `cover = "cover.jpg"` as a single line.** That form looks
> reasonable but is a different, invalid shape — it silently **breaks the
> entire site build** (not just that one post) the moment it's committed,
> because the template can't read an image filename out of plain text the
> way it can out of the `[cover]` block. If a deploy ever goes red right
> after adding a cover image, this is the first thing to check.

---

## 2. Adding images to an existing post

Each post is a folder under `content/posts/`. Drop image files in, then
reference them.

1. Navigate to the post's folder, e.g. `content/posts/indian-beach/`.
2. **Add file → Upload files** → drag your photos in → **Commit.**
3. Reference each one in the body of `index.md`:
   ```markdown
   ![white asters at dusk](my-photo.jpg)
   ```
   (Click `index.md` → pencil/Edit → add the line → Commit.)

**Imported posts** often already contain placeholders like `![](image-03.jpg)`.
Either:
- **Match the name** — upload a file named `image-03.jpg` and it just appears, or
- **Use your own name** — upload `sunset.jpg`, then edit the line to
  `![](sunset.jpg)`.

### Adding (or changing) a cover image on an existing post

Same idea as a new post's cover (above): upload the file into the post's
folder, then add this to the **top** of `index.md`, right after the other
`+++`-fenced fields, before the closing `+++`:

```toml
[cover]
  image = "cover.jpg"
  relative = true
```

For example, an existing post's front matter would go from:
```toml
+++
title = "senecio rowleyanus"
date = 2019-07-05
draft = false
tags = ["Garden", "Healing", "Home"]
+++
```
to:
```toml
+++
title = "senecio rowleyanus"
date = 2019-07-05
draft = false
tags = ["Garden", "Healing", "Home"]

[cover]
  image = "senecio.jpg"
  relative = true
+++
```
Same warning as above applies: it must be the `[cover]` block, never a single
`cover = "..."` line.

**`relative = true` matters:** the cover image lives inside the post's own
folder, not at the site root. Without `relative = true`, the on-page cover
still works, but the image used for social-media link previews (Slack,
iMessage, Twitter/X, Facebook) points to the wrong URL and shows up broken.

---

## 3. Adding a new page and putting it in the nav menu

**Step A — create the page.** Add file → Create new file → `content/now.md`:
```toml
+++
title = "Now"
url = "/now/"
+++

What I'm up to lately…
```
(If the page needs its own images, make it a bundle instead:
`content/now/index.md`, and upload images into that folder.)

**Step B — add it to the nav.** Edit `hugo.toml`, find the `[menu]` section, and
add a block. `weight` sets the order (currently Search 5, Archive 10, Tags 20,
About 30), so weight 25 slots "Now" between Tags and About:
```toml
  [[menu.main]]
    identifier = "now"
    name = "Now"
    url = "/now/"
    weight = 25
```
Commit — "Now" appears in the menu (desktop and the mobile hamburger).

---

## Quick reference

| Task | Where | Key bit |
|---|---|---|
| New post | `content/posts/<slug>/index.md` | `[cover]` `image = "cover.jpg"`, `relative = true` → card image |
| Post image | drop file in the post's folder | `![alt](file.jpg)` in `index.md` |
| New page | `content/<name>.md` | `url = "/name/"` |
| Nav item | `hugo.toml` `[menu]` | `[[menu.main]]` + `weight` for order |

## Dates and drafts

- `draft = true` → hidden until set to `false`.
- A `date` in the future stays hidden until that date arrives.
- Posts are sorted newest-first by `date`.
