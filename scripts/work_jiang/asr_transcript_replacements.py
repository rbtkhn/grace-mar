"""Phrase and token replacements for Predictive History ASR transcripts.

**SSOT split:** This file is the single source of truth for *replacement content*
(the phrase tables). *Which tiers run for which lecture series* lives in
``asr_light_clean.py`` (e.g. civilization vs geo-strategy vs common-only).

Edit this file when systematic mis-hearings show up on new ingests.
Replacement order is applied longest-first within each tier to avoid
partial matches (handled by the normalizer).

**Civilization** tier includes aggressive fixes (e.g. “thieves” → “Thebes”) that
must NOT run on Geo-Strategy transcripts — use series detection from filename.
"""

from __future__ import annotations

# Safe on any series (IR, geography, generic English glitches).
COMMON_REPLACEMENTS: list[tuple[str, str]] = [
    # Long / phrase first
    ("Memnon of RADS", "Memnon of Rhodes"),
    ("men of RADS", "Memnon of Rhodes"),
    ("men of Road set sail", "Memnon of Rhodes set sail"),
    ("men of roads", "Memnon of Rhodes"),
    ("men of Rose", "Memnon of Rhodes"),
    ("men of world set sail", "Memnon of Rhodes set sail"),
    ("when man of Rose Dies", "when Memnon of Rhodes dies"),
    ("Mena roads", "Memnon of Rhodes"),
    ("Men on of roads", "Memnon of Rhodes"),
    ("Menan of RADS", "Memnon of Rhodes"),
    ("what men Road proposes", "what Memnon proposes"),
    ("Cleopatra uidic", "Cleopatra Eurydice"),
    ("granticus", "Granicus"),
    ("battle of granticus", "battle of Granicus"),
    ("Battle of granticus", "Battle of Granicus"),
    ("grakis", "Granicus"),
    ("guacola", "Gaugamela"),
    ("gamola", "Gaugamela"),
    ("guaga", "Gaugamela"),
    ("guala", "Gaugamela"),
    ("Battle of Isis ", "Battle of Issus "),
    ("battles Isis ", "battles Issus "),
    ("Isis and and", "Issus and"),
    ("both battles Isis ", "both battles Issus "),
    ("cus black clus the black", "Cleitus the Black"),
    ("C is a black", "Cleitus the Black"),
    ("C as of black", "Cleitus the Black"),
    ("clus a black", "Cleitus the Black"),
    ("ctis of black", "Cleitus the Black"),
    ("cl of black", "Cleitus the Black"),
    ("class of black", "Cleitus the Black"),
    ("paronan", "Parmenion"),
    ("permon", "Parmenion"),
    ("parmonian", "Parmenion"),
    ("paronian", "Parmenion"),
    ("ponan", "Parmenion"),
    ("P pan", "Parmenion"),
    ("harmonia", "Parmenion"),
    ("olympas", "Olympias"),
    ("olympius", "Olympias"),
    ("EDC and her daughter", "Eurydice and her daughter"),
    ("your DC and Phillip", "Eurydice and Philip"),
    ("Attlas", "Attalus"),
    ("Theus do now", "Darius do now"),
    ("what does Theus", "what does Darius"),
    ("Moses forces", "most forces"),
    ("tamland", "Tamerlane"),
    ("dynastes", "dynasts"),
    ("isolate Oasis", "Siwa Oasis"),
    (" a syesis", " syncretism"),
    ("33 oce ", "330 BCE "),
    ("33c uh BCE", "336 BCE"),
    ("33c uh 336", "336"),
    ("gangas Khan", "Genghis Khan"),
    (" napan ", " Napoleon "),
    ("anal Tools", "analytical tools"),
    ("anal model", "analytical model"),
    ("anical model", "analytical model"),
    ("an antical model", "an analytical model"),
    ("Crow history", "through history"),
    ("calvalry", "cavalry"),
    ("calary", "cavalry"),
    ("SAT trops", "satraps"),
    ("SAT traps", "satraps"),
    ("Sops are", "satraps are"),
    ("stup's arm", "satrap's arm"),
    ("One S was about", "One satrap was about"),
    ("Eternal descent", "internal dissent"),
    ("self C's problem", "South Korea's problem"),
    ("self Korea", "South Korea"),
    ("self create", "South Korea"),
    ("F trility rate", "fertility rate"),
    ("low parate", "low birthrate"),
    ("he was a keymaker", "he was a kingmaker"),
    ("F lius Fus", "Philotas"),
    ("Phil fetas", "Philotas"),
    ("fites", "Philotas"),
    ("Mason Army", "Macedonian Army"),
    ("masonian", "Macedonian"),
    ("maonan", "Macedonian"),
    ("323 AER dies", "323 Alexander dies"),
    ("temperature Sun", "Iolaus"),
    ("this c a problem", "this created a problem"),
    ("caran mix", "Parmenion"),
    ("faithful decision", "fateful decision"),
    ("yria which is in North", "Illyria which is in North"),
    ("hoplight", "hoplite"),
    ("deop discipline", "develop discipline"),
    ("weren fighting", "weren't fighting"),
    ("trouble armies", "tribal armies"),
    ("a trial Army", "a tribal army"),
    ("darus ", "Darius "),
    ("darus commits", "Darius commits"),
    (" the persons flee", " the Persians flee"),
    ("spart to rebel", "Sparta to rebel"),
    (" spart ", " Sparta "),
    ("PHX", "phalanx"),
    # tokens
    ("permania", "Parmenion"),
    # --- Geo-strategy audit 2026-03-24 (common tier: safe for all series) ---
    # Strait of Hormuz (geo-01, -04, -07, -08, -13, -14)
    ("the trade of humus", "the Strait of Hormuz"),
    ("the street of Humus", "the Strait of Hormuz"),
    ("the straight of humus", "the Strait of Hormuz"),
    ("straight of humus", "Strait of Hormuz"),
    ("strait of homus", "Strait of Hormuz"),
    ("street of Humus", "Strait of Hormuz"),
    # Qasem Soleimani (geo-01, -04, -07, -08)
    ("Kasam salamani", "Qasem Soleimani"),
    ("Kasam salamini", "Qasem Soleimani"),
    ("salamani", "Soleimani"),
    ("solomani", "Soleimani"),
    ("salamini", "Soleimani"),
    # Netanyahu (geo-05, -08, -15, -17)
    ("Nanyahu", "Netanyahu"),
    ("Nan yahu", "Netanyahu"),
    ("nanyu", "Netanyahu"),
    ("natany", "Netanyahu"),
    ("Natanya", "Netanyahu"),
    # Hezbollah (geo-01, -04, -07)
    ("hesah", "Hezbollah"),
    ("heson", "Hezbollah"),
    # Houthis / Yemen (geo-01, -07)
    ("hthis in Yaman", "Houthis in Yemen"),
    ("hoovies in y man", "Houthis in Yemen"),
    ("hufi", "Houthi"),
    # Bretton Woods (geo-03, -10)
    ("Breton Woods", "Bretton Woods"),
    ("Brendon woods", "Bretton Woods"),
    ("Bron Woods", "Bretton Woods"),
    # Ayatollah (geo-14, -15)
    ("Yatollah", "Ayatollah"),
    ("Aatollah", "Ayatollah"),
    ("Alatollah", "Ayatollah"),
    ("Alatia", "Ayatollah"),
    # Khamenei (geo-07)
    ("mosta Kami", "Mojtaba Khamenei"),
    ("mosab kamani", "Mojtaba Khamenei"),
    ("MOBA Kami", "Mojtaba Khamenei"),
    ("Musta Kami", "Mojtaba Khamenei"),
    ("maaba kamani", "Mojtaba Khamenei"),
    ("kamani", "Khamenei"),
    ("camani", "Khamenei"),
    # Zelenskyy (geo-08)
    ("zalinski", "Zelenskyy"),
    ("zilinski", "Zelenskyy"),
    ("zinsky", "Zelenskyy"),
    # Zoroastrianism (geo-15, -16)
    ("Zorashinism", "Zoroastrianism"),
    ("Zorastronism", "Zoroastrianism"),
    # messianic (geo-15, -17)
    ("misinic", "messianic"),
    ("mezanite", "messianic"),
    ("mezzating", "messianic"),
    # Nikki Haley (geo-05, -08, -11)
    ("Niki Hill hilly", "Nikki Haley"),
    ("niiki heli", "Nikki Haley"),
    ("Nikki Hy", "Nikki Haley"),
    ("niiki Hy", "Nikki Haley"),
    # Rumsfeld / Wolfowitz (geo-06)
    ("Donald russfield", "Donald Rumsfeld"),
    ("Ron field", "Rumsfeld"),
    ("Paul wolitz", "Paul Wolfowitz"),
    ("Wolford", "Wolfowitz"),
    # de-Baathification (geo-13 — only unambiguous garble form)
    ("debuffification", "de-Baathification"),
    # Ebrahim Raisi (geo-07)
    ("Ibraham razy", "Ebrahim Raisi"),
    ("Ibraham Ry", "Ebrahim Raisi"),
    # Mahsa Amini (geo-07)
    ("masah ameni", "Mahsa Amini"),
    # Other proper names (multi-episode)
    ("Sheldon elderson", "Sheldon Adelson"),
    ("sandel elderson", "Sheldon Adelson"),
    ("Jamal Hashi", "Jamal Khashoggi"),
    ("jerk Kushner", "Jared Kushner"),
    ("the Mckender thesis", "the Mackinder thesis"),
    ("Barbarosa", "Barbarossa"),
    ("bar Barosa", "Barbarossa"),
    ("Constantinopole", "Constantinople"),
    ("Consipole", "Constantinople"),
    ("Caranopole", "Constantinople"),
    ("Haga Sophia", "Hagia Sophia"),
    ("Aragon of Turkey", "Erdoğan of Turkey"),
    ("Frederick Nichi", "Friedrich Nietzsche"),
    ("reproachment", "rapprochement"),
    ("encircumment", "encirclement"),
    ("synretatization", "syncretization"),
    ("Neestoran Christianity", "Nestorian Christianity"),
    ("hijgemony", "hegemony"),
    ("Leo Toy Story", "Leo Tolstoy"),
    ("John Maynor kings", "John Maynard Keynes"),
    ("Libby the Roman historian", "Livy the Roman historian"),
    ("Gerald art Ford", "Gerald R. Ford"),
    # Homophones (geo-strategy register)
    ("ear defense", "air defense"),
    ("ear power", "air power"),
    ("ear Supremacy", "air supremacy"),
    ("ear supery", "air supremacy"),
    ("military insulations", "military installations"),
    ("exclusion dominance", "escalation dominance"),
    ("possible deniability", "plausible deniability"),
    ("esquetology", "eschatology"),
]

