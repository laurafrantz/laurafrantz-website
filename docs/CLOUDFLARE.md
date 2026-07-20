# Cloudflare setup (optional): hotlink protection + scraper deterrence

Putting Cloudflare (free plan) in front of `laurafrantz.com` adds the one layer
a static host can't do on its own: **server-side image protection**. Specifically:

- **Hotlink Protection** — stops *other* websites from embedding your images
  directly (it checks the referring site).
- **Bot Fight Mode** — deters automated scrapers.
- Plus caching, "Always Use HTTPS," and it hides your origin.

> **Reality check:** this deters casual reuse and mass scraping. It does **not**
> stop someone from downloading an image and re-uploading it — nothing can, once
> an image is displayed in a browser. Pair it with web-sized images (already
> automated on this site) and, for real enforcement, copyright registration +
> takedown services (Pixsy, ImageRights).

---

## ⚠️ Read this before enabling — two important trade-offs

1. **Custom-domain HTTPS certificate.** GitHub issues your site's certificate by
   validating the domain over HTTP. Turning on Cloudflare's proxy (the orange
   cloud) can interfere with that validation/renewal. The safe recipe is below
   (SSL/TLS mode = **Full**, and grey-cloud briefly if GitHub ever needs to
   re-issue). Do **not** use SSL mode "Flexible" — it causes redirect loops with
   GitHub Pages.

2. **Hotlink protection can block your own syndication.** Because it blocks
   off-site image embedding, it can also stop **RSS readers, Substack imports,
   and social-share link previews (Open Graph images)** from showing your
   photos. Since the plan is to syndicate to Substack via RSS, weigh this: turning
   hotlink protection on may mean images don't appear in the Substack copies. You
   can leave hotlink protection **off** and still benefit from Bot Fight Mode +
   caching, or turn it on and accept that syndicated/preview copies won't show
   images.

---

## Setup steps

1. **Create a free Cloudflare account** and click **Add a site** →
   `laurafrantz.com`. Choose the **Free** plan.
2. Cloudflare scans your current DNS. Confirm these records were imported (add any
   that are missing):
   - Four **A** records, host `@` → `185.199.108.153`, `185.199.109.153`,
     `185.199.110.153`, `185.199.111.153`
   - One **CNAME**, host `www` → `laurafrantz.github.io`
   Start with all of them **grey-clouded (DNS only)** for the initial switch.
3. Cloudflare gives you **two nameservers**. Log in to your domain registrar and
   replace the current nameservers with those two. (This hands DNS to Cloudflare;
   propagation is usually minutes to a few hours.)
4. Wait until Cloudflare shows the site as **Active**, and confirm the site still
   loads at `https://laurafrantz.com`.
5. **SSL/TLS → Overview → set mode to `Full`.** Leave Universal SSL on (default).
6. Now enable the proxy: in **DNS**, click the grey cloud on the `@` A records and
   the `www` CNAME to turn them **orange (Proxied)**. Re-check the site loads over
   HTTPS. If the certificate misbehaves, grey-cloud again for ~an hour to let
   GitHub re-issue, then re-enable.
7. **Bot deterrence:** **Security → Bots → enable Bot Fight Mode.**
8. **Hotlink protection (optional — see trade-off #2 above):**
   **Scrape Shield → Hotlink Protection → On.**
9. Optional niceties: **SSL/TLS → Edge Certificates → Always Use HTTPS = On**;
   enable **Brotli** compression.

---

## If you outgrow this

For a large photo library or if you want *true* image access control
(signed URLs, referrer rules, on-the-fly resizing/watermarking, and keeping the
repo tiny), move images off the repo to an image CDN / object store — e.g.
**Cloudflare R2 + Images**, **Bunny.net**, or **Cloudinary**. That's the clean
path if the site's storage or bandwidth ever pushes GitHub Pages' limits
(1 GB published site, ~100 GB/month bandwidth).
