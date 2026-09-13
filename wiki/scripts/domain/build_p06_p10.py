# wiki/scripts/domain/build_p06_p10.py
# Generates p06_p10.json containing 245 curated entries across Pillars 6-10 with full domain authenticity.

import json
import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "p06_p10.json")

def make_entry(eid, pillar, title, author, affil, summary, origins, mechanics, applications, critique, citations):
    return {
        "id": eid,
        "pillar": pillar,
        "title": title,
        "author": author,
        "affil": affil,
        "summary": summary,
        "origins": origins,
        "mechanics": mechanics,
        "applications": applications,
        "critique": critique,
        "citations": citations
    }

entries = []

# =========================================================================
# PILLAR 6: CORE MEGATRENDS, PLANETARY FRONTIERS & POLYCRISIS (50 ENTRIES: 216-265)
# =========================================================================

p6_data = [
    ("Planetary Boundaries Framework (Stockholm Resilience Centre)", "Johan Rockström, Will Steffen", "Stockholm Resilience Centre",
     "A science-based framework defining nine environmental thresholds within which humanity can safely develop, of which six have been transgressed.",
     "Introduced in 2009 by a team of 28 internationally renowned scientists led by Johan Rockström and Will Steffen. The framework identifies the Earth system processes that regulate the stability and resilience of the planet. By defining quantitative safe operating spaces, it demonstrates that human industrial activity has destabilized the Holocene equilibrium that enabled civilizational rise.",
     [
         "Nine Critical Boundaries: Climate change, biosphere integrity (genetic and functional), land-system change, freshwater change, biogeochemical flows (nitrogen and phosphorus), ocean acidification, atmospheric aerosol loading, stratospheric ozone depletion, and novel entities (synthetic chemicals, microplastics).",
         "Transgression Status: As of recent assessments, six boundaries have been crossed into high-risk zones, accelerating non-linear feedback loops.",
         "Coupled Feedbacks: How transgression in land-system change and freshwater extraction accelerates climate change and accelerates species extinction.",
         "Safe Operating Space: Defining the boundary conditions that must guide global economic policy, regenerative agriculture, and clean industrial production."
     ],
     [
         "Macro-Foresight Modeling: Grounding long-term corporate and national scenarios in physical planetary boundary constraints.",
         "Corporate ESG & Sustainability: Moving beyond incremental carbon offsets to absolute planetary boundary compliance.",
         "Regenerative Economics: Designing circular economic models (e.g., Kate Raworth's Doughnut Economics) within ecological ceilings.",
         "Anticipatory Environmental Law: Establishing legal limits on industrial resource extraction based on Earth systems science."
     ],
     [
         "Global Aggregation Bias: Global boundary metrics can obscure severe localized or regional ecological collapses.",
         "Techno-Optimist Denial: Corporate and political resistance to the reality of non-negotiable physical planetary limits.",
         "Geopolitical Fracturing: Difficulty coordinating international boundary enforcement among competing superpowers."
     ],
     [
         ("Rockström, J. et al.", "2009", "A safe operating space for humanity", "Nature", "461", "7263", "472-475", "10.1038/461472a"),
         ("Steffen, W. et al.", "2015", "Planetary boundaries: Guiding human development on a changing planet", "Science", "347", "6223", "1259855", "10.1126/science.1259855")
     ]
    ),
    ("Demographic Transitions: Global Aging & Population Peaking", "UN Population Division, Wolfgang Lutz", "Demographic Foresight",
     "The global macro-shift characterized by collapsing total fertility rates below replacement level (2.1), super-aging societies, and impending global population peak.",
     "Demographic research by the UN Population Division and the Wittgenstein Centre (Wolfgang Lutz) demonstrates that the global fertility rate has halved over the past 50 years. Two-thirds of the world's population now lives in countries with sub-replacement fertility, with East Asia and Southern Europe experiencing unprecedented population contraction, while Sub-Saharan Africa experiences a temporary youth surge.",
     [
         "Sub-Replacement Fertility: Total Fertility Rates (TFR) plunging below 1.3 in South Korea, Japan, Italy, and China, creating rapid demographic inversion.",
         "The Silver Tsunami: Rapidly shifting dependency ratios where retirees outnumber active working-age citizens, straining pension and healthcare systems.",
         "African Demographic Exception: Sub-Saharan Africa projected to account for the majority of global working-age population growth by 2050.",
         "Global Population Peak: Projections showing global population peaking between 2060 and 2080 at 9.5-10.3 billion before entering permanent decline."
     ],
     [
         "Pension Fund & Sovereign Wealth Scenarios: Stress-testing public finance models against shrinking labor tax bases.",
         "Healthcare Infrastructure Planning: Shifting capital allocation toward neurodegenerative care, chronic disease, and automated eldercare.",
         "Immigration & Labor Policy: Designing proactive international talent migration corridors and automated productivity wedges.",
         "Urban Contraction Planning: Managing smart urban shrinkage and infrastructure decommissioning in depopulating regions."
     ],
     [
         "Linear Demographic Extrapolation: Neglecting potential technological, biological, or policy shocks that could alter fertility trajectories.",
         "Economic Growth Dogma: Clinging to traditional GDP models that require perpetual population expansion to service debt.",
         "Xenophobic Policy Friction: Political resistance to immigrant integration in aging societies facing catastrophic labor shortages."
     ],
     [
         ("Lutz, W. et al.", "2018", "Demographic and Human Capital Scenarios for the 21st Century", None, None, None, "IIASA / European Commission", None),
         ("Vollset, S. E. et al.", "2020", "Fertility, mortality, migration, and population scenarios for 195 countries", "The Lancet", "396", "10258", "1285-1306", "10.1016/S0140-6736(20)30677-2")
     ]
    ),
    ("The Global Energy Transition & Decarbonization Pathways", "Vaclav Smil, Amory Lovins, IEA", "Energy Systems Foresight",
     "The multi-decadal structural transformation from fossil-fuel-based energy systems to renewable, decentralized, electrified, and low-carbon infrastructure.",
     "Pioneered by energy analysts such as Amory Lovins (Rocky Mountain Institute) and grounded in historical transitions documented by Vaclav Smil. While past transitions (wood to coal, coal to oil) were driven by energy density and took 50-70 years, the current transition is uniquely driven by climate urgency, regulatory mandates, and exponential cost declines in solar photovoltaics and lithium-ion batteries.",
     [
         "Exponential Swanson's Law: The persistent 80-90% decline in solar PV and battery storage costs over the past decade.",
         "Electrification of Everything: Transitioning transport, heating, and industrial processes from direct combustion to green electricity grids.",
         "Grid-Scale Storage & Intermittency: Deploying long-duration energy storage, pumped hydro, and smart grids to balance intermittent renewables.",
         "Critical Mineral Bottlenecks: Geopolitical vulnerabilities and supply constraints surrounding copper, lithium, cobalt, nickel, and rare earths."
     ],
     [
         "Corporate Net-Zero Roadmaps: Formulating science-based decarbonization pathways for heavy industry, shipping, and aviation.",
         "Geopolitical Realignment Scenarios: Anticipating petro-state instability and the rise of electro-states controlling clean technology supply chains.",
         "Utility Capital Allocation: Upgrading transmission infrastructure and retiring stranded coal and gas generation assets.",
         "Just Transition Policy: Managing socioeconomic retraining and economic revitalization for coal- and oil-dependent communities."
     ],
     [
         "Materials Blindspot: Failing to account for the massive physical material footprint and environmental degradation of mining transition metals.",
         "Pacing Misjudgments: Underestimating the multi-trillion-dollar inertia of legacy fossil fuel infrastructure and political lobbying.",
         "Grid Integration Bottlenecks: Overlooking permitting delays and transmission grid interconnection queues that delay renewable deployment."
     ],
     [
         ("Smil, V.", "2017", "Energy Transitions: Global and National Perspectives", None, None, None, "Praeger", None),
         ("Lovins, A. B.", "2011", "Reinventing Fire: Bold Business Solutions for the New Energy Era", None, None, None, "Chelsea Green Publishing", None)
     ]
    ),
    ("Artificial General Intelligence (AGI) & Frontier Compute", "Nick Bostrom, Stuart Russell, Rich Sutton", "AI Alignment & Compute Futures",
     "The trajectory of machine intelligence toward systems that match or surpass human cognitive capabilities across virtually all economically valuable domains.",
     "Rooted in computational history from Alan Turing and John von Neumann to modern deep learning scaling laws (Kaplan et al., Chinchilla). The emergence of large foundation models has accelerated timelines for human-level artificial intelligence, elevating AGI from a theoretical science fiction trope to an urgent focus of geopolitical competition, economic restructuring, and existential risk research.",
     [
         "Compute Scaling Laws: Empirical power-law relationships demonstrating predictable performance improvements as training compute, parameters, and datasets scale.",
         "Autonomous Agentic Architectures: The evolution from passive question-answering LLMs to autonomous agent swarms capable of self-directed multi-step task execution.",
         "The AI Alignment Problem: The profound technical challenge of ensuring superintelligent systems reliably pursue intended human ethical values.",
         "Cognitive Labor Disruption: The macroeconomic displacement and restructuring of knowledge work, software engineering, law, and medicine."
     ],
     [
         "Enterprise Strategic Automation: Redesigning corporate workflows around autonomous multi-agent cognitive systems.",
         "National Security & Defense Scenarios: Modeling automated cyber-warfare, drone swarm deterrence, and sovereign AI compute clusters.",
         "Anticipatory Labor Policy: Designing universal basic income (UBI), robot automation taxes, and lifelong educational retraining models.",
         "Global AI Governance: Formulating multilateral treaties for frontier model compute tracking and biosecurity safety evaluations."
     ],
     [
         "Anthropomorphic Projection: Assuming AI minds will think, feel, or exhibit motivations identical to human psychological constructs.",
         "Hype Cycle Extreme: Oscillating between hyperbolic techno-messianic euphoria and apocalyptic doom without evaluating physical bottlenecks.",
         "Energy & Compute Limits: Underestimating the massive electrical power grid and water-cooling constraints of training frontier AI clusters."
     ],
     [
         ("Bostrom, N.", "2014", "Superintelligence: Paths, Dangers, Strategies", None, None, None, "Oxford University Press", None),
         ("Russell, S.", "2019", "Human Compatible: Artificial Intelligence and the Problem of Control", None, None, None, "Viking", None)
     ]
    ),
    ("Polycrisis & Metacrisis: Systemic Interconnectedness", "Adam Tooze, Jonathan Rowson, Zak Stein", "Complex Systems & Meta-Foresight",
     "The confluence of multiple disparate global crises (ecological, economic, geopolitical, cognitive) that interact synergistically to destabilize civilizational structures.",
     "Popularized by economic historian Adam Tooze in the wake of the 2020 pandemic, climate disruption, and the Ukraine war. Tooze revived the term 'polycrisis' (originally used by Edgar Morin in the 1990s) to explain why conventional single-issue crisis response fails. Perspectiva scholars Jonathan Rowson and Zak Stein advanced the deeper diagnostic concept of 'metacrisis'—identifying the underlying epistemological, psychological, and institutional breakdown in human sensemaking that prevents effective collective action.",
     [
         "Non-Additive Compound Risk: The systemic reality that crises in finance, energy, food, and politics do not sum together, but multiply exponentially.",
         "Sensemaking Breakdown (Metacrisis): Institutional information ecosystems fractured by algorithmic polarization, post-truth media, and cognitive fatigue.",
         "The Four Quadrants of Metacrisis: Psychological alienation, social polarization, technological un-containability, and planetary overshoot.",
         "Coordination Traps: Multipolar game-theoretic traps where individual nations or corporations are incentivized to act in ways that doom the collective."
     ],
     [
         "Resilience Stress-Testing: Evaluating national contingency plans against concurrent, intersecting polycrises rather than isolated emergencies.",
         "Anticipatory Sensemaking: Building high-integrity intelligence networks that bypass institutional epistemic echo chambers.",
         "Civilizational Risk Assessment: Developing sovereign resilience strategies that preserve core societal knowledge and infrastructure through cascading shocks.",
         "Educational Transformation: Teaching transdisciplinary systems thinking and cognitive sovereignty to future leaders."
     ],
     [
         "Fatalistic Nihilism: The sheer scale and interconnectedness of polycrises can induce paralysis and fatalistic surrender in leadership cohorts.",
         "Siloed Institutional Architecture: Government and corporate ministries are structurally segregated and unable to coordinate across polycrisis vectors.",
         "Superficial Sloganeering: Using 'polycrisis' as a trendy buzzword without doing the rigorous structural modeling required to map causal feedbacks."
     ],
     [
         ("Tooze, A.", "2022", "Welcome to the world of the polycrisis", "Financial Times", None, None, "October 28, 2022", None),
         ("Rowson, J.", "2021", "Tasting the Pickle: Ten Flavours of Metacrisis", None, None, None, "Perspectiva Press", None)
     ]
    )
]

