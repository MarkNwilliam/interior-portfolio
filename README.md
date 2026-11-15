# Nkugwa Mark William — Interior Design Portfolio

A warm-minimal static portfolio for interior design and spatial studies.

**Live site:** https://marknwilliam.github.io/interior-portfolio/

## Structure

- `build.py` — static site generator (project data, page templates, sitemap)
- `index.html`, `work/*.html` — generated pages (do not edit by hand)
- `assets/css/style.css` — design system and responsive layout
- `assets/js/main.js` — navigation, reveal animations, lightbox
- `assets/img/` — optimised WebP images (800/1200/1800 px, details, OG)
- `assets/source/` — original stock photographs
- `blender/render_rooms.py` — headless Blender scene + render script
- `blender/` — `.blend` scenes and PNG renders (not used by the site)

## Local preview

```sh
python3 -m http.server 8099
# http://localhost:8099/
```

## Rebuild pages

```sh
python3 build.py
```

Edit `PROJECTS`, `EMAIL`, `X_HANDLE` or `BASE` at the top of `build.py`, then rebuild.

## Deploy

GitHub Pages serves the repository root from `main`. Push changes:

```sh
git add -A && git commit -m "Update site" && git push
```
