#!/usr/bin/env python3
"""
Generate the Grace-Mar pilot dashboard.

Reads pilot-001 profile files and produces a single HTML dashboard with:
- Fork summary (identity, Lexile, pipeline status)
- PENDING-REVIEW queue (candidates awaiting approval)
- SKILLS container status (READ, WRITE, BUILD)
- Recent bot archive excerpts
- Benchmarks (pipeline stats, IX dimension counts)

Usage:
    python scripts/generate_dashboard.py
    open dashboard/index.html

The dashboard works as a Telegram Mini App when served over HTTPS. Configure the URL
in @BotFather (Bot Settings → Menu Button) and set DASHBOARD_MINIAPP_URL in .env.
"""

import json
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROFILE_DIR = REPO_ROOT / "users" / "pilot-001"
DASHBOARD_DIR = REPO_ROOT / "dashboard"


@dataclass
class DashboardData:
    name: str
    age: int
    lexile_output: str
    pending_count: int
    pending_candidates: list[dict]
    ix_a_count: int
    ix_b_count: int
    ix_c_count: int
    write_count: int
    read_count: int
    create_count: int
    skills_summary: dict
    knowledge_samples: list[str]
    curiosity_samples: list[str]
    personality_samples: list[str]
    library_entries: list[dict]
    journal_entries: list[dict]
    recent_exchanges: list[dict]
    generated_at: str
    last_pipeline_activity: str
    total_tokens: int
    tokens_today: int
    tokens_per_ix: str  # "X" or "—" when no IX
    pipeline_applied: int
    pipeline_rejected: int
    curation_ratio: str  # "X% human-approved" or "—"
    fork_checksum: str  # from FORK-MANIFEST.json or ""
    dyad_consultations_7d: int
    dyad_integrations_7d: int
    dyad_activity_reports_7d: int


def parse_pending_review(content: str) -> tuple[int, list[dict]]:
    """Extract pending candidates from PENDING-REVIEW.md."""
    candidates = []
    in_candidates = False
    in_processed = False
    current: dict | None = None

    for line in content.splitlines():
        if line.strip() == "## Candidates":
            in_candidates = True
            in_processed = False
            continue
        if line.strip() == "## Processed":
            in_candidates = False
            in_processed = True
            continue

        if in_candidates:
            if m := re.match(r"^### (CANDIDATE-\d+)", line):
                current = {"id": m.group(1), "summary": "", "mind_category": "", "priority_score": ""}
                candidates.append(current)
            elif current and line.strip().startswith("summary:"):
                current["summary"] = line.split(":", 1)[1].strip().strip('"')
            elif current and line.strip().startswith("mind_category:"):
                current["mind_category"] = line.split(":", 1)[1].strip()
            elif current and line.strip().startswith("priority_score:"):
                current["priority_score"] = line.split(":", 1)[1].strip()

    return len(candidates), candidates


def parse_self(content: str) -> dict:
    """Extract key fields from SELF.md."""
    data = {"name": "?", "age": 0, "lexile_output": "?", "ix_a_count": 0, "ix_b_count": 0, "ix_c_count": 0}

    if m := re.search(r"name:\s*(\S+)", content):
        data["name"] = m.group(1)
    if m := re.search(r"age:\s*(\d+)", content):
        data["age"] = int(m.group(1))
    if m := re.search(r'lexile_output:\s*["\']?([^"\'\n]+)', content):
        data["lexile_output"] = m.group(1).strip()

    data["ix_a_count"] = len(re.findall(r"id:\s+LEARN-\d+", content))
    data["ix_b_count"] = len(re.findall(r"id:\s+CUR-\d+", content))
    data["ix_c_count"] = len(re.findall(r"id:\s+PER-\d+", content))

    return data


def parse_evidence(content: str) -> dict:
    """Count evidence entries from EVIDENCE.md."""
    write = len(re.findall(r"id:\s+WRITE-\d+", content))
    read = len(re.findall(r"id:\s+READ-\d+", content))
    create = len(re.findall(r"id:\s+CREATE-\d+", content))
    return {"write": write, "read": read, "create": create}


