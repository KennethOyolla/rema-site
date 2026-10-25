# ReMA Solutions website

Marketing site for ReMA at **remasolutions.co.ke**. The app itself lives at rema.blue-flame.co.ke (repo `KennethOyolla/rema`).

Plain static HTML, no framework, no dependencies — light on data for phone visitors.

- `pages/*.html` — one file per page. The first line is a comment with the page title, description and active nav item.
- `assets/` — `site.css`, `site.js`, logo and icons.
- `build.py` — wraps each page in the shared head, header, demo form and footer and writes `dist/`.

Build locally: `python3 build.py`, then open `dist/index.html` (or `python3 -m http.server -d dist`).
Vercel runs the same command (see `vercel.json`) and serves `dist/`.

## Still to do
- Real BTL01 screenshots to replace the HTML phone mock-ups
- Connect the demo form to Zoho CRM web-to-lead (it currently opens an e-mail)
- `assets/og.png` share image
