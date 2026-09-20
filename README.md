# codesarray.com

The Codesarray site, served by GitHub Pages from this repository's `main` branch
at the custom domain in `CNAME`.

## Layout

```
index.html                          studio front page, one card per game
styles.css                          shared stylesheet, plus the paws theme tokens
build-privacy.py                    python3 build-privacy.py <slug>
privacy-policy.html                 redirect to /blockfall/privacy-policy.html
tools/check-links.py                link and asset check for every page
blockfall/index.html                Blockfall's page
blockfall/privacy-policy.md         policy wording (source of truth)
blockfall/privacy-policy.html       generated
blockfall/img/                      Blockfall screenshots
pawsandperils/index.html            Paws & Perils' page
pawsandperils/privacy-policy.md     policy wording (source of truth)
pawsandperils/privacy-policy.html   generated
pawsandperils/img/                  Paws & Perils screenshots
synapsy/index.html                  Synapsy's page
synapsy/privacy-policy.md           policy wording (source of truth)
synapsy/privacy-policy.html         generated
synapsy/img/                        Synapsy screenshots
```

## What is here

| File | Why it exists |
| --- | --- |
| `index.html` | Studio front page: the hero and a card for each game. |
| `blockfall/index.html` | Blockfall's page: the Play button, features and screenshots. Sets `data-theme="blockfall"` on `<html>`. |
| `pawsandperils/index.html` | Paws & Perils' page. Sets `data-theme="paws"` on `<html>`. |
| `synapsy/index.html` | Synapsy's page. Sets `data-theme="synapsy"` on `<html>`. |
| `<slug>/privacy-policy.md` | Source of truth for that game's policy wording, a copy of `docs/privacy-policy.md` in the game's repo. |
| `<slug>/privacy-policy.html` | The URL given to Google Play. Generated, do not edit by hand. |
| `<slug>/img/` | Screenshots from `store/screenshots/` in the game's repo (Synapsy: emulator captures), scaled to 720px tall as WebP with a JPEG fallback. |
| `build-privacy.py` | Regenerates a game's `privacy-policy.html` from its markdown. |
| `privacy-policy.html` | Meta-refresh redirect to `/blockfall/privacy-policy.html`, kept for the old Play Console URL and any links already out in the world. |
| `tools/check-links.py` | Resolves every internal `href`/`src`/`srcset` to a file on disk, and flags GitHub links and stale `/img/` paths. Prints `ok` when clean. |
| `styles.css` | Shared stylesheet for every page. |
| `app-ads.txt` | Declares the AdMob publisher ID. AdMob crawls it from the domain root; the developer website on the Play listing must be exactly `https://codesarray.com`. |
| `googleb8930721c04d2512.html` | Google Search Console ownership check. Search Console re-fetches it, so it has to stay. |
| `favicon.svg` | The Codesarray mark: an array `[…]`, thin off-white brackets and three gold dots on a flat navy tile; the same SVG is inlined in every page header. |

## Updating a privacy policy

Edit the policy in the game's repo, copy it here, rebuild and push:

```sh
cp ../blockfall/docs/privacy-policy.md blockfall/privacy-policy.md
python3 build-privacy.py blockfall

cp ../pawsandperils/docs/privacy-policy.md pawsandperils/privacy-policy.md
python3 build-privacy.py pawsandperils

cp ../synapsy/docs/privacy-policy.md synapsy/privacy-policy.md
python3 build-privacy.py synapsy

python3 build-privacy.py            # all at once
git commit -am "Update privacy policy" && git push
```

Keep the effective date in the markdown in step with the app release, and revise
it before a version that changes how data is handled reaches Play.

Blockfall's policy moved out of the site root. Change the privacy policy URL in
its Play Console listing to `https://codesarray.com/blockfall/privacy-policy.html`;
the root `privacy-policy.html` redirect exists only to cover the transition and
anything still pointing at the old address.

## When Paws & Perils reaches Google Play

Three places carry the "Coming soon to Google Play" placeholder. Swap each for
the real Play button once the listing is live:

1. `index.html` — the card's `<span class="btn btn-soon" aria-disabled="true">`
   becomes an `<a class="btn btn-primary" href="https://play.google.com/store/apps/details?id=com.codesarray.pawsandperils">`
   with the same arrow SVG the Blockfall card uses.
2. `pawsandperils/index.html` — the same swap in the hero's `.actions`.
3. `build-privacy.py` — set `SITES["pawsandperils"]["store"]` to
   `("Google Play", "https://play.google.com/store/apps/details?id=com.codesarray.pawsandperils")`
   and rerun `python3 build-privacy.py pawsandperils`, which turns the footer
   `<span>` into a link.

