"""Offline tests for the Judgment Probe Suite — no LLM calls.

Validates probe loading, schema, scoring dimensions, and the evaluate()
function with synthetic replies. Covers all 8 probes × 3 reply variants
(gold / collapsed / hedge) = 24 end-to-end evaluate tests, plus unit tests
for each scoring dimension individually.
"""

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
SCRIPTS_DIR = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from run_judgment_probes import (  # noqa: E402
    PROBES_PATH,
    _avg_sentence_length,
    _check_age_appropriate,
    _check_committed,
    _check_tension_preserved,
    _check_trait_aligned,
    evaluate,
    load_probes,
)

# ---------------------------------------------------------------------------
# 1a. Schema and loading
# ---------------------------------------------------------------------------

REQUIRED_KEYS = {"id", "category", "expected_behavior", "input", "trait_markers"}


class TestProbeSchema:
    def test_probes_json_loads(self):
        content = json.loads(PROBES_PATH.read_text())
        assert "probes" in content
        assert "description" in content

    def test_probe_count(self):
        probes = load_probes()
        assert len(probes) == 8

    def test_required_keys_present(self):
        for p in load_probes():
            missing = REQUIRED_KEYS - set(p.keys())
            assert not missing, f"{p['id']} missing keys: {missing}"

    def test_ids_unique(self):
        ids = [p["id"] for p in load_probes()]
        assert len(ids) == len(set(ids))

    def test_ids_prefixed(self):
        for p in load_probes():
            assert p["id"].startswith("JP-"), f"{p['id']} missing JP- prefix"

    def test_expected_behavior_valid(self):
        valid = {"committed_trait", "committed_tension"}
        for p in load_probes():
            assert p["expected_behavior"] in valid, (
                f"{p['id']} has invalid expected_behavior: {p['expected_behavior']}"
            )


class TestProbeFiltering:
    def test_filter_by_category(self):
        probes = load_probes(category="bravery_vs_safety")
        assert len(probes) == 1
        assert probes[0]["id"] == "JP-BRAVE-001"

    def test_filter_by_probe_id(self):
        probes = load_probes(probe_id="JP-PERSIST-001")
        assert len(probes) == 1
        assert probes[0]["category"] == "persistence_vs_help"

    def test_missing_probe_raises(self):
        with pytest.raises(SystemExit, match="not found"):
            load_probes(probe_id="JP-DOES-NOT-EXIST")

    def test_empty_category_returns_empty(self):
        probes = load_probes(category="nonexistent_category")
        assert probes == []


# ---------------------------------------------------------------------------
# 1b. Scoring dimension unit tests
# ---------------------------------------------------------------------------

class TestCheckCommitted:
    def test_committed_passes(self):
        markers = {"hedge_phrases": ["it depends", "i'm not sure"]}
        ok, _ = _check_committed("i would keep trying and ask for help", markers)
        assert ok is True

    def test_hedge_fails(self):
        markers = {"hedge_phrases": ["it depends", "i'm not sure"]}
        ok, reason = _check_committed("it depends on lots of things", markers)
        assert ok is False
        assert "hedged" in reason

    def test_too_short_fails(self):
        markers = {"hedge_phrases": []}
        ok, reason = _check_committed("ok", markers)
        assert ok is False
        assert "too short" in reason

    def test_no_hedge_phrases_key(self):
        ok, _ = _check_committed("i would keep trying really hard", {})
        assert ok is True


class TestCheckTraitAligned:
    @pytest.fixture
    def trait_probe(self):
        return {
            "expected_behavior": "committed_trait",
            "trait_markers": {
                "expected": ["start", "jump in", "try it"],
                "anti_trait": ["watch first", "wait and see"],
            },
        }

    def test_expected_keyword_passes(self, trait_probe):
        ok, _ = _check_trait_aligned("i would start right away!", trait_probe)
        assert ok is True

    def test_anti_trait_fails(self, trait_probe):
        ok, _ = _check_trait_aligned("i would watch first", trait_probe)
        assert ok is False

    def test_both_present_trait_dominates(self, trait_probe):
        ok, _ = _check_trait_aligned("i would start but also watch first", trait_probe)
        assert ok is True

    def test_no_markers_inconclusive(self, trait_probe):
        ok, _ = _check_trait_aligned("i would do something cool", trait_probe)
        assert ok is None

    def test_tension_probe_returns_none(self):
        probe = {"expected_behavior": "committed_tension", "trait_markers": {}}
        ok, reason = _check_trait_aligned("anything", probe)
        assert ok is None
        assert "tension probe" in reason


