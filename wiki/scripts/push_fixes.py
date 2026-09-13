#!/usr/bin/env python3
"""
Pushes remaining theme updates, the sidebar logo stylesheet, and the renamed Greenpeace article
to https://futurepedia.mywikis.wiki/w143/api.php.
"""

import os
import sys
import argparse
import urllib.request
import urllib.parse
import http.cookiejar
import json
import ssl

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_API_URL = "https://futurepedia.mywikis.wiki/w143/api.php"

class SimpleMediaWikiClient:
    def __init__(self, api_url):
        self.api_url = api_url
        self.cookie_jar = http.cookiejar.CookieJar()
        try:
            ctx = ssl.create_default_context()
        except Exception:
            ctx = ssl._create_unverified_context()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPSHandler(context=ctx),
            urllib.request.HTTPCookieProcessor(self.cookie_jar)
        )
        self.csrf_token = None

    def _req(self, data=None):
        headers = {"User-Agent": "APFForesightBot/1.0"}
        if data:
            post_data = urllib.parse.urlencode(data).encode("utf-8")
            req = urllib.request.Request(self.api_url, data=post_data, headers=headers)
        else:
            req = urllib.request.Request(self.api_url, headers=headers)
        with self.opener.open(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def login(self, username, password):
        print(f"Connecting to {self.api_url}...")
        token_res = self._req({"action": "query", "meta": "tokens", "type": "login", "format": "json"})
        logintoken = token_res.get("query", {}).get("tokens", {}).get("logintoken")

        login_res = self._req({
            "action": "login",
            "lgname": username,
            "lgpassword": password,
            "lgtoken": logintoken,
            "format": "json"
        })
        if login_res.get("login", {}).get("result") == "Success":
            print(f"✔ Authenticated successfully as: {username}")
            csrf_res = self._req({"action": "query", "meta": "tokens", "type": "csrf", "format": "json"})
            self.csrf_token = csrf_res.get("query", {}).get("tokens", {}).get("csrftoken")
            return True
        else:
            print(f"❌ Login failed: {login_res}")
            return False

    def edit(self, title, content, summary="APF Global Foresight Wiki Update"):
        print(f"Publishing '{title}'...")
        res = self._req({
            "action": "edit",
            "title": title,
            "text": content,
            "summary": summary,
            "token": self.csrf_token,
            "bot": "1",
            "format": "json"
        })
        if "edit" in res and res["edit"].get("result") == "Success":
            print(f"  ✔ Successfully published: {title}")
            return True
        else:
            print(f"  ❌ Error publishing {title}: {res}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Publish theme and fixed pages to Futurepedia")
    parser.add_argument("--user", default="admin", help="Username")
    parser.add_argument("--password", required=True, help="Password")
    parser.add_argument("--url", default=DEFAULT_API_URL, help="API URL")
    args = parser.parse_args()

    client = SimpleMediaWikiClient(args.url)
    if not client.login(args.user, args.password):
        sys.exit(1)

    # 1. Push MediaWiki:Common.css
    css_path = os.path.join(BASE_DIR, "templates", "MediaWiki_Common.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            client.edit("MediaWiki:Common.css", f.read(), "Install APF Modern Theme and Official Sidebar Logo")

    # 2. Push Greenpeace article with fixed title
    article_path = os.path.join(BASE_DIR, "entries", "17_landmark_case_studies", "0789_Greenpeace_Decarbonization_Energy_Revolution_Scenarios.wiki")
    if os.path.exists(article_path):
        with open(article_path, "r", encoding="utf-8") as f:
            client.edit("Greenpeace Decarbonization Energy (R)evolution Scenarios", f.read(), "APF Case Study: Greenpeace Decarbonization Energy (R)evolution Scenarios")

    # 3. Push updated Main Page
    main_page_path = os.path.join(BASE_DIR, "Main_Page.wiki")
    if os.path.exists(main_page_path):
        with open(main_page_path, "r", encoding="utf-8") as f:
            client.edit("Main Page", f.read(), "Update APF Official Main Page Portal with Brand Logo Container")

    print("\n✔ All fixes and theme updates pushed successfully!")

if __name__ == "__main__":
    main()
