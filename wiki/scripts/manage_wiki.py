#!/usr/bin/env python3
"""
APF Global Foresight Wiki — Autonomous Management Suite
Full-lifecycle management of Futurepedia (https://futurepedia.mywikis.wiki).
Reads credentials automatically from .env.
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
import ssl

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WORKSPACE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
DOTENV_PATH = os.path.join(WORKSPACE_DIR, ".env")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
ENTRIES_DIR = os.path.join(BASE_DIR, "entries")
MAIN_PAGE_PATH = os.path.join(BASE_DIR, "Main_Page.wiki")
IMAGES_DIR = os.path.join(BASE_DIR, "export", "images")

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

DEFAULT_API_URL = os.environ.get("MYWIKI_URL", "https://futurepedia.mywikis.wiki/w143/api.php")
DEFAULT_USER = os.environ.get("MYWIKI_USER", "admin")
DEFAULT_PASSWORD = os.environ.get("MYWIKI_PASSWORD", "")

class WikiManager:
    def __init__(self, api_url=None, user=None, password=None):
        self.api_url = (api_url or DEFAULT_API_URL).rstrip("/")
        if not self.api_url.endswith("api.php"):
            self.api_url += "/api.php"
        self.user = user or DEFAULT_USER
        self.password = password or DEFAULT_PASSWORD
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
        headers = {"User-Agent": "APFAutonomousManager/1.0 (Association of Professional Futurists; info@apf.org)"}
        if data:
            post_data = urllib.parse.urlencode(data).encode("utf-8")
            req = urllib.request.Request(self.api_url, data=post_data, headers=headers)
        else:
            req = urllib.request.Request(self.api_url, headers=headers)
        try:
            with self.opener.open(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            return {"error": {"info": str(e)}}

    def authenticate(self):
        if not self.user or not self.password:
            print("❌ Authentication failed: Missing username or password in .env")
            return False

        token_res = self._req({"action": "query", "meta": "tokens", "type": "login", "format": "json"})
        logintoken = token_res.get("query", {}).get("tokens", {}).get("logintoken")
        if not logintoken:
            print("❌ Could not obtain login token from wiki API.")
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
            print(f"✔ Authenticated as '{self.user}' on {self.api_url}")
            return True
        else:
            print(f"❌ Login failed: {login_res}")
            return False

    def edit_page(self, title, content, summary="APF Autonomous Manager Update"):
        if not self.csrf_token:
            csrf_res = self._req({"action": "query", "meta": "tokens", "type": "csrf", "format": "json"})
            self.csrf_token = csrf_res.get("query", {}).get("tokens", {}).get("csrftoken")

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
            return True, res["edit"]
        return False, res.get("error", res)

    def upload_image(self, filepath, filename, comment="APF Brand Asset"):
        if not os.path.exists(filepath):
            return False, f"File not found: {filepath}"
        
        boundary = "----WebKitFormBoundaryAPFManager"
        body = bytearray()
        def add_field(name, value):
            body.extend(f"--{boundary}\r\n".encode("utf-8"))
            body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
            body.extend(f"{value}\r\n".encode("utf-8"))

        add_field("action", "upload")
        add_field("filename", filename)
        add_field("comment", comment)
        add_field("token", self.csrf_token)
        add_field("ignorewarnings", "1")
        add_field("format", "json")

        with open(filepath, "rb") as f:
            file_bytes = f.read()

        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode("utf-8"))
        body.extend(b"Content-Type: application/octet-stream\r\n\r\n")
        body.extend(file_bytes)
        body.extend(b"\r\n")
        body.extend(f"--{boundary}--\r\n".encode("utf-8"))

        req = urllib.request.Request(self.api_url, data=bytes(body), headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": "APFAutonomousManager/1.0"
        })
        with self.opener.open(req, timeout=45) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            if "upload" in res and res["upload"].get("result") == "Success":
                return True, res["upload"]
            return False, res.get("error", res)

    def check_status(self):
        print(f"\nChecking Futurepedia Status ({self.api_url})...")
        res = self._req({"action": "query", "meta": "siteinfo", "siprop": "general|statistics", "format": "json"})
        stats = res.get("query", {}).get("statistics", {})
        general = res.get("query", {}).get("general", {})
        print(f"  • Site Name      : {general.get('sitename')}")
        print(f"  • MediaWiki Vers : {general.get('generator')}")
        print(f"  • Total Articles : {stats.get('articles', 0)}")
        print(f"  • Total Pages    : {stats.get('pages', 0)}")
        print(f"  • Total Edits    : {stats.get('edits', 0)}")
        print(f"  • Total Images   : {stats.get('images', 0)}")

        # Check MediaWiki:Common.css
        css_res = self._req({"action": "query", "prop": "revisions", "titles": "MediaWiki:Common.css", "rvprop": "size", "format": "json"})
        pages = css_res.get("query", {}).get("pages", {})
        for pid, pinfo in pages.items():
            if int(pid) > 0:
                print("  • Modern Theme   : ✔ ACTIVE (MediaWiki:Common.css is installed)")
            else:
                print("  • Modern Theme   : ⚠️ NOT INSTALLED (MediaWiki:Common.css missing)")

def cmd_push_fixes(wm):
    if not wm.authenticate():
        return
    print("\n--- Pushing Modern APF Theme & Brand Insignia ---")
    css_file = os.path.join(TEMPLATES_DIR, "MediaWiki_Common.css")
    if os.path.exists(css_file):
        with open(css_file, "r", encoding="utf-8") as f:
            ok, res = wm.edit_page("MediaWiki:Common.css", f.read(), "Deploy APF Modern Theme and Official Sidebar Logo")
            print("  ✔ MediaWiki:Common.css updated" if ok else f"  ❌ {res}")

    print("\n--- Pushing Missing Article (Greenpeace) ---")
    gp_file = os.path.join(ENTRIES_DIR, "17_landmark_case_studies", "0789_Greenpeace_Decarbonization_Energy_Revolution_Scenarios.wiki")
    if os.path.exists(gp_file):
        with open(gp_file, "r", encoding="utf-8") as f:
            ok, res = wm.edit_page("Greenpeace Decarbonization Energy (R)evolution Scenarios", f.read(), "APF Canonical Case Study: Greenpeace Decarbonization Energy (R)evolution Scenarios")
            print("  ✔ Greenpeace Decarbonization Energy (R)evolution Scenarios published" if ok else f"  ❌ {res}")

    print("\n--- Refreshing Main Page Banner ---")
    if os.path.exists(MAIN_PAGE_PATH):
        with open(MAIN_PAGE_PATH, "r", encoding="utf-8") as f:
            ok, res = wm.edit_page("Main Page", f.read(), "Update APF Main Page Portal with Brand Insignia Container")
            print("  ✔ Main Page refreshed" if ok else f"  ❌ {res}")

def main():
    parser = argparse.ArgumentParser(description="APF Global Foresight Wiki Autonomous Manager")
    parser.add_argument("action", choices=["status", "push-fixes", "upload-images", "sync"], help="Action to perform")
    args = parser.parse_args()

    wm = WikiManager()
    if args.action == "status":
        wm.check_status()
    elif args.action == "push-fixes":
        cmd_push_fixes(wm)
    elif args.action == "upload-images":
        if wm.authenticate():
            for fn in ["APF_Logo.2015.png", "APF_Wiki_Lockup.jpg", "APF_Emblem_Seal.jpg"]:
                fp = os.path.join(IMAGES_DIR, fn)
                ok, res = wm.upload_image(fp, fn)
                print(f"  ✔ {fn} uploaded" if ok else f"  ❌ {fn}: {res}")

if __name__ == "__main__":
    main()