def parse_skills(content: str) -> dict:
    """Extract container status from SKILLS.md."""
    summary = {}
    for container in ["READ", "WRITE", "BUILD"]:
        block = re.search(
            rf"### {container} Container.*?```yaml(.*?)```",
            content,
            re.DOTALL,
        )
        if block:
            yaml = block.group(1).strip()
            status = "?"
            if m := re.search(r"status:\s*(\S+)", yaml):
                status = m.group(1)
            edge = ""
            if m := re.search(r"edge:\s*[\"']?(.+?)[\"']?\s*(?:\n|$)", yaml, re.DOTALL):
                edge = m.group(1).strip().strip('"')[:80]
            summary[container] = {"status": status, "edge": edge}
    return summary


def parse_archive(content: str, limit: int = 10) -> list[dict]:
    """Extract recent USER/GRACE-MAR exchanges from archive (with timestamps)."""
    exchanges = []
    pattern = r"\*\*\[([^\]]+)\]\*\*\s+`(USER|GRACE-MAR[^`]*)`.*?\n> (.+?)(?=\n\n|\n\*\*\[|\Z)"
    for m in re.finditer(pattern, content, re.DOTALL):
        ts, role, text = m.group(1), m.group(2), m.group(3).strip().replace("\n> ", "\n")
        if "GRACE-MAR" in role or role == "USER":
            exchanges.append({"timestamp": ts, "role": role, "text": text})

    # Pair USER + GRACE-MAR, take last N pairs (include timestamp from USER)
    paired = []
    i = 0
    while i < len(exchanges) - 1:
        if exchanges[i]["role"] == "USER" and "GRACE-MAR" in exchanges[i + 1]["role"]:
            paired.append({
                "timestamp": exchanges[i]["timestamp"],
                "user": exchanges[i]["text"],
                "grace_mar": exchanges[i + 1]["text"],
            })
            i += 2
        else:
            i += 1

    return paired[-limit:]


def parse_library(content: str) -> list[dict]:
    """Extract active LIBRARY entries (id, title, scope, read_status, volume) from LIBRARY.md."""
    entries = []
    blocks = re.split(r'-\s+id:\s+LIB-', content)
    for block in blocks[1:]:  # skip first (header)
        num = re.match(r'(\d+)', block)
        lib_id = "LIB-" + num.group(1) if num else "?"
        title_m = re.search(r'title:\s*["\']([^"\']+)["\']', block)
        scope_m = re.search(r'scope:\s*\[([^\]]*)\]', block)
        status_m = re.search(r'status:\s*(\w+)', block)
        read_m = re.search(r'read_status:\s*(\w+)', block)
        volume_m = re.search(r'volume:\s*["\']([^"\']+)["\']', block)
        if status_m and status_m.group(1) != "active":
            continue
        title = title_m.group(1) if title_m else ""
        scope_str = scope_m.group(1) if scope_m else ""
        scope = [s.strip() for s in scope_str.split(",") if s.strip()]
        read_status = read_m.group(1) if read_m else "unread"
        volume = volume_m.group(1) if volume_m else None
        entries.append({"id": lib_id, "title": title, "scope": scope, "read_status": read_status, "volume": volume})
    return entries


def parse_journal(content: str) -> list[dict]:
    """Extract JOURNAL entries (date, entry) from JOURNAL.md. Approved only. Supports entry (prose) or legacy highlights (bullets)."""
    entries = []
    # Split into entry blocks: - date: "..." ... until next - date: or end
    blocks = re.findall(
        r'-\s+date:\s*["\']([^"\']+)["\'](.*?)(?=\n\s+-\s+date:|\Z)',
        content,
        re.DOTALL,
    )
    for date_str, block in blocks:
        if re.search(r'approved:\s*false', block):
            continue
        text = None
        # New format: entry: "..." or entry: |
        m = re.search(r'entry:\s*["\']((?:[^"\\]|\\.)*)["\']', block)
        if m:
            text = m.group(1).replace("\\n", "\n").replace('\\"', '"').strip()
        if not text:
            m = re.search(r'entry:\s*\|\s*\n((?:\s+.+\n?)*)', block)
            if m:
                text = re.sub(r"^\s+", "", m.group(1)).strip()
        # Legacy: highlights as bullets
        if not text:
            bullets = re.findall(r'-\s*"([^"]*)"', block)
            if bullets:
                text = " ".join(bullets)
        if text:
            entries.append({"date": date_str, "entry": text})
    return entries


