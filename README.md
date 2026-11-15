# Nkugwa Mark William — Interior Design Portfolio

A warm-minimal static portfolio built entirely from Blender-modelled rooms: five measured 3D studies, each rendered and published as an interactive model.

**Live site:** https://marknwilliam.github.io/interior-portfolio/

## Structure

- `build.py` — static site generator (project data, page templates, sitemap)
- `index.html`, `work/*.html` — generated pages (do not edit by hand)
- `assets/css/style.css` — design system and responsive layout
- `assets/js/main.js` — navigation, reveal animations, lightbox
- `assets/js/viewer3d.js` — lazy Three.js orbit viewer with poster fallback
- `assets/models/*.glb` — exported 3D models (ceiling removed)
- `assets/img/` — responsive WebP stills (800/1280 px) and 1200×630 OG images
- `assets/vendor/` — vendored Three.js r160 module and addons
- `blender/render_rooms.py` — headless scene builder, five rooms, Cycles renders
- `blender/export_glb.py` — exports each `.blend` to `assets/models/*.glb`
- `blender/audit_geometry.py` — wall, rug and depth checks for each room
- `blender/make_web_images.py` — converts renders into site WebP assets
- `blender/inspect_rooms.py` — diagnostic close-up renders

## Room dimensions

The scenes are drawn from researched anthropometric standards — seat heights around 450 mm, dining tops at 750 mm, worktops at 900 mm, 600 mm bed clearances, 900 mm circulation routes, a compact kitchen work triangle, pendants 750 mm above the table, artwork centred at 1.5 m and windows above one-eighth of the floor area. References include Neufert's *Architects' Data* and Panero & Zelnik's *Human Dimension and Interior Space*.

## Rebuild

Render the five scenes (Cycles CPU; `ROOMS_ONLY=dining-corner` limits the run):

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python blender/render_rooms.py
```

Audit, export the web models and regenerate images:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --python blender/audit_geometry.py
/Applications/Blender.app/Contents/MacOS/Blender -b --python blender/export_glb.py
python3 blender/make_web_images.py
python3 build.py
```

Edit `PROJECTS`, `EMAIL`, `X_HANDLE` or `BASE` at the top of `build.py`, then rebuild.

## Local preview

```sh
python3 -m http.server 8099
# http://localhost:8099/
```

## Deploy

GitHub Pages serves the repository root from `main`. Push changes:

```sh
git add -A && git commit -m "Update site" && git push
```
