# Landing Page Visual Parity Evidence

**Date:** 2026-11-12  
**Branch:** `landing-parity-2026-11-12`  
**Commit:** `5726a51`

## Gate

`just check` exited 0.

- Engine: 393 passed, 1 skipped.
- Website: 54 passed.
- Both production builds completed.
- Design-token, search-layer, legal-template, purchase and email fences passed.

## Screenshots

- [Production desktop, 1440×1000](./production-desktop-1440.png)
- [V2 desktop, 1440×1000](./v2-desktop-1440.png)
- [Production mobile, 390×844](./production-mobile-390.png)
- [V2 mobile, 390×844](./v2-mobile-390.png)

The V2 screenshots were recaptured from the final `5726a51` build after the
hero, wordmark, FAQ motion, blended nav fade and nav breathing-room refinements.

## Geometry

| Viewport | Production height | V2 height | Difference | Horizontal overflow |
|---|---:|---:|---:|---|
| 1440×1000 | 10,350px | 10,035px | -315px | None |
| 390×844 | 12,950px | 12,367px | -583px | None |

The intentional News & Updates substitution accounts for most of the gap:
169px on desktop and 512px on mobile. The other content sections remain close
to the production rhythm.

| Section | Production desktop | V2 desktop | Production mobile | V2 mobile |
|---|---:|---:|---:|---:|
| Hero | 1,000 | 1,000 | 844 | 844 |
| About | 652 | 648 | 814 | 803 |
| Divider 1 | 500 | 500 | 422 | 422 |
| Mission | 1,056 | 1,052 | 1,694 | 1,700 |
| Divider 2 | 500 | 500 | 422 | 422 |
| Model | 927 | 846 | 1,416 | 1,408 |
| Divider 3 | 500 | 500 | 422 | 422 |
| Marketplace | 1,328 | 1,293 | 2,100 | 2,001 |
| Divider 4 | 500 | 500 | 422 | 422 |
| News | 1,333 | 1,164 | 2,227 | 1,715 |
| FAQ | 1,365 | 1,370 | 1,511 | 1,520 |
| Footer CTA | Outside section count | 408 | Outside section count | 438 |

## Browser checks

- Desktop viewport: 1440×1000; scroll width 1440.
- Mobile viewport: 390×844; scroll width 390.
- Exactly one `h1` is present.
- The mobile navigation opens and Escape closes it.
- The navbar uses the muted-grey wordmark without the emblem and has a computed
  `border-bottom: 0px`.
- The navbar glass is masked from an opaque top through a transparent lower
  edge, with a 40px backdrop blur and no hard horizontal boundary.
- The navbar has 32px of additional visual breathing room (`112px` minimum
  height) while the 80px content row remains at the top, so the logo, links and
  CTA keep their original vertical positions.
- The two-horse hero artwork is visible: the rendered image covers 1440×1000 at
  desktop and is the top element at the hero sample point.
- FAQ answers open and close with a 300ms interpolated transition: an 80ms
  opening sample measured 48px / 0.686 opacity before settling at 102px / 1;
  an 80ms closing sample measured 4.56px / 0.212 before settling at 0px / 0.
- All 28 V2 images load; zero failed images after eager-loading the partner strip.
- Small-target count: V2 15 desktop / 11 mobile; production 16 desktop / 17 mobile.

## Independent audit

- `kimi-code-audit` returned **VERDICT: PASS** on all 9 claims.
- The audit's final tree-mutation warning is expected in its disposable clone:
  the gate created ignored `.next`/dependency artifacts and the copied evidence
  directory was intentionally untracked. The implementation worktree remained
  clean at commit `5726a51`.
- Full report: [KIMI-AUDIT.txt](./KIMI-AUDIT.txt).

### Navbar and FAQ refinement

- The focused audit passed all source, accessibility, interruptibility and scope
  claims. Its only WARN was that the read-only auditor did not execute the build
  step.
- The same `just check` gate was then run successfully in the disposable audit
  clone, clearing that process caveat: 393 engine passed, 1 skipped, 54 website
  passed, and both builds completed.
- Refinement report: [KIMI-REFINEMENT-AUDIT.txt](./KIMI-REFINEMENT-AUDIT.txt).

## Notes for the founder walk

- News & Updates deliberately uses an honest “Coming soon” presentation rather
  than production’s populated article grid.
- The V2 hero uses the existing SVG lockup, so its intrinsic bounding box differs
  from production’s PNG export while presenting the same logo system.
- Final visual acceptance remains the founder’s walk at the two captured sizes.