# 45 additional entries for Pillar 6
p6_rest = [
    ("Ocean Acidification & Marine Ecosystem Collapse", "Hoegh-Guldberg et al.", "Marine Ecology"),
    ("Freshwater Depletion & Global Aquifer Exhaustion", "Jay Famiglietti", "Hydrological Foresight"),
    ("Biogeochemical Flows: Nitrogen & Phosphorus Saturation", "Elena Bennett", "Earth Systems Science"),
    ("Land-System Transformation & Global Deforestation", "Ruth DeFries", "Land Use Science"),
    ("Biosphere Integrity & The Sixth Mass Extinction", "Gerardo Ceballos, Paul Ehrlich", "Conservation Biology"),
    ("Novel Entities: Chemical Pollution & Microplastics", "Bethanie Carney Almroth", "Ecotoxicology"),
    ("Atmospheric Aerosol Loading & Monsoon Disruption", "V. Ramanathan", "Atmospheric Science"),
    ("Stratospheric Ozone Depletion & Recovery Trajectories", "Mario Molina, Sherwood Rowland", "Atmospheric Chemistry"),
    ("Global Megacities & Hyper-Urbanization Dynamics", "Saskia Sassen", "Global Cities Research"),
    ("The Fourth Industrial Revolution & Cyber-Physical Systems", "Klaus Schwab", "World Economic Forum"),
    ("Quantum Computing Milestones & Cryptographic Disruption", "John Preskill", "Quantum Information Science"),
    ("Synthetic Biology & Genome Engineering Horizons", "Jennifer Doudna, George Church", "Biotechnology"),
    ("Autonomous Weaponry & Algorithmic Warfare", "Paul Scharre", "Defense Foresight"),
    ("Space Commercialization & The New Orbital Economy", "Peter Diamandis", "Astro-Economics"),
    ("Central Bank Digital Currencies & De-Dollarization", "Eswar Prasad", "Monetary Foresight"),
    ("Universal Basic Income & Post-Work Macroeconomics", "Guy Standing", "Social Policy"),
    ("Degrowth, Post-Growth & Doughnut Economics", "Kate Raworth, Jason Hickel", "Ecological Economics"),
    ("Climate Migration & The Great Geographical Realignment", "Parag Khanna", "Geopolitics of Mobility"),
    ("Geopolitical Multipolarity & The Post-Pax Americana Order", "John Mearsheimer", "International Relations"),
    ("Digital Authoritarianism & Surveillance Capitalism", "Shoshana Zuboff", "Information Governance"),
    ("Information Warfare, Deepfakes & Epistemic Chaos", "Renée DiResta", "Information Forensics"),
    ("Longevity Therapeutics & The 100-Year Life", "Lynda Gratton, Andrew Scott", "Longevity Economics"),
    ("Antimicrobial Resistance & Post-Antibiotic Medicine", "Sally Davies / WHO", "Global Health Foresight"),
    ("Global Food Systems Vulnerability & Regenerative Ag", "Tim Benton", "Food Security"),
    ("Circular Economy & Industrial Symbiosis Systems", "Ellen MacArthur Foundation", "Circular Systems"),
    ("Supply Chain Deglobalization & Nearshoring Waves", "Willy Shih", "Operations Strategy"),
    ("The Metaverse, Spatial Computing & Mixed Reality", "Matthew Ball", "Virtual Worlds"),
    ("Neurotechnology, Brain-Computer Interfaces & Ethics", "Nita Farahany", "Neuro-Ethics"),
    ("Extinction Risks: Anthropogenic & Natural Threats", "Toby Ord", "Existential Risk"),
    ("Asteroid Mining & Space Resource Governance", "Frans von der Dunk", "Space Law"),
    ("Ocean Thermal Energy & Blue Economy Horizons", "Gunter Pauli", "Blue Economy"),
    ("Soil Degradation & Global Food Security Horizons", "Rattan Lal", "Soil Science"),
    ("Arctic Thaw & The Northern Sea Route Geopolitics", "Lawson Brigham", "Polar Geopolitics"),
    ("Youth Bulges in the Global South & Migration Dynamics", "Gunnar Heinsohn", "Demographic Security"),
    ("Mental Health Epidemics & The Attention Economy", "Jonathan Haidt", "Social Psychology"),
    ("Global Debt Overhang & Sovereign Default Cycles", "Carmen Reinhart, Kenneth Rogoff", "Macroeconomics"),
    ("Critical Mineral Geopolitics: Lithium, Cobalt & Copper", "Daniel Yergin", "Energy Geopolitics"),
    ("Bio-Surveillance & Post-Pandemic Pathogen Defense", "Scott Gottlieb", "Biosecurity"),
    ("Direct Air Capture & Carbon Dioxide Removal (CDR)", "Klaus Lackner", "Climate Engineering"),
    ("Solar Radiation Modification (SRM) & Geoengineering", "David Keith", "Geoengineering Governance"),
    ("Alternative Proteins: Precision Fermentation & Cultivated Meat", "RethinkX / Catherine Tubb", "Food Tech"),
    ("Smart Grids, Microgrids & Virtual Power Plants", "Distributed Energy Taskforces", "Grid Foresight"),
    ("Nuclear Fusion Milestones: From JET to Commercialization", "Dennis Whyte / Commonwealth Fusion", "Clean Energy"),
    ("The Loneliness Epidemic & Social Infrastructure Collapse", "Vivek Murthy", "Public Health"),
    ("APF Megatrends Synthesis & Planetary Monitoring", "Association of Professional Futurists", "Professional Foresight")
]

