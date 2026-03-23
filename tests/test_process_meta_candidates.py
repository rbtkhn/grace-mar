"""META_INFRA candidate parsing and allowlist validation."""

import textwrap

from process_meta_candidates import (
    extract_meta_candidates,
    is_allowlisted_path,
    paths_in_unified_diff,
    validate_meta_candidate,
)


def test_allowlist_accepts_scripts_config_bot():
    assert is_allowlisted_path("scripts/foo.py")
    assert is_allowlisted_path("config/fork-config.json")
    assert is_allowlisted_path("users/grace-mar/artifacts/meta-diffs/x.patch")
    assert not is_allowlisted_path("users/grace-mar/self.md")
    assert not is_allowlisted_path("../escape")


def test_paths_in_unified_diff():
    diff = """--- a/scripts/x.py
+++ b/scripts/x.py
@@ -1 +1 @@
-a
+b
"""
    assert "scripts/x.py" in paths_in_unified_diff(diff)


def test_extract_meta_skips_non_meta():
    gate = textwrap.dedent(
        """\
        ## Candidates

        ### CANDIDATE-0001 (regular)
        ```yaml
        status: pending
        proposal_class: SELF_KNOWLEDGE_ADD
        summary: "x"
        mind_category: knowledge
        suggested_entry: "y"
        profile_target: IX-A.1
        ```
        ## Processed
        """
    )
    assert extract_meta_candidates(gate) == []


def test_extract_meta_with_inline_diff():
    gate = textwrap.dedent(
        """\
        ## Candidates

        ### CANDIDATE-0090 (META test)
        ```yaml
        proposal_class: META_INFRA
        status: pending
        summary: "test meta"
        channel_key: operator:cursor
        meta_risk: LOW
        meta_targets: |
          scripts/harness_warmup.py
        meta_diff: |
          --- a/scripts/harness_warmup.py
          +++ b/scripts/harness_warmup.py
          @@ -1 +1 @@
          -# old
          +# new
        ```
        ## Processed
        """
    )
    cands = extract_meta_candidates(gate)
    assert len(cands) == 1
    c = cands[0]
    assert c["id"] == "CANDIDATE-0090"
    assert "scripts/harness_warmup.py" in c["meta_targets"]
    assert "META" in c["diff_text"] or "harness_warmup" in c["diff_text"]
    ok, errs = validate_meta_candidate(c, "grace-mar")
    assert ok, errs


def test_validate_rejects_bad_target():
    c = {
        "id": "CANDIDATE-0091",
        "meta_targets": ["users/grace-mar/self.md"],
        "diff_text": """--- a/users/grace-mar/self.md
+++ b/users/grace-mar/self.md
@@ -1 +1 @@
-x
+y
""",
    }
    ok, errs = validate_meta_candidate(c, "grace-mar")
    assert not ok
    assert any("allowlisted" in e for e in errs)


def test_filter_proposal_class_substr():
    from recursion_gate_review import filter_review_candidates

    rows = [
        {"id": "CANDIDATE-1", "proposal_class": "SELF_KNOWLEDGE_ADD", "proposal_class_raw": None},
        {"id": "CANDIDATE-2", "proposal_class": "META_INFRA", "proposal_class_raw": "META_INFRA"},
    ]
    out = filter_review_candidates(rows, proposal_class_substr="META")
    assert len(out) == 1
    assert out[0]["id"] == "CANDIDATE-2"
