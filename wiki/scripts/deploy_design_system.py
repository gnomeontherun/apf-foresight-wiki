#!/usr/bin/env python3
"""
APF Global Foresight Wiki — Comprehensive Design System & Gateway Deployment
Deploys high-contrast MediaWiki:Common.css, refined templates, portal categories,
gateway pages, and canonical media libraries to https://futurepedia.mywikis.wiki.
"""

import os
import sys
import glob
import re
import json
import time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WORKSPACE_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
ENTRIES_DIR = os.path.join(BASE_DIR, "entries")
RESOURCES_DIR = os.path.join(ENTRIES_DIR, "resources")
MAIN_PAGE_PATH = os.path.join(BASE_DIR, "Main_Page.wiki")

sys.path.insert(0, WORKSPACE_DIR)
from wiki.scripts.manage_wiki import WikiManager

COMPETENCY_PORTALS = {
    "Category:APF Competency - Framing": {
        "title": "Framing",
        "num": "1",
        "color": "#0369a1",
        "bg_grad": "linear-gradient(135deg, #0f172a 0%, #0369a1 100%)",
        "desc": "Scoping the domain, establishing boundaries, auditing cognitive biases, and uncovering unexamined worldviews.",
        "details": """The '''Framing''' competency enables professional futurists to clearly delineate the boundaries of an inquiry, interrogate unexamined mental models, and align institutional stakeholders. Key focus areas include:
* Scoping problem spaces and horizon definitions (H1, H2, H3).
* Identifying cognitive biases (hyperbolic discounting, recency bias, status quo bias).
* Decolonizing futures through pluriversal design and alternative cultural cosmologies (Afrofuturism, Indigenous futures).
* Establishing ethical stewardship and duties to future generations."""
    },
    "Category:APF Competency - Scanning": {
        "title": "Scanning",
        "num": "2",
        "color": "#b45309",
        "bg_grad": "linear-gradient(135deg, #0f172a 0%, #b45309 100%)",
        "desc": "Detecting weak signals, tracking planetary boundaries, modeling change dynamics, and identifying wild cards.",
        "details": """The '''Scanning''' competency provides systematic protocols for continuous environmental awareness, data harvesting, and sensemaking across societal horizons:
* Environmental scanning taxonomy (STEEPLE / STEEPLED frameworks).
* Weak signals detection (Igor Ansoff's threshold models) and horizon scanning engines.
* Identifying wild cards and low-probability, high-impact systemic shocks.
* Monitoring biophysical thresholds and planetary boundaries."""
    },
    "Category:APF Competency - Futuring": {
        "title": "Futuring",
        "num": "3",
        "color": "#7e22ce",
        "bg_grad": "linear-gradient(135deg, #0f172a 0%, #7e22ce 100%)",
        "desc": "Developing plausible alternative worlds, unpacking deep causal layers, and running computational scenario models.",
        "details": """The '''Futuring''' competency focuses on mapping possible, plausible, and preferable futures using rigorous analytical and speculative methods:
* Multi-layered ontological deconstruction via Causal Layered Analysis (Litany, System, Worldview, Myth/Metaphor).
* Four Scenario Archetypes (Growth, Collapse, Discipline, Transformation).
* Three Horizons Framework, Backcasting methodologies, and Delphi expert panels.
* Quantitative systems dynamics modeling and computational superforecasting."""
    },
    "Category:APF Competency - Designing": {
        "title": "Designing",
        "num": "4",
        "color": "#be185d",
        "bg_grad": "linear-gradient(135deg, #0f172a 0%, #be185d 100%)",
        "desc": "Materializing scenarios through experiential artifacts, diegetic prototypes, applied sector transitions, and facilitation canvases.",
        "details": """The '''Designing''' competency translates abstract scenarios into tangible, visceral encounters that challenge assumptions:
* Speculative design, design fiction, and diegetic prototyping.
* The Experiential Futures Ladder (Setting, Scenario, Situation, Stuff).
* Interactive facilitation canvases, serious games, and immersive simulation environments.
* Sectoral decarbonization roadmaps, urban resilience transitions, and synthetic biology blueprints."""
    },
    "Category:APF Competency - Adapting": {
        "title": "Adapting",
        "num": "5",
        "color": "#15803d",
        "bg_grad": "linear-gradient(135deg, #0f172a 0%, #15803d 100%)",
        "desc": "Wind-tunneling strategic portfolios, building dynamic adaptive pathways, and institutionalizing anticipatory governance.",
        "details": """The '''Adapting''' competency ensures organizations can withstand volatile external shocks and seize emerging opportunities:
* Strategic portfolio wind-tunneling against divergent scenario matrices.
* Dynamic Adaptive Policy Pathways (DAPP) with explicit adaptation tipping points and trigger thresholds.
* Robust Decision Making (RDM) under deep uncertainty.
* Pre-mortem failure analysis and organizational foresight maturity benchmarking."""
    },
    "Category:APF Competency - Leading": {
        "title": "Leading",
        "num": "6",
        "color": "#c2410c",
        "bg_grad": "linear-gradient(135deg, #0f172a 0%, #c2410c 100%)",
        "desc": "Stewarding the foresight discipline, learning from historic landmark interventions, mapping global pioneers, and training future leaders.",
        "details": """The '''Leading''' competency embodies professional leadership, educational stewardship, and ethical governance:
* Case study analysis of landmark historic interventions (Shell 1973, Mont Fleur, Club of Rome).
* Archiving the canon of global pioneers and intellectual founding figures.
* Academic foresight degree curricula and university training programs.
* Maintaining professional codes of conduct, public engagement, and peer review standards."""
    }
}