# Greek / ancient history strand only — run when filename matches civilization-*.md
CIVILIZATION_REPLACEMENTS: list[tuple[str, str]] = [
    # --- Bug fix 2026-03-24: the old ("thians","Thebans") rule was too aggressive ---
    # It matched inside Parthians, Corinthians, Scythians, etc. Removed below;
    # specific patterns added instead. fix_civilization_thieves handles thieves→Thebes.
    ("parthians", "Parthians"),
    # --- Civilization audit 2026-03-24: recurring proper names ---
    # Brutus (civ-16, -27) — "Buddhist" / "Buddhas" is a devastating ASR swap
    ("Lucius junus Buddhas", "Lucius Junius Brutus"),
    ("Lucius Junius Buddhas", "Lucius Junius Brutus"),
    ("Marcus buddhis", "Marcus Brutus"),
    ("Marcus buddist", "Marcus Brutus"),
    ("Marcus Buddhas", "Marcus Brutus"),
    ("Decimus buddhis", "Decimus Brutus"),
    ("Decimus Buddhas", "Decimus Brutus"),
    # Cassius (civ-16)
    ("casassus", "Cassius"),
    ("Casas", "Cassius"),
    # Cicero (civ-16)
    ("cisero", "Cicero"),
    ("ciso", "Cicero"),
    ("Cyro", "Cicero"),
    # Sulla (civ-16)
    ("Sola", "Sulla"),
    # Agrippa (civ-16)
    ("agria", "Agrippa"),
    ("AG gria", "Agrippa"),
    # Lepidus (civ-16)
    ("leopardus", "Lepidus"),
    ("lepus", "Lepidus"),
    # Aeneid / Aeneas (civ-17) — highest-frequency garbles
    ("the inad", "the Aeneid"),
    ("the India", "the Aeneid"),
    # Dido (civ-17)
    ("queen ditto", "queen Dido"),
    # Etruscans (civ-32)
    ("truskin", "Etruscan"),
    ("ausans", "Etruscans"),
    # Pyrrhus (civ-32)
    ("pyrus", "Pyrrhus"),
    ("pyus", "Pyrrhus"),
    # Sejanus (civ-32)
    ("sanus", "Sejanus"),
    ("sanis", "Sejanus"),
    ("shanus", "Sejanus"),
    # Germanicus (civ-32)
    ("jericus", "Germanicus"),
    # Praetorian Guard (civ-32)
    ("ptan guard", "Praetorian Guard"),
    ("patan guard", "Praetorian Guard"),
    # Caracalla (civ-32)
    ("kakala", "Caracalla"),
    ("car kala", "Caracalla"),
    # Romulus Augustulus (civ-32)
    ("Romus Augustus", "Romulus Augustulus"),
    # Diocletian (civ-33)
    ("de Clan", "Diocletian"),
    ("dark Clan", "Diocletian"),
    # Belisarius (civ-33)
    ("bis serus", "Belisarius"),
    # Theodosian (civ-33)
    ("FI Doan walls", "Theodosian walls"),
    ("fi Doan", "Theodosian"),
    # Ottoman (civ-33)
    ("aroman Turks", "Ottoman Turks"),
    # Tarquinius Superbus (civ-33)
    ("tanius Superbus", "Tarquinius Superbus"),
    # Voltaire (civ-34)
    ("voler", "Voltaire"),
    # Carolingian (civ-34, -35)
    ("Carolian", "Carolingian"),
    ("coral legian Empire", "Carolingian Empire"),
    ("Corian Empire", "Carolingian Empire"),
    # Aachen (civ-34)
    ("Akin Cathedral", "Aachen Cathedral"),
    # Nicene (civ-34)
    ("nine creed", "Nicene Creed"),
    # Magyars (civ-35)
    ("mag yards", "Magyars"),
    # Novgorod (civ-35)
    ("novag grad", "Novgorod"),
    ("novad", "Novgorod"),
    # Scipio Africanus (civ-35)
    ("cpio africanist", "Scipio Africanus"),
    # Umayyad (civ-37)
    ("omaya calipat", "Umayyad Caliphate"),
    ("omantic calat", "Umayyad Caliphate"),
    # Sumerians (civ-19) — common-tier safe since used across series
    ("Samarian", "Sumerian"),
    ("samarians", "Sumerians"),
    # Sargon of Akkad (civ-19)
    ("Saron of aad", "Sargon of Akkad"),
    ("Saron the great", "Sargon the Great"),
    # Enkidu (civ-19)
    ("eadu", "Enkidu"),
    ("anadu", "Enkidu"),
    ("enadu", "Enkidu"),
    # Marduk (civ-19)
    ("mardock", "Marduk"),
    # cuneiform (civ-19)
    ("Kun form", "cuneiform"),
    ("kuna form", "cuneiform"),
    # Bathsheba (civ-21)
    ("basba", "Bathsheba"),
    ("basiba", "Bathsheba"),
    ("bisha", "Bathsheba"),
    # Gnosticism (civ-24) — "narcissism" is a real word, only fix in compound
    # Sadducees (civ-24)
    ("seduces", "Sadducees"),
    # Nicaea (civ-25)
    ("nessia", "Nicaea"),
    # Theodosius (civ-25)
    ("feel dois", "Theodosius"),
    # Charlemagne (civ-27)
    ("Charlamagne", "Charlemagne"),
    # Manichaeism (civ-27)
    ("manism", "Manichaeism"),
    # Khufu (civ-18)
    ("curfew", "Khufu"),
    # Imhotep (civ-18)
    ("imot", "Imhotep"),
    # Egyptologists (civ-18)
    ("otologists", "Egyptologists"),
    # Cortés (civ-44)
    ("Hernand Cortez", "Hernán Cortés"),
    ("conquestadors", "conquistadors"),
    # Crimean War (civ-46+) — "Korean war" in 19th-century context
    ("Korean war", "Crimean War"),
    # Ibn Fadlan (civ-36)
    ("ibben fadlin", "Ibn Fadlan"),
    ("ibben Fallon", "Ibn Fadlan"),
    # Paul Gauguin (civ-36)
    ("Paul Goan", "Paul Gauguin"),
    ("Paul go gain", "Paul Gauguin"),
    # Fukuyama (civ-27, -31)
    ("fukayama", "Fukuyama"),
    # Thomas Piketty (civ-31)
    ("tominus py", "Thomas Piketty"),
    # iconoclasm (civ-34)
    ("iconic clasm", "iconoclasm"),
    # eudaimonia (shared)
    ("udonia", "eudaimonia"),
    ("Sacred Band of Thieves", "Sacred Band of Thebes"),
    ("sacred Band of Thieves", "Sacred Band of Thebes"),
    ("sacred ban of Thieves", "Sacred Band of Thebes"),
    ("sacred Ben of Thieves", "Sacred Band of Thebes"),
    ("the SEC B thieves", "the Sacred Band"),
    ("SEC B thieves", "Sacred Band"),
    ("Battle of Tonia Tania", "Battle of Chaeronea"),
    ("battle of Sheria", "battle of Chaeronea"),
    ("so in Tania", "at Chaeronea"),
    (" in Tania ", " at Chaeronea "),
    ("palan war", "Peloponnesian War"),
    ("pelian war", "Peloponnesian War"),
    ("theevans", "Thebans"),
    (" thians ", " Thebans "),
    (" thians,", " Thebans,"),
    (" thians.", " Thebans."),
    ("the thians", "the Thebans"),
    ("primarily uh by a\nthe great", "primarily uh by Alexander the Great"),
    ("how did a the great", "how did Alexander the Great"),
    ("ex ex the great", "Alexander the Great"),
    ("macedone", "Macedon"),
    ("kingdom of ma Macedonia", "kingdom of Macedonia"),
    ("ma Macedonia", "Macedonia"),
    ("kingdom of phas", "kingdom of Paeonia"),
    ("then you havea over here", "then you have Epirus over here"),
    ("place called FIS", "place called Thessaly"),
    ("ayia attacked", "Illyria attacked"),
    ("Army th attacked", "Army Thebes attacked"),
    ("p par Monon parmenion", "Parmenion"),
    ("that permanon would", "that Parmenion would"),
    ("trusted p parmenion", "trusted Parmenion"),
    ("permanon would", "Parmenion would"),
    ("region okay", "regent okay"),
    ("became region", "became regent"),
    ("as region", "as regent"),
    ("the phic ", "the phalanx "),
    ("the phic breaks", "the phalanx breaks"),
    ("to the phic", "to the phalanx"),
    ("changes to the phic", "changes to the phalanx"),
    ("the Finks", "the phalanx"),
    ("phenx", "phalanx"),
    ("horation", "horsemen"),
    (" and ACC ", " and cavalry "),
    ("action of the great", "Alexander the Great"),
    ("in here a the Great", "Alexander the Great"),
    ("C all Persia", "conquer all Persia"),
    ("mstone", "Macedonian"),
    ("macons", "Macedonians"),
    ("madon", "Macedon"),
    ("maedon", "Macedon"),
    ("controlling Mason", "controlling Macedon"),
    ("philli II", "Philip II"),
    (" philli ", " Philip "),
    ("BC philli ", "BC Philip "),
    ("Phil philli", "Philip"),
    ("shooted", "treated"),
    ("roades", "roads"),
    ("kingom", "kingdom"),
    ("multip okay", "multiple okay"),
    ("amphibolis", "Amphipolis"),
    # Remaining “thieves” → Thebes: handled in asr_light_clean.fix_civilization_thieves
]
