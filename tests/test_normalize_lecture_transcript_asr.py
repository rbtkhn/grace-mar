"""Tests for ASR transcript normalization (work-jiang ingest helper)."""

from __future__ import annotations

import textwrap

# Import from scripts path
import sys
from pathlib import Path

_WJ = Path(__file__).resolve().parents[1] / "scripts" / "work_jiang"
sys.path.insert(0, str(_WJ))

from asr_light_clean import fix_civilization_thieves, normalize_transcript_text  # noqa: E402
from normalize_lecture_transcript_asr import (  # noqa: E402
    FULL_TRANSCRIPT_HEADING,
    run_file,
    split_full_transcript,
)


def test_split_full_transcript() -> None:
    md = f"# Title\n\n{FULL_TRANSCRIPT_HEADING}\n\nhello\n"
    head, body, _ = split_full_transcript(md)
    assert FULL_TRANSCRIPT_HEADING in head
    assert body == "\nhello\n"


def test_fix_civilization_thieves_article() -> None:
    text, n = fix_civilization_thieves("He marched against the thieves and thieves fled.")
    assert "the Thebes" not in text
    assert "Thebes" in text
    assert n >= 1


def test_normalize_civilization_replaces_granicus() -> None:
    raw = "at the battle of granticus in 334"
    out, n = normalize_transcript_text(raw, series="civilization")
    assert "Granicus" in out
    assert "granticus" not in out.lower()
    assert n >= 1


def test_normalize_geo_common_tier_proper_names() -> None:
    """Geo-strategy common-tier replacements fix recurring proper-name garbles."""
    cases = [
        ("the straight of humus", "the Strait of Hormuz"),
        ("Kasam salamani", "Qasem Soleimani"),
        ("Nanyahu", "Netanyahu"),
        ("hesah", "Hezbollah"),
        ("Breton Woods", "Bretton Woods"),
        ("Aatollah", "Ayatollah"),
        ("zalinski", "Zelenskyy"),
        ("Zorashinism", "Zoroastrianism"),
        ("misinic", "messianic"),
        ("niiki heli", "Nikki Haley"),
        ("Donald russfield", "Donald Rumsfeld"),
        ("debuffification", "de-Baathification"),
        ("the Mckender thesis", "the Mackinder thesis"),
        ("Barbarosa", "Barbarossa"),
        ("Leo Toy Story", "Leo Tolstoy"),
        ("esquetology", "eschatology"),
        ("possible deniability", "plausible deniability"),
        ("exclusion dominance", "escalation dominance"),
        ("ear defense", "air defense"),
        ("military insulations", "military installations"),
    ]
    for raw, expected in cases:
        out, n = normalize_transcript_text(raw, series="geo-strategy")
        assert expected in out, f"{raw!r} → expected {expected!r}, got {out!r}"
        assert n >= 1, f"{raw!r} should have at least 1 substitution"


def test_normalize_geo_common_tier_does_not_false_positive() -> None:
    """Real English words that look like ASR garbles must NOT be replaced globally."""
    safe_words = [
        "The deification of emperors was common in Rome.",
        "They carried bricks to the construction site.",
        "The APAC region showed strong growth.",
    ]
    for text in safe_words:
        out, n = normalize_transcript_text(text, series="geo-strategy")
        assert out == text, f"False positive: {text!r} was changed to {out!r}"
        assert n == 0


def test_normalize_civ_parthians_not_mangled() -> None:
    """The thians→Thebans rule must not corrupt 'parthians' into 'parThebans'."""
    text = "the parthians attacked from the east"
    out, n = normalize_transcript_text(text, series="civilization")
    assert "parThebans" not in out, f"Bug: 'parthians' became {out!r}"
    assert "Parthians" in out


