// Static-site Worker for morform.app
// - Redirects www.morform.app -> morform.app (301), matching prior GitHub Pages behavior
// - Restores "/" (and any dir/) -> index.html, since assets.html_handling = "none"
//   disables Cloudflare's automatic directory-index + .html canonicalization.
// - Serves extensionless paths from their .html file (so /morform-manager-privacy
//   serves morform-manager-privacy.html, 200) -- clean URLs for store privacy links.
// - Serves every other path straight from static assets (so /support.html stays /support.html, 200).
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // www -> apex
    if (url.hostname.startsWith("www.")) {
      url.hostname = url.hostname.slice(4);
      return Response.redirect(url.toString(), 301);
    }

    // Directory paths -> index.html (html_handling:"none" turns this off otherwise)
    if (url.pathname.endsWith("/")) {
      const idx = new URL(url);
      idx.pathname = url.pathname + "index.html";
      return env.ASSETS.fetch(new Request(idx, request));
    }

    // Extensionless paths -> try the matching .html file (clean URLs).
    // e.g. /morform-manager-privacy -> morform-manager-privacy.html
    const lastSegment = url.pathname.slice(url.pathname.lastIndexOf("/") + 1);
    if (lastSegment && !lastSegment.includes(".")) {
      const html = new URL(url);
      html.pathname = url.pathname + ".html";
      const res = await env.ASSETS.fetch(new Request(html, request));
      if (res.status !== 404) return res;
    }

    // Everything else: serve the asset exactly as requested (.html stays .html)
    return env.ASSETS.fetch(request);
  },
};
