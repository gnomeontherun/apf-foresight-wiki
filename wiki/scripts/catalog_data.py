# catalog_data.py - Master Catalog Definition for 457 APF Foresight Wiki Articles

CATALOG = [
    # ---------------------------------------------------------
    # Pillar 1: Foundations, Epistemology & Core Concepts (1-30)
    # ---------------------------------------------------------
    {
        "id": 1,
        "pillar": "01_foundations_and_epistemology",
        "title": "Strategic Foresight (Discipline Overview)",
        "type": "concept",
        "competency": "Framing",
        "domain": "Foundations of Futures Studies",
        "theorists": "Slaughter, Inayatullah, Bell, Dator",
        "era": "Post-WWII to Present",
        "app": "Strategic decision-making, organizational resilience, public policy",
        "summary": "Strategic foresight is the structured, systematic exploration of multiple plausible futures to inform current decision-making, foster strategic agility, and prevent organizational obsolescence.",
        "details": "Unlike predictive forecasting, strategic foresight does not attempt to pinpoint a single deterministic future. Instead, it expands the cone of possibility, questioning core assumptions and illuminating emerging disruptions.",
        "citations": [
            ("Slaughter, R. A.", "1995", "The Knowledge Base of Futures Studies", "Futures", "27", "2", "117-124", "10.1016/0016-3287(95)00001-A"),
            ("Bell, W.", "1997", "Foundations of Futures Studies: Human Science for a New Era", None, None, None, "Transaction Publishers", None)
        ]
    },
    {
        "id": 2,
        "pillar": "01_foundations_and_epistemology",
        "title": "Futures Studies (History & Evolution)",
        "type": "concept",
        "competency": "Framing",
        "domain": "Academic Lineage of Futures Studies",
        "theorists": "Ossip Flechtheim, Bertrand de Jouvenel, Fred Polak",
        "era": "1940s–Present",
        "app": "Epistemological framing and academic grounding",
        "summary": "Futures Studies traces its roots from early civilizational conjecture to post-WWII military and technological planning (RAND), expanding in the 1960s and 70s into humanistic, social, and post-structural traditions.",
        "details": "The discipline evolved through three distinct waves: first, the empirical/positivist wave (1940s-60s); second, the social/humanistic wave (1970s-80s); and third, the critical and pluriversal wave (1990s-present).",
        "citations": [
            ("Flechtheim, O. K.", "1966", "History and Futurology", None, None, None, "Verlag Anton Hain", None),
            ("Dator, J.", "2002", "Advancing Futures: Futures Studies in Higher Education", None, None, None, "Praeger", None)
        ]
    },
    {
        "id": 3,
        "pillar": "01_foundations_and_epistemology",
        "title": "The Futures Cone (Plausible, Possible, Probable, Preferable)",
        "type": "concept",
        "competency": "Framing",
        "domain": "Visual Taxonomy of Alternative Futures",
        "theorists": "Charles Taylor, Trevor Hancock, Joseph Voros",
        "era": "1990s–Present",
        "app": "Workshop scoping, horizon delineation, uncertainty mapping",
        "summary": "A geometric visualization depicting time expanding outward from the present into projected, probable, plausible, possible, and preposterous futures, intersected by normative (preferable) futures.",
        "details": "The Futures Cone serves as a primary cognitive scaffolding tool in foresight workshops, demonstrating to stakeholders that the future is not a predetermined line but an expanding space of possibilities.",
        "citations": [
            ("Voros, J.", "2003", "A generic foresight process framework", "Foresight", "5", "3", "10-21", "10.1108/14636680310698379"),
            ("Hancock, T. & Bezold, C.", "1994", "Possible futures, preferable futures", "Healthcare Forum Journal", "37", "2", "23-29", None)
        ]
    },
    {
        "id": 4,
        "pillar": "01_foundations_and_epistemology",
        "title": "Anticipatory Governance",
        "type": "concept",
        "competency": "Leading",
        "domain": "Public Policy & Strategic Statecraft",
        "theorists": "David Guston, Leon Fuerth, Cat Tully",
        "era": "2000s–Present",
        "app": "Government foresight units, regulatory policy, parliamentary oversight",
        "summary": "A governance framework that systematically incorporates foresight, horizon scanning, and feedback loops into policy design, budgeting, and regulation before crises occur.",
        "details": "Anticipatory governance bridges the gap between long-term strategic anticipation and short-term political cycles, embedding institutional mechanisms such as Finland's Committee for the Future and the Singapore CSF.",
        "citations": [
            ("Guston, D. H.", "2014", "Understanding 'anticipatory governance'", "Social Studies of Science", "44", "2", "218-242", "10.1177/0306312713508669"),
            ("Fuerth, L. S.", "2012", "Anticipatory Governance: Practical Approaches for Emerging Challenges", None, None, None, "National Defense University Press", None)
        ]
    },
    {
        "id": 5,
        "pillar": "01_foundations_and_epistemology",
        "title": "Post-Normal Times (Ziauddin Sardar)",
        "type": "concept",
        "competency": "Framing",
        "domain": "Complexity & Contemporary Epistemology",
        "theorists": "Ziauddin Sardar, Jordi Serra, John Sweeney",
        "era": "2010s–Present",
        "app": "Navigating systemic volatility, chaos, and institutional breakdown",
        "summary": "An epistemic theory describing an in-between era where orthodox frameworks fail, confident prediction is impossible, and phenomena are characterized by the 3 Cs: Complexity, Chaos, and Contradictions.",
        "details": "Post-Normal Times (PNT) challenges traditional linear forecasting by highlighting how the speed of change and mutual ignorance render standard risk management paradigms obsolete.",
        "citations": [
            ("Sardar, Z.", "2010", "Welcome to postnormal times", "Futures", "42", "5", "435-444", "10.1016/j.futures.2009.11.028"),
            ("Sardar, Z. & Sweeney, J. A.", "2016", "The Three Tomorrows of Postnormal Times", "Futures", "75", None, "1-13", "10.1016/j.futures.2015.10.004")
        ]
    },
    {
        "id": 6,
        "pillar": "01_foundations_and_epistemology",
        "title": "Futures Literacy (Riel Miller / UNESCO)",
        "type": "concept",
        "competency": "Leading",
        "domain": "Cognitive Capability & Anticipatory Action",
        "theorists": "Riel Miller, UNESCO Foresight Team",
        "era": "2010s–Present",
        "app": "Global education, community workshops, Futures Literacy Laboratories",
        "summary": "An essential 21st-century capability enabling individuals and groups to understand the role of the future in what they see and do, overcoming unconscious anticipatory assumptions.",
        "details": "Rather than treating the future as an empty vessel to be colonised or predicted, Futures Literacy trains participants to use the future as an epistemic mirror, diversifying why and how they anticipate.",
        "citations": [
            ("Miller, R.", "2018", "Transforming the Future: Anticipation in the 21st Century", None, None, None, "Routledge & UNESCO", "10.4324/9781351047999")
        ]
    },
    {
        "id": 7,
        "pillar": "01_foundations_and_epistemology",
        "title": "Second-Order and Third-Order Consequences",
        "type": "concept",
        "competency": "Framing",
        "domain": "Systems Thinking & Cascading Impact Analysis",
        "theorists": "Garrett Hardin, Jerome Glenn, Howard Gardner",
        "era": "1960s–Present",
        "app": "Futures Wheel, policy stress-testing, unintended consequences audits",
        "summary": "The systemic ripple effects that occur after an initial disruption or decision, where direct reactions produce secondary feedbacks and tertiary systemic transformations.",
        "details": "Most failures in technological deployment and strategic policy arise not from primary effects, but from unexpected second-order behavioral adaptations and third-order institutional shifts.",
        "citations": [
            ("Hardin, G.", "1968", "The Tragedy of the Commons", "Science", "162", "3859", "1243-1248", "10.1126/science.162.3859.1243"),
            ("Glenn, J. C.", "2009", "The Futures Wheel", "Futures Research Methodology Version 3.0", None, None, "The Millennium Project", None)
        ]
    },
    {
        "id": 8,
        "pillar": "01_foundations_and_epistemology",
        "title": "Temporal Depth & Long-Termism",
        "type": "concept",
        "competency": "Framing",
        "domain": "Temporal Epistemology & Deep Time",
        "theorists": "Richard Slaughter, Roman Krznaric, Stewart Brand",
        "era": "1980s–Present",
        "app": "Strategic horizon expansion, intergenerational sustainability",
        "summary": "The cognitive and cultural capacity to expand one's operational time horizon, integrating past historical trajectories with multi-decade and multi-century future horizons.",
        "details": "Modern hyper-capitalism and digital acceleration contract temporal depth into quarterly earnings cycles and 24-hour news feeds, making intentional temporal depth a vital counter-balance.",
        "citations": [
            ("Slaughter, R. A.", "1989", "Cultural reconstruction in the post-modern world", "Futures", "21", "3", "255-270", "10.1016/0016-3287(89)90004-9"),
            ("Krznaric, R.", "2020", "The Good Ancestor: A Radical Prescription for Long-Term Thinking", None, None, None, "The Experiment", None)
        ]
    },
    {
        "id": 9,
        "pillar": "01_foundations_and_epistemology",
        "title": "Plurality of Futures (Alternative Futures)",
        "type": "concept",
        "competency": "Futuring",
        "domain": "Foundational Ontology of Foresight",
        "theorists": "Jim Dator, Bertrand de Jouvenel, Eleonora Masini",
        "era": "1960s–Present",
        "app": "Scenario planning, challenging determinism, policy diversity",
        "summary": "The fundamental axiom that 'the future' does not exist as a singular, pre-determined destination, but as a plural field of alternative possibilities shaped by human choices and system dynamics.",
        "details": "Rejecting singular prophetic or technological determinism, the concept of alternative futures liberates organizations to prepare for divergent operating environments simultaneously.",
        "citations": [
            ("Dator, J.", "1993", "From buildings to cultures: The Hawaii futures studies programme", "Futures", "25", "10", "1061-1069", "10.1016/0016-3287(93)90074-S"),
            ("de Jouvenel, B.", "1967", "The Art of Conjecture", None, None, None, "Basic Books", None)
        ]
    },
    {
        "id": 10,
        "pillar": "01_foundations_and_epistemology",
        "title": "The Polak Dilemma / Images of the Future (Fred Polak)",
        "type": "concept",
        "competency": "Framing",
        "domain": "Sociological Foresight & Civilizational Dynamics",
        "theorists": "Fred Polak, Elise Boulding",
        "era": "1950s–1970s",
        "app": "Cultural visioning, community empowerment, civilizational renewal",
        "summary": "The sociological principle formulated by Dutch sociologist Fred Polak asserting that the rise and fall of civilizations is directly tied to the potency, optimism, and nobility of their collective images of the future.",
        "details": "When a society loses its ability to imagine an inspiring, positive future, it enters cynicism, decay, and cultural stagnation; vibrant images of the future act as the magnetic pull that draws civilization forward.",
        "citations": [
            ("Polak, F.", "1973", "The Image of the Future (Trans. Elise Boulding)", None, None, None, "Elsevier Scientific Publishing", None)
        ]
    }
]

print(f"Loaded initial core catalog items: {len(CATALOG)}")