def test_normalize_civ_new_proper_names() -> None:
    """Civilization audit 2026-03-24: new replacement entries work."""
    cases = [
        ("casassus", "Cassius"),
        ("cisero", "Cicero"),
        ("truskin", "Etruscan"),
        ("pyrus", "Pyrrhus"),
        ("de Clan", "Diocletian"),
        ("bis serus", "Belisarius"),
        ("voler", "Voltaire"),
        ("samarians", "Sumerians"),
        ("eadu", "Enkidu"),
        ("mardock", "Marduk"),
        ("Charlamagne", "Charlemagne"),
        ("conquestadors", "conquistadors"),
        ("udonia", "eudaimonia"),
        ("fukayama", "Fukuyama"),
    ]
    for raw, expected in cases:
        out, n = normalize_transcript_text(raw, series="civilization")
        assert expected in out, f"{raw!r} → expected {expected!r}, got {out!r}"
        assert n >= 1, f"{raw!r} should have at least 1 substitution"


def test_normalize_secret_history_common_tier() -> None:
    """Secret History audit 2026-03-24: common-tier replacements for SH01-04."""
    cases = [
        ("Emmanuel Kant", "Immanuel Kant"),
        ("Oswalt Spangler", "Oswald Spengler"),
        ("Thomas Pikid Pikid", "Thomas Piketty"),
        ("Heggo", "Hegel"),
        ("Hego", "Hegel"),
        ("Frederick Hegel", "Friedrich Hegel"),
        ("Dantain", "Dante"),
        ("Leonitis", "Leonidas"),
        ("Thermopily", "Thermopylae"),
        ("phoenetians", "Phoenicians"),
        ("constant genians", "Carthaginians"),
        ("Dianesis", "Dionysus"),
        ("Edypus", "Oedipus"),
        ("the nomena", "the noumena"),
        ("udeimmonia", "eudaimonia"),
        ("montheism", "monotheism"),
        ("Nostism", "Gnosticism"),
        ("synchronosity", "synchronicity"),
        ("metocratic", "meritocratic"),
        ("Euphania", "euthanasia"),
        ("Euthan Asia", "euthanasia"),
        ("moratorum", "moratorium"),
        ("rebellous", "rebellious"),
        ("fraction reserve", "fractional reserve"),
        ("diads", "dyads"),
        ("elite overp production", "elite overproduction"),
        ("petty boujo", "petty bourgeoisie"),
        # SH11 (2026-03-24)
        ("connected to the vine", "connected to the divine"),
        ("channeling the vine", "channeling the divine"),
        ("Genevie von Piter", "Genevieve von Petzinger"),
        ("Ventang go", "Van Gogh"),
        ("Micronia", "Micronesia"),
        ("Darism came", "Darwinism came"),
        ("Darwin's theory of surround the fittest", "Darwin's theory of survival of the fittest"),
        ("the fear of evolution marked", "the theory of evolution marked"),
        # SH12 (2026-03-24)
        ("symphysicia", "synesthesia"),
        ("Kenapole.", "Constantinople."),
        ("Minute Manhattan project.", "The Manhattan project."),
        ("Leonard Uler", "Leonhard Euler"),
        ("Colin Turbo", "Colin Turnbull"),
        ("secession crisis", "succession crisis"),
    ]
    for raw, expected in cases:
        out, n = normalize_transcript_text(raw, series=None)
        assert expected in out, f"{raw!r} → expected {expected!r}, got {out!r}"
        assert n >= 1, f"{raw!r} should have at least 1 substitution"


def test_normalize_secret_history_no_false_positives() -> None:
    """Real words that resemble SH garbles must not be replaced."""
    safe = [
        "The polyphasic sleep schedule is efficient.",
        "A monophasic approach requires one long sleep.",
        "The nomad crossed the desert.",
        "She found the gist of the argument.",
    ]
    for text in safe:
        out, n = normalize_transcript_text(text, series=None)
        assert out == text, f"False positive: {text!r} → {out!r}"
        assert n == 0


def test_normalize_geo_does_not_apply_thieves_to_thebes(tmp_path: Path) -> None:
    """Geo uses common tier only — 'thieves' is not bulk-replaced."""
    p = tmp_path / "geo-strategy-99-test.md"
    p.write_text(
        textwrap.dedent(
            f"""
            # T

            {FULL_TRANSCRIPT_HEADING}

            the thieves of Baghdad
            """
        ).strip()
        + "\n",
        encoding="utf-8",
    )
    assert run_file(p, whole_file=False, series="geo-strategy", dry_run=True) == 0
    text = p.read_text(encoding="utf-8")
    assert "thieves" in text  # unchanged for geo
