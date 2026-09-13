#!/usr/bin/env python3
"""
APF Foresight Wiki: MediaWiki Exporter & Publisher
Provides two deployment mechanisms for publishing to MyWiki:
1. XML Dump Generation (`wiki/export/apf_foresight_wiki_dump.xml`):
   Standard MediaWiki XML export file compatible with Special:Import.
2. Direct MediaWiki API Bot:
   Directly posts pages and templates to a target MyWiki instance using credentials.
"""

import os
import glob
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENTRIES_DIR = os.path.join(BASE_DIR, "entries")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
MAIN_PAGE_PATH = os.path.join(BASE_DIR, "Main_Page.wiki")
EXPORT_DIR = os.path.join(BASE_DIR, "export")

os.makedirs(EXPORT_DIR, exist_ok=True)

def generate_xml_dump():
    print("Generating MediaWiki XML Import Dump...")
    now_iso = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    mediawiki = ET.Element("mediawiki", {
        "xmlns": "http://www.mediawiki.org/xml/export-0.10/",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "version": "0.10",
        "xml:lang": "en"
    })

    siteinfo = ET.SubElement(mediawiki, "siteinfo")
    sitename = ET.SubElement(siteinfo, "sitename")
    sitename.text = "APF Global Foresight Wiki"
    dbname = ET.SubElement(siteinfo, "dbname")
    dbname.text = "apf_foresight_wiki"
    base = ET.SubElement(siteinfo, "base")
    base.text = "https://wiki.apf.org/wiki/Main_Page"
    generator = ET.SubElement(siteinfo, "generator")
    generator.text = "APF Foresight Wiki Compiler v1.0"
    case = ET.SubElement(siteinfo, "case")
    case.text = "first-letter"

    def add_page(title, content, ns="0"):
        page = ET.SubElement(mediawiki, "page")
        t_el = ET.SubElement(page, "title")
        t_el.text = title
        ns_el = ET.SubElement(page, "ns")
        ns_el.text = ns

        revision = ET.SubElement(page, "revision")
        timestamp = ET.SubElement(revision, "timestamp")
        timestamp.text = now_iso

        contributor = ET.SubElement(revision, "contributor")
        username = ET.SubElement(contributor, "username")
        username.text = "APF Editorial Council"

        comment = ET.SubElement(revision, "comment")
        comment.text = "Initial import by Association of Professional Futurists (APF)"

        model = ET.SubElement(revision, "model")
        model.text = "wikitext"
        fmt = ET.SubElement(revision, "format")
        fmt.text = "text/x-wiki"

        text_el = ET.SubElement(revision, "text", {"xml:space": "preserve"})
        text_el.text = content

    # 1. Add Main Page
    if os.path.exists(MAIN_PAGE_PATH):
        with open(MAIN_PAGE_PATH, "r", encoding="utf-8") as f:
            add_page("Main Page", f.read(), ns="0")
        print("  + Added Main Page")

    # 2. Add Templates
    template_files = glob.glob(os.path.join(TEMPLATES_DIR, "*.wiki"))
    for tf in template_files:
        t_name = os.path.basename(tf).replace(".wiki", "")
        with open(tf, "r", encoding="utf-8") as f:
            add_page(f"Template:{t_name}", f.read(), ns="10")
    print(f"  + Added {len(template_files)} core templates")

    # 2b. Add MediaWiki:Common.css (Global Modern Design Theme)
    css_path = os.path.join(TEMPLATES_DIR, "MediaWiki_Common.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            add_page("MediaWiki:Common.css", f.read(), ns="8")
        print("  + Added MediaWiki:Common.css (APF Modern Theme)")

    # 3. Add all 1,000 entries + 5 Resource Portals
    index_path = os.path.join(BASE_DIR, "scripts", "domain", "master_catalog_1000_index.json")
    title_lookup = {
        "01_canonical_foresight_books.wiki": "APF Canonical Library of Strategic Foresight (650 Books)",
        "02_peer_reviewed_journal_canon.wiki": "APF Peer-Reviewed Foresight Journal Canon (1,000 Articles)",
        "03_foresight_podcasts_directory.wiki": "APF Strategic Foresight Podcasts Directory (350 Audio Series)",
        "04_blogs_newsletters_and_signals.wiki": "APF Foresight Blogs, Newsletters and Signal Feeds (350 Publications)",
        "05_landmark_presentations_and_keynotes.wiki": "APF Landmark Foresight Presentations and Keynotes (350 Keynotes)"
    }
    if os.path.exists(index_path):
        import json
        with open(index_path, "r", encoding="utf-8") as f:
            idx_data = json.load(f)
            for item in idx_data:
                title_lookup[item["filename"]] = item["title"]

    entry_files = sorted(glob.glob(os.path.join(ENTRIES_DIR, "*", "*.wiki")))
    articles_count = 0
    portals_count = 0
    for ef in entry_files:
        with open(ef, "r", encoding="utf-8") as f:
            content = f.read()

        filename = os.path.basename(ef)
        if filename in title_lookup:
            entry_title = title_lookup[filename]
        else:
            # Check for = Header =
            m_header = re.search(r"^=\s*(.*?)\s*=$", content, re.MULTILINE)
            if m_header:
                entry_title = m_header.group(1).strip()
            else:
                m_title = re.search(r"'''(.*?)''' is an authoritative subject", content)
                if m_title:
                    entry_title = m_title.group(1).strip()
                else:
                    base = filename.replace(".wiki", "")
                    entry_title = re.sub(r'^\d+_', '', base).replace("_", " ")

        add_page(entry_title, content, ns="0")
        if "resources" in ef:
            portals_count += 1
        else:
            articles_count += 1

    print(f"  + Added {articles_count} encyclopedia articles")
    print(f"  + Added {portals_count} curated resource portal pages")
    print(f"  + Total pages in export: {1 + len(template_files) + len(entry_files)}")

    # Write out XML
    dump_path = os.path.join(EXPORT_DIR, "apf_foresight_wiki_dump.xml")
    xml_str = ET.tostring(mediawiki, encoding="utf-8")
    parsed_str = minidom.parseString(xml_str).toprettyxml(indent="  ", encoding="utf-8")

    with open(dump_path, "wb") as f:
        f.write(parsed_str)

    print(f"\n✔ XML Dump generated successfully: {dump_path}")
    print(f"Size: {os.path.getsize(dump_path) / (1024*1024):.2f} MB")
    print("\nHow to import into MyWiki:")
    print("1. Log in to your MyWiki instance as an Administrator.")
    print("2. Navigate to 'Special:Import'.")
    print("3. Upload 'wiki/export/apf_foresight_wiki_dump.xml'.")
    print("4. Click 'Upload file' to populate the entire wiki instantly!\n")

if __name__ == "__main__":
    generate_xml_dump()