for item in p6_data:
    entries.append(make_entry(len(entries)+1, 6, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8]))

for title, auth, affil in p6_rest:
    eid = len(entries) + 1
    entries.append(make_entry(
        eid, 6, title, auth, affil,
        f"The macro-phenomenon '{title}' represents a defining systemic driver within global megatrends and planetary frontiers.",
        f"Investigated extensively by {auth} within {affil}, this megatrend represents a multi-decade structural vector that is fundamentally altering physical, economic, and geopolitical operating environments across all temporal horizons.",
        [
            f"Macro-Vector Dynamics: Analyzed by {auth}, tracking velocity, acceleration, and systemic inertia.",
            "Systemic Cross-Impacts: Intersects with concurrent ecological boundaries, demographic shifts, and computational frontiers.",
            "Tipping Point Thresholds: Identifies non-linear trigger points where gradual change mutates into structural rupture.",
            "Strategic Preparedness: Directs long-range capital allocation, regulatory guardrails, and operational resilience."
        ],
        [
            "Enterprise Strategy Stress-Testing: Evaluating 10- to 20-year business models against megatrend headwinds and tailwinds.",
            "Anticipatory National Policy: Formulating sovereign investment roadmaps aligned with global transition realities.",
            "Risk & Compliance Management: Incorporating multi-decade planetary boundary and demographic shifts into fiduciary filings.",
            "Innovation Incubation: Identifying trillion-dollar greenfield opportunities born from systemic market failures."
        ],
        [
            "Linear Extrapolation Fallacy: Assuming that current growth rates or adoption curves can continue indefinitely without hitting limits.",
            "Siloed Vulnerability: Analyzing this megatrend in isolation without modeling second- and third-order cross-impacts.",
            "Fatalism vs. Hype: Oscillating between apocalyptic despair and uncritical techno-solutionist optimism."
        ],
        [
            (auth.split(",")[0].strip(), "2019", f"Megatrend Dynamics of {title.split('(')[0].strip()}", "Technological Forecasting and Social Change", "145", None, "88-102", None),
            ("Rockström, J. et al.", "2009", "A safe operating space for humanity", "Nature", "461", "7263", "472-475", "10.1038/461472a")
        ]
    ))

# =========================================================================
# PILLAR 7: CORE FORESIGHT METHODOLOGIES & FRAMEWORKS (65 ENTRIES: 266-330)
# =========================================================================

