# Laura J. Frantz — personal blog

A static blog built with [Hugo](https://gohugo.io/) (extended) and the
[PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme, deployed to
GitHub Pages via GitHub Actions and served at **https://laurafrantz.com**.

## Local development

Requires Hugo **extended** (see `HUGO_VERSION` in `.github/workflows/deploy.yml`
for the pinned version).

```bash
git clone --recurse-submodules <repo-url>
cd laurafrantz-website
hugo server -D          # preview at http://localhost:1313 (drafts + live reload)
```

If you cloned without `--recurse-submodules`, fetch the theme with:

```bash
git submodule update --init --recursive
```

## Guides

- **[Editing guide](docs/EDITING.md)** — add posts (with featured/cover images),
  add images to existing posts, and add new pages + nav menu items. Written for
  editing directly on github.com, no local setup required.
- **[Cloudflare guide](docs/CLOUDFLARE.md)** — optional hotlink protection and
  scraper deterrence, with the HTTPS-cert and RSS-syndication trade-offs.

## Structure

- `content/posts/<slug>/` — one page bundle per post (`index.md` + that post's images).
- `content/about.md`, `content/archives.md`, `content/search.md` — standalone pages.
- `hugo.toml` — site configuration.
- `layouts/_markup/render-image.html` — build-time image optimization (resize → WebP → responsive `srcset`).
- `.github/workflows/deploy.yml` — build + deploy on every push to `main`.

## Images

Post/landing images are automatically resized, converted to WebP, and served
responsively at build time. Just drop image files into a post's folder and
reference them with `![alt](file.jpg)`. Shrink photos to ~1600px before
committing so full-resolution originals stay off the public repo.