def parse_ix_samples(content: str) -> tuple[list[str], list[str], list[str]]:
    """Extract topics from IX-A, IX-B, IX-C in SELF.md (all entries)."""
    knowledge = re.findall(r'id: LEARN-\d+.*?topic:\s*["\']([^"\']+)["\']', content, re.DOTALL)
    curiosity = re.findall(r'id: CUR-\d+.*?topic:\s*["\']([^"\']+)["\']', content, re.DOTALL)
    personality = re.findall(r'id: PER-\d+.*?observation:\s*["\']([^"\']+)["\']', content, re.DOTALL)
    if not personality:
        personality = re.findall(r'id: PER-\d+.*?observation:\s*([^\n]+)', content, re.DOTALL)
    personality = [p.strip() for p in personality]
    return (knowledge, curiosity, personality)


def parse_seed_interests(content: str) -> list[str]:
    """Extract interest topics from Section V (current interests) in SELF.md."""
    # Match "topic: X" under current: block (before ## VI or next ##)
    section_v = re.search(r'## V\. INTERESTS.*?current:.*?(?=## |emerging:|$)', content, re.DOTALL)
    if not section_v:
        return []
    topics = re.findall(r'^\s+-\s+topic:\s*(.+?)(?:\n|$)', section_v.group(0), re.MULTILINE)
    return [t.strip() for t in topics if t.strip()]


def parse_seed_personality(content: str) -> list[str]:
    """Extract personality traits and patterns from Section IV in SELF.md."""
    section_iv = re.search(r'## IV\. PERSONALITY.*?(?=## V\.|$)', content, re.DOTALL)
    if not section_iv:
        return []
    out: list[str] = []
    # traits: trait: X
    for m in re.finditer(r'trait:\s*([^\n#]+)', section_iv.group(0)):
        t = m.group(1).strip()
        if t:
            out.append(t)
    # emotional_patterns: trigger → response
    for m in re.finditer(r'trigger:\s*(.+?)\n\s+response:\s*([^\n]+)', section_iv.group(0), re.DOTALL):
        trigger = m.group(1).strip()[:40]
        response = m.group(2).strip()[:50]
        out.append(f"{trigger} → {response}")
    # humor, empathy, problem_solving one-liners
    if m := re.search(r'humor:\s*\n\s+style:\s*([^\n]+)', section_iv.group(0)):
        out.append(f"humor: {m.group(1).strip()}")
    if m := re.search(r'empathy_mode:\s*(\w+[-]?\w*)', section_iv.group(0)):
        out.append(f"empathy: {m.group(1)}")
    if m := re.search(r'problem_solving:\s*\n\s+style:\s*([^\n]+)', section_iv.group(0)):
        out.append(f"problem-solving: {m.group(1).strip()}")
    return out[:15]  # cap to avoid overflow


