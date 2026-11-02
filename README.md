# Sticker Shock University

*Veni, Vidi, Solvi — "I came, I saw, I paid."*

A one-page website that shows a high school student (Class of 2031, starting Fall 2027) and their parent what each college on their list really costs. It's themed as a fake college website, with a mascot named Wally the wallet who explodes money.

- **Live site:** https://p2isecke.github.io/sticker-shock-university/ (once GitHub Pages is turned on)
- **Repo:** https://github.com/p2isecke/sticker-shock-university
- **Claude preview copy:** https://claude.ai/artifact/7WtphbtCHZm8gh79Zr4EF8 (private, separate copy; `index.html` here is the source of truth)

## Design requirements

These came from feedback while building it, and they matter more than any single feature.

1. **One simple page for both the kid and the parent.** "Relatable to someone under 18 and usable for a parent" is a design requirement, not a request for separate sections. Don't add a "for parents" section.
2. **Very little reading.** Lead with big numbers. Put detail behind a tap or hover, inside each school's card. No term-by-term tables.
3. **Relatable comparisons are fun, not work-based.** The student doesn't have a job, so no "hours of work." Use things like Chipotle burritos and iPhones.
4. **Costs are a minimum:** tuition, fees, housing and food only. No books or personal expenses.
5. **Don't single out a "favorite" school.** We don't know her preference, so the top line just shows the price range across all schools.
6. **The money confetti is the favorite feature.** Keep it working: on page load, when Wally is tapped, and (biggest) when a school is added.

## What's on the page

- **Header:** a college-style utility bar ("Office of the Bursar · Est. MMXXVII"), the SSU crest, the name and motto, and a maroon-and-gold nav bar.
- **Welcome:** "What will college cost?", a line with the price range across the schools, and Wally.
- **Period switch:** All years / 1 year / 1 semester. Every card updates.
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
| Home state (gets in-state prices at public schools) | NY | `HOME` |
| Scorecard data year → Fall 2027 | ×1.03² (data is 2025–26) | `LAG` |
| Fun prices | burrito $12, iPhone $1,000, car $25,000 | `FUN` |
| Scholarships | $0 until offers come in | per school |

### The six starting schools

The student lives in **New York**, so every school here is out-of-state. These use each school's own published **2026–27 on-campus** cost of attendance, raised 3% for 2027–28 and rounded. They're set in `STARTING` in `index.html`.

| School | Tuition & fees | Housing & food | Source |
|---|---|---|---|
| University of Tampa | $38,400 | $16,000 | [ut.edu](https://www.ut.edu/admissions/tuition-and-costs) |
| UCF (out-of-state) | $27,500 | $15,400 | [ucf.edu](https://www.ucf.edu/financial-aid/cost/), [15% out-of-state increase](https://floridaphoenix.com/2026/07/16/non-florida-students-will-pay-higher-public-university-tuition-this-year/) |
| Loyola New Orleans | $54,700 | $16,500 | [loyno.edu](https://www.loyno.edu/admissions/student-financial-services/tuition-fees/2026-27-undergraduate-tuition-fees) |
| Occidental College | $73,200 | $21,700 | [oxy.edu](https://oxy.edu/financial-aid/cost) |
| University of Miami | $70,400 | $27,100 | [miami.edu](https://admissions.miami.edu/undergraduate/financial-aid/cost-of-attendance/index.html) |
| UMD (out-of-state) | $45,400 | $17,600 | [USM FY2027 tuition](https://www.usmd.edu/usm/adminfinance/budget/FY2027/UMCP_Tuition_and_Fees_2027.pdf), housing estimated from the 2025–26 budget |

Caveats: the UCF out-of-state figure is an estimate from news coverage of the increase, and the UMD housing figure is an estimate.

### School search data

The search uses the U.S. Department of Education's [College Scorecard](https://collegescorecard.ed.gov/data/) (public domain). The data is **built into `index.html`** as a JSON block (`<script id="schoolData">`), so the site works on GitHub Pages with no API key. Filters: currently operating, mainly bachelor's-granting, 400+ undergrads.

When a school is picked, tuition is the in-state price if the school is in `HOME` (NY), otherwise out-of-state. Housing is on-campus room & board, or $14,000 if the school doesn't report it. Both get multiplied by `LAG`.

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

1. Edit `index.html` and open it in a browser to check it.
2. Commit and push to `main`:

   ```sh
   git add -A && git commit -m "Describe the change" && git push
   ```

3. GitHub Pages republishes within a minute or two. Pages setup: **Settings → Pages → Deploy from a branch → main → / (root)**.

Git on this Mac is signed in through the GitHub CLI (`gh auth login` as `p2isecke`).

## History of changes

1. **First version:** a multi-section planner with a compare chart, a semester table and a parent funding plan. Feedback: too much reading.
2. **Simplified** to one page with tappable school cards and the detail inside them.
3. **Added the real schools** (Tampa, UCF, Loyola New Orleans, Occidental, Miami, UMD). Removed books and personal costs; prices are now minimums.
4. **Replaced "hours of work"** with fun comparisons (Chipotle burritos, iPhones, cars).
5. **Switched to New York residency:** UCF became out-of-state.
6. **Rebranded as Sticker Shock University:** college-website theme, crest, motto.
7. **Mascot:** Sticky the price tag, then Wally the wallet with money confetti.
8. **Removed** the "Choosing X over Y" banner in favor of a simple range line.
9. **Added the automatic school search** (College Scorecard data, built in).
10. **Redrew Wally** in the doodle style. Made the confetti bigger when a school is added.
11. **Added the Legal & privacy panel and the MIT license.** Moved the site to this repo.

## Ideas not yet done

- A "favorite" star on cards, so the range line could compare against her top choice.
- A shared list both the student and parent edit (would need a backend; GitHub Pages is static).
- SUNY/CUNY schools for an in-state comparison.