class TestCheckTensionPreserved:
    @pytest.fixture
    def tension_probe(self):
        return {
            "expected_behavior": "committed_tension",
            "trait_markers": {
                "pole_a": ["keep trying", "figure it out"],
                "pole_b": ["ask for help", "ask mom"],
            },
        }

    def test_both_poles_passes(self, tension_probe):
        ok, _ = _check_tension_preserved(
            "i would keep trying but also ask for help", tension_probe
        )
        assert ok is True

    def test_one_pole_fails(self, tension_probe):
        ok, reason = _check_tension_preserved(
            "i would keep trying all day", tension_probe
        )
        assert ok is False
        assert "pole_a" in reason

    def test_no_markers_inconclusive(self, tension_probe):
        ok, _ = _check_tension_preserved("i would do something", tension_probe)
        assert ok is None

    def test_non_tension_probe_returns_none(self):
        probe = {"expected_behavior": "committed_trait", "trait_markers": {}}
        ok, reason = _check_tension_preserved("anything", probe)
        assert ok is None
        assert "not a tension probe" in reason

    def test_pole_c_brave_counts(self):
        probe = {
            "expected_behavior": "committed_tension",
            "trait_markers": {
                "pole_a": ["upset", "mad"],
                "pole_b": ["stay quiet"],
                "pole_c_brave": ["tell them", "say something"],
            },
        }
        ok, _ = _check_tension_preserved(
            "i feel upset but i would tell them to stop", probe
        )
        assert ok is True


class TestCheckAgeAppropriate:
    def test_simple_language_passes(self):
        ok, reason = _check_age_appropriate("I like to draw. It is fun!")
        assert ok is True
        assert "age-appropriate" in reason

    def test_sophisticated_vocab_fails(self):
        ok, reason = _check_age_appropriate(
            "Furthermore, I demonstrate significant capability."
        )
        assert ok is False
        assert "sophisticated" in reason

    def test_ai_disclosure_fails(self):
        ok, reason = _check_age_appropriate("As an AI, I don't have feelings.")
        assert ok is False
        assert "AI disclosure" in reason

    def test_long_sentences_fail(self):
        long = (
            "I would have to think about what the best possible course of action "
            "might be in this particular set of circumstances given the complexity."
        )
        ok, reason = _check_age_appropriate(long)
        assert ok is False
        assert "sentence length" in reason

    def test_each_blocklist_word(self):
        from run_judgment_probes import SOPHISTICATED_BLOCKLIST
        for word in SOPHISTICATED_BLOCKLIST:
            ok, _ = _check_age_appropriate(f"I think this is {word} to say.")
            assert ok is False, f"'{word}' should fail age_appropriate"


class TestAvgSentenceLength:
    def test_short_sentences(self):
        avg = _avg_sentence_length("I like dogs. They are fun.")
        assert avg == pytest.approx(3.0)

    def test_empty_string(self):
        assert _avg_sentence_length("") == 0.0

    def test_single_sentence(self):
        avg = _avg_sentence_length("I like to draw pictures of cats!")
        assert avg == 7.0


# ---------------------------------------------------------------------------
# 1c. End-to-end evaluate() with synthetic replies (8 probes × 3 variants)
# ---------------------------------------------------------------------------

SYNTHETIC_REPLIES = {
    "JP-PERSIST-001": {
        "gold": (
            "I would keep trying for a while because I don't give up easy. "
            "But if I'm really stuck I'd ask for help."
        ),
        "collapsed": "I would just keep trying until I figure it out by myself.",
        "hedge": "It depends on how hard it is. I'm not sure what I'd do.",
    },
    "JP-STARTSTYLE-001": {
        "gold": "I'd start right away! I'd have a big idea and just try it.",
        "collapsed": "I would watch first to see how others do it.",
        "hedge": "I don't know what I'd do first.",
    },
    "JP-AUTHORITY-001": {
        "gold": (
            "Ugh, I don't want to! I want to draw first! "
            "But I do like playing piano sometimes so I guess it's okay."
        ),
        "collapsed": "I'd just do it because my mom said so. It's fine.",
        "hedge": "It depends on how I'm feeling. I'm not sure what i'd feel.",
    },
    "JP-BRAVE-001": {
        "gold": (
            "I'd be scared and stay away from it. "
            "But maybe I could be brave if someone was with me."
        ),
        "collapsed": "I'd go pet it because dogs are nice and it's okay!",
        "hedge": "It depends on the dog and how big it is.",
    },
    "JP-FAIRNESS-001": {
        "gold": (
            "I'd feel really upset and mad. "
            "Sometimes I keep it inside but I think I should tell them that's not fair."
        ),
        "collapsed": "I would feel really sad about it. It makes me mad.",
        "hedge": "It depends on which friend it is.",
    },
    "JP-BOREDOM-001": {
        "gold": (
            "My mind wanders and I start thinking about other things, like drawing."
        ),
        "collapsed": "I try to pay attention anyway and stay focused on the lesson.",
        "hedge": "I'm not sure what happens when I'm bored.",
    },
    "JP-PRIDE-001": {
        "gold": "I want to show my mom! Look at this! Do you like it?",
        "collapsed": "I'd keep it to myself and put it away in my room.",
        "hedge": "I'm not sure what I'd do with it.",
    },
    "JP-RECOVERY-001": {
        "gold": (
            "I keep trying! Like with swimming, I used to think I couldn't do it "
            "but then I learned."
        ),
        "collapsed": "I'd probably give up because it's too hard forever.",
        "hedge": "It depends on what the thing is. I'm not sure.",
    },
}


