#!/usr/bin/env python3
"""
APF Global Foresight Wiki — High-Speed Concurrent Article Synchronizer
Pushes all 1,000 canonical articles with repaired inline category links and
competency distribution to https://futurepedia.mywikis.wiki.
"""

import os
import sys
import glob
import re
import json
import time
import ssl
import urllib.request
import urllib.parse
import http.cookiejar
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WORKSPACE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
DOTENV_PATH = os.path.join(WORKSPACE_DIR, ".env")
ENTRIES_DIR = os.path.join(BASE_DIR, "entries")
INDEX_PATH = os.path.join(BASE_DIR, "scripts", "domain", "master_catalog_1000_index.json")

# Auto-load .env
if os.path.exists(DOTENV_PATH):
    with open(DOTENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                if k not in os.environ:
                    os.environ[k] = v

API_URL = os.environ.get("MYWIKI_URL", "https://futurepedia.mywikis.wiki/w143/api.php")
USER = os.environ.get("MYWIKI_USER", "admin")
PASSWORD = os.environ.get("MYWIKI_PASSWORD", "")

class FastMediaWikiSyncer:
    def __init__(self, api_url, user, password, workers=5):
        self.api_url = api_url.rstrip("/")
        if not self.api_url.endswith("api.php"):
            self.api_url += "/api.php"
        self.user = user
        self.password = password
        self.workers = workers
        self.cookie_jar = http.cookiejar.CookieJar()
        
        try:
            self.ctx = ssl.create_default_context()
        except Exception:
            self.ctx = ssl._create_unverified_context()
            
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPSHandler(context=self.ctx),
            urllib.request.HTTPCookieProcessor(self.cookie_jar)
        )
        self.csrf_token = None

    def _req(self, data=None):
        headers = {"User-Agent": "APFConcurrentSync/1.0 (Association of Professional Futurists; info@apf.org)"}
        if data:
            post_data = urllib.parse.urlencode(data).encode("utf-8")
            req = urllib.request.Request(self.api_url, data=post_data, headers=headers)
        else:
            req = urllib.request.Request(self.api_url, headers=headers)
        with self.opener.open(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def login(self):
        print(f"Connecting to MediaWiki API at {self.api_url}...")
        token_res = self._req({"action": "query", "meta": "tokens", "type": "login", "format": "json"})
        logintoken = token_res.get("query", {}).get("tokens", {}).get("logintoken")
        if not logintoken:
            print("❌ Failed to obtain login token.")
            return False

        login_res = self._req({
            "action": "login",
            "lgname": self.user,
            "lgpassword": self.password,
            "lgtoken": logintoken,
            "format": "json"
        })
        if login_res.get("login", {}).get("result") == "Success":
            csrf_res = self._req({"action": "query", "meta": "tokens", "type": "csrf", "format": "json"})
            self.csrf_token = csrf_res.get("query", {}).get("tokens", {}).get("csrftoken")
            print(f"✔ Authenticated successfully as '{self.user}'.")
            return True
        else:
            print(f"❌ Login failed: {login_res}")
            return False

    def edit_single_page(self, title, content, summary="APF Foresight Article: Inline Link & Category Refinement"):
        data = {
            "action": "edit",
            "title": title,
            "text": content,
            "summary": summary,
            "token": self.csrf_token,
            "bot": "1",
            "format": "json"
        }
        headers = {"User-Agent": "APFConcurrentSync/1.0"}
        post_data = urllib.parse.urlencode(data).encode("utf-8")
        
        for attempt in range(3):
            try:
                req = urllib.request.Request(self.api_url, data=post_data, headers=headers)
                with self.opener.open(req, timeout=35) as resp:
                    res = json.loads(resp.read().decode("utf-8"))
                    if "edit" in res and res["edit"].get("result") == "Success":
                        return True, title, None
                    error_info = res.get("error", res)
                    if attempt < 2:
                        time.sleep(1)
                        continue
                    return False, title, str(error_info)
            except Exception as e:
                if attempt < 2:
                    time.sleep(1.5)
                    continue
                return False, title, str(e)
        return False, title, "Exceeded retries"

def load_catalog_articles():
    article_titles = {}
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            for item in json.load(f):
                article_titles[item["filename"]] = item["title"]

    articles = []
    entry_dirs = sorted([d for d in glob.glob(os.path.join(ENTRIES_DIR, "*")) if not d.endswith("resources")])
    for ed in entry_dirs:
        for ef in sorted(glob.glob(os.path.join(ed, "*.wiki"))):
            filename = os.path.basename(ef)
            with open(ef, "r", encoding="utf-8") as f:
                content = f.read()
            title = article_titles.get(filename)
            if not title:
                m = re.search(r"^=\s*(.+?)\s*=$", content, re.MULTILINE)
                if m:
                    title = m.group(1).strip()
                else:
                    title = re.sub(r'^\d+_', '', filename.replace(".wiki", "")).replace("_", " ")
            articles.append((title, content, filename))
    return articles

def run_sync():
    print("====================================================================")
    print("APF Global Foresight Wiki — 1,000 Articles High-Speed Synchronizer")
    print("====================================================================")
    
    syncer = FastMediaWikiSyncer(API_URL, USER, PASSWORD, workers=5)
    if not syncer.login():
        sys.exit(1)

    articles = load_catalog_articles()
    total = len(articles)
    print(f"Loaded {total} canonical articles from {ENTRIES_DIR} to synchronize.")
    
    start_time = time.time()
    success_count = 0
    fail_count = 0
    failures = []

    print(f"\nDispatching {total} edits across {syncer.workers} concurrent workers...")
    
    with ThreadPoolExecutor(max_workers=syncer.workers) as executor:
        futures = {
            executor.submit(syncer.edit_single_page, title, content): (title, fn)
            for title, content, fn in articles
        }
        
        completed = 0
        for fut in as_completed(futures):
            ok, title, err = fut.result()
            completed += 1
            if ok:
                success_count += 1
            else:
                fail_count += 1
                failures.append((title, err))
                print(f"\n  ❌ Failed: {title} -> {err}")

            if completed % 50 == 0 or completed == total:
                elapsed = time.time() - start_time
                rate = completed / elapsed if elapsed > 0 else 0
                print(f"  ... synchronized {completed}/{total} articles ({rate:.1f} articles/sec) | Success: {success_count} | Fail: {fail_count}")

    total_time = time.time() - start_time
    print("\n================ SYNCHRONIZATION SUMMARY ================")
    print(f"Total Articles Processed : {total}")
    print(f"Successfully Synchronized: {success_count}")
    print(f"Failed                   : {fail_count}")
    print(f"Total Duration           : {total_time:.1f}s ({total/total_time:.1f} articles/sec)")
    if failures:
        print("\nFailures:")
        for t, err in failures[:10]:
            print(f"  - {t}: {err}")
    else:
        print("\n✔ 100% of articles successfully updated on live wiki!")
    print("=========================================================")

if __name__ == "__main__":
    run_sync()
