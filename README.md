# The World in One Page: Tuesday 24 November 2026

This entry is a small drawing program that renders one 1024x1024 PNG: a
complete newspaper front page summing up the world news of Tuesday
24 November 2026. Nothing is placed by hand in an image editor — every
headline, rule line and column is drawn by code, so the page can be
rebuilt exactly, byte for byte, at any time.

The lead story is the day's biggest shock: Jensen Huang reinstated as
Nvidia CEO after President Trump intervened in his ouster, sending
Nvidia shares up 31% and chip stocks rallying around the world. Below it
sit three secondary stories — Ukraine sinking a Russian warship off
Libya with sea drones, Trump's planned Wednesday meeting with NATO chief
Mark Rutte in Florida, and NATO's vow of a space defence after reports
that Russia may put a nuclear weapon in orbit. Around them, a dense grid
of 33 one-line briefs carries the rest of the day: the UN court ruling
on Myanmar and the Rohingya, Gaza, Sudan, Brazil's deadly storm, the
Ebola discharge in Kenya, oil and market moves, and the day's sport.

## How to run

```
python3 compose.py        # draws the page, writes entry.png
```

`compose.py` needs only Python 3 and Pillow. Its output is
deterministic — fixed text, fixed fonts, no randomness and no clock —
so two runs produce identical files. The hand-in program then delivers
the picture to the harness:

```
deno run --allow-read --allow-write main.ts   # or an equivalent Node run
```

`main.ts` copies `entry.png` from the repository directory to
`/output/entry.png` and does nothing else.

## Design

The page follows a dense-hybrid broadsheet layout on a warm paper
background (#f7f3ea) with near-black ink (#1a1712) and a single accent
red (#8f1d22). A serif masthead, "THE WORLD IN ONE PAGE", tops the page;
the lead headline is set large beneath it; and the date itself is the
centrepiece — a full-width red band across the vertical middle of the
page carrying "TUESDAY / 24 NOVEMBER 2026" in oversized paper-coloured
serif type, so the day is unmistakable even at thumbnail size. The brief
grid fills the remaining space in three tight columns with small red
markers, trading white space for breadth: one page, the whole day.

## License

MIT — see `LICENSE`. Copyright (c) 2026 cimumuy.