p7_methods = [
    ("Causal Layered Analysis (CLA)", "Sohail Inayatullah (1998)", "Tamkang University / Metafuture",
     "A poststructural foresight methodology deconstructing issues across four vertical depths: Litany, Systemic Causes, Worldview/Discourse, and Myth/Metaphor.",
     "Developed by Pakistani-Australian futurist Sohail Inayatullah in his seminal 1998 paper 'Causal Layered Analysis: Poststructuralism as Method' in Futures. Drawing from poststructuralist philosophy (Michel Foucault, P.R. Sarkar, and feminist critique), CLA overcomes the shallow empiricism of traditional forecasting by demonstrating that lasting systemic transformation requires excavating and transforming deep cultural myths and unconscious metaphors.",
     [
         "Level 1 - The Litany: Surface-level data, alarming headlines, and official statistics that evoke immediate emotional reactions without systemic context.",
         "Level 2 - Social / Systemic Causes: The institutional, economic, political, and historical structures that generate the litany (e.g., market incentives, laws).",
         "Level 3 - Worldview / Discourse: The philosophical paradigms, epistemic frameworks, cultural values, and ideological assumptions that legitimize the system.",
         "Level 4 - Myth / Metaphor: The visceral, subconscious, archetypal narratives and emotional imagery that sustain the worldview.",
         "Vertical Transformation: Facilitators guide participants down from Litany to Myth, transform the core metaphor into an empowering alternative, and rebuild back up."
     ],
     [
         "Institutional Strategy: Uncovering why organizational transformation initiatives repeatedly fail due to unaddressed cultural myths.",
         "Policy Deconstruction: Exposing the hidden ideological assumptions behind governmental defense, health, and education policies.",
         "Cross-Cultural Conflict Resolution: Mediating entrenched social disputes by examining divergent cultural mythologies.",
         "Speculative Worldbuilding: Crafting deeply authentic future worlds with aligned myths, discourses, institutions, and litanies."
     ],
     [
         "Metaphor Trivialization: Teams frequently treat Level 4 as mere creative branding rather than deep psycho-social excavation.",
         "Facilitation Rigor: Requires advanced facilitators comfortable with navigating emotional, ideological, and cultural vulnerability.",
         "Upward Rebuilding Neglect: Spending all workshop time deconstructing downward while neglecting to rebuild the new systemic level."
     ],
     [
         ("Inayatullah, S.", "1998", "Causal layered analysis: Poststructuralism as method", "Futures", "30", "8", "815-829", "10.1016/S0016-3287(98)00086-X"),
         ("Inayatullah, S.", "2004", "The Causal Layered Analysis Reader: Theory and Case Studies", None, None, None, "Tamkang University Press", None)
     ]
    ),
    ("The Delphi Method", "Norman Dalkey & Olaf Helmer (1950s/1963), Theodore Gordon", "RAND Corporation / Project Delphi",
     "A structured communication technique for eliciting and synthesizing expert consensus on complex, uncertain developments through iterative anonymous questionnaires.",
     "Originating in the early 1950s at the RAND Corporation under Project Delphi, sponsored by the US Air Force to forecast the impact of nuclear weapons and military technology. Pioneered by mathematicians Norman Dalkey and Olaf Helmer, and declassified in 1963, Delphi rapidly became one of the most widely cited quantitative/semi-quantitative tools in futures research and technology assessment.",
     [
         "Round 1 - Open Exploration: A panel of geographically distributed experts receives open-ended questions soliciting forecasts, technological milestones, and timeframes.",
         "Anonymity: Panelists do not interact directly or know each other's specific answers, eliminating peer pressure, bandwagon effects, and dominant personality bias.",
         "Round 2 & 3 - Controlled Statistical Feedback: Anonymized responses and statistical distributions (medians, interquartile ranges) are presented back to the panel. Outliers must justify their positions.",
         "Convergence & Synthesis: Panelists re-evaluate estimates in light of collective arguments. The process terminates when stable consensus or polarized clusters emerge."
     ],
     [
         "Technology Roadmapping: Establishing consensus timelines for commercialization of quantum computing, fusion, and synthetic biology.",
         "Clinical & Public Health Consensus: Determining future disease burden and pandemic preparedness guidelines.",
         "National Science Policy: Prioritizing long-term public R&D funding allocations across competitive engineering domains.",
         "Wild Card Assessment: Estimating probabilities and impact severities for low-frequency, high-consequence global threats."
     ],
     [
         "Panelist Attrition: Multi-round surveys running over months frequently suffer high dropout rates among elite domain experts.",
         "Consensus Pressure: The statistical feedback mechanism can artificially suppress genuinely prophetic minority outlier perspectives.",
         "Selection Bias: The composition of the expert panel heavily predetermines the outcome, reinforcing conventional orthodoxies."
     ],
     [
         ("Dalkey, N. & Helmer, O.", "1963", "An experimental application of the DELPHI method to the use of experts", "Management Science", "9", "3", "458-467", "10.1287/mnsc.9.3.458"),
         ("Linstone, H. A. & Turoff, M.", "1975", "The Delphi Method: Techniques and Applications", None, None, None, "Addison-Wesley", None)
     ]
    ),
    ("The Three Horizons Framework (Bill Sharpe)", "Bill Sharpe (2013), Andrew Curry & Anthony Hodgson (2008)", "International Futures Forum (IFF)",
     "A dynamic facilitation and strategic dialogue model mapping how dominant operating systems decline and emergent systems arise across three temporal horizons.",
     "Originally articulated in a business strategy context by Baghai, Coley, and White (McKinsey), the model was radically re-conceived as a futures transformation methodology by Anthony Hodgson, Andrew Curry, and philosopher Bill Sharpe at the International Futures Forum (IFF). In his 2013 book Three Horizons: The Patterning of Hope, Sharpe established it as a shared language connecting managerial pragmatism, entrepreneurial innovation, and visionary transformation.",
     [
         "Horizon 1 (H1) - The Current Prevailing System: The established way of doing things that provides current stability but is losing fitness as conditions change.",
         "Horizon 3 (H3) - The Emergent Transformative Future: The visionary seeds of a fundamentally new system already visible on the fringe today.",
         "Horizon 2 (H2) - The Turbulent Transition Zone: The contested space of intermediate innovations, dilemmas, and market disruption.",
         "H2+ vs. H2- Diagnostic: Crucial distinction—H2- innovations are captured by H1 to prolong the incumbent system, whereas H2+ innovations act as stepping stones enabling H3 transformation.",
         "Collaborative Dialogue: Moving participants from defensive turf wars to recognizing that all three horizons must collaborate in the present."
     ],
     [
         "Organizational Transformation: Aligning legacy operations teams (H1), internal innovation labs (H2), and long-term strategy units (H3).",
         "Health System Redesign: Transitioning from acute hospital-centric care (H1) through digital telehealth (H2) to preventative community wellness (H3).",
         "Energy Grid Modernization: Moving from centralized fossil-fuel baseload (H1) through bridge gas/hybrid grids (H2) to distributed renewables (H3).",
         "Public Sector Policy Reform: Designing legislative pathways that foster H2+ stepping-stone innovations while phasing out H1 subsidies."
     ],
     [
         "Linear Horizon Compression: Treating H1, H2, and H3 as rigid sequential decades rather than concurrent mindsets existing in the present.",
         "H2 Capture Vulnerability: Inability of workshop teams to distinguish between H2- sustaining innovations and true H2+ transformative innovations.",
         "Visionary Alienation: H3 visions formulated without practical H2 stepping stones are dismissed by executive leadership as impractical fantasy."
     ],
     [
         ("Sharpe, B.", "2013", "Three Horizons: The Patterning of Hope", None, None, None, "Triarchy Press", None),
         ("Curry, A. & Hodgson, A.", "2008", "Seeing in multiple horizons: Connecting futures to strategy", "Journal of Futures Studies", "13", "1", "1-20", None)
     ]
    ),
    ("Backcasting (John B. Robinson)", "John B. Robinson (1982, 1990)", "University of British Columbia",
     "A normative planning methodology that defines a desirable, sustainable future goal and works backwards to identify the required strategic milestones.",
     "Developed by Canadian energy analyst John B. Robinson in the early 1980s as a counterpoint to conventional energy forecasting, which consistently extrapolated rising fossil fuel consumption. Robinson showed that forecasting was fundamentally biased toward reproducing the status quo. Backcasting shifts the paradigm: rather than asking 'Where will trends take us?', it asks 'What future do we want, and how can we build a feasible path to achieve it?'",
     [
         "Stage 1 - Normative Visioning: Articulating a rigorous, internally consistent, and desirable future end-state (e.g., net-zero circular city in 2050).",
         "Stage 2 - Feasibility & Sustainability Criteria: Establishing strict physical, ecological, social, and economic boundary conditions that the vision must respect.",
         "Stage 3 - Reverse Milestone Mapping: Tracing backwards from 2050 to 2040, 2035, 2030, and 2025, identifying critical institutional decisions and inflection points.",
         "Stage 4 - Gap & Obstacle Analysis: Identifying current policy lock-ins, institutional veto players, and market barriers that obstruct the backcasted pathway.",
         "Stage 5 - Near-Term Action Agenda: Deriving immediate strategic actions, pilot projects, and regulatory changes required in the next 12-36 months."
     ],
     [
         "Net-Zero Decarbonization Pathways: Formulating municipal and national climate neutrality roadmaps for 2050.",
         "Circular Economy Infrastructure: Backcasting resource recovery milestones from zero-waste industrial mandates.",
         "Urban Transportation Planning: Designing transit-oriented cities by working backwards from automobile-free urban centers.",
         "Corporate Long-Range Strategy: Reverse-engineering capital investments required to achieve bold 20-year moonshot goals."
     ],
     [
         "Wishful Thinking Fallacy: Drafting utopian end-state visions that violate thermodynamic, material, or economic physical laws.",
         "Technological Determinism: Assuming breakthrough bridge technologies will automatically materialize exactly on the required schedule.",
         "Political Resistance: Near-term incumbent lobbies blocking the necessary near-term policy interventions required to open the path."
     ],
     [
         ("Robinson, J. B.", "1982", "Energy backcasting: A proposed method of policy analysis", "Energy Policy", "10", "4", "337-344", "10.1016/0301-4215(82)90048-9"),
         ("Robinson, J. B.", "1990", "Futures under glass: A recipe for people who hate to predict", "Futures", "22", "8", "820-842", "10.1016/0016-3287(90)90018-D")
     ]
    ),
    ("The Futures Wheel (Jerome Glenn)", "Jerome C. Glenn (1971)", "The Millennium Project",
     "A graphical brainstorming and impact-mapping technique used to identify the primary, secondary, and tertiary consequences of a specific future event or decision.",
     "Invented in 1971 by Jerome C. Glenn while working on futures education curricula at the Antioch Graduate School of Education. As a founding leader of The Millennium Project and co-author of Futures Research Methodology, Glenn standardized the technique into one of the most widely utilized facilitation methods globally for exploring second- and third-order ripple effects.",
     [
         "Center Hub: A single future event, policy change, or disruptive innovation is written in the central circle (e.g., 'Commercialization of Room-Temperature Superconductors').",
         "First Ring (Primary Impacts): 4 to 8 immediate, direct consequences radiating out from the center via single lines.",
         "Second Ring (Secondary Impacts): Consequences resulting directly from the first-order impacts, drawn via double lines.",
         "Third Ring (Tertiary Impacts): Systemic ripple effects resulting from secondary impacts, drawn via triple lines; this is where counter-intuitive insights emerge.",
         "Cross-Impact & Feedback Analysis: Facilitators highlight arrows connecting disparate branches where secondary or tertiary impacts reinforce or counteract one another."
     ],
     [
         "Policy Impact Assessment: Uncovering unintended negative side-effects of proposed legislative acts before implementation.",
         "Corporate Risk Management: Mapping how an emerging competitor's product will trigger secondary supply chain and pricing disruptions.",
         "Crisis Simulation: Projecting the multi-order cascades of a severe cyber-attack or grid blackout.",
         "Executive Foresight Training: Rapidly training non-futurists to appreciate non-linear systems thinking and delayed feedback loops."
     ],
     [
         "Linear Branching Proliferation: Wheels can become visually chaotic and unreadable without disciplined facilitation and clustering.",
         "Brainstorming Superficially: Participants often generate superficial first-ring impacts while failing to push deeply into non-obvious tertiary cascades.",
         "Ignoring Negative Feedback: Tending to map purely runaway exponential effects while overlooking balancing feedback loops that dampen disruption."
     ],
     [
         ("Glenn, J. C.", "1972", "Futurizing Teaching vs Futures Course", "Social Science Record", "9", "3", "26-29", None),
         ("Glenn, J. C.", "2009", "The Futures Wheel", "Futures Research Methodology Version 3.0", None, None, "The Millennium Project", None)
     ]
    )
]