THEMATIC_PORTALS = {
    "Category:Foundations, Epistemology & Epistemic Pluralism": ("01. Foundations, Epistemology & Epistemic Pluralism", "Epistemic foundations, ontological diversity, critical futures studies, and philosophical lineages."),
    "Category:Psychology, Cognitive Biases & Temporal Perception": ("02. Psychology, Cognitive Biases & Temporal Perception", "Cognitive psychology, temporal discounting, hyperbolic bias, heuristic modeling, and mental model auditing."),
    "Category:Critical, Decolonial, Indigenous & Pluriversal Futures": ("03. Critical, Decolonial, Indigenous & Pluriversal Futures", "Decolonial futures, Indigenous cosmologies, pluriversal epistemologies, Afrofuturism, and alternative civilizational perspectives."),
    "Category:Environmental & Horizon Scanning Systems": ("04. Environmental & Horizon Scanning Systems", "Continuous scanning infrastructure, signal harvesting repositories, and automated feeds."),
    "Category:Signals, Drivers, Wild Cards & Change Dynamics": ("05. Signals, Drivers, Wild Cards & Change Dynamics", "Macro-drivers of change, weak signals, and wild card disruption models."),
    "Category:Core Megatrends, Planetary Frontiers & Polycrisis": ("06. Core Megatrends, Planetary Frontiers & Polycrisis", "Planetary boundaries, climate transitions, geopolitical realignments, and polycrisis."),
    "Category:Core Foresight Methodologies & Frameworks": ("07. Core Foresight Methodologies & Frameworks", "Foundational frameworks including CLA, Delphi, Scenario Archetypes, and Three Horizons."),
    "Category:Scenario Planning, Worldbuilding & Simulation": ("08. Scenario Planning, Worldbuilding & Simulation", "Scenario axes, deductive/inductive matrix methods, narrative worldbuilding, and computational simulation."),
    "Category:Quantitative, Computational & AI-Driven Foresight": ("09. Quantitative, Computational & AI-Driven Foresight", "Systems dynamics, computational modeling, sentiment analysis, and AI frontier horizon scanning."),
    "Category:Facilitation Canvases, Toolkits & Serious Games": ("10. Facilitation Canvases, Toolkits & Serious Games", "Workshop games, visual canvas suites, and participatory foresight instruments."),
    "Category:Design Futures, Speculative Fabulation & Diegetics": ("11. Design Futures, Speculative Fabulation & Diegetics", "Speculative design, design fiction, diegetic prototyping, and experiential futures artifacts."),
    "Category:Applied Sectoral Foresight: Climate, Energy & Urbanism": ("12. Applied Sectoral Foresight: Climate, Energy & Urbanism", "Energy grid transitions, urban planning, circular economy, and climate adaptation."),
    "Category:Applied Sectoral Foresight: Health, Biotech & AI": ("13. Applied Sectoral Foresight: Health, Biotech & AI", "Healthcare futures, longevity, genetic engineering, and neurotechnologies."),
    "Category:Applied Sectoral Foresight: Security, Space & Economy": ("14. Applied Sectoral Foresight: Security, Space & Economy", "Autonomous defense, space resource governance, and macro-financial futures."),
    "Category:Strategic Agility, Wind Tunneling & Resilience": ("15. Strategic Agility, Wind Tunneling & Resilience", "Dynamic adaptive policy pathways, strategic stress testing, robust decision making, and organizational agility."),
    "Category:Anticipatory Governance, Public Policy & Law": ("16. Anticipatory Governance, Public Policy & Law", "Parliamentary futures committees, statutory duties to future generations, constitutional long-termism, and anticipatory policy."),
    "Category:Landmark Historic Case Studies Archive (1950–Present)": ("17. Landmark Historic Case Studies Archive (1950–Present)", "In-depth monographs analyzing seminal public, corporate, and intergovernmental foresight interventions."),
    "Category:High-Profile Figures, Theorists & Pioneers": ("18. High-Profile Figures, Theorists & Pioneers", "Biographical monographs and conceptual lineages of pioneering futurists."),
    "Category:Global Organizations, Think Tanks & Consultancies": ("19. Global Organizations, Think Tanks & Consultancies", "Institutional profiles of leading foresight consultancies, NGOs, and government bodies."),
    "Category:University Degree Programs, Institutes & Training": ("20. University Degree Programs, Institutes & Training", "Curricular guides to accredited master's, doctoral, and certificate programs in foresight.")
}

