# codesarray.com

The Codesarray site, served by GitHub Pages from this repository's `main` branch
at the custom domain in `CNAME`.

## What is here

| File | Why it exists |
| --- | --- |
| `index.html` | Studio landing page and the Blockfall listing. |
| `privacy-policy.html` | Blockfall's privacy policy, the URL given to Google Play. Generated, do not edit by hand. |
| `privacy-policy.md` | Source of truth for the policy wording, a copy of `docs/privacy-policy.md` in the blockfall repo. |
| `build-privacy.py` | Regenerates `privacy-policy.html` from the markdown. |
| `styles.css` | Shared stylesheet for both pages. |
| `app-ads.txt` | Declares the AdMob publisher ID. AdMob crawls it from the domain root; the developer website on the Play listing must be exactly `https://codesarray.com`. |
| `googleb8930721c04d2512.html` | Google Search Console ownership check. Search Console re-fetches it, so it has to stay. |
| `favicon.svg` | Four-block mark matching the Blockfall icon. |
| `img/` | Screenshots from `store/screenshots/` in the blockfall repo, scaled to 720px tall as WebP with a JPEG fallback. |

## Updating the privacy policy

Edit the policy in the blockfall repo, copy it here, rebuild and push:

```sh
cp ../blockfall/docs/privacy-policy.md privacy-policy.md
python3 build-privacy.py
git commit -am "Update privacy policy" && git push
```

Keep the effective date in the markdown in step with the app release, and revise
it before a version that changes how data is handled reaches Play.

## Design notes

Colors come straight from the game's own palettes in `ui/GameColors.kt`: Navy for
dark, Light for light, switched on `prefers-color-scheme`. Two tokens carry the
gold, because one value cannot do both jobs: `--brand` (`#ffc53d`) fills buttons,
where navy text on it reaches 10:1 in either scheme, while `--gold` tints text and
icons and darkens to `#8a5e00` in light mode to clear 4.5:1. Every text pair on
both pages meets WCAG AA.

Type is Space Grotesk for headings and Archivo for body, both from Google Fonts.
No JavaScript, no build step beyond `build-privacy.py`.

## Local preview

```sh
python3 -m http.server 8899
```

Then open <http://127.0.0.1:8899/>.