def collect_data() -> DashboardData:
    """Collect all dashboard data from profile files."""
    pending_path = PROFILE_DIR / "PENDING-REVIEW.md"
    self_path = PROFILE_DIR / "SELF.md"
    evidence_path = PROFILE_DIR / "EVIDENCE.md"
    skills_path = PROFILE_DIR / "SKILLS.md"
    archive_path = PROFILE_DIR / "VOICE-ARCHIVE.md"
    session_transcript_path = PROFILE_DIR / "SESSION-TRANSCRIPT.md"
    library_path = PROFILE_DIR / "LIBRARY.md"
    journal_path = PROFILE_DIR / "JOURNAL.md"

    pending_content = pending_path.read_text() if pending_path.exists() else ""
    self_content = self_path.read_text() if self_path.exists() else ""
    evidence_content = evidence_path.read_text() if evidence_path.exists() else ""
    skills_content = skills_path.read_text() if skills_path.exists() else ""
    archive_content = archive_path.read_text() if archive_path.exists() else ""
    transcript_content = session_transcript_path.read_text() if session_transcript_path.exists() else ""
    library_content = library_path.read_text() if library_path.exists() else ""
    journal_content = journal_path.read_text() if journal_path.exists() else ""

    pending_count, pending_candidates = parse_pending_review(pending_content)
    self_data = parse_self(self_content)
    evidence_data = parse_evidence(evidence_content)
    skills_summary = parse_skills(skills_content)
    knowledge_samples, curiosity_ix, personality_ix = parse_ix_samples(self_content)
    seed_interests = parse_seed_interests(self_content)
    seed_personality = parse_seed_personality(self_content)
    # Merge seed + post-seed: seed first (from detailed phases), then IX (pipeline growth)
    curiosity_samples = seed_interests + curiosity_ix
    personality_samples = seed_personality + personality_ix
    library_entries = parse_library(library_content)
    journal_entries = parse_journal(journal_content)
    recent = parse_archive(transcript_content or archive_content, limit=15)

    last_activity = "—"
    if pending_path.exists():
        mtime = pending_path.stat().st_mtime
        last_activity = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")

    ledger_path = PROFILE_DIR / "COMPUTE-LEDGER.jsonl"
    total_tokens = 0
    tokens_today = 0
    today = datetime.now().strftime("%Y-%m-%d")
    if ledger_path.exists():
        for line in ledger_path.read_text().strip().splitlines():
            if not line:
                continue
            try:
                row = json.loads(line)
                t = row.get("total_tokens", row.get("prompt_tokens", 0) + row.get("completion_tokens", 0))
                total_tokens += t
                if row.get("ts", "").startswith(today):
                    tokens_today += t
            except (json.JSONDecodeError, KeyError):
                pass
    ix_total = self_data["ix_a_count"] + self_data["ix_b_count"] + self_data["ix_c_count"]
    tokens_per_ix = str(total_tokens // ix_total) if ix_total and total_tokens else "—"

    events_path = PROFILE_DIR / "PIPELINE-EVENTS.jsonl"
    pipeline_applied = pipeline_rejected = 0
    dyad_consultations_7d = dyad_integrations_7d = dyad_activity_reports_7d = 0
    cutoff_7d = datetime.now() - timedelta(days=7)

    def _in_window(ts_str: str) -> bool:
        if not ts_str:
            return False
        try:
            dt = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
            if dt.tzinfo:
                dt = dt.replace(tzinfo=None)
            return dt >= cutoff_7d
        except (ValueError, TypeError):
            return False

    if events_path.exists():
        for line in events_path.read_text().strip().splitlines():
            if not line:
                continue
            try:
                row = json.loads(line)
                e = row.get("event", "")
                ts = row.get("ts", "")
                if e == "applied" or e == "approved":
                    pipeline_applied += 1
                    if _in_window(ts):
                        dyad_integrations_7d += 1
                elif e == "rejected":
                    pipeline_rejected += 1
                elif e == "dyad:activity_report" and _in_window(ts):
                    dyad_activity_reports_7d += 1
                elif e in ("dyad:lookup", "dyad:grounded_query") and _in_window(ts):
                    dyad_consultations_7d += 1
            except json.JSONDecodeError:
                pass

    if dyad_consultations_7d == 0 and ledger_path.exists():
        for line in ledger_path.read_text().strip().splitlines():
            if not line:
                continue
            try:
                row = json.loads(line)
                if row.get("bucket") == "lookup_rephrase" and _in_window(row.get("ts", "")):
                    dyad_consultations_7d += 1
            except (json.JSONDecodeError, KeyError):
                pass

    total_decisions = pipeline_applied + pipeline_rejected
    curation_ratio = f"{100 * pipeline_applied // total_decisions}% approved" if total_decisions else "—"

    manifest_path = PROFILE_DIR / "FORK-MANIFEST.json"
    fork_checksum = ""
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text())
            fork_checksum = manifest.get("checksum", "")[:16] + "…" if manifest.get("checksum") else ""
        except (json.JSONDecodeError, KeyError):
            pass

    return DashboardData(
        name=self_data["name"],
        age=self_data["age"],
        lexile_output=self_data["lexile_output"],
        pending_count=pending_count,
        pending_candidates=pending_candidates,
        ix_a_count=self_data["ix_a_count"],
        ix_b_count=self_data["ix_b_count"],
        ix_c_count=self_data["ix_c_count"],
        write_count=evidence_data["write"],
        read_count=evidence_data["read"],
        create_count=evidence_data["create"],
        skills_summary=skills_summary,
        knowledge_samples=knowledge_samples,
        curiosity_samples=curiosity_samples,
        personality_samples=personality_samples,
        library_entries=library_entries,
        journal_entries=journal_entries,
        recent_exchanges=recent,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        last_pipeline_activity=last_activity,
        total_tokens=total_tokens,
        tokens_today=tokens_today,
        tokens_per_ix=tokens_per_ix,
        pipeline_applied=pipeline_applied,
        pipeline_rejected=pipeline_rejected,
        curation_ratio=curation_ratio,
        fork_checksum=fork_checksum,
        dyad_consultations_7d=dyad_consultations_7d,
        dyad_integrations_7d=dyad_integrations_7d,
        dyad_activity_reports_7d=dyad_activity_reports_7d,
    )


