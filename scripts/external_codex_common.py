"""Shared deterministic helpers for external codex explorer scripts (grace-mar WORK-only)."""

from __future__ import annotations

from pathlib import Path

MAX_READ_TITLE_BYTES = 8192


def posix_relative(base: Path, target: Path) -> str:
    return target.relative_to(base).as_posix()


def reject_dotgit(path: Path) -> None:
    if ".git" in path.parts:
        raise ValueError(f"path resolves under .git (forbidden): {path}")


def is_inside_checkout(checkout_res: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(checkout_res)
        return True
    except ValueError:
        return False


def resolve_subject_under_checkout(checkout: Path, subject_rel: str) -> Path:
    """Return absolute Path to subject; raise ValueError if traversal or outside checkout."""
    if not checkout.is_dir():
        raise ValueError(f"checkout is not a directory: {checkout}")
    rel = Path(subject_rel.replace("\\", "/"))
    if rel.is_absolute():
        raise ValueError("subject must be relative to checkout")
    if ".." in rel.parts:
        raise ValueError("subject must not contain path traversal (..)")
    full = (checkout / rel).resolve()
    checkout_res = checkout.resolve()
    try:
        full.relative_to(checkout_res)
    except ValueError as e:
        raise ValueError("subject escapes checkout root") from e
    reject_dotgit(full)
    if not full.exists():
        raise ValueError(f"subject path does not exist: {full}")
    return full


def resolve_repo_path(repo_root: Path, repo_path: str | Path) -> Path:
    """Resolve external codex checkout directory relative to repo_root or absolute."""
    p = Path(repo_path)
    if p.is_absolute():
        out = p.resolve()
    else:
        out = (repo_root / p).resolve()
    if not out.is_dir():
        raise ValueError(f"--repo-path is not a directory: {out}")
    reject_dotgit(out)
    return out


def civilization_token_from_path(path_rel: str) -> str | None:
    parts = path_rel.replace("\\", "/").split("/")
    try:
        i = parts.index("civilizations")
        if i + 1 < len(parts) and parts[i + 1]:
            return parts[i + 1]
    except ValueError:
        pass
    return None


def infer_file_class(filename: str) -> str:
    if filename.startswith("MEM--"):
        return "memory_spine"
    if filename.startswith("CIV--STATE--"):
        return "civ_state"
    if filename.startswith("CIV--INDEX--"):
        return "civ_index"
    if filename.startswith("CIV--"):
        return "civ_marker"
    if "TEMPLATE" in filename.upper():
        return "template_marker"
    if filename.upper().startswith("README"):
        return "readme"
    return "other"


def is_index_core_scholar_path(path_rel: str, basename: str) -> bool:
    pl = path_rel.lower()
    bu = basename.upper()
    if "/minds/" in pl or "scholar" in pl:
        return True
    if bu.startswith("MEM--") or "INDEX" in bu or "STATE--" in bu:
        return True
    return False


def is_governance_template_path(path_rel: str, basename: str) -> bool:
    pl = path_rel.lower()
    bu = basename.upper()
    if "/templates/" in pl or "TEMPLATE" in bu:
        return True
    return False


def extract_markdown_title(abs_path: Path) -> str | None:
    if not abs_path.is_file():
        return None
    try:
        raw = abs_path.read_text(encoding="utf-8", errors="replace")[:MAX_READ_TITLE_BYTES]
    except OSError:
        return None
    for line in raw.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return None


def compute_neighbor_edges(
    checkout: Path,
    subject: Path,
) -> tuple[list[tuple[str, str]], list[str]]:
    """Structural peers (posix relative path, edge kind); deduped by path (same rules as neighborhood)."""
    warnings: list[str] = []
    checkout_res = checkout.resolve()
    subject = subject.resolve()
    raw: list[tuple[str, str]] = []

    def list_visible(directory: Path) -> list[Path]:
        out: list[Path] = []
        if not directory.is_dir():
            return out
        try:
            for entry in sorted(directory.iterdir(), key=lambda p: p.name.lower()):
                if entry.name.startswith("."):
                    continue
                ent_res = entry.resolve()
                try:
                    ent_res.relative_to(checkout_res)
                except ValueError:
                    continue
                if ".git" in ent_res.parts:
                    continue
                out.append(entry)
        except OSError as e:
            warnings.append(f"listdir failed for {directory}: {e}")
        return out

    if subject.is_file():
        container = subject.parent
        sub_name = subject.name
        peers = list_visible(container)
        for p in peers:
            if p.name == sub_name:
                continue
            raw.append((posix_relative(checkout_res, p.resolve()), "same_directory"))
        parent = container.parent
        if is_inside_checkout(checkout_res, parent):
            for p in list_visible(parent):
                raw.append((posix_relative(checkout_res, p.resolve()), "parent_directory"))
    elif subject.is_dir():
        for p in list_visible(subject):
            raw.append((posix_relative(checkout_res, p.resolve()), "same_directory"))
        parent = subject.parent
        if is_inside_checkout(checkout_res, parent):
            subj_name = subject.name
            for p in list_visible(parent):
                if p.name == subj_name:
                    continue
                raw.append((posix_relative(checkout_res, p.resolve()), "parent_directory"))
    else:
        raise ValueError(f"subject is neither file nor directory: {subject}")

    seen: set[str] = set()
    deduped: list[tuple[str, str]] = []
    for path_rel, edge in sorted(raw, key=lambda x: (x[0], x[1])):
        if path_rel in seen:
            continue
        seen.add(path_rel)
        deduped.append((path_rel, edge))
    return deduped, warnings


def compute_neighbor_relative_paths(
    checkout: Path,
    subject: Path,
) -> tuple[list[str], list[str]]:
    """Deduped neighbor posix paths only (same semantics as neighborhood membership sweep)."""
    edges, warnings = compute_neighbor_edges(checkout, subject)
    return [pr for pr, _ in edges], warnings


def checkout_relative_to_repo(repo_root: Path, checkout: Path) -> str:
    """Best-effort posix path string for reports."""
    cr = checkout.resolve()
    rr = repo_root.resolve()
    try:
        return cr.relative_to(rr).as_posix()
    except ValueError:
        return str(cr)
