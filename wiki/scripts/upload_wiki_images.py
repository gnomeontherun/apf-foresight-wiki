#!/usr/bin/env python3
"""
Uploads the official APF brand assets directly to MediaWiki Special:Upload / api.php?action=upload.
Assets:
- File:APF_Logo.2015.png
- File:APF_Wiki_Lockup.jpg
- File:APF_Emblem_Seal.jpg
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
IMAGES_DIR = os.path.join(BASE_DIR, "export", "images")
DEFAULT_API_URL = "https://futurepedia.mywikis.wiki/w143/api.php"

def upload_file(api_url, username, password, filepath, filename, comment="Official APF Brand Asset"):
    print(f"Uploading {filename} to {api_url}...")
    cookie_jar = http.cookiejar.CookieJar()
    try:
        ctx = ssl.create_default_context()
    except Exception:
        ctx = ssl._create_unverified_context()
    opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx), urllib.request.HTTPCookieProcessor(cookie_jar))
    
    # 1. Get login token
    token_req = urllib.request.Request(f"{api_url}?action=query&meta=tokens&type=login&format=json", headers={"User-Agent": "APFBot/1.0"})
    with opener.open(token_req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        login_token = data.get("query", {}).get("tokens", {}).get("logintoken")

    # 2. Login
    login_data = urllib.parse.urlencode({
        "action": "login",
        "lgname": username,
        "lgpassword": password,
        "lgtoken": login_token,
        "format": "json"
    }).encode("utf-8")
    with opener.open(urllib.request.Request(api_url, data=login_data, headers={"User-Agent": "APFBot/1.0"})):
        pass

    # 3. Get CSRF token
    csrf_req = urllib.request.Request(f"{api_url}?action=query&meta=tokens&type=csrf&format=json", headers={"User-Agent": "APFBot/1.0"})
    with opener.open(csrf_req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        csrf_token = data.get("query", {}).get("tokens", {}).get("csrftoken")

    # 4. Upload multipart
    boundary = "----WebKitFormBoundaryAPFForesightWiki"
    body = bytearray()
    
    def add_field(name, value):
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode("utf-8"))
        body.extend(f"{value}\r\n".encode("utf-8"))

    add_field("action", "upload")
    add_field("filename", filename)
    add_field("comment", comment)
    add_field("token", csrf_token)
    add_field("ignorewarnings", "1")
    add_field("format", "json")

    # Add file
    with open(filepath, "rb") as f:
        file_bytes = f.read()

    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode("utf-8"))
    body.extend(b"Content-Type: application/octet-stream\r\n\r\n")
    body.extend(file_bytes)
    body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode("utf-8"))

    req = urllib.request.Request(api_url, data=bytes(body), headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "User-Agent": "APFBot/1.0"
    })
    with opener.open(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        if "upload" in res and res["upload"].get("result") == "Success":
            print(f"✔ Successfully uploaded {filename}")
            return True
        else:
            print(f"❌ Upload failed: {res}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Upload APF brand images to MediaWiki")
    parser.add_argument("--url", default=DEFAULT_API_URL, help="MediaWiki API URL")
    parser.add_argument("--user", required=True, help="Username or Bot Username")
    parser.add_argument("--password", required=True, help="Password or Bot Password")
    args = parser.parse_args()

    files = [
        ("APF_Logo.2015.png", os.path.join(IMAGES_DIR, "APF_Logo.2015.png")),
        ("APF_Wiki_Lockup.jpg", os.path.join(IMAGES_DIR, "APF_Wiki_Lockup.jpg")),
        ("APF_Emblem_Seal.jpg", os.path.join(IMAGES_DIR, "APF_Emblem_Seal.jpg")),
    ]

    for fname, fpath in files:
        if os.path.exists(fpath):
            upload_file(args.url, args.user, args.password, fpath, fname)

if __name__ == "__main__":
    main()
