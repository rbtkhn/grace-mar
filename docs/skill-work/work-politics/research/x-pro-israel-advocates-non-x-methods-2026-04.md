# Pro-Israel advocacy voices — non-X research playbook + results shell

**Territory:** work-politics · **WORK only** — methodology memo and **reproducible** search strategy without X/Twitter API or scraping. Pairs with [x-pro-israel-advocates-landscape-2026-04.md](x-pro-israel-advocates-landscape-2026-04.md) (X-centric baseline). **Do not** treat as Voice knowledge or campaign copy without verification.

**Date:** 2026-04-08

---

## 1. Analysis windows (fixed before any cross-metric comparison)

| Mode | Definition | Use |
|------|------------|-----|
| **Steady state** | Rolling **90 days** ending on the memo’s **as-of date** (here: **2026-04-08**) | YouTube 90d views, Wikipedia 90d pageviews, podcast trailing metrics, Substack where visible |
| **Crisis comparator** | **7 calendar days** anchored to a **named exogenous event** (e.g. Oct 7–13, 2023 local time stack for Israel–Gaza escalation) | Google Trends peaks, Wikipedia surge vs baseline, news headline counts — **same window** for all names in a batch |
| **Survey / study windows** | **As published** (TLVI, Pew, etc.) — **never** merge cohorts across studies | Persuasion and demographic trends only |

**Rule:** Do not compare **Steady state** YouTube subs to **Crisis** Trends spikes on the same row without labeling the column **Window**.

---

## 2. Layer 1 — Primary name harvest (no social graph)

### 2.1 Search query bank (Google Scholar / Semantic Scholar / open web)

Run in **Boolean** or **keyword** form; export **bibliographies** and **appendix tables** that **name individuals**.

| # | Query string (paste and adapt) | Target output |
|---|--------------------------------|---------------|
| 1 | `("hasbara" OR "Israel advocacy" OR "pro-Israel") AND (influencer OR "social media" OR YouTube OR podcast)` | Papers naming messengers or campaign typologies |
| 2 | `("Israel" OR Gaza OR Hamas) AND ("public diplomacy" OR stratcom OR "strategic communication")` | Think-tank and IR literature |
| 3 | `("antisemitism" AND survey) AND (Israel OR Zionism) AND (young OR campus OR Gen Z)` | Demographic complements to named-advocate lists |
| 4 | `site:fdd.org OR site:adl.org OR site:aipac.org (speaker OR "annual summit" OR biography)` PDF | **Event rosters** and **staff** pages |
| 5 | `StandWithUs OR CAMERA OR "Honest Reporting" (speaker OR fellow OR "campus advisor")` | NGO **named** roles |

### 2.2 Institutional rosters (repeatable, version-controlled)

| Source type | Examples | What to capture |
|-------------|----------|-----------------|
| Think tanks | FDD, INSS, JINSA, Tel Aviv Institute | **Fellows**, event **speakers** |
| NGOs | StandWithUs, CAMERA, UN Watch, ADL | **Leadership**, **digital** leads |
| Trade / advocacy press | *Jewish Insider*, *Jerusalem Post* op-ed bylines | **Recurring** columnists |

### 2.3 Seed roster (aligned to X memo for **continuity**)

The table below **reuses the same 30 individuals** as [x-pro-israel-advocates-landscape-2026-04.md](x-pro-israel-advocates-landscape-2026-04.md) so non-X metrics can be **joined** to the X baseline in a spreadsheet. **Category** tags reduce **plane merge** (see [template-three-lenses](../analytical-lenses/template-three-lenses.md)).

| # | Person | Category tag |
|---|--------|----------------|
| 1–18 | Hen Mazzig … Itamar Ben Gvir (Favikon block) | activist / journalist / pol / creator (per prior memo) |
| 19–30 | Ben Shapiro … Jake Wallis Simons (US/UK add-ons) | commentator / NGO / pol / journalist |

**Harvest status:** Layer 1 is **satisfied** when each row has **≥1** non-X **primary** pointer: org bio URL, **conference PDF**, **book**, **court filing name match**, or **peer-reviewed** mention — not only Wikipedia.

---

## 3. Layer 2 — Cross-platform reach (numeric, not X)

