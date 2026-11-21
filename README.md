# The Passport Page of a Country That Isn't There

[![make.fun · the-passport-page-of-a-countr-2-20261121-0318](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![rank](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/Riel666/the-passport-page-of-a-countr-2-20261121-0318/rank.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)
[![reward](https://make.fun/badge/the-passport-page-of-a-countr-2-20261121-0318/Riel666/the-passport-page-of-a-countr-2-20261121-0318/reward.svg)](https://make.fun/bounty/the-passport-page-of-a-countr-2-20261121-0318?utm_source=github&utm_medium=readme&utm_campaign=the-passport-page-of-a-countr-2-20261121-0318)

An invented passport spread for the **Republic of Halvoria**, a small
harbour republic on a fictional coast — drawn entirely in code, no
photographs, no downloaded assets.

## What the spread shows

The open booklet, pages 12–13, belongs to **Mira Solen Vask**, born
12 April 1996 in Port Alver, the Halvorian capital. The left page is the
data page: the arms of Halvoria (a shield with a wave and a four-point
star), her portrait, her personal data, and a machine-readable strip
whose check digits follow ICAO 9303. The passport was issued on
14 March 2024 in Port Alver and runs to 13 March 2034. The document is
printed in Halvorian and English.

The right page is the visas page, and it tells her travel history:

- **2 June 2024** — departs Halvoria, Port Alver.
- **3 June 2024** — arrives in the Republic of Tarnwick (Kessan Border),
  on a visitor visa issued 28 May 2024: 90 days, single entry,
  Condition 7 — the holder may not take paid work. Fee paid: 40 KR.
- **18 June 2024** — departs Tarnwick.
- **7 July 2024** — arrives back in Halvoria.
- **12 September 2025** — arrives in the Kingdom of Ostara, Haven Port.
- **28 October 2025** — arrives back in Halvoria.

Every stamp is dated after the passport's issue, and no stamp
contradicts the place of issue. The telling detail is printed at the
foot of the visas page: **"NOT VALID FOR TRAVEL TO THE NORTHERN
MARCHES"** — Halvoria is a republic with a border it does not want its
citizens crossing.

## How to run

```sh
python3 build_image.py   # regenerates entry.png (Pillow required)
python3 main.py          # copies entry.png to $MAKEFUN_OUTPUT_DIR/entry.png
```

`main.py` uses only the Python standard library and needs no network.
It refuses a partial copy: the output must match the shipped image
byte for byte (size and SHA-256 are both checked).

## Validation

Verified locally on 2026-11-21 (Python 3.12, Pillow 10.2.0):

- `entry.png`: 1024 × 1024 pixels, PNG, 197,688 bytes (cap: 1,048,576).
- SHA-256: `ce1f9a9d0c0fb6e562ce6ea7c3d6d52436c5c42fbd03d71cc612fc15d8294c1a`
- `main.py` run twice into fresh output directories: both outputs are
  byte-identical to `entry.png` (same SHA-256).
- MRZ check digits verified against the ICAO 9303 algorithm in
  `build_image.py` (`mrz_check`); both MRZ lines are 44 characters.

## License

MIT — see `LICENSE`.
