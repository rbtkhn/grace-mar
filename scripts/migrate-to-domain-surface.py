#!/usr/bin/env python3
"""
Migrate work-* domains: create <DOMAIN>.md from _template/DOMAIN.md (dry-run by default).

Usage:
  python3 scripts/migrate-to-domain-surface.py
  python3 scripts/migrate-to-domain-surface.py --execute
  python3 scripts/migrate-to-domain-surface.py --execute --domain politics
"""

from __future__ import annotations

import argparse
import shutil
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from _domain_surface_links import (
    assert_domain_surface_links_rebased,
    rebase_domain_surface_markdown,
)

REPO_ROOT = _SCRIPT_DIR.parent
TEMPLATE_PATH = REPO_ROOT / '_template' / 'DOMAIN.md'
SKILL_WORK = REPO_ROOT / 'docs' / 'skill-work'


def _slug_from_work_dir(name: str) -> str:
    if not name.startswith('work-'):
        return ''
    return name[5:].lower()


def _domain_upper(slug: str) -> str:
    return slug.upper()


def _title_case(slug: str) -> str:
    return slug.replace('-', ' ').title()


def discover_domain_dirs(
    roots: list[Path],
) -> tuple[list[Path], list[tuple[Path, Path]]]:
    by_slug: dict[str, list[Path]] = defaultdict(list)
    for root in roots:
        if not root.is_dir():
            continue
        for child in sorted(root.iterdir(), key=lambda p: p.name):
            if not child.is_dir():
                continue
            if not child.name.startswith('work-'):
                continue
            slug = _slug_from_work_dir(child.name)
            if not slug:
                continue
            by_slug[slug].append(child)

    chosen: list[Path] = []
    warnings: list[tuple[Path, Path]] = []
    skill_resolved = SKILL_WORK.resolve()

    for slug in sorted(by_slug.keys()):
        dirs = by_slug[slug]
        if len(dirs) == 1:
            chosen.append(dirs[0])
            continue
        preferred = [d for d in dirs if d.parent.resolve() == skill_resolved]
        if preferred:
            keep = preferred[0]
            chosen.append(keep)
            for d in dirs:
                if d.resolve() != keep.resolve():
                    warnings.append((d, keep))
        else:
            chosen.append(dirs[0])
            for d in dirs[1:]:
                warnings.append((d, dirs[0]))

    return chosen, warnings


def migrate_one(
    domain_dir: Path,
    *,
    execute: bool,
    backup_root: Path,
    user_id: str,
    single_domain: bool = False,
) -> tuple[bool, bool]:
    """Returns (ok, would_create_or_created)."""
    slug = _slug_from_work_dir(domain_dir.name)
    dom_upper = _domain_upper(slug)
    target = domain_dir / f'{dom_upper}.md'

    if slug == 'strategy':
        legacy = domain_dir / 'civilizational-strategy-surface.md'
        if not target.is_file() and legacy.is_file():
            print(
                f'SKIP {domain_dir.name}: rename legacy to STRATEGY.md first:\n'
                f'  git mv {legacy.relative_to(REPO_ROOT)} '
                f'{target.relative_to(REPO_ROOT)}',
                file=sys.stderr,
            )
            return (False, False) if single_domain else (True, False)

    if target.is_file():
        print(f'SKIP {target.relative_to(REPO_ROOT)} (already exists)')
        return True, False

    if not TEMPLATE_PATH.is_file():
        print(f'ERROR missing template {TEMPLATE_PATH}', file=sys.stderr)
        return False, False

    content = TEMPLATE_PATH.read_text(encoding='utf-8')
    content = content.replace('{{DOMAIN}}', dom_upper)
    content = content.replace('{{DOMAIN_LOWER}}', slug)
    content = content.replace('{{DOMAIN_TITLE}}', _title_case(slug))
    content = rebase_domain_surface_markdown(content, target, REPO_ROOT, user_id=user_id)
    assert_domain_surface_links_rebased(content, target)

    rel = target.relative_to(REPO_ROOT)
    if not execute:
        print(f'[dry-run] would create {rel}')
        return True, True

    backup_root.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    backup_dest = backup_root / f'{domain_dir.name}_backup_{ts}'
    shutil.copytree(domain_dir, backup_dest)
    print(f'backup: {backup_dest.relative_to(REPO_ROOT)}')

    target.write_text(content, encoding='utf-8')
    print(f'created: {rel}')
    return True, True


def main() -> int:
    parser = argparse.ArgumentParser(
        description='Create <DOMAIN>.md from _template/DOMAIN.md for work-* dirs (dry-run default)'
    )
    parser.add_argument(
        '--execute',
        action='store_true',
        help='Write files and backups (default is dry-run only)',
    )
    parser.add_argument('--domain', type=str, default=None, help='Only work-<slug> (e.g. politics)')
    parser.add_argument(
        '--roots',
        action='append',
        default=None,
        help='Extra root to scan (repeatable). Default: docs/skill-work',
    )
    parser.add_argument(
        '--include-root-work',
        action='store_true',
        help='Also scan repo root for work-* directories',
    )
    parser.add_argument(
        '--backup-root',
        type=Path,
        default=None,
        help='Backup parent directory (default: REPO_ROOT/backups/domain-migration)',
    )
    parser.add_argument(
        '--user-id',
        type=str,
        default='grace-mar',
        help='users/<id>/self.md link target (default grace-mar)',
    )
    args = parser.parse_args()

    roots: list[Path] = []
    if args.roots:
        for r in args.roots:
            roots.append((REPO_ROOT / r).resolve())
    else:
        roots.append(SKILL_WORK.resolve())
    if args.include_root_work:
        roots.append(REPO_ROOT.resolve())

    backup_root = (
        args.backup_root.resolve()
        if args.backup_root
        else (REPO_ROOT / 'backups' / 'domain-migration')
    )

    if args.domain:
        slug = args.domain.strip().lower()
        domain_dir = None
        for root in roots:
            cand = root / f'work-{slug}'
            if cand.is_dir():
                domain_dir = cand
                break
        if domain_dir is None:
            print(f'ERROR work-{slug} not found under roots', file=sys.stderr)
            return 1
        ok, _ = migrate_one(
            domain_dir,
            execute=args.execute,
            backup_root=backup_root,
            user_id=args.user_id,
            single_domain=True,
        )
        return 0 if ok else 1

    chosen, warns = discover_domain_dirs(roots)
    for skipped, kept in warns:
        print(
            f'WARN duplicate slug: skip {skipped.relative_to(REPO_ROOT)} '
            f'(prefer {kept.relative_to(REPO_ROOT)})',
            file=sys.stderr,
        )

    if not chosen:
        print('No work-* directories found.')
        return 0

    mode = 'EXECUTE' if args.execute else 'DRY-RUN'
    print(f'{mode}: {len(chosen)} domain dir(s)\n')
    n_would = 0
    for d in sorted(chosen, key=lambda p: p.name):
        ok, would = migrate_one(
            d,
            execute=args.execute,
            backup_root=backup_root,
            user_id=args.user_id,
            single_domain=False,
        )
        if not ok:
            return 1
        if would:
            n_would += 1

    if not args.execute:
        print(f'\nDry-run complete ({n_would} would create). Use --execute to apply.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