| Platform | Tool / method | URL or access | Metric captured |
|----------|---------------|---------------|-----------------|
| YouTube | Channel **About** + **VidIQ** / **Social Blade** public (if used) | `https://www.youtube.com/` + channel search | Subscribers; **90d** views on **uploads** (manual sum or tool) |
| Podcasts | **Listen Notes** search by creator | `https://www.listennotes.com/` | Show **listen score** / episode count; **not** downloads unless host publishes |
| Substack | Publication page (where public) | `https://substack.com/` | **Subscriber tier** often hidden — use **rank** lists or **About** claims only with caveat |
| Newsletters | **Ghost** / **Beehiiv** public stats | varies | Often absent — mark **NA** |

**Steady-state rule:** For YouTube, prefer **last 30/90 day** view sum from **YouTube Studio**-equivalent **public** aggregates only (third-party estimates = **low confidence**).

---

## 4. Layer 3 — Attention without social accounts

| Proxy | Tool | URL | Metric |
|-------|------|-----|--------|
| Wikipedia interest | **Pageviews** Toolforge | `https://pageviews.wmcloud.org/` | **enwiki** article views — **90d** or **crisis week** |
| Relative search interest | **Google Trends** | `https://trends.google.com/` | **0–100 index**; compare **≤5** entities per chart |
| Global news agenda | **GDELT** Event Database or **BigQuery** sample | `https://www.gdeltproject.org/` | **Article counts** matching `Actor1Name` + themes (advanced) |
| Manual news hits | Google News with quotes | `https://news.google.com/` | **Headline** count in fixed window — document query string |

---

## 5. Layer 4 — Persuasion and opinion (off-X)

| Source | What it yields |
|--------|----------------|
| TLVI / institute surveys (e.g. *Jewish Journal* writeups) | **Named** influencer **A/B** style results — cite **n**, **screening** |
| Pew / Gallup / Morning Consult | **No** individual names usually — **demographic** **floor** for messaging |
| Academic pre/post message tests | **Causal** hints for **message** — rarely **rank** 30 people |

---

## 6. Layer 5 — Paid / coordinated (disclosure plane)

| Source | URL | Use |
|--------|-----|-----|
| U.S. DOJ FARA eFile | `https://www.fara.gov/` | **Registrants** and **exhibit** PDFs naming campaigns |
| Meta Ad Library | `https://www.facebook.com/ads/library/` | **Issue** ads; **spend** bands by region |
| EU Transparency Register | `https://transparencyregister.ec.europa.eu/` | EU-facing advocacy |

Tag rows **organic** / **institutional** / **disclosed paid** when evidence exists.

---

## 7. Results shell — fill per research pass

**Instructions:** For each person, fill **one row per window** (duplicate rows if both Steady and Crisis). **NA** = tool did not expose data. **Verify** = re-pull same day before external use.

### 7.1 Master metric table (blank template)

| # | Name | Category | Primary non-X channel | YouTube subs (date) | Podcast LN score / URL | Wikipedia 90d views (en) | Google Trends peak index (window) | News hits (query + n) | Organic / inst. / paid tag | Notes |
|---|------|----------|------------------------|----------------------|---------------------------|---------------------------|-------------------------------------|-------------------------|----------------------------|-------|
| 1 | Hen Mazzig | activist | | | | | | | | |
| 2 | Eli Afriat | activist | | | | | | | | |
| 3 | Hananya Naftali | creator | | | | | | | | |
| 4 | Emily Schrader | journalist | | | | | | | | |
| 5 | Nuseir Yassin (Nas Daily) | creator | | | | | | | | |
| 6 | Sissi Emperatriz | activist | | | | | | | | |
| 7 | Eddie Cohen | journalist | | | | | | | | |
| 8 | Arsen Ostrovsky | NGO / legal | | | | | | | | |
| 9 | Uri Kurlianchik | author | | | | | | | | |
| 10 | Gabriel Yerushalmi | analyst | | | | | | | | |
| 11 | Ahmad Mansour | psychologist / author | | | | | | | | |
| 12 | Yoseph Haddad | activist | | | | | | | | |
| 13 | Hillel Fuld | tech / advocate | | | | | | | | |
| 14 | Jonathan Conricus | think tank / mil | | | | | | | | |
| 15 | Tamer Masudin | educator | | | | | | | | |
| 16 | Rabbi Elchanan Poupko | clergy / educator | | | | | | | | |
| 17 | Lahav Harkov | journalist | | | | | | | | |
| 18 | Itamar Ben Gvir | politician | | | | | | | | |
| 19 | Ben Shapiro | commentator | | | | | | | | |
| 20 | Bari Weiss | journalist | | | | | | | | |
| 21 | Douglas Murray | commentator | | | | | | | | |
| 22 | Caroline Glick | columnist | | | | | | | | |
| 23 | Mark Levin | broadcaster | | | | | | | | |
| 24 | Alan Dershowitz | legal scholar | | | | | | | | |
| 25 | Hillel Neuer (UN Watch) | NGO | | | | | | | | |
| 26 | Ritchie Torres | politician | | | | | | | | |
| 27 | Michael Dickson (StandWithUs) | NGO | | | | | | | | |
| 28 | Noa Tishby | entertainer / advocate | | | | | | | | |
| 29 | Eylon Levy | gov-adjacent / commentator | | | | | | | | |
| 30 | Jake Wallis Simons | journalist | | | | | | | | |

