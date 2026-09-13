# APF Global Foresight Wiki
**The Official Knowledge Canon & Working Encyclopedia of the Association of Professional Futurists (APF)**

Welcome to the **APF Global Foresight Wiki** repository. This project contains the foundational reference encyclopedia and multimedia knowledge canon for strategic foresight, futures studies, speculative design, and anticipatory governance — stewarded by the **Association of Professional Futurists (APF)**.

All 1,000 encyclopedia articles are currently in **Working Draft (Pending Peer Review)** status. This repository provides both the compilation toolchain and an interactive peer-review validation portal designed for deployment to static web hosts such as **GitHub Pages** and **Cloudflare Pages**.

---

## 1. Project Overview & Verification Benchmarks

- **Stewarding Body**: Association of Professional Futurists (APF)
- **Official Branding**: Authentic APF armillary sphere & futures navigation insignia with glowing cyan/deep navy typography and 3D Futures Cone seals.
- **Publication Status**: **Working Draft (Pending Peer Review)**. Every entry is marked with editorial status badges and linked directly to the peer-review audit protocol.
- **Canon Scale**:
  - **1,000 Curated Encyclopedic Articles** across **20 Thematic Pillars**
  - **2,700 Curated Foresight Media & Literature Resources** across **5 Formats**
  - **5 Curated Master Resource Portals** in Wikitext and interactive HTML
  - **12 MediaWiki Templates** (Infoboxes, Badges, Citations, Publications, Media)
- **Repository Word Count**: **720,127 words** (575,204 encyclopedia words + 144,923 resource portal words)
- **Quality Assurance**: 100% pass rate across the APF Editorial Quality Gates (`validate_wiki.py` & `validate_media_canon.py`)
- **Taxonomy Integration**: Full alignment with the **6 APF Core Foresight Competencies**:
  - `Framing`: **135 articles** + **410 media resources**
  - `Scanning`: **130 articles** + **404 media resources**
  - `Futuring`: **155 articles** + **406 media resources**
  - `Designing`: **230 articles** + **668 media resources**
  - `Adapting`: **80 articles** + **136 media resources**
  - `Leading`: **270 articles** + **676 media resources**
- **Hosting Architecture**: Zero-dependency static site compiled to `wiki/preview/`, optimized for **Cloudflare Pages** and **GitHub Pages**.

---

## 2. The 2,700-Item Foresight Media & Literature Canon

In addition to the 1,000 encyclopedia articles, this repository catalogs **2,700 high-caliber media items** spanning over seven decades of futures inquiry:

| Media Format | Count | Coverage & Representative Works |
|---|:---:|---|
| 📚 **Foundational & Modern Books** | **650** | Canonical volumes from Fred Polak, Bertrand de Jouvenel, Herman Kahn, Alvin Toffler, Wendy Schultz, Sohail Inayatullah, Jennifer Gidley, Richard Slaughter, and modern practitioners. |
| 📄 **Peer-Reviewed Journal Articles** | **1,000** | Foundational and high-impact papers across *Futures*, *Technological Forecasting & Social Change*, *Journal of Futures Studies*, *Foresight*, *European Journal of Futures Research*, and *World Futures Review*. |
| 🎙️ **Podcasts & Audio Series** | **350** | International foresight broadcasts including *Future Pod*, *The Long Time Academy*, *IFTF Future 9:01*, *Exponential View*, *Flash Forward*, and *Team Human*. |
| 📰 **Newsletters, Blogs & Signal Feeds** | **350** | High-velocity scanning hubs, Substack publications, and signal newsletters including *APF Compass*, *IFTF Vantage*, *Exponential View*, *Superforecasting*, and *Sentient Syllabus*. |
| 🎥 **Keynotes & Landmark Presentations** | **350** | Recorded addresses, university masterclasses, TED/TEDx talks, and conference keynotes from Stuart Candy, Jane McGonigal, Amy Webb, Jim Dator, and Riel Miller. |

The catalog is stored in `wiki/resources/foresight_media_canon_2700.json` (2.26 MB) and compiled into client-side JS (`wiki/preview/preview_media_data.js`, 1.94 MB).

---

## 3. The 20 Thematic Pillars Architecture

The 1,000 encyclopedia entries are systematically distributed across 20 specialized pillars:

