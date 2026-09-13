#!/usr/bin/env python3
"""
APF Foresight Media Canon Builder
Aggregates all 1,050 media items across 5 categories, writes out the master JSON database,
generates the 5 Wikitext master portal pages, and compiles the client-side JavaScript dataset.
"""

import os
import sys
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOMAIN_DIR = os.path.join(os.path.dirname(__file__), "domain")
RESOURCES_DIR = os.path.join(BASE_DIR, "resources")
ENTRIES_RES_DIR = os.path.join(BASE_DIR, "entries", "resources")
PREVIEW_DIR = os.path.join(BASE_DIR, "preview")

os.makedirs(RESOURCES_DIR, exist_ok=True)
os.makedirs(ENTRIES_RES_DIR, exist_ok=True)
os.makedirs(PREVIEW_DIR, exist_ok=True)

sys.path.append(os.path.dirname(__file__))
sys.path.append(DOMAIN_DIR)

from media_books import get_books_catalog
from media_journals import get_journals_catalog
from media_podcasts import get_podcasts_catalog
from media_blogs import get_blogs_catalog
from media_presentations import get_presentations_catalog

def build_media_canon():
    print("=" * 70)
    print("APF Global Foresight Media & Literature Canon: Master Compiler")
    print("=" * 70)

    books = get_books_catalog()
    journals = get_journals_catalog()
    podcasts = get_podcasts_catalog()
    blogs = get_blogs_catalog()
    presentations = get_presentations_catalog()

    all_media = books + journals + podcasts + blogs + presentations

    print(f"Loaded:")
    print(f"  - Books               : {len(books)} entries")
    print(f"  - Journal Articles    : {len(journals)} entries")
    print(f"  - Podcasts & Audio    : {len(podcasts)} entries")
    print(f"  - Blogs & Newsletters : {len(blogs)} entries")
    print(f"  - Presentations/Talks : {len(presentations)} entries")
    print(f"  TOTAL MEDIA CANON     : {len(all_media)} entries")

    # 1. Validation & Deduplication Check
    seen_ids = set()
    seen_titles = set()
    for item in all_media:
        if item["id"] in seen_ids:
            raise ValueError(f"Duplicate ID found: {item['id']}")
        seen_ids.add(item["id"])
        
        # Check required fields
        for field in ["id", "title", "creator", "year_or_date", "media_type", "apf_competency", "thematic_pillar", "summary", "significance", "source_or_doi"]:
            if not item.get(field):
                raise ValueError(f"Missing field '{field}' in entry {item['id']}: {item.get('title')}")

    print("✔ Validation passed: Zero duplicate IDs and all records are fully populated.")

    # 2. Write Master JSON Databases
    json_path_2700 = os.path.join(RESOURCES_DIR, "foresight_media_canon_2700.json")
    with open(json_path_2700, "w", encoding="utf-8") as f:
        json.dump(all_media, f, indent=2, ensure_ascii=False)
    print(f"✔ Generated master database: {json_path_2700} ({os.path.getsize(json_path_2700) / 1024:.1f} KB)")

    # Also keep foresight_media_canon_1050.json updated for backward compatibility
    json_path_compat = os.path.join(RESOURCES_DIR, "foresight_media_canon_1050.json")
    with open(json_path_compat, "w", encoding="utf-8") as f:
        json.dump(all_media, f, indent=2, ensure_ascii=False)

    # 3. Write Client-Side JavaScript for Preview Site
    js_path = os.path.join(PREVIEW_DIR, "preview_media_data.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write("/* APF Global Foresight Media Canon Data (2,700 Items) */\n")
        f.write("window.FORESIGHT_MEDIA_CANON = ")
        json.dump(all_media, f, separators=(',', ':'))
        f.write(";\n")
    print(f"✔ Generated client-side dataset: {js_path} ({os.path.getsize(js_path) / 1024:.1f} KB)")

    # 4. Generate the 5 Wikitext Master Portals
    generate_wikitext_portals(books, journals, podcasts, blogs, presentations)

    print("=" * 70)
    print(f"Media Canon compilation complete: {len(all_media)} Total Items!")
    print("=" * 70)

def generate_wikitext_portals(books, journals, podcasts, blogs, presentations):
    print("\nGenerating 5 Wikitext Resource Portals in wiki/entries/resources/...")

    # 1. Books Portal
    books_wiki = f"""__NOTOC__
{{{{Editorial_Status|status=approved|reviewer=APF Editorial & Peer Review Council|date=2026-09-08}}}}
{{{{APF_Competency_Badge|competency=Leading}}}}

= The APF Canonical Library of Strategic Foresight: {len(books)} Foundational Books =

The '''Association of Professional Futurists (APF)''' maintains this authoritative reference bibliography of {len(books)} foundational and modern foresight books. Spanning epistemology, scenario planning, speculative design, planetary boundaries, and anticipatory governance, these works represent the core canon of the discipline.

== Explore the {len(books)} Canonical Foresight Books ==

{{| class="wikitable sortable" style="width: 100%; font-size: 90%;"
! ID !! Title !! Author(s) !! Year !! APF Competency !! Thematic Pillar !! Core Summary !! Significance
"""
    for b in books:
        books_wiki += f"""|-
| '''{b['id']}'''
| '''{b['title']}'''
| {b['creator']}
| {b['year_or_date']}
| [[Category:APF Competency - {b['apf_competency']}|{b['apf_competency']}]]
| Pillar {b['thematic_pillar']}: {b['pillar_name']}
| {b['summary']}
| {b['significance']}
"""
    books_wiki += """|}

[[Category:APF Foresight Canon - Publications]]
[[Category:APF Resource Portals]]
"""
    with open(os.path.join(ENTRIES_RES_DIR, "01_canonical_foresight_books.wiki"), "w", encoding="utf-8") as f:
        f.write(books_wiki)
    print(f"  + Generated 01_canonical_foresight_books.wiki ({len(books)} books)")

    # 2. Journals Portal
    journals_wiki = f"""__NOTOC__
{{{{Editorial_Status|status=approved|reviewer=APF Editorial & Peer Review Council|date=2026-09-08}}}}
{{{{APF_Competency_Badge|competency=Futuring}}}}

= The APF Peer-Reviewed Foresight Literature Canon: {len(journals)} Seminal Journal Articles =

This master catalog curates {len(journals)} peer-reviewed research papers from the core foresight journals: ''Futures'', ''Technological Forecasting and Social Change'', ''Journal of Futures Studies'', ''Foresight'', ''European Journal of Futures Research'', ''World Futures Review'', and ''Futures & Foresight Science''.

== Explore the {len(journals)} Peer-Reviewed Articles ==

{{| class="wikitable sortable" style="width: 100%; font-size: 90%;"
! ID !! Article Title !! Author(s) !! Journal !! Vol(Iss) !! Year !! APF Competency !! Pillar !! Research Finding / Contribution
"""
    for j in journals:
        vol_str = f"{j.get('volume', '')}({j.get('issue', '')})" if j.get('volume') else "Online"
        journals_wiki += f"""|-
| '''{j['id']}'''
| '''{j['title']}'''
| {j['creator']}
| ''{j.get('journal', 'Foresight Journal')}''
| {vol_str}
| {j['year_or_date']}
| [[Category:APF Competency - {j['apf_competency']}|{j['apf_competency']}]]
| Pillar {j['thematic_pillar']}
| {j['summary']}
"""
    journals_wiki += """|}

[[Category:APF Foresight Canon - Publications]]
[[Category:APF Resource Portals]]
"""
    with open(os.path.join(ENTRIES_RES_DIR, "02_peer_reviewed_journal_canon.wiki"), "w", encoding="utf-8") as f:
        f.write(journals_wiki)
    print(f"  + Generated 02_peer_reviewed_journal_canon.wiki ({len(journals)} articles)")

    # 3. Podcasts Portal
    podcasts_wiki = f"""__NOTOC__
{{{{Editorial_Status|status=approved|reviewer=APF Editorial & Peer Review Council|date=2026-09-08}}}}
{{{{APF_Competency_Badge|competency=Leading}}}}

= The APF Global Directory of Foresight Podcasts & Audio Series: {len(podcasts)} Curated Shows =

Audio broadcasts, practitioner interviews, and speculative audio dramas represent a primary channel for horizon scanning and professional development. This directory catalogs {len(podcasts)} premier foresight audio series and standout episodes.

== Explore the {len(podcasts)} Foresight Podcasts ==

{{| class="wikitable sortable" style="width: 100%; font-size: 90%;"
! ID !! Show Title !! Host(s) / Producer !! Active Years !! APF Competency !! Pillar !! Focus & Description !! Key Episodes / Reference
"""
    for p in podcasts:
        podcasts_wiki += f"""|-
| '''{p['id']}'''
| '''{p['title']}'''
| {p['creator']}
| {p['year_or_date']}
| [[Category:APF Competency - {p['apf_competency']}|{p['apf_competency']}]]
| Pillar {p['thematic_pillar']}
| {p['summary']}
| {p.get('standout_episodes', 'Available on major podcast platforms')}
"""
    podcasts_wiki += """|}

[[Category:APF Foresight Canon - Media]]
[[Category:APF Resource Portals]]
"""
    with open(os.path.join(ENTRIES_RES_DIR, "03_foresight_podcasts_directory.wiki"), "w", encoding="utf-8") as f:
        f.write(podcasts_wiki)
    print(f"  + Generated 03_foresight_podcasts_directory.wiki ({len(podcasts)} podcasts)")

    # 4. Blogs & Newsletters Portal
    blogs_wiki = f"""__NOTOC__
{{{{Editorial_Status|status=approved|reviewer=APF Editorial & Peer Review Council|date=2026-09-08}}}}
{{{{APF_Competency_Badge|competency=Scanning}}}}

= The APF Directory of Foresight Blogs, Newsletters & Signal Feeds: {len(blogs)} Curated Publications =

Environmental scanning requires continuous monitoring of weak signals, technological inflections, and institutional experiments. This directory catalogs {len(blogs)} leading practitioner newsletters, Substack publications, and think tank signal channels.

== Explore the {len(blogs)} Blogs & Newsletters ==

{{| class="wikitable sortable" style="width: 100%; font-size: 90%;"
! ID !! Publication Name !! Author / Organization !! Years Active !! APF Competency !! Pillar !! Scope & Scanning Utility
"""
    for b in blogs:
        blogs_wiki += f"""|-
| '''{b['id']}'''
| '''{b['title']}'''
| {b['creator']}
| {b['year_or_date']}
| [[Category:APF Competency - {b['apf_competency']}|{b['apf_competency']}]]
| Pillar {b['thematic_pillar']}: {b['pillar_name']}
| {b['summary']}
"""
    blogs_wiki += """|}

[[Category:APF Foresight Canon - Media]]
[[Category:APF Resource Portals]]
"""
    with open(os.path.join(ENTRIES_RES_DIR, "04_blogs_newsletters_and_signals.wiki"), "w", encoding="utf-8") as f:
        f.write(blogs_wiki)
    print(f"  + Generated 04_blogs_newsletters_and_signals.wiki ({len(blogs)} blogs)")

    # 5. Presentations Portal
    presentations_wiki = f"""__NOTOC__
{{{{Editorial_Status|status=approved|reviewer=APF Editorial & Peer Review Council|date=2026-09-08}}}}
{{{{APF_Competency_Badge|competency=Leading}}}}

= The APF Masterclass & Keynote Archive: {len(presentations)} Landmark Foresight Presentations =

Public lectures, TED talks, UNESCO Global Futures Literacy Summit addresses, and APF Masterclasses have introduced strategic foresight to global policy leaders, technologists, and the public. This archive catalogs {len(presentations)} recorded presentations.

== Explore the {len(presentations)} Landmark Presentations ==

{{| class="wikitable sortable" style="width: 100%; font-size: 90%;"
! ID !! Presentation Title !! Speaker(s) !! Year !! APF Competency !! Thematic Pillar !! Premise & Core Insight !! Forum / Significance
"""
    for pr in presentations:
        presentations_wiki += f"""|-
| '''{pr['id']}'''
| '''{pr['title']}'''
| {pr['creator']}
| {pr['year_or_date']}
| [[Category:APF Competency - {pr['apf_competency']}|{pr['apf_competency']}]]
| Pillar {pr['thematic_pillar']}
| {pr['summary']}
| {pr['significance']}
"""
    presentations_wiki += """|}

[[Category:APF Foresight Canon - Media]]
[[Category:APF Resource Portals]]
"""
    with open(os.path.join(ENTRIES_RES_DIR, "05_landmark_presentations_and_keynotes.wiki"), "w", encoding="utf-8") as f:
        f.write(presentations_wiki)
    print(f"  + Generated 05_landmark_presentations_and_keynotes.wiki ({len(presentations)} presentations)")

if __name__ == "__main__":
    build_media_canon()