### 7.2 Example partial fills (illustrative — **refresh** before reliance)

These demonstrate **how** to populate; numbers are **not** audited same-day.

| Name | Wikipedia (concept) | Trends (concept) |
|------|---------------------|------------------|
| Ben Shapiro | High **enwiki** traffic vs niche Israeli activists — run `pageviews` on **Ben_Shapiro** article | Often tracks **U.S. political** cycles — compare only within **same region** setting |
| Hen Mazzig | Lower article traffic than U.S. cable names — **niche** advocate pattern | Spike possible during **hostage** news — use **Crisis** window |

---

## 8. Three parallel mini-rankings + optional composite

**Do not** force a single “#1” without declaring weights.

| Mini-ranking | Primary driver | Best for |
|--------------|----------------|----------|
| **R1 — Institutional footprint** | Count of **think-tank / NGO** **roles** + **speaker PDF** hits | **Durability** and **access** |
| **R2 — Cross-platform reach** | YouTube subs + podcast **Listen Notes** presence + **Substack** where public | **Scale** |
| **R3 — General attention** | Wikipedia **90d** + **Trends** (steady) | **Broad public curiosity** |

**Optional composite (example weights — change explicitly):**  
`Score = 0.4 * norm(R2) + 0.35 * norm(R3) + 0.25 * norm(R1)`  
where **norm** = min–max within the cohort of 30 on **Steady state** window.

**vs X-native memo:** X gives **short-horizon impression velocity** and **platform-native scores** (Favikon). Non-X **cannot** recover **per-post view curves**; substitute **R3** spikes in **Crisis** week and **news hit** counts.

---

## 9. Patterns and trends (hypotheses to test with filled table)

1. **Video-first** advocates (YouTube-heavy) may **outrank** print journalists on **R2** while **losing** on **R1** (fewer institutional titles).
2. **U.S. partisan commentators** dominate **R3** (Wikipedia, Trends) vs **Israel-resident** activists — **country** bias in **Trends** settings.
3. **Crisis week** **R3** surges for **hostage** and **military** spokespeople more than for **columnists** — test with Oct 2023 comparator.
4. **Paid / FARA-visible** names may show **high R2** with **low organic** tagging — **do not** merge without **Layer 5**.

---

## 10. Caveats (non-X–specific)

- **Wikipedia** **notability** rules **suppress** many working advocates — **undercounts** niche voices.
- **Google Trends** is **relative** within the chart — **not** absolute audience.
- **GDELT** requires **query discipline** — false positives on **common names**.
- **Listen Notes** / **Social Blade** — **third-party**; platforms may **block** or **inaccurate**.

---

## 11. Execution checklist (operator)

- [ ] Lock **Steady** and **Crisis** dates in the spreadsheet header.
- [ ] Complete **Layer 1** primary pointer for all 30 rows.
- [ ] Fill **R1 / R2 / R3** columns for the same window.
- [ ] Run **optional composite** only if weights are **documented**.
- [ ] Add **Related** link from project dashboard or second memo pass.

---

## Related

- [x-pro-israel-advocates-landscape-2026-04.md](x-pro-israel-advocates-landscape-2026-04.md) — X-centric baseline.
- [template-three-lenses](../analytical-lenses/template-three-lenses.md) — verify tier and **plane tags**.
