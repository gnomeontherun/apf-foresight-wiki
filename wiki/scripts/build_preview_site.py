#!/usr/bin/env python3
"""
APF Foresight Wiki: Complete Interactive HTML Preview Site Generator
Compiles all 1,000 Wikitext entries across 20 Thematic Pillars and Main_Page.wiki
into an offline-browsable static site in wiki/preview/.

Features:
- Instant client-side search across all 1,000 entries
- APF 6 Core Competencies live filter (Framing, Scanning, Futuring, Designing, Adapting, Leading)
- Collapsible 20-Pillar accordion navigation
- Dark / Light mode toggle
- Intelligent internal Wikilink resolution
- Formatted infoboxes, citations, and editorial peer-review badges
"""

import os
import glob
import re
import html
import json
import shutil
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENTRIES_DIR = os.path.join(BASE_DIR, "entries")
PREVIEW_DIR = os.path.join(BASE_DIR, "preview")
ARTICLES_DIR = os.path.join(PREVIEW_DIR, "articles")
MAIN_PAGE_PATH = os.path.join(BASE_DIR, "Main_Page.wiki")
INDEX_PATH = os.path.join(BASE_DIR, "scripts", "domain", "master_catalog_1000_index.json")

os.makedirs(ARTICLES_DIR, exist_ok=True)

def sanitize_for_url(title):
    clean = re.sub(r'[\\/*?:"<>|()]', "", title)
    clean = clean.replace("&", "and").replace(" / ", " - ")
    return clean.strip().replace(" ", "_")

def build_title_lookup(catalog):
    """Builds a rich lookup table mapping titles, variations, and acronyms to article slugs."""
    lookup = {}
    for item in catalog:
        slug = item["filename"].replace(".wiki", "")
        title = item["title"]
        
        # 1. Exact title
        lookup[title.lower()] = slug
        lookup[slug.lower()] = slug
        
        # 2. Base title without parentheses: "Strategic Foresight (Discipline Overview)" -> "Strategic Foresight"
        base_match = re.match(r"^([^(]+)\s*\(", title)
        if base_match:
            lookup[base_match.group(1).strip().lower()] = slug

        # 3. Inside parentheses if it looks like an acronym or subtitle: "(CLA)" -> "cla"
        paren_match = re.findall(r"\(([^)]+)\)", title)
        for pm in paren_match:
            if len(pm.strip()) <= 10:
                lookup[pm.strip().lower()] = slug

        # 4. Sanitized form
        clean_key = sanitize_for_url(title).lower()
        lookup[clean_key] = slug
        
    return lookup

