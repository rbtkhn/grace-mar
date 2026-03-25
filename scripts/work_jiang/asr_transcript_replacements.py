"""Phrase and token replacements for Predictive History ASR transcripts.

**SSOT split:** This file is the single source of truth for *replacement content*
(the phrase tables). *Which tiers run for which lecture series* lives in
``asr_light_clean.py`` (civilization vs geo-strategy vs secret-history vs game-theory vs great-books vs common-only).

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
    ("Zorashianism", "Zoroastrianism"),
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
    # --- Secret History audit 2026-03-24 (common tier: safe for all series) ---
    # Immanuel Kant (SH01, SH04)
    ("Emmanuel Kant", "Immanuel Kant"),
    ("Emanuel Kant", "Immanuel Kant"),
    # Oswald Spengler (SH02)
    ("Oswalt Spangler", "Oswald Spengler"),
    ("Oswald Spangler", "Oswald Spengler"),
    # Thomas Piketty (SH02)
    ("Thomas Pikid Pikid", "Thomas Piketty"),
    ("Pikody", "Piketty"),
    # Hegel (SH04)
    ("Frederick Hegel", "Friedrich Hegel"),
    ("Heggo", "Hegel"),
    ("Hego", "Hegel"),
    # Dante (SH04)
    ("Dantain", "Dante"),
    # Leonidas (SH04)
    ("Leonitis", "Leonidas"),
    # Thermopylae (SH04)
    ("Thermopily", "Thermopylae"),
    # Phoenicians (SH04)
    ("phoenetians", "Phoenicians"),
    ("Infineticians", "Phoenicians"),
    # Carthaginians (SH04)
    ("constant genians", "Carthaginians"),
    # Calhoun (SH02)
    ("Cahoun", "Calhoun"),
    # Dionysus (SH01)
    ("Dianesis", "Dionysus"),
    # Oedipus (SH01)
    ("Edypus", "Oedipus"),
    # Noumena (SH01) — "nomina" skipped (valid Latin word)
    ("the nomena", "the noumena"),
    # Eudaimonia (SH01) — "udonia" in civ tier; these longer forms safe for common
    ("udeimmonia", "eudaimonia"),
    ("Youmonia", "eudaimonia"),
    ("ulmonia", "eudaimonia"),
    # Monotheism / monotheistic (SH01, SH02, SH05)
    ("montheistic", "monotheistic"),
    ("montheism", "monotheism"),
    ("monetism", "monotheism"),
    # Polytheistic / monotheistic — ASR "polyphasic"/"monophasic" are real words,
    # so use phrase context; "polyphysic"/"politistic" are not real words
    ("three great monophasic religions", "three great monotheistic religions"),
    ("the polyphasic system", "the polytheistic system"),
    ("polyphysic", "polytheistic"),
    ("politistic", "polytheistic"),
    # Gnosticism (SH04)
    ("Nostism", "Gnosticism"),
    # Synchronicity (SH04)
    ("synchronosity", "synchronicity"),
    # Meritocratic (SH02)
    ("metocratic", "meritocratic"),
    # Euthanasia (SH03)
    ("Euphania", "euthanasia"),
    ("Euthan Asia", "euthanasia"),
    ("insunasia", "euthanasia"),
    ("insunia", "euthanasia"),
    # Dianne Feinstein (SH03)
    ("Dian Feinstein", "Dianne Feinstein"),
    # Elite overproduction (SH02)
    ("elite overp production", "elite overproduction"),
    # Petty bourgeoisie (SH02)
    ("petty boujo", "petty bourgeoisie"),
    # Rumsfeld (SH06) — supplement existing "Donald russfield" entries
    ("Rumsfield", "Rumsfeld"),
    # Martin Seligman (SH06)
    ("Martin Sigloman", "Martin Seligman"),
    # Sidney Gottlieb (SH06)
    ("Sydney Gobble", "Sidney Gottlieb"),
    ("Sime Gobbley", "Sidney Gottlieb"),
    # Abu Ghraib (SH06)
    ("Abu Grabi", "Abu Ghraib"),
    # Guantánamo Bay (SH06)
    ("Guanton Bay", "Guantánamo Bay"),
    # Harappan (SH06)
    ("Harapen", "Harappan"),
    # Mesopotamia (SH06)
    ("Mesoptitania", "Mesopotamia"),
    ("Mesopotitania", "Mesopotamia"),
    # Apophis — Egyptian serpent (SH06); "Opus" skipped (real word)
    ("Opthus", "Apophis"),
    ("Oythus", "Apophis"),
    # Jane Mayer (SH06)
    ("Jay Mir", "Jane Mayer"),
    # Dissenters (SH07)
    ("denters", "dissenters"),
    # Johns Hopkins (SH07) — missing 's'
    ("John Hopkins", "Johns Hopkins"),
    # Richard Feynman (SH07)
    ("Richard Feman", "Richard Feynman"),
    # Gini coefficient (SH07)
    ("genie coefficient", "Gini coefficient"),
    # James B. Conant (SH07)
    ("James B. Conit", "James B. Conant"),
    # Pulitzer Prize (SH07)
    ("politer prize", "Pulitzer Prize"),
    # Tim Geithner (SH07)
    ("Tim Gner", "Tim Geithner"),
    # Ivy League (SH07) — "Ivory" ASR error
    ("Ivory League", "Ivy League"),
    # utilitarian (SH07)
    ("utarian", "utilitarian"),
    # soulless (SH07)
    ("soless", "soulless"),
    # Franz Kafka (SH08)
    ("France Kafka", "Franz Kafka"),
    # Hannah Arendt (SH08) — ASR garbles + gender swap
    ("Henry Rant is a", "Hannah Arendt is a"),
    ("Hannah Rant", "Hannah Arendt"),
    # quiet quitting (SH08) — "quite" is real-word collision but phrase is unambiguous
    ("quite quitting", "quiet quitting"),
    # totalitarianism (SH08)
    ("totitarianism", "totalitarianism"),
    # consumerist (SH08)
    ("consumerous", "consumerist"),
    # high modernist ideology — James C. Scott (SH08)
    ("high marers ideology", "high modernist ideology"),
    # Peter Turchin (SH02) — ASR garbles
    ("Peter Church", "Peter Turchin"),
    # Tang dynasty (SH02)
    ("the Ting dynasty", "the Tang dynasty"),
    # Axel Rudakubana (SH03) — Southport attacker
    ("Axel Ruda Kubana", "Axel Rudakubana"),
    # Generic ASR glitches (SH01–04)
    ("moratorum", "moratorium"),
    ("healthare", "healthcare"),
    ("rebellous", "rebellious"),
    ("fraction reserve", "fractional reserve"),
    ("Azteex", "Aztecs"),
    ("diads", "dyads"),
    ("analyical model", "analytical model"),
    ("analy model", "analytical model"),
    ("flash eating", "flesh-eating"),
    ("flesheating", "flesh-eating"),
    # --- Secret History SH11 (2026-03-24): divine vs ASR "vine" ---
    ("channeling the vine", "channeling the divine"),
    ("connected to the vine", "connected to the divine"),
    ("connection to the vine", "connection to the divine"),
    ("connection with the vine", "connection with the divine"),
    ("removed from the vine", "removed from the divine"),
    ("return to the vine", "return to the divine"),
    # --- Secret History SH11: names / places / book ---
    ("Genevie von Piter", "Genevieve von Petzinger"),
    ("Ventang go", "Van Gogh"),
    ("Micronia", "Micronesia"),
    ("Darism came", "Darwinism came"),
    ("Darwin's theory of surround the fittest", "Darwin's theory of survival of the fittest"),
    ("the fear of evolution marked", "the theory of evolution marked"),
    # --- Secret History SH12 (2026-03-24) ---
    ("symphysicia", "synesthesia"),
    ("primive people", "primitive people"),
    ("printive cultures", "primitive cultures"),
    ("survival of the fittish.", "survival of the fittest."),
    ("Kenapole.", "Constantinople."),
    ("It's still instant.", "It's still standing."),
    ("Aken Cathedral", "Aachen Cathedral"),
    ("Minute Manhattan project.", "The Manhattan project."),
    ("Leonard Uler", "Leonhard Euler"),
    ("Colin Turbo", "Colin Turnbull"),
    ("the wayfinders by Wayade Davis", "The Wayfinders by Wade Davis"),
    ("secession crisis", "succession crisis"),
    ("This is a thought of everything uh by David Grabber and David Wangro", "This is The Dawn of Everything by David Graeber and David Wengrow"),
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

# Secret History (Volume III) — Roman / late-antique arc and shared SH phrases.
# Applied only when ``series == "secret-history"`` (filename ``secret-history-*`` on auto).
# Prefer multi-word / distinctive strings to avoid false positives vs generic English.
SECRET_HISTORY_REPLACEMENTS: list[tuple[str, str]] = [
    ("Brontage collapse", "Bronze Age collapse"),
    ("marinian Greeks", "Magna Graecia Greeks"),
    ("The Atrusian civilization", "The Etruscan civilization"),
    ("the atricians", "the Etruscans"),
    ("ser fairing people", "seafaring people"),
    ("such a disbanded position", "such a disadvantaged position"),
    ("Pyrus of Eperis", "Pyrrhus of Epirus"),
    ("So he and Hoplights sail over to Italy", "So he and hoplites sail over to Italy"),
    ("So he and Hoplights sail over to Greece", "So he and hoplites sail over to Italy"),
    ("the battle of Trivia", "the battle of the Trebia"),
    ("Lake Tresamine", "Lake Trasimene"),
    ("the battle of Kaine", "the battle of Cannae"),
    ("battle of Kaine", "battle of Cannae"),
    ("battle canal", "battle of Cannae"),
    ("does the battle of cannot fit", "does the battle of Cannae fit"),
    ("understand the back canal", "understand the battle of Cannae"),
    ("the back canal did not happen", "the battle of Cannae did not happen"),
    ("the back canal our conclusion", "the battle of Cannae our conclusion"),
    ("every historian that you talk to tells you the battle canal must be", "every historian that you talk to tells you the battle of Cannae must be"),
    ("chat GBT which battles", "ChatGPT which battles"),
    ("50,000 100,000 women are dead", "50,000 to 100,000 men are dead"),
    ("Kavar Barka", "Hannibal Barca"),
    ("Hannah Barker", "Hannibal Barca"),
    ("Hammer Barker", "Hannibal Barca"),
    ("The cockian told him", "The Carthaginian Senate told him"),
    ("Palibius", "Polybius"),
    ("Palibus", "Polybius"),
    ("Po Palibius.", "Polybius."),
    ("invented the battle of Canaan", "invented the battle of Cannae"),
    ("psychopunic war", "Punic War"),
    ("It's called a grain do.", "It's called a grain dole."),
    ("R woman war machine", "Roman war machine"),
    ("Tyberus Graas", "Tiberius Gracchus"),
    ("It belongs to women state.", "It belongs to the Roman state."),
    ("Then you have Solo.", "Then you have Sulla."),
    ("Solo's solution", "Sulla's solution"),
    ("escape Solah", "escape Sulla"),
    ("mil military campaigns", "military campaigns"),
    ("the battle of Alicia", "the battle of Alesia"),
    ("Caesar's G campaign", "Caesar's Gaul campaign"),
    ("all the gic tribes", "all the Gallic tribes"),
    ("Caesar basically rebelss", "Caesar basically rebels"),
    ("the Ottomates are", "the optimates are"),
    ("General Pompei is fighting for the Ottomans", "General Pompey is fighting for the optimates"),
    ("Pompei, General Pompei", "Pompey, General Pompey"),
    ("the optimist afraid that if Pompei won", "the optimates afraid that if Pompey won"),
    ("they would make Pompei king", "they would make Pompey king"),
    ("Pompei and Juju Caesar", "Pompey and Julius Caesar"),
    ("force Pompei and", "force Pompey and"),
    ("Caesar needs to go fight Pompei", "Caesar needs to go fight Pompey"),
    ("But Pompei doesn't", "But Pompey doesn't"),
    ("battle of Farcus", "battle of Pharsalus"),
    ("battle called farceless", "battle called Pharsalus"),
    ("the ultimates force", "the optimates force"),
    ("they defeat Pompei", "they defeat Pompey"),
    ("Pompe has more soldiers", "Pompey has more soldiers"),
    ("August Augustus Caesar", "Augustus Caesar"),
    ("Remember Pibius is", "Remember Polybius is"),
    ("and he tells Libby to basically rewrite", "and he tells Livy to basically rewrite"),
    ("book written by Libby", "book written by Livy"),
    ("named Inas and his wife Kisha", "named Aeneas and his wife Creusa"),
    ("rape of the Sabian", "rape of the Sabine"),
    ("the Sabian women", "the Sabine women"),
    ("Kentinius", "Collatinus"),
    ("Lucius Buddhist", "Lucius Brutus"),
    ("Lucas Buddhist", "Lucius Brutus"),
    ("superbut.", "Tarquin Superbus."),
    ("Prudence is traumatized", "Brutus is traumatized"),
    ("kicking out uh the Tarkkins", "kicking out uh the Tarquins"),
    ("Tarun to recover", "Tarquin to recover"),
    ("Val Valyrias with the infant infantry and Fallon's information uh formation.", "Valerius with the infantry and Horatius in formation."),
    ("Areronus Tarkin", "Arruns Tarquin"),
    ("list licers", "lictors"),
    ("listenitor", "lictors"),
    ("junian hoon junian house", "Junian house"),
    ("bearbacks", "bare backs"),
    ("consil's children", "consul's children"),
    ("international conduct", "unnatural conduct"),
    ("The amuseiest reciprocating", "Mucius reciprocating"),
    ("unheers and safe", "unharmed and safe"),
    ("oo mucus cried", "Mucius cried"),
    ("Choi blazing", "Troy blazing"),
    ("Piriam", "Priam"),
    ("life bloodl", "life blood"),
    ("Petetro", "Patroclus"),
    ("Iniad", "Aeneid"),
    ("write the INAD", "write the Aeneid"),
    ("chatbt is a scam", "ChatGPT is a scam"),
    ("loses Brutus", "Lucius Brutus"),
    ("Zorustra", "Zarathustra"),
    ("port prophets", "poet prophets"),
    ("Azen the Great", "Alexander the Great"),
    ("Exen the Great", "Alexander the Great"),
    ("Neopalamus degrades", "Neoptolemus degrades"),
    ("Fire's brazen shield", "Pyrrhus's brazen shield"),
    ("Pyrus shouts back", "Pyrrhus shouts back"),
    ("Eupites", "Euripides"),
    ("Alabades", "Alcibiades"),
    ("deping depicting", "depicting"),
    ("romance rape", "Roman rape"),
    ("all this woman history", "all this Roman history"),
    ("preconert the preconer", "preconcerted the preconcert"),
    ("concernation", "consternation"),
    ("impious perity", "impious impiety"),
    ("womenish fears", "womanish fears"),
    ("inner marriage", "intermarriage"),
    ("They regret citizenship. they were not grant grant citizenship.", "They resent not being granted citizenship."),
    ("wolf destruction", "wealth destruction"),
    ("innovate release of social tension", "innovation, release of social tension"),
    ("Bman thought", "Romans thought"),
    ("these are out mountains", "these are the Alps"),
    ("costbenefit", "cost-benefit"),
    ("So the carters surrender the first Punic war they s the second Punic war", "So the Carthaginians surrender the first Punic war, they surrender the second Punic war"),
    ("They're going to be wed up", "They're going to be wiped out"),
    ("Carthageians", "Carthaginians"),
    ("Napoleon U or", "Napoleon or"),
    ("mess calling", "messianic calling"),
    ("Hannibal Bark Hannibal Barca", "Hannibal Barca"),
    ("come together to dis to discuss", "come together to discuss"),
    ("the hoplets", "the hoplites"),
    ("each hoplet", "each hoplite"),
    ("The legioners", "The legionaries"),
    ("legionnaers", "legionaries"),
    ("double involvement strategy", "double envelopment strategy"),
    ("battle canine", "battle of Cannae"),
    # Etruscan / Pyrrhus — same garbles as civilization tier; SH does not run civilization tier
    ("truskin civilization", "Etruscan civilization"),
    ("truskin", "Etruscan"),
    ("pyrus is defeating", "Pyrrhus is defeating"),
    ("pyrus hands", "Pyrrhus's hands"),
]

# Applied when ``series == "game-theory"`` (filename ``game-theory-*`` on auto).
# Start empty; add systematic mis-hearings after Volume IV ingests.
GAME_THEORY_REPLACEMENTS: list[tuple[str, str]] = []

# Applied when ``series == "great-books"`` (filename ``great-books-*`` on auto).
# Start empty; add systematic mis-hearings after Volume V ingests.
GREAT_BOOKS_REPLACEMENTS: list[tuple[str, str]] = []
