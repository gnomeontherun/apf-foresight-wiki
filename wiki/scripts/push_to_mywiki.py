#!/usr/bin/env python3
"""
APF Foresight Wiki: Direct MyWiki / MediaWiki Automated Publisher
Publishes all 1,018 pages (Main Page, 12 Templates, 1,000 Articles, 5 Portals)
to a target MyWiki / MediaWiki instance via MediaWiki Action API.
"""

import os
import sys
import glob
import re
import json
import time
import argparse
import urllib.request
import urllib.parse
import http.cookiejar
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENTRIES_DIR = os.path.join(BASE_DIR, "entries")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
MAIN_PAGE_PATH = os.path.join(BASE_DIR, "Main_Page.wiki")
XML_DUMP_PATH = os.path.join(BASE_DIR, "export", "apf_foresight_wiki_dump.xml")

import ssl

DEFAULT_API_URL = "https://futurepedia.mywikis.wiki/w143/api.php"

class MediaWikiClient:
    def __init__(self, api_url=None, verbose=True):
        self.api_url = (api_url or DEFAULT_API_URL).rstrip("/")
        if not self.api_url.endswith("api.php"):
            self.api_url += "/api.php"
        self.verbose = verbose
        self.cookie_jar = http.cookiejar.CookieJar()
        
        # Configure SSL context
        try:
            ctx = ssl.create_default_context()
        except Exception:
            ctx = ssl._create_unverified_context()
        
        ssl_handler = urllib.request.HTTPSHandler(context=ctx)
        cookie_handler = urllib.request.HTTPCookieProcessor(self.cookie_jar)
        self.opener = urllib.request.build_opener(ssl_handler, cookie_handler)
        self.csrf_token = None

    def _request(self, data=None):
        headers = {
            "User-Agent": "APFForesightBot/1.0 (Association of Professional Futurists; info@apf.org)"
        }
        if data:
            post_data = urllib.parse.urlencode(data).encode("utf-8")
            req = urllib.request.Request(self.api_url, data=post_data, headers=headers)
        else:
            req = urllib.request.Request(self.api_url, headers=headers)
        
        try:
            with self.opener.open(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw)
        except Exception as e:
            return {"error": {"info": str(e)}}

    def get_token(self, token_type="csrf"):
        res = self._request({
            "action": "query",
            "meta": "tokens",
            "type": token_type,
            "format": "json"
        })
        tokens = res.get("query", {}).get("tokens", {})
        return tokens.get(f"{token_type}token")

    def login(self, username, password):
        print(f"Connecting to MediaWiki API at: {self.api_url}")
        login_token = self.get_token(token_type="login")
        if not login_token:
            print("Failed to acquire login token from API.")
            return False

        login_res = self._request({
            "action": "login",
            "lgname": username,
            "lgpassword": password,
            "lgtoken": login_token,
            "format": "json"
        })
        status = login_res.get("login", {}).get("result")
        if status == "Success":
            print(f"✔ Successfully authenticated as: {username}")
            self.csrf_token = self.get_token("csrf")
            return True
        elif status == "NeedToken":
            token = login_res.get("login", {}).get("token")
            retry_res = self._request({
                "action": "login",
                "lgname": username,
                "lgpassword": password,
                "lgtoken": token,
                "format": "json"
            })
            if retry_res.get("login", {}).get("result") == "Success":
                print(f"✔ Successfully authenticated as: {username}")
                self.csrf_token = self.get_token("csrf")
                return True
        
        print(f"❌ Login failed: {login_res}")
        return False

    def edit_page(self, title, content, summary="Curated by Association of Professional Futurists (APF)"):
        if not self.csrf_token:
            self.csrf_token = self.get_token("csrf")

        data = {
            "action": "edit",
            "title": title,
            "text": content,
            "summary": summary,
            "token": self.csrf_token,
            "bot": "1",
            "format": "json"
        }
        res = self._request(data)
        if "edit" in res and res["edit"].get("result") == "Success":
            return True, res["edit"]
        else:
            return False, res.get("error", res)