def wikitext_to_html(wiki, title_lookup, is_article=True):
    h = wiki
    prefix = "" if is_article else "articles/"

    # 1. Editorial status banner
    status_match = re.search(r'\{\{Editorial_Status\|status=(.*?)(?:\|reviewer=(.*?))?(?:\|date=(.*?))?\}\}', h)
    if status_match:
        status_val = status_match.group(1).strip().lower()
        reviewer = status_match.group(2) or "Pending Assignment"
        date = status_match.group(3) or "2026/2027"
        if status_val == "approved":
            status_html = '<span class="badge-approved">✔ Vetted &amp; Approved</span>'
            badge_class = ""
            review_text = f"Evaluated by {reviewer}"
        elif status_val == "in_review":
            status_html = '<span class="badge-draft-pill" style="color:#d97706; font-weight:700;">⏳ In Peer Review</span>'
            badge_class = "badge-draft"
            review_text = f"Reviewer: {reviewer}"
        else:
            status_html = '<span class="badge-draft-pill" style="color:#64748b; font-weight:700;">📝 Working Draft (Pending Peer Review)</span>'
            badge_class = "badge-draft"
            review_text = "Awaiting Verification"

        banner_html = f'''
        <div class="apf-editorial-badge {badge_class}">
            <div><strong>APF Editorial Status:</strong> {status_html} &bull; {review_text} &bull; <a href="../review.html" style="color:inherit; text-decoration:underline;">Submit Peer Audit &rarr;</a></div>
            <div class="audit-date">Cycle: {date}</div>
        </div>
        '''
        h = re.sub(r'\{\{Editorial_Status.*?\}\}', banner_html, h)

    # 2. Infoboxes
    def parse_infobox(m):
        box_text = m.group(1)
        lines = box_text.strip().split("\n")
        rows = []
        name = "Encyclopedia Entry Overview"
        for line in lines[1:]:
            if line.startswith("|") and "=" in line:
                k, v = line[1:].split("=", 1)
                k_clean = k.strip().replace("_", " ").title()
                v_clean = v.strip()
                if k_clean.lower() == "name":
                    name = v_clean
                else:
                    # Clean wikilinks inside table
                    v_clean = re.sub(r'\[\[(?:[^|\]]+\|)?([^\]]+)\]\]', r'\1', v_clean)
                    rows.append(f"<tr><th>{html.escape(k_clean)}</th><td>{html.escape(v_clean)}</td></tr>")
        
        return f'''
        <div class="infobox-card">
            <div class="infobox-header">{html.escape(name)}</div>
            <table class="infobox-table">
                {"".join(rows)}
            </table>
        </div>
        '''

    h = re.sub(r'(\{\{Infobox [^}]+(?:\{[^}]+?\}[^}]*)*\}\})', parse_infobox, h, flags=re.DOTALL)

    # 3. Citations
    def parse_citation(m):
        params = dict(re.findall(r'\|([a-zA-Z_]+)\s*=\s*([^|\}]+)', m.group(0)))
        author = params.get("author", "Academic Reference")
        year = params.get("year", "n.d.")
        title = params.get("title", "Foundational Research Document")
        journal = params.get("journal", "")
        volume = params.get("volume", "")
        pages = params.get("pages", "")
        doi = params.get("doi", "")
        publisher = params.get("publisher", "")
        
        j_str = f"<em>{html.escape(journal)}</em>, <strong>{html.escape(volume)}</strong>, pp. {html.escape(pages)}." if journal else f"<em>{html.escape(publisher)}</em>."
        doi_str = f" <a href='https://doi.org/{html.escape(doi)}' target='_blank' class='wiki-link'>doi:{html.escape(doi)}</a>" if doi else ""
        return f"<li class='citation-item'><strong>{html.escape(author)}</strong> ({html.escape(year)}). \"{html.escape(title)}\". {j_str}{doi_str}</li>"

    h = re.sub(r'\{\{Foresight_Citation[^\}]+\}\}', parse_citation, h)

    # 4. Competency badge
    def parse_badge(m):
        comp = m.group(1).strip()
        return f'<span class="competency-tag tag-{comp}">✦ APF Core Competency: {comp}</span>'
    h = re.sub(r'\{\{APF_Competency_Badge\|(?:competency=)?(.*?)\}\}', parse_badge, h)

    # Clean any leftover unknown templates
    h = re.sub(r'\{\{[^\}]+\}\}', '', h)

    # 5. Headers with auto-anchors
    def parse_h2(m):
        title = m.group(1).strip()
        slug = sanitize_for_url(title).lower()
        return f'<h2 id="{slug}">{title}</h2>'
    h = re.sub(r'^== (.*?) ==$', parse_h2, h, flags=re.MULTILINE)

    def parse_h3(m):
        title = m.group(1).strip()
        slug = sanitize_for_url(title).lower()
        return f'<h3 id="{slug}">{title}</h3>'
    h = re.sub(r'^=== (.*?) ===$', parse_h3, h, flags=re.MULTILINE)

    h = re.sub(r'^==== (.*?) ====$', r'<h4>\1</h4>', h, flags=re.MULTILINE)

    # 6. Bold and italics
    h = re.sub(r"'''(.*?)'''", r'<strong>\1</strong>', h)
    h = re.sub(r"''(.*?)''", r'<em>\1</em>', h)

    # 7. Wikilinks resolution
    def replace_wikilink(m):
        content = m.group(1).strip()
        if "|" in content:
            target, label = content.split("|", 1)
        else:
            target, label = content, content

        target = target.strip()
        label = label.strip()

        if target.startswith("Category:APF Competency - "):
            comp_name = target.replace("Category:APF Competency - ", "").strip()
            return f'<a href="javascript:filterByCompetency(\'{comp_name}\')" class="wiki-link" title="Filter by APF {comp_name}">{html.escape(label)}</a>'
        if target.startswith("Category:"):
            return ""

        target_key = target.lower()
        if target_key in title_lookup:
            target_slug = title_lookup[target_key]
            return f'<a href="{prefix}{target_slug}.html" class="wiki-link" title="{html.escape(target)}">{html.escape(label)}</a>'
        
        # Check base without paren
        base = re.sub(r'\s*\([^)]*\)', '', target_key).strip()
        if base in title_lookup:
            target_slug = title_lookup[base]
            return f'<a href="{prefix}{target_slug}.html" class="wiki-link" title="{html.escape(target)}">{html.escape(label)}</a>'

        return f'<span class="wiki-link-unresolved" title="Topic reference">{html.escape(label)}</span>'

    h = re.sub(r'\[\[(.*?)\]\]', replace_wikilink, h)

    # 8. Tables
    def parse_table(m):
        table_raw = m.group(1)
        lines = table_raw.strip().split("\n")
        out = ['<table class="apf-data-table">']
        in_tr = False
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("|-"):
                if in_tr:
                    out.append("</tr>")
                out.append("<tr>")
                in_tr = True
            elif line.startswith("! "):
                cells = line[2:].split("!!")
                if not in_tr:
                    out.append("<tr>")
                    in_tr = True
                for c in cells:
                    out.append(f"<th>{c.strip()}</th>")
            elif line.startswith("| "):
                cells = line[2:].split("||")
                if not in_tr:
                    out.append("<tr>")
                    in_tr = True
                for c in cells:
                    out.append(f"<td>{c.strip()}</td>")
        if in_tr:
            out.append("</tr>")
        out.append("</table>")
        return "\n".join(out)

    h = re.sub(r'\{\|(.*?)\|\}', parse_table, h, flags=re.DOTALL)

    # 9. Lists
    lines = h.split("\n")
    processed_lines = []
    in_ul = False
    in_ol = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("* "):
            if not in_ul:
                if in_ol:
                    processed_lines.append("</ol>")
                    in_ol = False
                processed_lines.append("<ul>")
                in_ul = True
            processed_lines.append(f"<li>{stripped[2:]}</li>")
        elif stripped.startswith("# "):
            if not in_ol:
                if in_ul:
                    processed_lines.append("</ul>")
                    in_ul = False
                processed_lines.append("<ol>")
                in_ol = True
            processed_lines.append(f"<li>{stripped[2:]}</li>")
        else:
            if in_ul:
                processed_lines.append("</ul>")
                in_ul = False
            if in_ol:
                processed_lines.append("</ol>")
                in_ol = False
            processed_lines.append(line)

    if in_ul:
        processed_lines.append("</ul>")
    if in_ol:
        processed_lines.append("</ol>")

    h = "\n".join(processed_lines)

    # 10. Wrap paragraphs
    blocks = h.split("\n\n")
    processed_blocks = []
    for b in blocks:
        b = b.strip()
        if not b:
            continue
        if any(b.startswith(tag) for tag in ["<h", "<div", "<ul", "<ol", "<li", "<table", "<table", "<span"]):
            processed_blocks.append(b)
        else:
            processed_blocks.append(f"<p>{b}</p>")

    return "\n".join(processed_blocks)

