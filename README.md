# Laura J. Frantz — personal blog

A static blog built with [Hugo](https://gohugo.io/) (extended) and the
[PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme, deployed to
GitHub Pages via GitHub Actions and served at **https://laurafrantz.com**.

## Local development

Requires Hugo **extended** (see `HUGO_VERSION` in `.github/workflows/hugo.yaml`
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

## Structure

- `content/posts/<slug>/` — one page bundle per post (`index.md` + that post's images).
- `content/about.md`, `content/archives.md`, `content/search.md` — standalone pages.
- `hugo.toml` — site configuration.
- `.github/workflows/hugo.yaml` — build + deploy on every push to `main`.

## Adding images to a post

Many posts reference image files that are not yet present (e.g.
`![](image-03.jpg)`). These come from the original blog and were placeholders in
the source document. To add a photo, drop a file with the matching name into
that post's folder and push — the site rebuilds automatically.

## Writing a new post

```bash
hugo new posts/my-post-title/index.md
```

Then edit the front matter (`draft = false` to publish) and add your text.
