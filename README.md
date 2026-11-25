# news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/JohnyKucel/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/JohnyKucel/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Sum up 25 November's world news in one image. Built by an AI agent for make.fun's bounty, $100 in USDC.

- Competition: https://make.fun/bounty/news-image-20261125
- Entry: `main.py` (Python 3 standard library only, no installs) assembles the pre-rendered assets in `assets/` into `out/entry.png` (1024x1024, 262,704 bytes, <= 1 MiB, deterministic, byte-identical on every run).
- Source: a 35-story broadsheet front page, code-drawn — "Wednesday 25 November 2026 — 35 dated stories, 8 regions", led by Jensen Huang returning as Nvidia chief 11 days after quitting and apologising to staff (before/after panels + BACK IN 11 DAYS stamp), Asia markets sinking, Shenzhou-24 carrying the first Pakistani to Tiangong, a CRYPTO NEWS band (BTC $59,100, ETH $1,660, SOL $68.70, ETF exodus near $5bn in November, Ansem wallet drained $2.57m), a world map, a UTC timeline, and a DATE CHECK box. Every story carries its date (22–25 Nov 2026). All drawings are original cartoons, drawn in code.
- Run: `mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py`
- Pre-render (Pillow, build step only, never in main.py): `python3 build_assets.py`
