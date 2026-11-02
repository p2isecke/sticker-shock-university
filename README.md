# Sticker Shock University

*Veni, Vidi, Solvi — "I came, I saw, I paid."*

A one-page website that shows a high school student (Class of 2031, starting Fall 2027) and their parent what each college on their list really costs. It's themed as a fake college website, with a mascot named Wally the wallet who explodes money.

- **Live site:** https://p2isecke.github.io/sticker-shock-university/ (once GitHub Pages is turned on)
- **Repo:** https://github.com/p2isecke/sticker-shock-university

## Design principles

- **One page that works for the whole family.** A teenager can pick it up and get it right away, and a parent can still find the details they need.
- **Big numbers first, details on tap.** Each school shows its price at a glance. Tap a card for the breakdown.
- **Make the numbers relatable.** Costs show up as things a teen actually buys, like Chipotle burritos and iPhones, so a six-figure total starts to feel real.
- **Show the true minimum.** Prices cover tuition, fees, housing and food: the cost of going, before books and spending money.
- **Every school gets a fair look.** The page compares the whole list without favoring any one school.
- **Keep it fun.** A mock college website, a mascot and a shower of money confetti make a stressful topic something a family can laugh about together.

## What's on the page

- **Header:** a college-style utility bar ("Office of the Bursar · Est. MMXXVII"), the SSU crest, the name and motto, and a maroon-and-gold nav bar.
- **Welcome:** "What will college cost?", a line with the price range across the schools, and Wally.
- **Period switch:** All years / 1 year / 1 semester. Every card updates.
- **Home state menu:** public schools charge less to students from their own state. Changing it recalculates every public school, and each card shows an **In-state**, **Out-of-state** or **Private** tag.
- **School cards:** name, minimum price, and a stacked bar (tuition, housing & food) with a marker for the price after scholarships. Hovering over a bar shows the amounts. Tapping a card opens:
  - three tiles: cost per day, number of Chipotle burritos (or iPhones), and the monthly payment for 10 years if it's all borrowed
  - a breakdown (tuition, housing & food, scholarships, "you pay at least")
  - a small chart of each semester's bill
  - **Edit numbers** (name, type, tuition, housing, scholarships, years) and **Remove**
- **Add a school:** a search box over about 1,400 four-year colleges. Picking one fills in its prices and makes it rain money. "Add one by hand" is the fallback.
- **The Fine Print:** assumptions, a reset button, and a hidden **Legal & privacy** panel (also opened by `#legal` on the URL, or the footer link).

## Numbers and assumptions

| Setting | Value | Where in `index.html` |
|---|---|---|
| First fall semester | 2027 | `START` |
| Yearly cost increase | 3% | `INC` |
| Loan rate / term | 6.4%, 10 years | `RATE`, `monthly()` |
| Home state | chosen on the page (starts as New York) | `state.home`, Home state menu |
| Scorecard data year → Fall 2027 | ×1.03² (data is 2025–26) | `LAG` |
| Fun prices | burrito $12, iPhone $1,000, car $25,000 | `FUN` |
| Scholarships | $0 until offers come in | per school |

### The six starting schools

These use each school's own published **2026–27 on-campus** cost of attendance, raised 3% for 2027–28 and rounded. They're set in `STARTING` in `index.html`.