| # | Pillar Name | Directory Name | Competency | Entries |
|---|---|---|---|:---:|
| **01** | Foundations, Epistemology & Epistemic Pluralism | `01_foundations_and_epistemology` | Framing | 45 |
| **02** | Temporal Cognition, Psychology & Futures Consciousness | `02_psychology_and_temporal_cognition` | Framing | 40 |
| **03** | Decolonial, Indigenous & Pluriversal Futures | `03_critical_and_decolonial_futures` | Framing | 50 |
| **04** | Horizon Scanning, Sensemaking & Signal Processing | `04_horizon_scanning_and_signals` | Scanning | 40 |
| **05** | Drivers of Change & Disruption Dynamics | `05_drivers_and_change_dynamics` | Scanning | 40 |
| **06** | Megatrends, Planetary Boundaries & Polycrises | `06_megatrends_and_planetary_frontiers` | Scanning | 50 |
| **07** | Core Foresight Methodologies & Frameworks | `07_core_foresight_methodologies` | Futuring | 65 |
| **08** | Scenarios, Narrative Forensics & Worldbuilding | `08_scenarios_and_worldbuilding` | Futuring | 50 |
| **09** | Computational Foresight, System Dynamics & Quantitative Modeling | `09_computational_and_quantitative_foresight` | Futuring | 40 |
| **10** | Facilitation Tools, Matrices & Canvases | `10_facilitation_tools_and_canvases` | Designing | 40 |
| **11** | Speculative Design, Experiential Futures & Artifacts | `11_design_and_experiential_futures` | Designing | 40 |
| **12** | Applied Climate, Energy & Urban Transitions | `12_applied_climate_energy_and_cities` | Designing | 50 |
| **13** | Applied Health, Biotech, Longevity & Cognitive Frontiers | `13_applied_health_biotech_and_ai` | Designing | 50 |
| **14** | Applied Geopolitics, Security, Space & Global Horizons | `14_applied_security_space_and_economy` | Designing | 50 |
| **15** | Strategy Wind-Tunneling, Agility & Antifragility | `15_strategy_wind_tunneling_and_agility` | Adapting | 40 |
| **16** | Anticipatory Governance, Institutional Foresight & Policy | `16_anticipatory_governance_and_policy` | Leading | 40 |
| **17** | Landmark Historical Case Studies Archive (1950–Present) | `17_landmark_case_studies` | Leading | 75 |
| **18** | High-Profile Figures, Theorists & Pioneers | `18_high_profile_figures_and_pioneers` | Leading | 100 |
| **19** | Foresight Organizations, Centers & Think Tanks | `19_foresight_organizations_and_think_tanks` | Leading | 50 |
| **20** | University Degree Programs, Institutes & Training | `20_university_and_training_programs` | Leading | 45 |
| **—** | **Total Canonical Entries** | | | **1,000** |

---

## 4. Repository Directory Structure

```
/Volumes/Projects/apf-wifi/
├── .github/
│   └── workflows/
│       ├── deploy.yml                 # Automated deployment to GitHub Pages
│       └── validate.yml               # Automated validation & QA gate on PRs
├── .gitignore                         # Excludes secrets, caches, environment configs
├── index.html                         # Root redirect to wiki/preview/index.html
├── README.md                          # Master documentation & deployment guide
└── wiki/
    ├── Main_Page.wiki                 # The official APF landing portal wikitext
    ├── templates/                     # 12 Wikitext infobox & metadata templates
    ├── entries/                       # 1,000 wikitext articles across 20 pillar folders
    │   ├── 01_foundations_and_epistemology/ ... 20_university_and_training_programs/
    │   └── resources/                 # 5 Wikitext master bibliographies
    ├── resources/                     # Master media databases (2,700 items JSON)
    ├── export/                        # Turnkey MediaWiki XML export archive
    ├── preview/                       # Modern static site (Deploy target for Cloudflare/GitHub)
    │   ├── _headers                   # Cloudflare Pages security & caching headers
    │   ├── index.html                 # Main encyclopedia explorer portal
    │   ├── resources.html             # Media & Literature Hub (2,700 items)
    │   ├── review.html                # Editorial Review & Peer Validation Portal
    │   ├── preview.css                # APF design system stylesheet (dark/light mode)
    │   ├── preview_app.js             # Client search, filter, navigation engine
    │   ├── preview_data.js            # Article catalog index (1,000 entries)
    │   ├── preview_media_data.js      # Media canon catalog index (2,700 records)
    │   ├── assets/                    # Official APF vector lockups and insignia
    │   └── articles/                  # 1,005 static HTML article pages
    └── scripts/
        ├── build_preview_site.py      # Generates preview/ HTML site from wikitext
        ├── build_full_wiki.py         # Recompiles 1,000 wikitext entries from JSON
        ├── validate_wiki.py           # Editorial quality audit (1,000 entries)
        └── validate_media_canon.py    # Media canon quality audit (2,700 records)
```