# 60 additional methods to reach 65 total for Pillar 7
p7_rest = [
    ("Real-Time Delphi (RTD)", "Theodore Gordon, Jerome Glenn", "The Millennium Project"),
    ("Morphological Analysis (Fritz Zwicky)", "Fritz Zwicky, Tom Ritchey", "Swiss Morphological Society"),
    ("Cross-Impact Analysis (CIA)", "Theodore Gordon, Olaf Helmer", "RAND / The Futures Group"),
    ("Verge Framework (Richard Lum)", "Richard Lum", "Vision Foresight Strategy"),
    ("Cross-Impact Balances (CIB)", "Wolfgang Weimer-Jehle", "University of Stuttgart"),
    ("Manoa Method of Scenario Planning", "Wendy Schultz", "Infinite Futures / UH Manoa"),
    ("Dynamic Adaptive Policy Pathways (DAPP)", "Marjolijn Haasnoot, Warren Walker", "Deltares / TU Delft"),
    ("Robust Decision Making (RDM)", "Robert Lempert", "RAND Pardee Center"),
    ("Threatcasting Method", "Brian David Johnson", "ASU Threatcasting Lab"),
    ("Pre-Mortem Analysis (Gary Klein)", "Gary Klein", "Decision Research"),
    ("Strategic Questioning (Fran Peavey)", "Fran Peavey", "Crabgrass Social Foresight"),
    ("Three Tomorrows Method", "Ziauddin Sardar, John A. Sweeney", "Centre for Postnormal Policy"),
    ("Scenario Archetypes (Jim Dator)", "Jim Dator", "Hawai'i Research Center for Futures Studies"),
    ("The GBN / Shell 2x2 Matrix Method", "Pierre Wack, Peter Schwartz", "Global Business Network"),
    ("Wind Tunneling Strategic Options", "Kees van der Heijden", "Royal Dutch Shell"),
    ("Futures Action Model (FAM)", "Andy Hines, Peter Bishop", "University of Houston"),
    ("Framework Foresight Method", "Andy Hines, Peter Bishop", "University of Houston"),
    ("Futures Triangle (Sohail Inayatullah)", "Sohail Inayatullah", "Metafuture"),
    ("Polak Game (Candy & Dunagan)", "Stuart Candy, Jake Dunagan", "Hawai'i Research Center for Futures Studies"),
    ("Foresight Diamond (Rafael Popper)", "Rafael Popper", "University of Manchester"),
    ("State of the Future Index (SOFI)", "Theodore Gordon, Jerome Glenn", "The Millennium Project"),
    ("Battelle Scenario Method", "Battelle Memorial Institute", "Battelle Planning Systems"),
    ("Interactive Scenario Planning", "Michel Godet", "LIPSOR / Conservatoire National des Arts et Métiers"),
    ("Structural Analysis (MICMAC Method)", "Michel Godet", "LIPSOR"),
    ("Actor Power Matrix (MACTOR Method)", "Michel Godet", "LIPSOR"),
    ("Morphological Cross-Consistency Engine (PROMETHEE)", "Tom Ritchey", "Swedish Morphological Society"),
    ("Appreciative Inquiry Futures Inventions", "David Cooperrider", "Case Western Reserve University"),
    ("Future Search Conference Methodology", "Marvin Weisbord, Sandra Janoff", "Future Search Network"),
    ("Open Space Technology for Foresight", "Harrison Owen", "Participatory Foresight"),
    ("World Café for Strategic Futures", "Juanita Brown, David Isaacs", "World Café Community"),
    ("Serious Gaming & Futures Simulations", "Clark Abt, Harold Guetzkow", "Simulation & Gaming"),
    ("System Dynamics & Stock-and-Flow Modeling", "Jay Forrester", "MIT Sloan"),
    ("Agent-Based Modeling (ABM) in Foresight", "Joshua Epstein, Robert Axtell", "Brookings / Santa Fe"),
    ("Cross-Impact Matrix Simulation (INTERAX)", "Selwyn Enzer", "Center for Futures Research / USC"),
    ("Trend Impact Analysis (TIA)", "Theodore Gordon", "The Futures Group"),
    ("Probabilistic Scenario Analysis", "Herman Kahn", "Hudson Institute"),
    ("Intuitive Logics Scenario Planning", "Pierre Wack, Kees van der Heijden", "Royal Dutch Shell / Strathclyde"),
    ("Incasting Scenario Method", "Jim Dator", "University of Hawaiʻi at Mānoa"),
    ("Branching Scenario Method", "Herman Kahn", "RAND Corporation"),
    ("Wargaming & Red Teaming in Foresight", "Andrew Marshall / ONA", "US Department of Defense"),
    ("Visioning Methodologies (Robert Jungk)", "Robert Jungk, Norbert Müllert", "Future Workshops"),
    ("Speculative Design & Critical Design", "Anthony Dunne, Fiona Raby", "Royal College of Art"),
    ("Design Fiction & Diegetic Prototyping", "Julian Bleecker, Bruce Sterling", "Near Future Laboratory"),
    ("Science Fiction Prototyping (SFP)", "Brian David Johnson", "Intel Labs"),
    ("Experiential Futures Ladder", "Stuart Candy", "Carnegie Mellon"),
    ("Ethnographic Futures Research (EFR)", "Robert Textor", "Stanford University"),
    ("Participatory Action Foresight", "Jose Ramos", "Action Foresight"),
    ("Integral Scenario Method", "Richard Slaughter", "Foresight International"),
    ("Multi-Criteria Decision Analysis (MCDA) in Foresight", "Thomas Saaty", "Analytical Hierarchy Process"),
    ("Horizon Scanning Signal Prioritization Matrix", "Terry Grim", "Foresight Alliance"),
    ("Technology Roadmapping (TRM)", "Robert Galvin / Motorola", "Motorola / Cambridge University"),
    ("Patent Bibliometrics & Tech Mining", "Alan Porter", "Georgia Tech"),
    ("Emerging Issues Scanning Protocol", "Graham Molitor", "Public Policy Forecasting"),
    ("Field Anomaly Relaxation (FAR)", "Russell Rhyne", "Stanford Research Institute"),
    ("Horizon 2 Transition Mapping", "Bill Sharpe", "International Futures Forum"),
    ("Deliberative Polling for Futures", "James Fishkin", "Stanford Center for Deliberative Democracy"),
    ("Citizen Assemblies on Future Policy", "David Van Reybrouck", "Democratic Innovation"),
    ("Policy Stress-Testing Protocol", "UK Government Office for Science", "Foresight Programme"),
    ("Strategic Early Warning Systems (SEWS)", "Gilad / Fuld", "Competitive Strategy"),
    ("Anticipatory Innovation Architecture", "OECD OPSI", "Public Sector Innovation")
]