ARTICLE_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title} - APF Global Foresight Wiki</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../preview.css">
</head>
<body>
    <div id="sidebar-mount"></div>

    <main class="content-wrap">
        <header class="apf-top-bar">
            <div class="breadcrumbs">
                <a href="../index.html">Main Portal</a> &rsaquo;
                <span>{pillar_name}</span> &rsaquo;
                <strong>{page_title}</strong>
            </div>
            <div style="display: flex; gap: 16px; align-items: center;">
                <a href="../review.html" class="tool-btn" style="color: #fbbf24;">📋 Review Queue</a>
                <a href="../resources.html" class="tool-btn" style="color: var(--apf-cyan);">📚 Media Hub (2,700)</a>
                <button type="button" class="theme-toggle-btn tool-btn" title="Toggle Dark/Light Mode">🌓 Theme</button>
                <a href="../index.html" class="tool-btn">⌂ Main Portal</a>
            </div>
        </header>

        <article class="article-container">
            <div class="page-header">
                <h1>{page_title}</h1>
                <div class="article-meta-bar">
                    <span class="competency-tag tag-{competency}">✦ APF Core Competency: {competency}</span>
                    <span>&bull; Pillar {pillar_num}: {pillar_name}</span>
                    <span>&bull; {word_count:,} words</span>
                    <span>&bull; ~{read_time} min read</span>
                </div>
            </div>

            <div class="article-body">
                {rendered_content}
            </div>

            <footer class="article-footer">
                <div>
                    <strong>Association of Professional Futurists (APF)</strong> &bull; Official Knowledge Canon &bull; Working Draft (Pending Peer Review)
                </div>
                <div>
                    <a href="#top" class="wiki-link" onclick="window.scrollTo({{top:0, behavior:'smooth'}}); return false;">↑ Back to Top</a>
                </div>
            </footer>
        </article>
    </main>

    <script src="../preview_data.js"></script>
    <script src="../preview_app.js"></script>