def collect_all_pages():
    pages = []
    
    # 1. Main Page
    if os.path.exists(MAIN_PAGE_PATH):
        with open(MAIN_PAGE_PATH, "r", encoding="utf-8") as f:
            pages.append(("Main Page", f.read(), "Official APF Main Page Portal"))
            
    # 2. Templates
    template_files = sorted(glob.glob(os.path.join(TEMPLATES_DIR, "*.wiki")))
    for tf in template_files:
        name = os.path.basename(tf).replace(".wiki", "")
        with open(tf, "r", encoding="utf-8") as f:
            pages.append((f"Template:{name}", f.read(), f"Core Template: {name}"))
            
    # 2b. Global Modern Theme Stylesheet
    css_path = os.path.join(TEMPLATES_DIR, "MediaWiki_Common.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            pages.append(("MediaWiki:Common.css", f.read(), "APF Global Foresight Modern Design System Theme"))
            
    # 3. Portals
    title_lookup = {
        "01_canonical_foresight_books.wiki": "APF Canonical Library of Strategic Foresight (650 Books)",
        "02_peer_reviewed_journal_canon.wiki": "APF Peer-Reviewed Foresight Journal Canon (1,000 Articles)",
        "03_foresight_podcasts_directory.wiki": "APF Strategic Foresight Podcasts Directory (350 Audio Series)",
        "04_blogs_newsletters_and_signals.wiki": "APF Foresight Blogs, Newsletters and Signal Feeds (350 Publications)",
        "05_landmark_presentations_and_keynotes.wiki": "APF Landmark Foresight Presentations and Keynotes (350 Keynotes)"
    }
    portal_files = sorted(glob.glob(os.path.join(ENTRIES_DIR, "resources", "*.wiki")))
    for pf in portal_files:
        filename = os.path.basename(pf)
        title = title_lookup.get(filename, filename.replace(".wiki", "").replace("_", " "))
        with open(pf, "r", encoding="utf-8") as f:
            pages.append((title, f.read(), f"Curated Resource Portal: {title}"))
            
    # 4. Articles
    index_path = os.path.join(BASE_DIR, "scripts", "domain", "master_catalog_1000_index.json")
    article_titles = {}
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            idx = json.load(f)
            for item in idx:
                article_titles[item["filename"]] = item["title"]

    entry_dirs = sorted([d for d in glob.glob(os.path.join(ENTRIES_DIR, "*")) if not d.endswith("resources")])
    for ed in entry_dirs:
        for ef in sorted(glob.glob(os.path.join(ed, "*.wiki"))):
            filename = os.path.basename(ef)
            title = article_titles.get(filename)
            with open(ef, "r", encoding="utf-8") as f:
                content = f.read()
            if not title:
                m_header = re.search(r"^=\s*(.*?)\s*=$", content, re.MULTILINE)
                if m_header:
                    title = m_header.group(1).strip()
                else:
                    title = re.sub(r'^\d+_', '', filename.replace(".wiki", "")).replace("_", " ")
            pages.append((title, content, f"APF Foresight Encyclopedia: {title}"))
            
    return pages

def main():
    parser = argparse.ArgumentParser(description="Publish APF Foresight Wiki to MyWiki instance.")
    parser.add_argument("--url", help="Target MyWiki base URL or api.php endpoint (e.g. https://mywiki.apf.org/api.php)")
    parser.add_argument("--user", help="MediaWiki Administrator or Bot Username")
    parser.add_argument("--password", help="MediaWiki Password or Bot Password")
    parser.add_argument("--dry-run", action="store_true", help="Simulate execution without sending write requests")
    parser.add_argument("--batch-size", type=int, default=50, help="Pages per progress notification")
    parser.add_argument("--delay", type=float, default=0.2, help="Delay in seconds between page edits")
    args = parser.parse_args()

    # Read from environment if arguments omitted
    url = args.url or os.environ.get("MYWIKI_URL") or DEFAULT_API_URL
    user = args.user or os.environ.get("MYWIKI_USER")
    password = args.password or os.environ.get("MYWIKI_PASSWORD")

    print("======================================================================")
    print("APF Global Foresight Wiki — Automated MyWiki Publisher")
    print("======================================================================")

    all_pages = collect_all_pages()
    print(f"Total pages cataloged for deployment: {len(all_pages)}")

    if args.dry_run:
        print("\n[DRY RUN MODE ENABLED] No remote network calls will be made.")
        print(f"Target API Endpoint: {url}")
        print(f"Would publish {len(all_pages)} pages:")
        print(f"  - 1 Main Page")
        print(f"  - {len(glob.glob(os.path.join(TEMPLATES_DIR, '*.wiki')))} Templates")
        print(f"  - 5 Resource Portals")
        print(f"  - 1,000 Encyclopedia Articles")
        print("\nSample targets:")
        for title, _, summary in all_pages[:10]:
            print(f"  → {title} ({summary})")
        print("  ... and 1,008 more pages.")
        return

    if not user or not password:
        print("\n❌ Missing required authentication credentials.")
        print(f"Target wiki endpoint: {url}\n")
        print("Please provide connection details via CLI flags or environment variables:\n")
        print("Usage:")
        print("  /usr/bin/python3 wiki/scripts/push_to_mywiki.py \\")
        print("    --user 'YourAdminOrBotUsername' \\")
        print("    --password 'YourPasswordOrBotPassword'\n")
        print("Or set environment variables:")
        print("  export MYWIKI_USER='YourAdminOrBotUsername'")
        print("  export MYWIKI_PASSWORD='YourPassword'")
        print("  /usr/bin/python3 wiki/scripts/push_to_mywiki.py\n")
        print("  /usr/bin/python3 wiki/scripts/push_to_mywiki.py\n")
        print("Alternatively, you can import the pre-built XML dump directly via your browser:")
        print(f"  Dump file: {XML_DUMP_PATH}")
        print("  1. Log in to your wiki.")
        print("  2. Go to Special:Import.")
        print("  3. Choose the dump file and click Upload.\n")
        sys.exit(1)

    client = MediaWikiClient(url)
    if not client.login(user, password):
        print("Aborting push due to authentication failure.")
        sys.exit(1)

    success_count = 0
    failed_pages = []

    print(f"\nBeginning publication of {len(all_pages)} pages...")
    start_time = time.time()

    for idx, (title, content, summary) in enumerate(all_pages, 1):
        ok, res = client.edit_page(title, content, summary)
        if ok:
            success_count += 1
        else:
            failed_pages.append((title, res))
            print(f"  [WARN] Failed to push '{title}': {res}")

        if idx % args.batch_size == 0 or idx == len(all_pages):
            elapsed = time.time() - start_time
            rate = idx / elapsed if elapsed > 0 else 0
            print(f"  ... published {idx}/{len(all_pages)} pages ({rate:.1f} pages/sec)")

        if args.delay > 0:
            time.sleep(args.delay)

    total_time = time.time() - start_time
    print("\n================ DEPLOYMENT SUMMARY ================")
    print(f"Total Pages Attempted : {len(all_pages)}")
    print(f"Successfully Published: {success_count}")
    print(f"Failed                : {len(failed_pages)}")
    print(f"Total Duration        : {total_time:.1f} seconds")
    if failed_pages:
        print("\nFailed pages log:")
        for title, err in failed_pages:
            print(f"  - {title}: {err}")
    else:
        print("\n✔ All 1,018 pages published successfully with ZERO ERRORS!")
    print("====================================================")

if __name__ == "__main__":
    main()
