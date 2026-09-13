#!/usr/bin/env python3
"""
APF Global Foresight Wiki: Master Media & Literature Catalog Data
Contains curated canonical data for 1,050 foresight resources:
- 260 Books (Classics, Methods, Scenarios, Design, Governance, MSFW Winners)
- 360 Journal Articles (Futures, TF&SC, JFS, Foresight, EJFR, WFR)
- 150 Podcasts & Audio Series
- 140 Blogs, Substacks & Signal Monitoring Feeds
- 140 Landmark Presentations, Keynotes & Recorded Talks
"""

import json

# Pillar map for clean reference
PILLAR_MAP = {
    1: ("01_foundations_and_epistemology", "Foundations, Epistemology & Epistemic Pluralism", "Framing"),
    2: ("02_psychology_and_temporal_cognition", "Temporal Cognition, Psychology & Futures Consciousness", "Framing"),
    3: ("03_critical_and_decolonial_futures", "Decolonial, Indigenous & Pluriversal Futures", "Framing"),
    4: ("04_horizon_scanning_and_signals", "Horizon Scanning, Sensemaking & Signal Processing", "Scanning"),
    5: ("05_weak_signals_and_wild_cards", "Weak Signals, Wild Cards & Disruption Dynamics", "Scanning"),
    6: ("06_megatrends_and_planetary_frontiers", "Megatrends, Planetary Boundaries & Polycrises", "Scanning"),
    7: ("07_methods_and_frameworks", "Methods, Frameworks & Process Design", "Futuring"),
    8: ("08_scenarios_and_worldbuilding", "Scenarios, Narrative Forensics & Worldbuilding", "Futuring"),
    9: ("09_computational_and_quantitative_foresight", "Computational Foresight, System Dynamics & AI Modeling", "Futuring"),
    10: ("10_specialized_tools_and_canvases", "Specialized Tools, Matrixes & Canvases", "Designing"),
    11: ("11_design_and_experiential_futures", "Speculative Design, Experiential Futures & Artifacts", "Designing"),
    12: ("12_climate_and_urban_futures", "Climate, Energy & Urban Transition Futures", "Designing"),
    13: ("13_health_and_biotech_futures", "Health, Bioethics & Frontier Intelligence", "Designing"),
    14: ("14_security_and_space_futures", "Geopolitics, Security & Deep Space Horizons", "Designing"),
    15: ("15_strategic_agility_and_resilience", "Strategic Agility, War Gaming & Antifragility", "Adapting"),
    16: ("16_strategy_and_governance", "Anticipatory Governance & Public Policy Scaffolding", "Leading"),
    17: ("17_landmark_case_studies", "Landmark Global Case Studies & Institutional Precedents", "Leading"),
    18: ("18_high_profile_figures_and_pioneers", "Global Thought Leaders, Pioneers & Theorists", "Leading"),
    19: ("19_foresight_organizations_and_think_tanks", "Foresight Centers, Think Tanks & Professional Bodies", "Leading"),
    20: ("20_university_and_training_programs", "University Degrees, Academic Chairs & Masterclasses", "Leading")
}

print("Loaded Media Catalog Reference Mappings.")