def render_html(data: DashboardData) -> str:
    """Render dashboard as self-contained HTML (fits viewport, no scroll)."""
    css = """
    :root { --bg: #1a1917; --surface: #252422; --text: #e8e6e3; --muted: #9c9a96; --accent: #88b4d4; --success: #6bcf7f; --warn: #e0b858; }
    * { box-sizing: border-box; }
    html, body { margin: 0; padding: 0; min-height: 100%; height: 100%; overflow: hidden; }
    body { font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif; background: var(--bg); color: var(--text); font-size: 14px; line-height: 1.5; padding: 0.5rem; padding-left: max(0.5rem, env(safe-area-inset-left)); padding-right: max(0.5rem, env(safe-area-inset-right)); padding-bottom: max(0.5rem, env(safe-area-inset-bottom)); }
    .dash { display: flex; flex-direction: column; gap: 0.4rem; height: 100vh; max-height: 100vh; min-height: 0; }
    .header { display: flex; align-items: center; gap: 1rem; flex-shrink: 0; }
    h1 { font-size: 1.25rem; margin: 0; }
    .meta { color: var(--muted); font-size: 0.9rem; }
    h2 { font-size: 0.9rem; color: var(--accent); margin: 0 0 0.25rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }
    section { background: var(--surface); border-radius: 8px; padding: 0.6rem 0.75rem; min-height: 0; overflow: hidden; display: flex; flex-direction: column; }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(80px, 1fr)); gap: 0.3rem; }
    .stat { background: var(--bg); padding: 0.35rem 0.5rem; border-radius: 4px; }
    .stat .label { font-size: 0.8rem; color: var(--muted); }
    .stat .value { font-size: 1.1rem; font-weight: 600; }
    .badge { display: inline-block; padding: 0.15rem 0.4rem; border-radius: 4px; font-size: 0.8rem; margin-right: 0.35rem; }
    .badge.pending { background: var(--warn); color: var(--bg); }
    .badge.ok { background: var(--success); color: var(--bg); }
    .badge.read { background: var(--success); color: var(--bg); }
    .badge.unread { background: var(--muted); color: var(--bg); }
    .lib-section { list-style: none; margin-left: -1.2rem; font-weight: 600; color: var(--accent); margin-top: 0.5rem; }
    .lib-section:first-child { margin-top: 0; }
    .volume { color: var(--muted); font-weight: normal; font-size: 0.9em; }
    .journal-day { margin-bottom: 0.75rem; }
    .journal-date { font-weight: 600; color: var(--accent); font-size: 0.9rem; margin-bottom: 0.2rem; }
    .journal-day p { margin: 0.25rem 0 0; font-size: 0.9rem; line-height: 1.5; }
    .candidate { padding: 0.25rem 0; font-size: 0.95rem; }
    .exchange { padding: 0.3rem 0; font-size: 0.9rem; border-bottom: 1px solid var(--bg); word-wrap: break-word; overflow-wrap: break-word; }
    .exchange:last-child { border-bottom: none; }
    .exchange-ts { font-size: 0.8rem; color: var(--muted); }
    .exchange .user { color: var(--muted); }
    .exchange .gm { color: var(--accent); }
    .skills-wrap { overflow-y: auto; max-height: 5rem; -webkit-overflow-scrolling: touch; }
    .skills-lexile { margin-bottom: 0.5rem; padding: 0.35rem 0; font-size: 0.95rem; }
    .skills-lexile .label { color: var(--muted); margin-right: 0.5rem; }
    .skills-lexile .value { font-weight: 600; color: var(--accent); }
    .skills-row { display: flex; gap: 0.5rem; flex-wrap: wrap; }
    .skill { flex: 1 1 160px; min-width: 0; background: var(--bg); padding: 0.45rem; border-radius: 6px; font-size: 0.95rem; }
    .skill .name { font-weight: 600; color: var(--accent); }
    .skill .edge { color: var(--muted); font-size: 0.85rem; }
    .tabs { display: flex; gap: 0.3rem; margin-bottom: 0.3rem; flex-shrink: 0; overflow-x: auto; -webkit-overflow-scrolling: touch; flex-wrap: nowrap; padding-bottom: 2px; }
    .tab { padding: 0.35rem 0.65rem; font-size: 0.85rem; background: var(--bg); border-radius: 6px; cursor: pointer; color: var(--muted); border: 1px solid transparent; white-space: nowrap; flex-shrink: 0; }
    .tab:hover { color: var(--text); }
    .tab.active { color: var(--accent); background: var(--surface); border-color: var(--accent); cursor: default; }
    .tab-content { flex: 1; min-height: 0; display: flex; flex-direction: column; overflow: hidden; }
    .tab-panel { display: none; flex: 1; min-height: 0; flex-direction: column; overflow: hidden; }
    .tab-panel.active { display: flex; }
    .tab-panel ul { margin: 0; padding-left: 1.2rem; overflow-y: auto; flex: 1; min-height: 0; -webkit-overflow-scrolling: touch; font-size: 0.9rem; }
    .tab-panel li { margin-bottom: 0.3rem; word-wrap: break-word; overflow-wrap: break-word; }
    .tab-panel.skills-panel { display: none; flex-direction: column; overflow: hidden; }
    .tab-panel.skills-panel.active { display: flex; }
    .tab-panel .skills-row { flex-wrap: wrap; gap: 0.5rem; overflow-y: auto; flex: 1; min-height: 0; -webkit-overflow-scrolling: touch; }
    .panel-scroll { overflow-y: auto; min-height: 0; -webkit-overflow-scrolling: touch; }
    .row-main { display: grid; grid-template-columns: 2fr 1fr; gap: 0.4rem; min-height: 0; flex: 1; overflow: hidden; }
    .col-left { display: flex; flex-direction: column; gap: 0.4rem; min-height: 0; overflow: hidden; }
    .col-right { display: flex; flex-direction: column; gap: 0.4rem; min-height: 0; overflow: hidden; }
    @media (max-width: 600px) {{
      body {{ font-size: 13px; padding: 0.4rem; }}
      .row-main {{ grid-template-columns: 1fr; grid-template-rows: 1fr auto; }}
      .col-left {{ min-height: 200px; }}
      .col-right {{ min-height: 0; }}
      .header {{ flex-wrap: wrap; gap: 0.3rem; }}
      .meta {{ font-size: 0.8rem; }}
      h2 {{ font-size: 0.85rem; }}
      section {{ padding: 0.5rem 0.6rem; }}
      .tab {{ font-size: 0.8rem; padding: 0.3rem 0.5rem; }}
      .stat .value {{ font-size: 1rem; }}
      .grid {{ grid-template-columns: repeat(3, 1fr); }}
    }}
    """

    skills_html = "".join(
        f'<div class="skill"><span class="name">{k}</span> {v["status"]}'
        + (f'<div class="edge">{v["edge"]}</div>' if v.get("edge") else '')
        + '</div>'
        for k, v in data.skills_summary.items()
    )

    exchanges_html = "".join(
        f'<div class="exchange">'
        f'<div class="exchange-ts">{e["timestamp"]}</div>'
        f'<div class="user">USER: {e["user"]}</div>'
        f'<div class="gm">GRACE-MAR: {e["grace_mar"]}</div>'
        f'</div>'
        for e in reversed(data.recent_exchanges)
    )

    k_samples = "".join(f'<li>{s}</li>' for s in data.knowledge_samples) or '<li class="meta">—</li>'
    c_samples = "".join(f'<li>{s}</li>' for s in data.curiosity_samples) or '<li class="meta">—</li>'
    p_samples = "".join(f'<li>{s}</li>' for s in data.personality_samples) or '<li class="meta">—</li>'
    read_entries = [e for e in data.library_entries if e.get("read_status") == "read"]
    unread_entries = [e for e in data.library_entries if e.get("read_status") != "read"]

    def _lib_label(e: dict) -> str:
        if e.get("volume"):
            return f'{e["title"]} <span class="volume">({e["volume"]})</span>'
        return e["title"]

    lib_read = "".join(f'<li><span class="badge read">read</span> {_lib_label(e)}</li>' for e in read_entries)
    lib_unread = "".join(f'<li><span class="badge unread">unread</span> {_lib_label(e)}</li>' for e in unread_entries)
    lib_samples = (
        (f'<li class="lib-section">Read ({len(read_entries)})</li>{lib_read}'
         f'<li class="lib-section">Unread ({len(unread_entries)})</li>{lib_unread}')
        if data.library_entries
        else '<li class="meta">—</li>'
    )

    def _journal_entry_html(e: dict) -> str:
        entry_text = e.get("entry", "")
        # Preserve paragraphs (double newline) as separate <p>
        paras = [
            f'<p>{p.strip()}</p>' for p in entry_text.split("\n\n") if p.strip()
        ] if entry_text else []
        if not paras:
            paras = ['<p class="meta">—</p>']
        return f'<div class="journal-day"><div class="journal-date">{e["date"]}</div>{"".join(paras)}</div>'

    journal_html = "".join(
        _journal_entry_html(e) for e in reversed(data.journal_entries)
    ) if data.journal_entries else '<p class="meta">—</p>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
    <title>Grace-Mar — {data.name}</title>
    <style>{css}</style>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
