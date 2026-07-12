# Setup — animated GitHub profile

What's different from a generic template: instead of a photo-based ASCII
portrait + neofetch panel + plain contribution heatmap, this uses a **typed
terminal boot log** (no photo needed), a **match-scoreboard style info
card**, and an **"Activity Pitch"** — your contribution graph rendered on a
football-pitch grid with a scoreboard stats strip. Same core trick (self-
hosted SMIL-animated SVGs, so nothing ever 404s or gets rate-limited), fully
re-skinned content and visuals.

## 1. Create the repo

Create a **public repo named exactly `Jay007mach`** (must match your
username) — GitHub auto-detects this and shows its README on your profile.

## 2. Add the files

Push everything in this folder to that repo:

```
README.md
boot-log.svg
scoreboard-card.svg
activity-pitch.svg
data/contributions.json
scripts/
.github/workflows/update-profile.yml
```

## 3. Generate the SVGs once locally (optional — they're already included)

```bash
pip install -r scripts/requirements.txt

python scripts/make_boot_sequence.py       # -> boot-log.svg
python scripts/make_scoreboard_card.py     # -> scoreboard-card.svg

GH_PROFILE_USER=Jay007mach python scripts/fetch_contributions.py
python scripts/render_activity_pitch.py    # -> activity-pitch.svg
```

## 4. Turn on the daily refresh

**Settings → Actions → General → Workflow permissions → Read and write
permissions** on the new repo, then run **"Update profile art"** once from
the Actions tab so `activity-pitch.svg` populates immediately. After that it
refreshes itself every night.

## Tuning cheatsheet

| Want to…                          | Where |
| ---------------------------------- | ----- |
| Change the boot-log lines           | `LINES` in `scripts/make_boot_sequence.py` |
| Change the scoreboard rows          | `ROWS` in `scripts/make_scoreboard_card.py` |
| Type faster / slower                | `CPS` in `make_boot_sequence.py` |
| Recolor the pitch / palette         | `PALETTE`, `PITCH`, `GOLD` in `render_activity_pitch.py` |
| Activity level thresholds           | `level_for()` in `render_activity_pitch.py` |