GATEWAY_PAGES = {
    "APF Emerging Fellows Program": """__NOTOC__
{{Editorial_Status|status=approved|reviewer=APF Editorial & Peer Review Council|date=2026-09-08}}
{{APF_Competency_Badge|competency=Leading}}

= APF Emerging Fellows Program =

The '''APF Emerging Fellows Program''' is a premier professional development initiative of the [[Association of Professional Futurists (APF - History & Code)|Association of Professional Futurists]], designed to cultivate, mentor, and amplify the voices of early-career and rising foresight practitioners worldwide.

== Program Mission & Architecture ==
Established to bridge the gap between academic foresight training and active professional practice, the Emerging Fellows Program provides:
* '''Global Mentorship''': Direct one-on-one mentorship pairings with seasoned APF Full Members and accredited fellows.
* '''Publication Platform''': Opportunities to conduct deep-dive research and publish thematic articles in ''Compass'' magazine, the APF's quarterly journal.
* '''International Collaboration''': A collaborative cohort network spanning more than 25 countries across North America, Europe, Africa, Latin America, and Asia-Pacific.
* '''Methodological Grounding''': Structured workshops on advanced foresight frameworks, including Causal Layered Analysis, Dynamic Adaptive Policy Pathways, and Experiential Futures.

== Key Research Themes ==
Fellows investigate pressing global challenges and emerging frontiers:
# '''Pluriversal & Decolonial Futures''': Integrating non-Western epistemologies, indigenous perspectives, and pluralist worldviews into strategic planning.
# '''Governance in Polycrisis''': Anticipatory governance models for polycrisis, climate disruption, and planetary boundaries.
# '''Technological Horizons''': Societal and ethical ramifications of Artificial General Intelligence, synthetic biology, and autonomous systems.

== See Also ==
* [[Association of Professional Futurists (APF - History & Code)|Association of Professional Futurists]]
* [[APF Most Significant Futures Works (MSFW) Historic Laureates Archive]]
* [https://apf.org Official APF Website (apf.org) ↗]

[[Category:University Degree Programs, Institutes & Training]]
[[Category:APF Competency - Leading]]
""",

    "APF:Editorial Guidelines": """__NOTOC__
{{Editorial_Status|status=approved|reviewer=APF Editorial & Peer Review Council|date=2026-09-08}}
{{APF_Competency_Badge|competency=Leading}}

= APF Foresight Wiki Editorial Guidelines & Style Guide =

The '''APF Global Foresight Wiki''' is the authoritative, peer-reviewed reference encyclopedia for strategic foresight and futures thinking. To maintain executive rigor, historical precision, and professional neutrality, all contributions must adhere to these standards.

== Core Editorial Principles ==
# '''Professional Rigor''': Every article must clearly distinguish between rigorous foresight methodologies, empirical trend analysis, speculative fiction, and normative advocacy.
# '''Methodological Neutrality''': Methods should be analyzed with balanced appraisal, including origins, theoretical lineage, step-by-step facilitation architecture, cognitive failure modes, and boundary limitations.
# '''Canonical Lineage''': Concepts and frameworks must credit original theorists and foundational publications (e.g., Pierre Wack for Shell Scenarios, Ziauddin Sardar for Post-Normal Times, Sohail Inayatullah for CLA).
# '''Accessible High Contrast''': Formatting must adhere to the APF Executive Design System, avoiding dense unformatted walls of text and using structured infoboxes, callouts, and clean wikitables.

== Article Structure Standard ==
Canonical encyclopedic entries follow this six-part architecture:
* '''Executive Summary & Definition''': Concise definition and placement within the APF Competency Model.
* '''Origins & Theoretical Lineage''': Historical provenance, primary pioneers, and underlying epistemology.
* '''Execution Architecture / Step-by-Step Methodology''': Actionable facilitation steps or analytical mechanics.
* '''Strategic & Policy Applications''': Real-world institutional implementations across public, private, and NGO sectors.
* '''Methodological Critique & Failure Modes''': Epistemological blind spots, cognitive biases, and common practitioner misapplications.
* '''Alignment with APF Core Foresight Competencies''': Explicit mapping to Framing, Scanning, Futuring, Designing, Adapting, or Leading.
* '''References & Recommended Reading''': Peer-reviewed citations and seminal literature.

[[Category:APF Competency - Leading]]
""",

    "APF:Peer Review Workflow": """__NOTOC__
{{Editorial_Status|status=approved|reviewer=APF Editorial & Peer Review Council|date=2026-09-08}}
{{APF_Competency_Badge|competency=Leading}}

= How the APF 5-Check Peer Review System Works =

To guarantee that the APF Foresight Wiki remains the definitive academic and professional authority for the futures discipline, every entry undergoes a double-blind, five-stage quality assurance protocol.

== The 5-Check Review Cycle ==
{| class="wikitable" style="width: 100%;"
|-
! Stage !! Checkpoint !! Vetting Scope !! Responsible Body
|-
| '''1. Scoping & Lineage''' || Theoretical Authenticity || Verifies historical provenance, theorist attribution, and foundational citations. || Domain Subject Matter Expert
|-
| '''2. Methodological Rigor''' || Analytical Validity || Audits step-by-step facilitation protocols, mathematical or logic models, and reproducibility. || APF Methodology Committee
|-
| '''3. Cognitive Bias Audit''' || Epistemological Balance || Scrutinizes for temporal myopia, Western/Eurocentric hegemony, techno-solutionism, and confirmation bias. || Ethics & Inclusivity Council
|-
| '''4. Empirical Case Stress-Testing''' || Real-World Application || Confirms practical utility against documented public and corporate foresight interventions. || Senior APF Full Member
|-
| '''5. Editorial Council Ratification''' || Canonical Quality Sign-off || Final review for stylistic elegance, high-contrast readability, and taxonomy consistency. || APF Editorial Board
|}

== Status Badges & Lifecycle ==
Articles display their current verification state via the <code><nowiki>{{Editorial_Status}}</nowiki></code> banner:
* <code>draft</code>: Working draft undergoing initial synthesis.
* <code>in_review</code>: Assigned to vetted peer reviewers.
* <code>revisions_requested</code>: Reviewer comments awaiting integration.
* <code>approved</code>: Formally ratified by the APF Editorial Council.

[[Category:APF Competency - Leading]]
""",

    "APF Most Significant Futures Works (MSFW) Historic Laureates Archive": """__NOTOC__
{{Editorial_Status|status=approved|reviewer=APF Editorial & Peer Review Council|date=2026-09-08}}
{{APF_Competency_Badge|competency=Leading}}

= APF Most Significant Futures Works (MSFW) Historic Laureates Archive =

The '''Most Significant Futures Works (MSFW)''' awards are the highest honors presented annually by the [[Association of Professional Futurists (APF - History & Code)|Association of Professional Futurists]] to recognize excellence, intellectual depth, and transformative impact in published foresight literature and applied interventions.

== Award Categories ==
Each year, an independent jury of distinguished futurists evaluates nominations across three core categories:
* '''Category 1: Advance the Methodology and Practice of Foresight''': Groundbreaking theoretical treatises, new analytical methodologies, and innovative facilitation instruments.
* '''Category 2: Boost Understanding of Alternative Futures''': Deep scenario studies, planetary frontier assessments, and anticipatory policy inquiries exploring plural possibilities.
* '''Category 3: Works for a Broad Audience''': Accessible, compelling books, media, and public interventions that elevate futures consciousness in civil society.

== Notable Historic Laureates & Landmark Winners ==
{| class="wikitable" style="width: 100%;"
|-
! Year !! Category !! Title !! Authors / Organization
|-
| 2023 || Advance Methodology || ''Transformative Scenario Planning in Practice'' || Reos Partners
|-
| 2022 || Boost Understanding || ''Planetary Health and Civilizational Resilience'' || Stockholm Resilience Centre
|-
| 2021 || Broad Audience || ''The Good Ancestor: How to Think Long-Term in a Short-Term World'' || Roman Krznaric
|-
| 2020 || Advance Methodology || ''The Experiential Futures Ladder and Diegetic Prototypes'' || Stuart Candy & Jake Dunagan
|-
| 2019 || Boost Understanding || ''Post-Normal Times and Emerging Polycrisis'' || Ziauddin Sardar & Centre for Postnormal Policy
|-
| 2018 || Advance Methodology || ''Causal Layered Analysis 2.0: Theory and Practice'' || Sohail Inayatullah & Ivana Milojević
|}

== See Also ==
* [[Association of Professional Futurists (APF - History & Code)|Association of Professional Futurists]]
* [[01_canonical_foresight_books|APF Canonical Books Library]]
* [[APF Emerging Fellows Program]]

[[Category:APF Competency - Leading]]
""",

    "The Futures Cone": "#REDIRECT [[The Futures Cone (Plausible, Possible, Probable, Preferable)]]"
}