---

## 5. Peer Review & Validation Workflow

Every article in the wiki begins in **Working Draft (Pending Peer Review)** status. To avoid misleading readers or attributing false scholarly endorsements, no article is marked as canonical until it completes peer evaluation.

### Interactive Review Portal (`review.html`)
The static site includes a dedicated **APF Editorial Review & Peer Validation Portal** accessible at:
- `http://localhost:8080/review.html` (locally)
- Or via the **📋 Review Queue** button in the site header and sidebar.

### The APF 4-Point Peer Review Rubric
1. **Historical & Epistemic Lineage**: Verify theoretical originators, founding years, and lineage accuracy.
2. **Methodological Rigor**: Verify step-by-step facilitation mechanics, prerequisite logic, and outputs.
3. **Primary Literature Authenticity**: Ensure genuine peer-reviewed journal articles and monographs are cited.
4. **Pluriversal & Critical Bias Audit**: Check that Western/corporate biases are balanced with global and indigenous perspectives.

### Elevating Drafts to Approved Status
Reviewers click **Audit & Review Entry** next to any article in `review.html` to generate a pre-filled evaluation checklist copied to the clipboard. Reviewers submit evaluations as GitHub Issues or Pull Requests. Once approved by the APF Editorial Council:
1. Update `status=approved` in the entry's `Editorial_Status` banner.
2. Re-run `/usr/bin/python3 wiki/scripts/build_preview_site.py`.
3. The article automatically displays the green **✔ Vetted & Approved** badge.

---

## 6. Static Hosting Deployment Guide

The static site in `wiki/preview/` is completely self-contained, requiring zero server-side runtimes, databases, or PHP.

### Option A: GitHub Pages (Recommended)

This repository includes a turnkey GitHub Actions deployment workflow at `.github/workflows/deploy.yml`.

1. Initialize git and push this repository to GitHub:
   ```bash
   git remote add origin https://github.com/<your-org-or-username>/<repo-name>.git
   git push -u origin main
   ```
2. On GitHub, navigate to **Settings** &rarr; **Pages**.
3. Under **Build and deployment** &rarr; **Source**, select **GitHub Actions**.
4. The workflow will automatically run on every push to `main`, compile the preview site, and deploy it to `https://<username>.github.io/<repo-name>/`.

### Option B: Cloudflare Pages

Cloudflare Pages delivers ultra-fast edge delivery and automatic SSL.

1. In the [Cloudflare Dashboard](https://dash.cloudflare.com/), go to **Workers & Pages** &rarr; **Create application** &rarr; **Pages** &rarr; **Connect to Git**.
2. Select this repository.
3. Configure the build settings:
   - **Framework preset**: `None`
   - **Build command**: `python3 wiki/scripts/build_preview_site.py`
   - **Build output directory**: `wiki/preview`
   - **Root directory**: `/` (leave default)
4. Click **Save and Deploy**.
5. Cloudflare will automatically read `wiki/preview/_headers` to enforce HTTP security headers and aggressive asset caching.

### Option C: Local Static Web Server

To run the site locally for inspection:
```bash
# Serve directly from preview directory
/usr/bin/python3 -m http.server 8080 --directory wiki/preview

# Or serve from repository root (index.html will auto-redirect to preview)
/usr/bin/python3 -m http.server 8080
```
Then open your browser to `http://localhost:8080`.

---

## 7. Quality Assurance & Auditing Commands

Run the automated test suites at any time to verify catalog integrity:

```bash
# 1. Audit all 1,000 encyclopedia articles across 20 pillars
/usr/bin/python3 wiki/scripts/validate_wiki.py

# 2. Audit all 2,700 media and literature canon records
/usr/bin/python3 wiki/scripts/validate_media_canon.py

# 3. Rebuild the static HTML site
/usr/bin/python3 wiki/scripts/build_preview_site.py
```

---

*Maintained for the Association of Professional Futurists (APF)*