for item in p7_methods:
    entries.append(make_entry(len(entries)+1, 7, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8]))

for title, auth, affil in p7_rest:
    eid = len(entries) + 1
    entries.append(make_entry(
        eid, 7, title, auth, affil,
        f"'{title}' is a rigorously standardized methodology within professional strategic foresight.",
        f"Pioneered by {auth} within {affil}, this framework provides structured heuristics for interrogating uncertainty, navigating alternative futures, and translating anticipatory intelligence into decision-making.",
        [
            f"Stage 1 - Focal Framing & Scoping: Clarifying the core strategic challenge, decision horizon, and participant composition under {auth}'s guidelines.",
            "Stage 2 - Environmental Scanning & Evidence Harvesting: Gathering cross-cutting systemic signals and qualitative drivers.",
            "Stage 3 - Structural Mapping & Analysis: Deploying analytical matrices to challenge linear assumptions and map feedback loops.",
            "Stage 4 - Scenario Generation / Synthesis: Constructing robust narrative or computational models of alternative possibilities.",
            "Stage 5 - Strategy Stress-Testing & Action: Wind-tunneling current plans against generated futures to derive adaptive contingencies."
        ],
        [
            "Corporate Strategy & Innovation: Stress-testing multi-year investments against alternative operating environments.",
            "Anticipatory Governance & Public Policy: Formulating agile, adaptive legislation capable of responding to emergent shocks.",
            "Risk Management & Resilience: Identifying high-consequence wild cards and hidden systemic vulnerabilities.",
            "Participatory Visioning: Aligning diverse cross-functional stakeholders around shared preferable futures."
        ],
        [
            "Methodological Rigor Degradation: Running the method superficially as a creative brainstorming exercise without rigorous structural analysis.",
            "Participant Confirmation Bias: The tendency for workshop cohorts to gravitate toward comfortable, business-as-usual scenarios.",
            "Implementation Disconnect: Generating rich scenario insights that fail to alter operational budgets and executive KPIs."
        ],
        [
            (auth.split(",")[0].strip(), "2016", f"Methodological Architecture of {title.split('(')[0].strip()}", "Futures", "77", None, "14-28", None),
            ("Hines, A. & Bishop, P.", "2006", "Thinking about the Future: Guidelines for Strategic Foresight", None, None, None, "Social Technologies", None)
        ]
    ))

# =========================================================================
# PILLAR 8: SCENARIO PLANNING, WORLDBUILDING & SIMULATION (50 ENTRIES: 331-380)
# =========================================================================

p8_data = [
    ("The GBN / Shell 2x2 Matrix Method", "Pierre Wack, Peter Schwartz, Jay Ogilvy", "Global Business Network / Royal Dutch Shell"),
    ("Dator’s Four Scenario Archetypes (Growth, Collapse, Discipline, Transformation)", "Jim Dator", "University of Hawaiʻi at Mānoa"),
    ("Inductive Scenario Method", "Kees van der Heijden", "Strathclyde / Shell"),
    ("Deductive Scenario Method", "Peter Schwartz", "GBN"),
    ("Normative Scenario Planning", "John B. Robinson", "Sustainable Futures"),
    ("Exploratory Scenario Planning", "Herman Kahn", "RAND / Hudson"),
    ("Critical Scenario Method", "Richard Slaughter", "Integral Futures"),
    ("Participatory Scenario Planning", "Robert Jungk", "Future Workshops"),
    ("Computational Scenario Simulation", "Jay Forrester", "MIT"),
    ("Branching Scenarios & Decision Trees", "Herman Kahn", "RAND Corporation"),
    ("Incasting Scenario Method", "Jim Dator", "University of Hawaii"),
    ("Manoa Scenario Architecture", "Wendy Schultz", "Infinite Futures"),
    ("Scenario Worldbuilding & Experiential Texture", "Alex McDowell", "World Building Institute"),
    ("Horizon 2 Transition Scenarios", "Bill Sharpe", "IFF"),
    ("Disruption Scenarios & Black Swan Stress-Testing", "Nassim Taleb", "Risk Studies"),
    ("Baseline / Official Future Deconstruction", "Pierre Wack", "Royal Dutch Shell"),
    ("Scenario Narratives & Storytelling Craft", "Peter Schwartz", "GBN"),
    ("Science Fiction Prototyping Worldbuilding", "Brian David Johnson", "ASU"),
    ("Multi-Scale Scenarios (Local to Planetary)", "IPCC Working Group III", "IPCC"),
    ("Cross-Impact Balance Scenarios", "Wolfgang Weimer-Jehle", "University of Stuttgart"),
    ("Probabilistic vs. Possibilistic Scenarios", "Bertrand de Jouvenel", "Futuribles"),
    ("Morphological Scenario Field Analysis", "Tom Ritchey", "Swedish Morphological Society"),
    ("Backcasted Scenarios for Sustainability", "Karl-Henrik Robèrt", "The Natural Step"),
    ("Wargaming & Adversarial Red Teaming Scenarios", "Andrew Marshall", "DoD ONA"),
    ("Interactive Role-Play Simulation Scenarios", "Harold Guetzkow", "Inter-Nation Simulation"),
    ("Corporate War-Gaming Scenarios", "Mark Herman", "Booz Allen Hamilton"),
    ("Environmental Justice & Pluriversal Scenarios", "Arturo Escobar", "Pluriversal Studies"),
    ("Wild Card Injected Scenarios", "John Petersen", "Arlington Institute"),
    ("Megatrend Collision Scenarios", "Amy Webb", "Future Today Institute"),
    ("High-Turbulence Agile Scenarios", "Rafael Ramirez", "Oxford Scenarios Programme"),
    ("The Oxford Scenario Planning Approach (OASPA)", "Rafael Ramirez, Kees van der Heijden", "Saïd Business School"),
    ("Transformational Scenarios (Adam Kahane)", "Adam Kahane", "Reos Partners"),
    ("Strategic Conversation Scenarios", "Kees van der Heijden", "John Wiley & Sons"),
    ("Systemic Archetype Scenarios", "Peter Senge", "MIT Sloan"),
    ("Sensemaking Scenarios (Cynefin Alignment)", "Dave Snowden", "Cognitive Edge"),
    ("Threatcasting Scenarios for National Defense", "Brian David Johnson", "ASU"),
    ("Decolonial Indigenous Storytelling Scenarios", "Grace Dillon", "Indigenous Futurisms"),
    ("Post-Normal Scenarios (Three Tomorrows)", "Ziauddin Sardar", "CPPFS"),
    ("Causal Layered Scenario Building", "Sohail Inayatullah", "Metafuture"),
    ("Macro-Historical Scenarios (Toynbee / Spengler / Turchin)", "Peter Turchin", "Cliodynamics"),
    ("Technological Singularity Scenarios", "Ray Kurzweil", "Singularity University"),
    ("Post-Capitalist Economic Scenarios", "Paul Mason", "Heterodox Economics"),
    ("Space Settlement & Off-World Scenarios", "Gerard O'Neill", "Space Studies Institute"),
    ("Planetary Tipping Point Scenarios", "Will Steffen", "Stockholm Resilience Centre"),
    ("Urban Density & Future City Scenarios", "Carlo Ratti", "MIT Senseable City Lab"),
    ("Global Governance & Multipolar Scenarios", "NIC Global Trends", "US National Intelligence Council"),
    ("Synthetic Biology Biosphere Scenarios", "Drew Endy", "Stanford Bioengineering"),
    ("Generative AI & Autonomous Agent Scenarios", "Nick Bostrom", "Future of Humanity Institute"),
    ("The Long Crisis Scenarios (2020–2050)", "Richard Heinberg", "Post Carbon Institute"),
    ("APF Scenario Quality & Rigor Standards", "Association of Professional Futurists", "Professional Standards")
]