## When Synapsy reaches Google Play

The same three placeholders as above, for `com.codesarray.synapsy`:

1. `index.html` — the Synapsy card's `<span class="btn btn-soon" aria-disabled="true">`
   becomes the Play button with `href="https://play.google.com/store/apps/details?id=com.codesarray.synapsy"`.
2. `synapsy/index.html` — the same swap in the hero's `.actions`.
3. `build-privacy.py` — set `SITES["synapsy"]["store"]` to the Play link and rerun
   `python3 build-privacy.py synapsy`.

Synapsy's Play Console privacy policy URL is `https://codesarray.com/synapsy/privacy-policy.html`.

## Design notes

The studio pages take their colours from Blockfall's own palettes in
`ui/GameColors.kt`: Navy for dark, Light for light, switched on
`prefers-color-scheme`. Two tokens carry the gold, because one value cannot do
both jobs: `--brand` (`#ffc53d`) fills buttons, where navy text on it reaches
10:1 in either scheme, while `--gold` tints text and icons and darkens to
`#8a5e00` in light mode to clear 4.5:1.

Game pages are pinned to their game's own look regardless of the visitor's system
scheme: `data-theme="blockfall"` on `<html>` locks the Navy palette, and
`data-theme="paws"` locks the warm pastel palette from the game's `PastelPalette`
(dim text darkened `#8A7B75` → `#6E5F58` and gold `#F5B301` → `#8A5E00` so both clear
4.5:1 on cream). `data-theme="synapsy"` locks Synapsy's Calm Dusk palette from the game's `DuskPalette`
(`ui/theme/GamePalette.kt`): navy `#0F1626`, teal `#3FC1B0` for buttons with `#08201C` text on
them, gold `#F2B441` for text and icons. Only the studio front page still switches on
`prefers-color-scheme`.

| Pair | Light | Dark |
| --- | --- | --- |
| `--text` on `--bg` | 12.10 | 14.22 |
| `--text` on `--surface` | 12.85 | 15.88 |
| `--text` on `--surface-2` | 11.06 | 11.81 |
| `--text-dim` on `--bg` | 5.75 | 8.05 |
| `--text-dim` on `--surface` | 6.10 | 8.98 |
| `--text-dim` on `--surface-2` | 5.25 | 6.68 |
| `--gold` on `--bg` | 5.37 | 8.33 |
| `--gold` on `--surface` | 5.70 | 9.29 |
| `--gold` on `--surface-2` | 4.91 | 6.91 |
| `--on-brand` on `--brand` | 5.53 | 6.82 |

Light uses `--bg #FFF7EC`, `--surface #FFFFFF`, `--surface-2 #FFEBD2`,
`--text #3B2F2F`, `--text-dim #6E5F58`, `--brand #FF8A5B`, `--on-brand #3B2F2F`,
`--gold #8A5E00`, `--border #F0DCC4`. Dark uses `--bg #2A2321`,
`--surface #1F1A18`, `--surface-2 #3A302C`, `--text #FFF4E8`,
`--text-dim #C9B8AE`, `--brand #FF8A5B`, `--on-brand #2A2020`, `--gold #F5B301`,
`--border #4A3E39`. Every text pair on every page meets WCAG AA at 4.5:1.

| Pair | Synapsy (Dusk) |
| --- | --- |
| `--text` on `--bg` | 15.25 |
| `--text` on `--surface` | 13.08 |
| `--text` on `--surface-2` | 10.94 |
| `--text-dim` on `--bg` | 7.36 |
| `--text-dim` on `--surface` | 6.31 |
| `--text-dim` on `--surface-2` | 5.28 |
| `--gold` on `--bg` | 9.78 |
| `--gold` on `--surface` | 8.39 |
| `--gold` on `--surface-2` | 7.02 |
| `--on-brand` on `--brand` | 7.67 |

Synapsy uses `--bg #0F1626`, `--surface #1B2438`, `--surface-2 #26314A`, `--text #E8ECF4`,
`--text-dim #9AA6BD`, `--brand #3FC1B0`, `--on-brand #08201C`, `--gold #F2B441`,
`--border #26314A`.

The paw mark on the Paws & Perils pages is the app's `res/drawable/ic_paw.xml`
path data inlined as SVG: paw-print by Lorc, [game-icons.net](https://game-icons.net),
CC BY 3.0.

Type is Space Grotesk for headings and Archivo for body, both from Google Fonts.
No JavaScript, no build step beyond `build-privacy.py`.

## Local preview

```sh
python3 -m http.server 8899
python3 tools/check-links.py
```

Then open <http://127.0.0.1:8899/>.