</body>
</html>
"""

PORTAL_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>APF Global Foresight Wiki — Definitive Encyclopedia of Strategic Foresight</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="preview.css">
    <style>
        .hero-banner {{
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0369a1 100%);
            color: white;
            padding: 50px 40px;
            border-radius: 16px;
            margin-bottom: 40px;
            box-shadow: var(--shadow-lg);
        }}
        .hero-badge {{
            text-transform: uppercase;
            letter-spacing: 2px;
            font-size: 12px;
            font-weight: 700;
            color: var(--apf-accent);
            margin-bottom: 8px;
        }}
        .hero-title {{
            font-size: 42px;
            font-weight: 800;
            line-height: 1.15;
            margin-bottom: 14px;
        }}
        .hero-subtitle {{
            font-size: 17px;
            line-height: 1.6;
            color: #e2e8f0;
            max-width: 820px;
            margin-bottom: 24px;
            font-weight: 300;
        }}
        .hero-stats {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            margin-bottom: 28px;
        }}
        .hero-stat-pill {{
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(8px);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            border: 1px solid rgba(255, 255, 255, 0.25);
        }}
        .hero-search {{
            max-width: 600px;
            position: relative;
        }}
        .hero-search input {{
            width: 100%;
            padding: 14px 20px;
            font-size: 16px;
            border-radius: 10px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            background: rgba(255, 255, 255, 0.95);
            color: var(--apf-navy);
            outline: none;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            transition: all 0.2s ease;
        }}
        .hero-search input:focus {{
            border-color: var(--apf-accent);
            background: white;
            box-shadow: 0 6px 25px rgba(0,0,0,0.3);
        }}
        .competency-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin-bottom: 50px;
        }}
        .comp-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-light);
            border-radius: 12px;
            padding: 24px;
            box-shadow: var(--shadow-sm);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            cursor: pointer;
        }}
        .comp-card:hover {{
            transform: translateY(-3px);
            box-shadow: var(--shadow-md);
        }}
        .comp-card-header {{
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .comp-count {{
            font-size: 12px;
            padding: 2px 8px;
            border-radius: 12px;
            font-weight: 600;
        }}
        .comp-card p {{
            font-size: 13.5px;
            color: var(--text-muted);
            margin-bottom: 12px;
            line-height: 1.5;
        }}
        .comp-card-links {{
            font-size: 13px;
        }}
        .pillars-section {{
            margin-bottom: 60px;
        }}
        .pillars-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px;
        }}
        .pillar-card {{
            background: var(--bg-surface);
            border: 1px solid var(--border-light);
            border-radius: 10px;
            padding: 20px;
            box-shadow: var(--shadow-sm);
        }}
        .pillar-card-title {{
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 6px;
            color: var(--text-main);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .pillar-card-links {{
            margin-top: 10px;
            padding-left: 18px;
            font-size: 13px;
        }}
        .pillar-card-links li {{
            margin-bottom: 4px;
        }}
    </style>
</head>
<body>
    <div id="sidebar-mount"></div>

    <main class="content-wrap">
        <header class="apf-top-bar">
            <div>
                <strong>Association of Professional Futurists</strong> &bull; Official Knowledge Canon
            </div>
            <div style="display: flex; gap: 16px; align-items: center;">
                <a href="review.html" class="tool-btn" style="color: #fbbf24;">📋 Review Queue</a>
                <a href="resources.html" class="tool-btn" style="color: var(--apf-cyan);">📚 Media Hub (2,700)</a>
                <button type="button" class="theme-toggle-btn tool-btn" title="Toggle Dark/Light Mode">🌓 Theme</button>
                <a href="https://apf.org" target="_blank" class="tool-btn">APF.org ↗</a>
            </div>
        </header>

        <div class="article-container" style="max-width: 1100px;">
            <section class="hero-banner" style="display: flex; align-items: center; gap: 32px; flex-wrap: wrap;">
                <img src="assets/apf_wiki_official_lockup.jpg" alt="Association of Professional Futurists Official Logo" class="hero-logo-img">
                <div style="flex: 1; min-width: 300px;">
                    <div class="hero-badge">Official Global Knowledge Repository</div>
                    <h1 class="hero-title">APF Global Foresight Wiki</h1>
                    <p class="hero-subtitle">
                        The foundational reference encyclopedia and working canon for strategic foresight and futures thinking — stewarded by the <strong>Association of Professional Futurists (APF)</strong> in draft form, undergoing open editorial and peer validation across the global community.
                    </p>
                    <div class="hero-stats">
                        <span class="hero-stat-pill">📚 1,000 Curated Articles</span>
                        <span class="hero-stat-pill">🏛️ 20 Thematic Pillars</span>
                        <span class="hero-stat-pill">🎯 6 APF Core Competencies</span>
                        <a href="resources.html" class="hero-stat-pill" style="color: #38bdf8; text-decoration: none; border-color: #38bdf8;">📖 2,700 Media Canon &rarr;</a>
                        <span class="hero-stat-pill">🏆 MSFW Awards Archive</span>
                        <span class="hero-stat-pill">🎓 45+ University Degrees</span>
                        <a href="review.html" class="hero-stat-pill" style="color: #fbbf24; text-decoration: none; border-color: #fbbf24;">📝 Editorial Review Queue (Drafts) &rarr;</a>
                    </div>
                    <div class="hero-search">
                        <input type="text" id="heroPortalSearch" placeholder="Search the 1,000-article foresight canon (e.g. CLA, Delphi, Shell Scenarios, Polak)...">
                    </div>
                </div>
            </section>

            <section>
                <h2 style="font-size: 24px; font-weight: 800; margin-bottom: 16px; color: var(--text-main);">
                    Navigate by APF 6 Core Competencies
                </h2>
                <p style="font-size: 15px; color: var(--text-muted); margin-bottom: 24px;">
                    The APF Competency Model defines the essential skillsets for professional futurists. Click any competency to filter the library or explore featured entries:
                </p>

                <div class="competency-grid">
                    <div class="comp-card" onclick="filterByCompetency('Framing')">
                        <div class="comp-card-header" style="color: #0284c7;">
                            <span>1. Framing</span>
                            <span class="comp-count tag-Framing">135 Articles</span>
                        </div>
                        <p>Scoping domains, auditing cognitive biases, temporal discounting, and uncovering deep unexamined worldviews.</p>
                        <div class="comp-card-links">
                            <strong>Featured:</strong>
                            <a href="articles/0001_Strategic_Foresight_(Discipline_Overview).html" class="wiki-link">Strategic Foresight</a> &bull;
                            <a href="articles/0003_The_Futures_Cone_(Plausible,_Possible,_Probable,_Preferable).html" class="wiki-link">Futures Cone</a> &bull;
                            <a href="articles/0005_Post-Normal_Times_(Ziauddin_Sardar).html" class="wiki-link">Post-Normal Times</a>
                        </div>
                    </div>

                    <div class="comp-card" onclick="filterByCompetency('Scanning')">
                        <div class="comp-card-header" style="color: #d97706;">
                            <span>2. Scanning</span>
                            <span class="comp-count tag-Scanning">130 Articles</span>
                        </div>
                        <p>Detecting weak signals, tracking planetary boundaries, monitoring megatrends, and modeling wild cards.</p>
                        <div class="comp-card-links">
                            <strong>Featured:</strong>
                            <a href="articles/0151_Horizon_Scanning_(Environmental_Scanning_Principles).html" class="wiki-link">Horizon Scanning</a> &bull;
                            <a href="articles/0154_Weak_Signals_(Igor_Ansoff's_Theory).html" class="wiki-link">Weak Signals</a> &bull;
                            <a href="articles/0156_Black_Swan_Theory_(Nassim_Nicholas_Taleb).html" class="wiki-link">Black Swans</a>
                        </div>
                    </div>

                    <div class="comp-card" onclick="filterByCompetency('Futuring')">
                        <div class="comp-card-header" style="color: #7c3aed;">
                            <span>3. Futuring</span>
                            <span class="comp-count tag-Futuring">155 Articles</span>
                        </div>
                        <p>Developing plausible alternative scenarios, causal layered analysis, and computational system dynamics.</p>
                        <div class="comp-card-links">
                            <strong>Featured:</strong>
                            <a href="articles/0296_Causal_Layered_Analysis_(CLA).html" class="wiki-link">CLA</a> &bull;
                            <a href="articles/0297_The_Delphi_Method.html" class="wiki-link">Delphi Method</a> &bull;
                            <a href="articles/0299_Backcasting_(John_B._Robinson).html" class="wiki-link">Backcasting</a>
                        </div>
                    </div>

                    <div class="comp-card" onclick="filterByCompetency('Designing')">
                        <div class="comp-card-header" style="color: #059669;">
                            <span>4. Designing</span>
                            <span class="comp-count tag-Designing">230 Articles</span>
                        </div>
                        <p>Speculative design, experiential futures, artifact creation, and multi-century visionary synthesis.</p>
                        <div class="comp-card-links">
                            <strong>Featured:</strong>
                            <a href="articles/0491_Speculative_Design_(Dunne_and_Raby).html" class="wiki-link">Speculative Design</a> &bull;
                            <a href="articles/0492_Design_Fiction_(Bruce_Sterling,_Julian_Bleecker).html" class="wiki-link">Design Fiction</a> &bull;
                            <a href="articles/0493_Experiential_Futures_(Stuart_Candy).html" class="wiki-link">Experiential Futures</a>
                        </div>
                    </div>

                    <div class="comp-card" onclick="filterByCompetency('Adapting')">
                        <div class="comp-card-header" style="color: #ea580c;">
                            <span>5. Adapting</span>
                            <span class="comp-count tag-Adapting">80 Articles</span>
                        </div>
                        <p>Dynamic adaptive policy pathways, strategic agility, war gaming, and organizational antifragility.</p>
                        <div class="comp-card-links">
                            <strong>Featured:</strong>
                            <a href="articles/0661_Dynamic_Adaptive_Policy_Pathways_(DAPP).html" class="wiki-link">DAPP</a> &bull;
                            <a href="articles/0662_Robust_Decision_Making_(RDM___Robert_Lempert).html" class="wiki-link">RDM</a> &bull;
                            <a href="articles/0665_Antifragility_in_Strategy_(Nassim_Nicholas_Taleb).html" class="wiki-link">Antifragility</a>
                        </div>
                    </div>

                    <div class="comp-card" onclick="filterByCompetency('Leading')">
                        <div class="comp-card-header" style="color: #e11d48;">
                            <span>6. Leading</span>
                            <span class="comp-count tag-Leading">270 Articles</span>
                        </div>
                        <p>Anticipatory governance, institutional case studies, thought leaders, organizations, and university degrees.</p>
                        <div class="comp-card-links">
                            <strong>Featured:</strong>
                            <a href="articles/0721_Singapore_Centre_for_Strategic_Futures_(CSF).html" class="wiki-link">Singapore CSF</a> &bull;
                            <a href="articles/0723_Mont_Fleur_Scenarios_(South_Africa_1991-1992).html" class="wiki-link">Mont Fleur</a> &bull;
                            <a href="articles/0956_University_of_Houston_Master_of_Science_in_Foresight.html" class="wiki-link">UH Foresight</a>
                        </div>
                    </div>
                </div>
            </section>

            <section class="pillars-section">
                <h2 style="font-size: 24px; font-weight: 800; margin-bottom: 16px; color: var(--text-main);">
                    The 20 Thematic Pillars of Strategic Foresight
                </h2>
                <div class="pillars-grid" id="portalPillarsGrid">
                    {pillars_grid_html}
                </div>
            </section>

            <footer class="article-footer">
                <div>
                    <strong>Association of Professional Futurists (APF)</strong> &bull; Official Knowledge Canon &bull; 1,000 Working Drafts (Under Peer Review)
                </div>
                <div>
                    <a href="#top" class="wiki-link" onclick="window.scrollTo({{top:0, behavior:'smooth'}}); return false;">↑ Back to Top</a>
                </div>
            </footer>
        </div>
    </main>

    <script src="preview_data.js"></script>
    <script src="preview_app.js"></script>
</body>
</html>
"""