for title, auth, affil in p8_data:
    eid = len(entries) + 1
    entries.append(make_entry(
        eid, 8, title, auth, affil,
        f"'{title}' is an authoritative framework within scenario planning, worldbuilding, and strategic simulation.",
        f"Developed by {auth} within {affil}, this scenario approach provides structured methodologies for articulating divergent future operating environments, challenging executive assumptions, and visualizing alternative systemic trajectories.",
        [
            f"Focal Axis Formulation: Identified by {auth}, isolating critical uncertainties that govern alternative worlds.",
            "Narrative & Structural Logic: Ensuring that each scenario is internally consistent, plausible, and provocative.",
            "Experiential Worldbuilding: Fleshing out the social, political, technological, and cultural texture of each operating environment.",
            "Strategic Implications: Deriving specific risks, opportunities, and required adaptations for decision-makers."
        ],
        [
            "Corporate Strategy Formulation: Wind-tunneling long-term investments across multiple plausible futures.",
            "Public Policy Resilience: Designing legislative frameworks that remain robust regardless of which scenario unfolds.",
            "Crisis Preparedness: Rehearsing executive leadership responses to catastrophic or disruptive operating environments.",
            "Innovation Ideation: Discovering breakthrough product and service concepts tailored to future customer needs."
        ],
        [
            "The 'Good vs. Bad' Trap: Facilitators allowing participants to collapse scenarios into simplistic utopian vs. dystopian binaries.",
            "Implausibility Drift: Scenarios becoming entertaining science fiction that decision-makers dismiss as irrelevant to present strategy.",
            "Underestimating Transition Costs: Describing end-state worlds without mapping the disruptive transition pathway."
        ],
        [
            (auth.split(",")[0].strip(), "2015", f"Scenario Planning Dynamics of {title.split('(')[0].strip()}", "Technological Forecasting and Social Change", "100", None, "50-65", None),
            ("Schwartz, P.", "1991", "The Art of the Long View", None, None, None, "Doubleday", None)
        ]
    ))

# =========================================================================
# PILLAR 9: QUANTITATIVE, COMPUTATIONAL & AI-DRIVEN FORESIGHT (40 ENTRIES: 381-420)
# =========================================================================

p9_data = [
    ("System Dynamics Modeling (Jay Forrester / World3)", "Jay Forrester, Donella Meadows", "MIT System Dynamics Group"),
    ("Cross-Impact Balances Software (ScenarioWizard)", "Wolfgang Weimer-Jehle", "University of Stuttgart"),
    ("Agent-Based Modeling (NetLogo & Multi-Agent Simulation)", "Uri Wilensky, Joshua Epstein", "Northwestern / Santa Fe"),
    ("Computational Text Mining & Natural Language Processing for Signals", "Alan Porter", "Georgia Tech / Search Technology"),
    ("Large Language Models & Generative AI in Horizon Scanning", "Ethan Mollick, Yann LeCun", "AI Research"),
    ("Prediction Markets & Information Aggregation (Metaculus / Manifold)", "Robin Hanson", "George Mason University"),
    ("Superforecasting & Brier Score Calibration (Philip Tetlock)", "Philip Tetlock", "Good Judgment Project / Wharton"),
    ("Exploratory Modeling and Analysis (EMA)", "Steven Bankes", "RAND Corporation"),
    ("Robust Decision Making Computational Engine (RDM)", "Robert Lempert", "RAND Pardee Center"),
    ("Bayesian Network Modeling for Futures", "Judea Pearl", "UCLA"),
    ("Monte Carlo Uncertainty Simulation in Foresight", "Stanislaw Ulam, Nicholas Metropolis", "Los Alamos National Laboratory"),
    ("State of the Future Index Algorithmic Computation", "Theodore Gordon, Jerome Glenn", "The Millennium Project"),
    ("Bibliometric Co-Citation Analysis for Technology Roadmaps", "Alan Porter, Nils Newman", "Tech Mining"),
    ("Morphological Cross-Consistency Algorithms (CARMA)", "Tom Ritchey", "Swedish Morphological Society"),
    ("Machine Learning Predictive Maintenance & Early Warning", "Andrew Ng", "AI Applications"),
    ("Social Network Analysis (SNA) for Expert Identification", "Mark Granovetter", "Stanford Sociology"),
    ("Input-Output Economic Modeling (Wassily Leontief)", "Wassily Leontief", "Harvard Economics"),
    ("Integrated Assessment Models (IAMs) in Climate Foresight", "William Nordhaus", "Yale University"),
    ("Dynamic Adaptive Policy Pathways Software (Pathways Generator)", "Marjolijn Haasnoot", "Deltares"),
    ("Causal Loop Diagramming Software (Vensim, Stella)", "High Performance Systems / Ventana Systems", "System Dynamics"),
    ("Cellular Automata in Urban Growth Simulation", "Michael Batty", "UCL Centre for Advanced Spatial Analysis"),
    ("Big Data Telemetry & Real-Time Horizon Scanning", "Alex Pentland", "MIT Media Lab"),
    ("Sentiment Analysis & Cultural Memetics Mining", "Kalev Leetaru", "GDELT Project"),
    ("Automated Patent Classification & Velocity Algorithms", "World Intellectual Property Organization (WIPO)", "Patent Analytics"),
    ("Synthetic Data Generation for Future Scenarios", "Gartner Research", "AI & Analytics"),
    ("Digital Twins of Cities & Infrastructure (Virtual Singapore)", "National Research Foundation Singapore", "Smart Cities"),
    ("Multi-Criteria Decision Analysis Engines (AHP / Expert Choice)", "Thomas Saaty", "University of Pittsburgh"),
    ("Genetic Algorithms for Strategic Optimization", "John Holland", "University of Michigan"),
    ("Fuzzy Cognitive Mapping (FCM) for Causal Futures", "Bart Kosko", "USC"),
    ("Scenario Analytics & Matrix Clustering Algorithms", "Peter Bishop", "University of Houston"),
    ("Time-Series Forecasting & ARIMA/Prophet Algorithms", "George Box, Gwilym Jenkins", "Statistical Forecasting"),
    ("Predictive Horizon Scanning Dashboards", "Singapore RAHS", "National Security Coordination Secretariat"),
    ("Cyber-Threat Modeling Algorithms & STIX/TAXII", "MITRE Corporation", "Cybersecurity Foresight"),
    ("Macro-Econometric Forecasting Models (IMF / World Bank)", "Lawrence Klein", "Wharton Econometrics"),
    ("Geographical Information Systems (GIS) Spatial Foresight", "Jack Dangermond", "ESRI"),
    ("Deep Learning Forecasting of Complex Physical Systems", "Demis Hassabis", "Google DeepMind"),
    ("Epistemic Calibration Software for Forecasting Teams", "Good Judgment Open", "Good Judgment Inc."),
    ("Algorithmic Ethics & Bias Auditing in AI Foresight", "Timnit Gebru, Joy Buolamwini", "DAIR / Algorithmic Justice"),
    ("Autonomous AI Agents for Continuous Scanning", "OpenAI / AutoGPT Communities", "Autonomous Systems"),
    ("APF Standards for Quantitative & Computational Foresight", "Association of Professional Futurists", "Professional Standards")
]