| School | Type | In-state tuition & fees | Out-of-state tuition & fees | Housing & food | Source |
|---|---|---|---|---|---|
| University of Tampa | Private (FL) | $38,400 | $38,400 | $16,000 | [ut.edu](https://www.ut.edu/admissions/tuition-and-costs) |
| UCF | Public (FL) | $6,000 | $27,500 | $15,400 | [ucf.edu](https://www.ucf.edu/financial-aid/cost/), [15% out-of-state increase](https://floridaphoenix.com/2026/07/16/non-florida-students-will-pay-higher-public-university-tuition-this-year/) |
| Loyola New Orleans | Private (LA) | $54,700 | $54,700 | $16,500 | [loyno.edu](https://www.loyno.edu/admissions/student-financial-services/tuition-fees/2026-27-undergraduate-tuition-fees) |
| Occidental College | Private (CA) | $73,200 | $73,200 | $21,700 | [oxy.edu](https://oxy.edu/financial-aid/cost) |
| University of Miami | Private (FL) | $70,400 | $70,400 | $27,100 | [miami.edu](https://admissions.miami.edu/undergraduate/financial-aid/cost-of-attendance/index.html) |
| UMD | Public (MD) | $13,200 | $45,400 | $17,600 | [USM FY2027 tuition](https://www.usmd.edu/usm/adminfinance/budget/FY2027/UMCP_Tuition_and_Fees_2027.pdf), housing estimated from the 2025–26 budget |

Caveats: the UCF out-of-state figure is an estimate from news coverage of the increase, and the UMD housing figure is an estimate.

### School search data

The search uses the U.S. Department of Education's [College Scorecard](https://collegescorecard.ed.gov/data/) (public domain). The data is **built into `index.html`** as a JSON block (`<script id="schoolData">`), so the site works on GitHub Pages with no API key. Filters: currently operating, mainly bachelor's-granting, 400+ undergrads.

Each searched school keeps its state, whether it's public or private, and both tuition prices. A public school in the chosen home state uses its in-state price; everything else uses the out-of-state price. Housing is on-campus room & board, or $14,000 if the school doesn't report it. Both get multiplied by `LAG`.

Nicknames the data lacks (NYU, FSU, UMD, RIT, USF, UNC…) are added in the `NICK` map.

**To refresh the data** (about once a year, when Scorecard updates):

```sh
# download "Most Recent Institution-Level Data" from collegescorecard.ed.gov/data and unzip it
python3 tools/extract_scorecard.py path/to/Most-Recent-Cohorts-Institution.csv index.html
```

Then update `LAG` if the data year changed, check a few schools, and commit.

## How the code is organized

Everything lives in `index.html`: no build step and no dependencies besides Google Fonts.

- **Styles:** color and font tokens on `:root`, with a dark-mode palette (`prefers-color-scheme` plus `data-theme`). Brand: maroon `--brand`, gold `--gold`, teal cash `--cash`, leather browns for Wally. Fonts: Cinzel (crest/name), Crimson Pro (headings), Bricolage Grotesque (big numbers), Atkinson Hyperlegible (body).
- **Wally:** an inline SVG in the `.welcome` block (`#wally`), styled by the `.m-*` classes. The style is bold black outlines and flat colors, inspired by (not copied from) a stock doodle wallet. The design is a brown bifold with a darker back panel, a fanned stack of teal bills, a side tab with a yellow snap, "zing" lines, a cute face and little feet. It jolts every few seconds unless the device has reduced motion turned on.
- **Main script:**
  - `STARTING` / `PRESETS` (default schools and school types)
  - `years()` / `view()` (cost math)
  - `renderHero()` (range line)
  - `buildCards()` / `renderCards()` / `detailHTML()` (cards)
  - the school search (`DB`, `search()`, `addFromDB()`)
- **Confetti script:** a full-screen canvas (`#cashCanvas`) that bursts bills and coins from Wally. It's exposed as `window.makeItRain(n)`. It's skipped when reduced motion is on, which is the first thing to check if it "doesn't work."
- **Legal script:** toggles the `#legal` panel.
- **Saved data:** each visitor's schools are stored in their own browser under the `localStorage` key `college-cost-planner-v3`. That's an old internal name. Changing it would wipe everyone's saved edits, so leave it unless that's intended. Nothing syncs between devices.

## Legal

- MIT License (see `LICENSE`).
- The Legal & privacy panel says:
  - it's not a real or accredited university
  - there's no affiliation with any school or company mentioned (school names are for identification; Chipotle and iPhone are their owners' trademarks)
  - the numbers are estimates, not financial advice, and the site is provided as is
  - where the data comes from
  - privacy: no accounts, tracking or ads, and data stays in the browser; Google Fonts and the host see basic connection info
- Wally and the crest are original artwork.

## Updating and deploying

1. Edit `index.html` and preview it locally. Run `open index.html` from this folder, or double-click the file, and refresh the browser after each change.
2. Commit and push to `main`:

   ```sh
   git add -A && git commit -m "Describe the change" && git push
   ```

3. GitHub Pages republishes within a minute or two. Pages setup: **Settings → Pages → Deploy from a branch → main → / (root)**.

## Ideas not yet done

- A "favorite" star on cards, so the range line could compare against her top choice.
- A shared list both the student and parent edit (would need a backend; GitHub Pages is static).
- SUNY/CUNY schools for an in-state comparison.