</head>
<body>
    <div class="dash">
        <div class="header">
            <h1>{data.name}</h1>
            <span class="meta">{data.generated_at} · pilot-001</span>
        </div>
        <div class="row-main">
            <div class="col-left">
                <section style="flex:1; min-height:0;">
                    <h2>Profile</h2>
                    <div class="tabs">
                        <button class="tab active" data-tab="knowledge">Knowledge</button>
                        <button class="tab" data-tab="skills">Skills</button>
                        <button class="tab" data-tab="curiosity">Curiosity</button>
                        <button class="tab" data-tab="personality">Personality</button>
                        <button class="tab" data-tab="library">Library</button>
                        <button class="tab" data-tab="journal">Journal</button>
                        <button class="tab" data-tab="disclosure">Disclosure</button>
                    </div>
                    <div class="tab-content">
                        <div class="tab-panel active" id="panel-knowledge"><ul>{k_samples}</ul></div>
                        <div class="tab-panel skills-panel" id="panel-skills"><div class="skills-lexile"><span class="label">Lexile output</span> <span class="value">{data.lexile_output}</span></div><div class="skills-row">{skills_html}</div></div>
                        <div class="tab-panel" id="panel-curiosity"><ul>{c_samples}</ul></div>
                        <div class="tab-panel" id="panel-personality"><ul>{p_samples}</ul></div>
                        <div class="tab-panel" id="panel-library"><ul>{lib_samples}</ul></div>
                        <div class="tab-panel" id="panel-journal"><div class="journal-entries">{journal_html}</div></div>
                        <div class="tab-panel" id="panel-disclosure" style="flex-direction:column; overflow-y:auto;">
                            <p><strong>What&rsquo;s in the fork</strong></p>
                            <ul>
                                <li>Identity, Lexile ({data.lexile_output}), IX-A/B/C counts: {data.ix_a_count} / {data.ix_b_count} / {data.ix_c_count}</li>
                                <li>Only content that passed the gated pipeline (staged → user approval → profile update)</li>
                            </ul>
                            <p><strong>Knowledge boundary</strong></p>
                            <ul>
                                <li>The emulated self knows only what is documented in its profile (SELF.md). No LLM training data.</li>
                            </ul>
                            <p><strong>Attestation</strong></p>
                            <ul>
                                <li>Last checksum: {data.fork_checksum or "— (run scripts/fork_checksum.py --manifest)"}</li>
                                <li>Harness: run Counterfactual Pack to verify knowledge boundary.</li>
                            </ul>
                        </div>
                    </div>
                </section>
            </div>
            <div class="col-right">
                <section style="flex:1; min-height:0; overflow:hidden; display:flex; flex-direction:column;">
                    <h2>Recent exchanges</h2>
                    <div class="panel-scroll" style="flex:1;">{exchanges_html or '<p class="meta">—</p>'}</div>
                </section>
                <section>
                    <h2>Benchmarks</h2>
                    <div class="grid">
                        <div class="stat"><div class="label">Lexile</div><div class="value">{data.lexile_output}</div></div>
                        <div class="stat"><div class="label">Backlog</div><div class="value">{data.pending_count}</div></div>
                        <div class="stat"><div class="label">IX total</div><div class="value">{data.ix_a_count + data.ix_b_count + data.ix_c_count}</div></div>
                        <div class="stat"><div class="label">Last pipeline activity</div><div class="value">{data.last_pipeline_activity}</div></div>
                        <div class="stat"><div class="label">Tokens today</div><div class="value">{data.tokens_today:,}</div></div>
                        <div class="stat"><div class="label">Tokens total</div><div class="value">{data.total_tokens:,}</div></div>
                        <div class="stat"><div class="label">Tokens/IX</div><div class="value">{data.tokens_per_ix}</div></div>
                        <div class="stat"><div class="label">Curation</div><div class="value">{data.curation_ratio}</div></div>
                        <div class="stat"><div class="label">Approved / Rejected</div><div class="value">{data.pipeline_applied} / {data.pipeline_rejected}</div></div>
                        <div class="stat"><div class="label">Consultations (7d)</div><div class="value">{data.dyad_consultations_7d}</div></div>
                        <div class="stat"><div class="label">Integrations (7d)</div><div class="value">{data.dyad_integrations_7d}</div></div>
                        <div class="stat"><div class="label">Activity reports (7d)</div><div class="value">{data.dyad_activity_reports_7d}</div></div>
                    </div>
                </section>
            </div>
        </div>
    </div>
    <script>
    (function() {{
        function switchTab(tabId) {{
            var tab = document.querySelector('.tab[data-tab="' + tabId + '"]');
            var panel = document.getElementById('panel-' + tabId);
            if (tab && panel) {{
                document.querySelectorAll('.tab').forEach(function(b) {{ b.classList.remove('active'); }});
                document.querySelectorAll('.tab-panel').forEach(function(p) {{ p.classList.remove('active'); }});
                tab.classList.add('active');
                panel.classList.add('active');
            }}
        }}
        document.querySelectorAll('.tab').forEach(function(btn) {{
            btn.addEventListener('click', function() {{ switchTab(this.dataset.tab); }});
        }});
        if (window.Telegram && window.Telegram.WebApp) {{
            var w = window.Telegram.WebApp;
            w.ready();
            w.expand();
            var tp = w.themeParams;
            if (tp && (tp.bg_color || tp.secondary_bg_color)) {{
                var s = document.createElement('style');
                s.textContent = ':root{{' +
                    (tp.bg_color ? '--bg:' + tp.bg_color + ';' : '') +
                    (tp.secondary_bg_color ? '--surface:' + tp.secondary_bg_color + ';' : '') +
                    (tp.text_color ? '--text:' + tp.text_color + ';' : '') +
                    (tp.hint_color ? '--muted:' + tp.hint_color + ';' : '') +
                    (tp.button_color ? '--accent:' + tp.button_color + ';' : '') +
                '}}';
                document.head.appendChild(s);
            }}
            var start = w.initDataUnsafe && w.initDataUnsafe.start_param;
            if (start) switchTab(start);
        }}
    }})();
    </script>
</body>
</html>
"""


def main() -> None:
    data = collect_data()
    html = render_html(data)
    DASHBOARD_DIR.mkdir(exist_ok=True)
    out_path = DASHBOARD_DIR / "index.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"Dashboard written to {out_path}")


if __name__ == "__main__":
    main()
