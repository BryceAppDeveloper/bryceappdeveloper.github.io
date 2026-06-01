# MorForm Screenshots + Website - Carry-Over

**Status: DONE.** 30 screenshots badged (RGB/no-alpha, original dims), exported JPG+WebP.
Website index.html rewired to the curated set. Look locked in `morform_glass.py`.

## The approved look
Zilla Slab Bold caption + brand-plum (88,30,78 @ 52%) frosted glass + real edge
refraction (cv2.remap) + beveled 3D rim + drop shadow. Top-center, auto-scaled per image.

## Files
- `index.html` - website, gallery rewired (drop in repo root, replaces current)
- `morform-web-assets.zip` - the 12 featured WebP in assets/{mf,mm,mo}-screenshot/ (extract at repo root)
- `morform-screenshots-badged.zip` - ALL 30 in jpg/ (stores) and webp/ (web)
- `morform_glass.py` + `ZillaSlab-Bold.ttf` - locked script + font (re-run / tweak)
- `morform_glass_PROMPT.txt` - paste-in prompt for a low-cost chat

## Naming: {app}-{platform}-{feature}  (mf=Supervisor mm=Manager mo=Office)

## Website gallery (what index.html now points to)
Decision: Android for both phone apps, Windows for Office. Visible text captions were
REMOVED - the glass badge on each image is now the label. Featured 4 per section:
- Supervisor: mf-android-time, -jobs, -safety, -reports
- Manager:    mm-android-estimate, -jobs, -overview, -budget
- Office:     mo-windows-estimate, -overview, -contacts, -settings
To deploy the site: extract morform-web-assets.zip at repo root (creates the webp files),
drop in the new index.html, commit/push. (Old mf-01.../mm-01.../mo-01... files are now
unreferenced - safe to delete.)

## App stores (use the JPGs from morform-screenshots-badged.zip, no alpha)
- Apple App Store -> the mf-ios-* / mm-ios-* JPGs (iOS sizes 1242x2688)
- Google Play     -> the mf-android-* / mm-android-* JPGs (1080x2340)
- Microsoft Store -> the mo-windows-* JPGs (1920x1080)

## Re-run / tweak a caption
Upload morform_glass.py + ZillaSlab-Bold.ttf + working.zip to a chat, run
`python3 morform_glass.py`. To change wording: edit that entry's caption/out in JOBS,
re-run. OUT_FORMATS toggles jpg/webp. Do NOT touch the LOCKED LOOK constants.

## Notes
- Android & iOS use locked sizing; Office uses per-job fsize:58, pill_y:30.
- mm-android-reports and -2 are the same Reports screen (two UI iterations) - keep one.
- Optional polish: Android demo data shows your name / "Safeway" - swap to neutral
  fictional names later and regenerate if you want.
