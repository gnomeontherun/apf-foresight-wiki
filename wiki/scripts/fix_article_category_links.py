#!/usr/bin/env python3
"""
Fixes inline category links across all 1,000 APF Foresight Wiki entries.
Replaces:
  Classified under the [[Category:APF Competency - ...|...]]
with:
  Classified under [[:Category:APF Competency - ...|...]]

This ensures that MediaWiki renders an active, clickable inline link
instead of treating it as an invisible category assignment tag.
"""

import os
import glob
import re

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENTRIES_DIR = os.path.join(BASE_DIR, "entries")

def fix_links():
    pattern = os.path.join(ENTRIES_DIR, "*", "*.wiki")
    files = glob.glob(pattern)
    print(f"Scanning {len(files)} entries in {ENTRIES_DIR}...")
    modified_count = 0

    for fp in files:
        if "resources" in fp:
            continue
        with open(fp, "r", encoding="utf-8") as f:
            content = f.read()

        new_content = content

        # 1. Fix "Classified under the [[Category:" -> "Classified under [[:Category:"
        new_content = re.sub(
            r"Classified under the \[\[Category:",
            r"Classified under [[:Category:",
            new_content
        )

        # 2. Fix inline category links in "Complementary Competencies" or body text:
        # [[Category:APF Competency - Foo|Foo]] -> [[:Category:APF Competency - Foo|Foo]]
        new_content = re.sub(
            r"\[\[Category:(APF Competency - [^\]\|]+)\|",
            r"[[:Category:\1|",
            new_content
        )

        if new_content != content:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(new_content)
            modified_count += 1

    print(f"✔ Successfully updated {modified_count} entries with proper [[:Category:...]] inline links.")

if __name__ == "__main__":
    fix_links()