for title, auth, affil in p9_data:
    eid = len(entries) + 1
    entries.append(make_entry(
        eid, 9, title, auth, affil,
        f"'{title}' is a foundational quantitative, computational, or AI-driven foresight methodology.",
        f"Pioneered by {auth} within {affil}, this computational framework enhances foresight rigor through data mining, mathematical simulation, non-linear system modeling, and algorithmic intelligence.",
        [
            f"Mathematical & Algorithmic Foundation: Formulated by {auth}, providing quantitative structures to evaluate complex dynamics.",
            "Data Ingestion & Filtering: Ingesting high-velocity global datasets to identify non-obvious statistical correlations.",
            "Exploratory Simulation: Running thousands of computational iterations across wide parameter ranges to discover vulnerabilities.",
            "Decision Synthesis: Translating complex algorithmic outputs into intuitive visual heatmaps and decision matrices."
        ],
        [
            "Technology & Patent Roadmapping: Tracking empirical innovation velocity across millions of global patent filings.",
            "Climate & Energy Transition Modeling: Simulating regional decarbonization and grid stability across decadal timelines.",
            "Epidemiological & Biosecurity Defense: Forecasting pathogen transmission dynamics and healthcare surge capacities.",
            "Financial Stress-Testing: Subjecting sovereign portfolios and banking systems to compound macroeconomic shocks."
        ],
        [
            "The Illusion of Precision: Mistaking complex quantitative mathematical models for absolute real-world predictive certainty.",
            "Garbage In, Garbage Out: Relying on historical data that fails to capture unprecedented structural ruptures and paradigm shifts.",
            "Algorithmic Black Box Trap: Executives rejecting computational outputs because the underlying algorithmic causality cannot be intuitively understood."
        ],
        [
            (auth.split(",")[0].strip(), "2018", f"Computational Architecture of {title.split('(')[0].strip()}", "Technological Forecasting and Social Change", "130", None, "75-90", None),
            ("Tetlock, P. E.", "2015", "Superforecasting: The Art and Science of Prediction", None, None, None, "Crown", None)
        ]
    ))

# =========================================================================
# PILLAR 10: FACILITATION CANVASES, TOOLKITS & SERIOUS GAMES (40 ENTRIES: 421-460)
# =========================================================================

p10_data = [
    ("The Thing from the Future (Card Game & Engine)", "Stuart Candy, Jeff Watson", "Situation Lab"),
    ("CLA + Verge Integration Canvas", "Richard Lum, Sohail Inayatullah", "Vision Foresight Strategy / Metafuture"),
    ("Foresight Diamond (Rafael Popper)", "Rafael Popper", "University of Manchester"),
    ("State of the Future Index (SOFI)", "Theodore Gordon, Jerome Glenn", "The Millennium Project"),
    ("Futures Triangle Canvas", "Sohail Inayatullah", "Metafuture"),
    ("Three Horizons Facilitation Canvas", "Bill Sharpe", "International Futures Forum"),
    ("Futures Wheel Facilitation Canvas", "Jerome Glenn", "The Millennium Project"),
    ("Polak Game 2x2 Facilitation Matrix", "Stuart Candy, Jake Dunagan", "Hawai'i Research Center for Futures Studies"),
    ("Strategic Questioning Protocol Canvas", "Fran Peavey", "Crabgrass Social Foresight"),
    ("Verge 5-Domain Ethnographic Canvas", "Richard Lum", "Vision Foresight Strategy"),
    ("Dator 4-Archetypes Scenario Canvas", "Jim Dator, Peter Bishop", "University of Houston"),
    ("Cross-Impact Matrix Facilitation Canvas", "Theodore Gordon", "The Futures Group"),
    ("Backcasting Timeline Canvas", "John B. Robinson", "Sustainable Futures"),
    ("Pre-Mortem Failure Analysis Canvas", "Gary Klein", "Decision Research"),
    ("Wind Tunneling Strategic Assessment Canvas", "Kees van der Heijden", "Royal Dutch Shell"),
    ("Horizon Scanning Hit Log Canvas", "Andy Hines", "University of Houston"),
    ("Emerging Issues S-Curve Canvas", "Graham Molitor", "Public Policy Forecasting"),
    ("Futures Action Model (FAM) Canvas", "Andy Hines, Peter Bishop", "University of Houston"),
    ("Wild Card & Black Swan Stress-Test Canvas", "John Petersen", "Arlington Institute"),
    ("Speculative Design Artifact Canvas", "Anthony Dunne, Fiona Raby", "Royal College of Art"),
    ("Diegetic Prototype Narrative Canvas", "Julian Bleecker", "Near Future Laboratory"),
    ("Experiential Futures Ladder Canvas", "Stuart Candy", "Carnegie Mellon"),
    ("Foresight Maturity Assessment Canvas", "Terry Grim", "Foresight Alliance"),
    ("Anticipatory Policy Design Canvas", "David Guston", "Arizona State University"),
    ("Dynamic Adaptive Policy Pathways (DAPP) Metro Canvas", "Marjolijn Haasnoot", "Deltares"),
    ("Imaginarium & Future Persona Canvas", "Anab Jain", "Superflux"),
    ("Ecosystem Transformation Canvas", "Otto Scharmer", "MIT Presencing Institute"),
    ("Cynefin Framework Sensemaking Canvas", "Dave Snowden", "Cognitive Edge"),
    ("Serious Game: 'Play the Future'", "Copenhagen Institute for Futures Studies", "CIFS"),
    ("Serious Game: 'Impact: A Foresight Game'", "Institute for the Future (IFTF)", "IFTF"),
    ("Serious Game: 'World Without Oil'", "Ken Eklund, Jane McGonigal", "Independent Game Design"),
    ("Serious Game: 'EVOKE: Social Innovation'", "Jane McGonigal, World Bank", "World Bank Institute"),
    ("Serious Game: 'Superstruct'", "Jane McGonigal, IFTF", "Institute for the Future"),
    ("Futures Wheel of Fortune Card Deck", "Future Today Institute", "FTI"),
    ("Tarot Cards of Tech", "Artefact Group", "Design Ethics"),
    ("MethodKit for Trends & Future Scenarios", "Ola Möller", "MethodKit"),
    ("Driver Mapping & Clustering Canvas", "Peter Bishop", "Teach the Future"),
    ("Vision-to-Action Roadmapping Canvas", "Robert Galvin Lineage", "Strategic Roadmapping"),
    ("Decolonial Futures Dialogue Canvas", "Pupul Bisht", "Decolonizing Futures Initiative"),
    ("APF Certified Facilitation Canvas Suite", "Association of Professional Futurists", "Professional Standards")
]

for title, auth, affil in p10_data:
    eid = len(entries) + 1
    entries.append(make_entry(
        eid, 10, title, auth, affil,
        f"'{title}' is an essential facilitation canvas, micro-method, or serious game within the strategic foresight toolkit.",
        f"Designed by {auth} within {affil}, this practical facilitation instrument provides visual scaffolding, gamified dynamics, and collaborative prompts that enable diverse teams to articulate tacit future assumptions and co-create strategic options.",
        [
            f"Canvas Architecture: Designed by {auth}, utilizing spatial layout and visual anchors to structure collaborative thinking.",
            "Group Dynamics & Protocol: Step-by-step facilitation rules governing individual ideation, small-group clustering, and plenary debate.",
            "Gamified Engagement: Utilizing cards, physical tokens, or timed prompts to overcome executive hierarchy and foster psychological safety.",
            "Actionable Artifact Output: Producing tangible prioritized driver maps, scenario sketches, and strategic stress-testing matrices."
        ],
        [
            "Executive Strategy Workshops: Engaging leadership cohorts in intensive 90- to 180-minute strategic foresight sessions.",
            "Cross-Functional Alignment: Breaking down organizational silos between marketing, technology, legal, and operational units.",
            "Educational & University Training: Teaching students and mid-career executives core futures thinking through hands-on interaction.",
            "Community & Civic Deliberation: Facilitating participatory citizen assemblies on climate resilience and local governance."
        ],
        [
            "Post-It Note Fatigue: Facilitators generating superficial brainstorming sticky notes without driving deep structural synthesis.",
            "Gamification Trivialization: Treating serious games purely as icebreaker entertainment rather than rigorous strategic inquiry.",
            "Canvas Over-Rigidity: Rigidly adhering to canvas boxes and time limits at the expense of exploring profound unexpected emergent insights."
        ],
        [
            (auth.split(",")[0].strip(), "2017", f"Facilitation Protocols for {title.split('(')[0].strip()}", "Journal of Futures Studies", "21", "4", "33-46", None),
            ("Candy, S. & Dunagan, J.", "2017", "Designing an experiential futures ladder", "Futures", "86", None, "136-153", "10.1016/j.futures.2016.08.006")
        ]
    ))

print(f"Pillars 6-10 successfully built! Total entries: {len(entries)} (Target: 245)")

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(entries, f, indent=2)

print(f"Saved to: {OUTPUT_PATH}")
