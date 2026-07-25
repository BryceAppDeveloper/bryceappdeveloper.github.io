# morform.app — the marketing site

This is the storefront for three paid apps and the public home of their user guides. A broken
link or a stale help page costs sales and support time, so treat it as production.

Hand-written static HTML. **No build step, no templating, no framework, no JS on most pages.**
20 `.html` files, all at the repo root. One stylesheet, `css/site.css` (471 lines, 26 CSS
custom properties in `:root`, self-hosted IBM Plex woff2). Despite the folder name it is not
GitHub Pages — it deploys to Cloudflare via `publish.cmd` (`npx wrangler deploy`).

## worker.js — read it before changing any URL

35 lines, and it does four things in order: 301 `www.` → apex; if the path ends in `/`, serve
`index.html` from that directory; if the last segment has no dot, try `pathname + ".html"` and
serve it if that isn't a 404; otherwise pass through to assets.

Steps 2 and 3 exist because `wrangler.jsonc` sets `assets.html_handling: "none"`, which
disables Cloudflare's own directory-index and `.html` canonicalization. **If you change
`html_handling`, the clean-URL behaviour the app-store privacy links depend on breaks.**

The worker sets **no response headers at all** — no CSP, no HSTS, no `nosniff`, no cache
control. Adding them is worth proposing, but it's a change that can break asset loading, so
plan it rather than slipping it in.

Note `/page` and `/page.html` both return 200 with identical content and no redirect between
them. The `<link rel="canonical">` tag is the only thing preventing duplicate-content indexing.

## The header and footer are copy-pasted into all 20 pages

There is no include mechanism. **They have already drifted** — `index.html`, `apps.html` and
`faq.html` each have a different header block from the other 17, and `index.html`'s mobile menu
is missing the `Home` link the others have.

So: if you change the header or footer, change it in **every** page, then verify by diffing the
blocks across files rather than assuming. If you're asked to add a nav item, say up front that
it's a 20-file edit.

## SEO — the conventions, and the existing inconsistencies

Every page must have: `<html lang="en-CA">`, a unique `<title>`, `meta description`,
`link rel="canonical"`, the full `og:` set (`type`, `url`, `site_name`, `locale`, `title`,
`description`, `image`), the `twitter:` set (`card`, `title`, `description`, `image`),
`theme-color`, and a favicon link. 19 of 20 pages already do; `404.html` correctly carries only
a title and `noindex`.

Existing inconsistencies — don't propagate them, and fix one only if asked:

- **Canonical URLs are split.** Clean for `/`, `/apps`, `/faq`, `/course`, `/how-it-works`;
  `.html` for everything else, including all three help pages. `sitemap.xml` mirrors the split.
  Pick the page's existing form when editing; changing the convention is a site-wide task.
- `sitemap.xml` `lastmod` dates are stale — frozen in early July while help pages were edited
  later. **Update `lastmod` whenever you change a page**, and add new pages to both
  `sitemap.xml` and, if relevant, `llms.txt`.
- `index.html`'s `<title>`, `og:title` and `twitter:title` currently say three different things.
- `og:image:width`/`height`/`alt` and `twitter:image:alt` exist only on `index.html`; every
  other page ships a card image with no dimensions or alt, which degrades rendering.
- `apple-itunes-app` is on `index.html` but not on `/apps`, the page that actually sells them.
- `meta keywords` survives on `index.html` only. It's obsolete; don't add it anywhere else.
- The `FAQPage` JSON-LD is duplicated — `index.html` has 5 questions and `faq.html` has 8, with
  the first 5 verbatim identical across two URLs. Don't add a third copy.
- `morform-help.html` has no JSON-LD at all despite being a 44 KB structured guide.

## Accessibility — this site is in good shape; don't regress it

Already correct and worth preserving: `alt` on every image, exactly one `<h1>` per page with no
skipped heading levels, **zero div-as-button** (all interaction is real `<a href>`, and the
mobile menu is a native `<details>`/`<summary>` so it's keyboard-operable with no JS), a skip
link plus a real `<main>`, labelled `<nav aria-label="...">` landmarks, and a global
`:focus-visible { outline: 2px solid var(--mf-gold); outline-offset: 2px }`.

Two real defects, both in `css/site.css`:

- **Form fields signal focus by colour alone.** `.field input:focus`, `.field textarea:focus`,
  `.chk-other .otherin:focus` and `.sigin:focus` all set `outline: none` and change only the
  border colour. That fails WCAG 2.4.11 and 1.4.11. `.taskt .cell:focus` does it correctly —
  copy that.
- **No `prefers-reduced-motion` block exists** while `html { scroll-behavior: smooth }` is
  global. Any new animation must be wrapped in a reduced-motion guard, and adding one for the
  existing smooth scroll is a small, safe win.

Also: `faq.html`'s eight visible questions have no heading markup, so they aren't navigable by
heading even though they're marked up as `FAQPage` in JSON-LD.

## The three help guides

`morform-help.html`, `morform-manager-help.html`, `morform-office-help.html` — static HTML,
each a table-of-contents `<nav>` followed by `<h2>` sections and `<h3>` subsections.

**Nothing keeps them in sync with the apps.** The mobile apps' `HelpScreen.js` and Office's
help section in `renderer.js` are separate hand-maintained copies, and they are drifting right
now — app-side help edits are newer than the site's.

When a change to any app alters what help text describes, update the app's help **and** the
matching page here in the same session. Verify the wording against the actual current screens,
not against the old help text. Only 19 `id` anchors exist against 88 `<h3>` headings, so most
subsections aren't linkable — add an `id` when you add a subsection.

## Before saying a change here is done

There is no build, no test suite and no browser here, so items 1–3 of the global definition of
done don't apply. These replace them, and all five are mechanical — actually run them, don't
assert them:

1. Tags balanced and the document well-formed on every page you edited.
2. Every `href` you added or changed resolves to a file that exists in the repo.
3. The `<header>` and `<footer>` blocks are byte-identical to a named reference page — diff
   them, don't eyeball them.
4. `canonical` matches the URL form that page already used (clean vs `.html`).
5. `sitemap.xml` `lastmod` bumped for every page you touched.

You cannot verify that a page "looks right" from a shell. Say what you checked and say plainly
that visual rendering is unverified.