def generate_preview():
    print("=" * 70)
    print("APF Foresight Wiki: Interactive HTML Preview Builder")
    print("=" * 70)

    # 1. Load Index
    if not os.path.exists(INDEX_PATH):
        raise FileNotFoundError(f"Missing master catalog index: {INDEX_PATH}")

    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    print(f"Loaded {len(catalog)} entries from master catalog index.")

    # 2. Build Title Lookup
    title_lookup = build_title_lookup(catalog)
    print(f"Built wikilink lookup table with {len(title_lookup)} indexed variants.")

    # 3. Write preview_data.js
    compact_catalog = []
    for item in catalog:
        compact_catalog.append({
            "id": item["id"],
            "p": item["pillar_num"],
            "pDir": item["pillar_dir"],
            "pName": item["pillar_name"],
            "c": item["competency"],
            "t": item["title"],
            "a": item.get("author", ""),
            "s": item["filename"].replace(".wiki", ""),
            "w": item.get("word_count", 550)
        })

    preview_data_js_path = os.path.join(PREVIEW_DIR, "preview_data.js")
    with open(preview_data_js_path, "w", encoding="utf-8") as f:
        f.write("/* APF Global Foresight Wiki — Catalog Metadata */\n")
        f.write("window.APF_CATALOG = ")
        json.dump(compact_catalog, f, separators=(',', ':'))
        f.write(";\n")
    print(f"Generated preview_data.js ({os.path.getsize(preview_data_js_path) / 1024:.1f} KB)")

    # 4. Clean and Render 1,000 Articles
    if os.path.exists(ARTICLES_DIR):
        shutil.rmtree(ARTICLES_DIR)
    os.makedirs(ARTICLES_DIR, exist_ok=True)

    print("\nRendering 1,000 HTML article pages...")
    rendered_count = 0
    total_words = 0

    for item in catalog:
        filepath = item["filepath"]
        if not os.path.exists(filepath):
            print(f"Warning: file not found: {filepath}")
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            wikitext = f.read()

        rendered_body = wikitext_to_html(wikitext, title_lookup, is_article=True)
        word_count = item.get("word_count", len(wikitext.split()))
        total_words += word_count
        read_time = max(1, word_count // 200)

        slug = item["filename"].replace(".wiki", "")
        article_html = ARTICLE_HTML_TEMPLATE.format(
            page_title=html.escape(item["title"]),
            pillar_num=item["pillar_num"],
            pillar_name=html.escape(item["pillar_name"]),
            competency=item["competency"],
            word_count=word_count,
            read_time=read_time,
            rendered_content=rendered_body
        )

        out_path = os.path.join(ARTICLES_DIR, f"{slug}.html")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(article_html)

        rendered_count += 1
        if rendered_count % 200 == 0:
            print(f"  ... rendered {rendered_count}/1,000 articles")

    print(f"✔ Successfully rendered {rendered_count} article pages ({total_words:,} total words).")

    # Also render any resource portals from wiki/entries/resources/
    res_files = sorted(glob.glob(os.path.join(BASE_DIR, "entries", "resources", "*.wiki")))
    if res_files:
        print(f"Rendering {len(res_files)} resource portal pages...")
        for rf in res_files:
            with open(rf, "r", encoding="utf-8") as f:
                r_wiki = f.read()
            r_slug = os.path.basename(rf).replace(".wiki", "")
            r_body = wikitext_to_html(r_wiki, title_lookup, is_article=True)
            r_clean_title = re.sub(r'^\d+_', '', r_slug).replace('_', ' ').title()
            r_html = ARTICLE_HTML_TEMPLATE.format(
                page_title=html.escape(r_clean_title),
                pillar_num="Resource",
                pillar_name="Foresight Media & Literature Canon",
                competency="Leading",
                word_count=len(r_wiki.split()),
                read_time=max(1, len(r_wiki.split()) // 200),
                rendered_content=r_body
            )
            with open(os.path.join(ARTICLES_DIR, f"{r_slug}.html"), "w", encoding="utf-8") as f:
                f.write(r_html)

    # 5. Build Pillars Grid HTML for Portal
    pillars_map = {}
    for item in catalog:
        p_num = item["pillar_num"]
        if p_num not in pillars_map:
            pillars_map[p_num] = {
                "num": p_num,
                "name": item["pillar_name"],
                "competency": item["competency"],
                "items": []
            }
        pillars_map[p_num]["items"].append(item)

    pillars_grid_cards = []
    for p_num in sorted(pillars_map.keys()):
        p_info = pillars_map[p_num]
        items = p_info["items"]
        sample_links = []
        for it in items[:4]:
            it_slug = it["filename"].replace(".wiki", "")
            sample_links.append(f'<li><a href="articles/{it_slug}.html" class="wiki-link">{html.escape(it["title"])}</a></li>')
        
        card = f'''
        <div class="pillar-card">
            <div class="pillar-card-title">
                <span>Pillar {p_num}: {html.escape(p_info["name"])}</span>
                <span class="comp-count tag-{p_info["competency"]}">{len(items)} Entries</span>
            </div>
            <div style="font-size: 11.5px; color: var(--text-muted); margin-bottom: 8px;">
                APF Core Competency: <strong>{p_info["competency"]}</strong>
            </div>
            <ul class="pillar-card-links">
                {"".join(sample_links)}
                <li style="margin-top: 6px;"><a href="javascript:void(0)" onclick="const h = document.querySelector('.pillar-header[data-pnum=\\'{p_num}\\']'); if(h) {{ h.click(); h.scrollIntoView({{behavior: 'smooth'}}); }}" class="wiki-link"><em>View all {len(items)} entries &rarr;</em></a></li>
            </ul>
        </div>
        '''
        pillars_grid_cards.append(card)

    # 6. Render Main Portal index.html
    portal_html = PORTAL_HTML_TEMPLATE.format(
        pillars_grid_html="\n".join(pillars_grid_cards)
    )

    index_html_path = os.path.join(PREVIEW_DIR, "index.html")
    with open(index_html_path, "w", encoding="utf-8") as f:
        f.write(portal_html)

    print(f"✔ Rendered Main Portal index.html ({os.path.getsize(index_html_path) / 1024:.1f} KB)")
    print(f"\nPreview site build complete!")
    print(f"Open locally in any browser: file://{index_html_path}")
    print("=" * 70)

if __name__ == "__main__":
    generate_preview()