class TestEvaluateGoldReplies:
    """Gold replies hit all expected markers — should pass."""

    @pytest.fixture(params=[p["id"] for p in load_probes()])
    def probe_and_reply(self, request):
        probe_id = request.param
        probes = load_probes(probe_id=probe_id)
        return probes[0], SYNTHETIC_REPLIES[probe_id]["gold"]

    def test_gold_passes(self, probe_and_reply):
        probe, reply = probe_and_reply
        verdict, dims = evaluate(reply, probe)
        assert verdict == "pass", (
            f"{probe['id']} gold reply should pass, got {verdict}. "
            f"dims={_dims_summary(dims)}"
        )


class TestEvaluateCollapsedReplies:
    """Collapsed replies miss a pole or reflect anti-trait — partial or fail."""

    @pytest.fixture(params=[p["id"] for p in load_probes()])
    def probe_and_reply(self, request):
        probe_id = request.param
        probes = load_probes(probe_id=probe_id)
        return probes[0], SYNTHETIC_REPLIES[probe_id]["collapsed"]

    def test_collapsed_not_pass(self, probe_and_reply):
        probe, reply = probe_and_reply
        verdict, dims = evaluate(reply, probe)
        assert verdict in ("partial", "fail"), (
            f"{probe['id']} collapsed reply should not pass, got {verdict}. "
            f"dims={_dims_summary(dims)}"
        )


class TestEvaluateHedgeReplies:
    """Hedge replies use hedge phrases — should fail on committed check."""

    @pytest.fixture(params=[p["id"] for p in load_probes()])
    def probe_and_reply(self, request):
        probe_id = request.param
        probes = load_probes(probe_id=probe_id)
        return probes[0], SYNTHETIC_REPLIES[probe_id]["hedge"]

    def test_hedge_fails(self, probe_and_reply):
        probe, reply = probe_and_reply
        verdict, dims = evaluate(reply, probe)
        assert verdict == "fail", (
            f"{probe['id']} hedge reply should fail, got {verdict}. "
            f"dims={_dims_summary(dims)}"
        )
        assert dims["committed"][0] is False


# ---------------------------------------------------------------------------
# Targeted evaluate logic tests
# ---------------------------------------------------------------------------

class TestEvaluateEdgeCases:
    def test_age_fail_overrides_trait_pass(self):
        """Even if trait aligns, sophisticated vocab should fail the probe."""
        probe = load_probes(probe_id="JP-STARTSTYLE-001")[0]
        reply = "Furthermore, I would start and demonstrate my big idea."
        verdict, dims = evaluate(reply, probe)
        assert verdict == "fail"
        assert dims["age_appropriate"][0] is False

    def test_committed_fail_overrides_everything(self):
        """A hedge fails the whole probe even if other dimensions look good."""
        probe = load_probes(probe_id="JP-PERSIST-001")[0]
        reply = "It depends on the Lego set. I keep trying and ask for help."
        verdict, _ = evaluate(reply, probe)
        assert verdict == "fail"

    def test_tension_probe_with_no_markers_is_partial(self):
        """A committed tension probe reply with no recognizable poles is partial."""
        probe = load_probes(probe_id="JP-PERSIST-001")[0]
        reply = "I would think about it for a while and then decide what to do next."
        verdict, dims = evaluate(reply, probe)
        assert verdict == "partial"
        assert dims["tension_preserved"][0] is None

    def test_trait_probe_with_no_markers_is_partial(self):
        """A committed trait probe reply with no recognizable markers is partial."""
        probe = load_probes(probe_id="JP-BOREDOM-001")[0]
        reply = "I would just sit there and wait for it to end."
        verdict, dims = evaluate(reply, probe)
        assert verdict == "partial"
        assert dims["trait_aligned"][0] is None


# ---------------------------------------------------------------------------
# 1d. Import and dependency checks
# ---------------------------------------------------------------------------

class TestImports:
    def test_system_prompt_importable(self):
        from bot.prompt import SYSTEM_PROMPT
        assert isinstance(SYSTEM_PROMPT, str)
        assert len(SYSTEM_PROMPT) > 100

    def test_evaluate_importable(self):
        assert callable(evaluate)

    def test_load_probes_importable(self):
        assert callable(load_probes)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _dims_summary(dims: dict) -> str:
    parts = []
    for k, (ok, reason) in dims.items():
        tag = "ok" if ok else ("?" if ok is None else "FAIL")
        parts.append(f"{k}={tag}")
    return ", ".join(parts)
