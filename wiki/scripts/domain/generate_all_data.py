# wiki/scripts/domain/generate_all_data.py
# High-fidelity domain generator that builds the complete 1,000-entry knowledge modules.

import json
import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DOMAIN_DIR = os.path.join(BASE_DIR, "wiki", "scripts", "domain")

print(f"Generating 1,000-entry domain data in: {DOMAIN_DIR}")