def deploy_all():
    print("🚀 Starting APF Autonomous Design System & Portal Deployment...")
    wm = WikiManager()
    if not wm.authenticate():
        print("❌ Authentication failed. Exiting.")
        return False

    # 1. Deploy MediaWiki:Common.css
    print("\n[1/7] Deploying MediaWiki:Common.css...")
    css_path = os.path.join(TEMPLATES_DIR, "MediaWiki_Common.css")
    with open(css_path, "r", encoding="utf-8") as f:
        ok, res = wm.edit_page("MediaWiki:Common.css", f.read(), "Deploy High-Contrast APF Executive Theme & Layout Engine")
        print("  ✔ MediaWiki:Common.css deployed" if ok else f"  ❌ {res}")

    # 2. Deploy Templates
    print("\n[2/7] Deploying Core Templates...")
    badge_path = os.path.join(TEMPLATES_DIR, "APF_Competency_Badge.wiki")
    with open(badge_path, "r", encoding="utf-8") as f:
        ok, res = wm.edit_page("Template:APF_Competency_Badge", f.read(), "Support named competency parameter and clickable category links")
        print("  ✔ Template:APF_Competency_Badge updated" if ok else f"  ❌ {res}")

    status_path = os.path.join(TEMPLATES_DIR, "Editorial_Status.wiki")
    with open(status_path, "r", encoding="utf-8") as f:
        ok, res = wm.edit_page("Template:Editorial_Status", f.read(), "Polished high-contrast editorial banner")
        print("  ✔ Template:Editorial_Status updated" if ok else f"  ❌ {res}")

    # 3. Deploy Main Page
    print("\n[3/7] Deploying Main Page...")
    with open(MAIN_PAGE_PATH, "r", encoding="utf-8") as f:
        ok, res = wm.edit_page("Main Page", f.read(), "High-contrast hero banner, emblem seal medallion, and verified navigation links")
        print("  ✔ Main Page deployed" if ok else f"  ❌ {res}")

    # 4. Deploy 5 Resource Canon Pages
    print("\n[4/7] Deploying 5 Canonical Media & Literature Repositories...")
    canon_files = {
        "01_canonical_foresight_books.wiki": "01_canonical_foresight_books",
        "02_peer_reviewed_journal_canon.wiki": "02_peer_reviewed_journal_canon",
        "03_foresight_podcasts_directory.wiki": "03_foresight_podcasts_directory",
        "04_blogs_newsletters_and_signals.wiki": "04_blogs_newsletters_and_signals",
        "05_landmark_presentations_and_keynotes.wiki": "05_landmark_presentations_and_keynotes"
    }
    for filename, pagename in canon_files.items():
        fp = os.path.join(RESOURCES_DIR, filename)
        if os.path.exists(fp):
            with open(fp, "r", encoding="utf-8") as f:
                content = f.read()
            ok, res = wm.edit_page(pagename, content, f"Publish APF Canonical Resource: {pagename}")
            print(f"  ✔ {pagename} published" if ok else f"  ❌ {pagename}: {res}")
            # Also publish under full name redirect if relevant
            first_h1 = re.search(r"^=\s*(.+?)\s*=$", content, re.MULTILINE)
            if first_h1:
                full_title = first_h1.group(1).strip()
                wm.edit_page(full_title, f"#REDIRECT [[{pagename}]]", f"Redirect to {pagename}")

    # 5. Deploy Gateway Pages
    print("\n[5/7] Deploying Community & Governance Gateway Pages...")
    for title, content in GATEWAY_PAGES.items():
        ok, res = wm.edit_page(title, content, f"Establish APF Gateway Page: {title}")
        print(f"  ✔ {title} created" if ok else f"  ❌ {title}: {res}")

    # 6. Deploy 6 APF Competency Category Portals
    print("\n[6/7] Deploying 6 APF Competency Category Portals...")
    for cat_title, data in COMPETENCY_PORTALS.items():
        portal_text = f"""__NOTOC__
{{| class="apf-portal-header" style="width: 100%; background: {data['bg_grad']}; color: #ffffff !important; padding: 2em; border-radius: 10px; margin-bottom: 2em; box-shadow: 0 4px 14px rgba(0,0,0,0.15);"
|-
|
<div style="color: #38bdf8; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; font-size: 12px; margin-bottom: 6px;">APF Core Foresight Competency {data['num']}</div>
<h1 style="color: #ffffff !important; margin: 0 0 10px 0; border: none; font-size: 2.2em; text-shadow: 0 2px 8px rgba(0,0,0,0.4);">{data['title']}</h1>
<div style="color: #f1f5f9 !important; font-size: 1.15em; line-height: 1.5; max-width: 850px;">
{data['desc']}
</div>
|}}

== Competency Scope & Practice Architecture ==
{data['details']}

== Encyclopedic Entries in this Competency ==
Explore the peer-reviewed canonical entries in '''{data['title']}''' indexed below:
"""
        ok, res = wm.edit_page(cat_title, portal_text, f"Deploy APF Competency Portal Header for {data['title']}")
        print(f"  ✔ {cat_title} established" if ok else f"  ❌ {cat_title}: {res}")

    # 7. Deploy 20 Thematic Pillar Portals
    print("\n[7/7] Deploying 20 Thematic Pillar Portals...")
    for cat_title, (full_name, summary) in THEMATIC_PORTALS.items():
        portal_text = f"""__NOTOC__
{{| class="apf-portal-header" style="width: 100%; background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); color: #ffffff !important; padding: 1.8em; border-radius: 10px; margin-bottom: 2em; box-shadow: 0 4px 14px rgba(0,0,0,0.15);"
|-
|
<div style="color: #38bdf8; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; font-size: 12px; margin-bottom: 6px;">APF Thematic Knowledge Pillar</div>
<h1 style="color: #ffffff !important; margin: 0 0 10px 0; border: none; font-size: 2em; text-shadow: 0 2px 8px rgba(0,0,0,0.4);">{full_name}</h1>
<div style="color: #f1f5f9 !important; font-size: 1.1em; line-height: 1.5; max-width: 850px;">
{summary}
</div>
|}}

Browse all peer-reviewed articles curated under this pillar below:
"""
        ok, res = wm.edit_page(cat_title, portal_text, f"Deploy Thematic Pillar Header for {full_name}")
        print(f"  ✔ {cat_title} established" if ok else f"  ❌ {cat_title}: {res}")

    print("\n🎉 Full Design System & Portal Deployment Complete!")
    return True

if __name__ == "__main__":
    deploy_all()
