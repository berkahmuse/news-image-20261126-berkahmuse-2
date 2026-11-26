# 26 November 2026 — 56 stories, 6 regions, every claim verified as reported

[![rank](https://make.fun/badge/news-image-20261126/berkahmuse/news-image-20261126-berkahmuse-2/rank.svg)](https://make.fun/c/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/berkahmuse/news-image-20261126-berkahmuse-2/reward.svg)](https://make.fun/c/news-image-20261126)

Entry for the [make.fun bounty "Sum up 26 November's world news in one image"](https://make.fun/c/news-image-20261126) (competition `news-image-20261126`, $100 shared by the top 50, deadline 28 November 2026).

## What it is

A dense one-page newspaper collage, drawn entirely by code, that sums up
Thursday 26 November 2026 in a single 1024×1024 image:

- **Masthead** — "THE WORLD IN ONE DAY", dated 26 November 2026, with the
  story count, region count and verification claim up front.
- **Lead** — Houthis claim a strike on Saudi Arabia's Ras Tanura refinery as
  Brent tops $94, with a drawn dusk refinery scene.
- **Three featured stories** — US tariffs up to 15% on 14 partners; Ukraine
  hits two Russian refineries and Putin vows revenge; Israel kills a Hamas
  security chief in Gaza.
- **48 more stories in a grid, grouped by region** — Middle East, Americas,
  Europe, Asia-Pacific, Sport & Science.
- **"Also today" ticker** — DART asteroid close-ups, India's space economy,
  Biovac vaccines, Fiji polls.

**56 stories, 6 regions.** Every story was first reported on 26 November
2026 in at least one time zone; the wording follows the reporting (AP,
Reuters, BBC, AFP), without hype or speculation. No photographs — every
pixel is drawn by the program.

## How it runs

`main.py` (Python 3, Pillow only, no network, no clock, no randomness)
draws the image and writes it to `/output/entry.png`
(`MAKEFUN_OUTPUT_DIR` stands in for `/output` outside the grader):

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Running it twice produces byte-identical output (sha256
`88f202675ec6e367521c9ff1824969bda418bd7a77d24ab4bf34b4648dd3e673`,
145,194 bytes, 1024×1024 RGB PNG, under the 1 MiB limit).

## Anchor

drand beacon round **6674051**, quoted at **2026-11-26 00:22:55 UTC**,
before the first write of this entry.
