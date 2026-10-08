#!/usr/bin/env python3
"""Manifest reader and conservative installer. Python standard library only."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import sys
import tempfile
import textwrap
from datetime import datetime, timezone
from uuid import uuid4


class SkillError(Exception):
    pass


def within(path, parent):
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def exists(path):
    return os.path.lexists(path)


def linklike(path):
    if path.is_symlink() or getattr(path, "is_junction", lambda: False)():
        return True
    if os.name == "nt" and exists(path):
        # Python 3.9-3.11 lack Path.is_junction; catch reparse points too.
        return bool(path.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
    return False


def require_real_parents(path):
    # Linked roots could redirect writes into the source or an unrelated tree.
    for part in (path, *path.parents):
        if linklike(part):
            raise SkillError(f"linked directory is not an installation root: {part}")
        if exists(part) and not part.is_dir():
            raise SkillError(f"installation parent is not a directory: {part}")


def manifest_skills(repo):
    repo = repo.resolve(strict=True)
    try:
        data = json.loads((repo / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise SkillError(f"cannot read manifest: {exc}") from exc
    entries = data.get("skills") if isinstance(data, dict) else None
    if not isinstance(entries, list) or not entries:
        raise SkillError("manifest field .skills must be a nonempty array")
    skills, names, paths = [], set(), set()
    for entry in entries:
        if not isinstance(entry, str) or not entry or "\\" in entry or "\n" in entry or "\r" in entry:
            raise SkillError(f"invalid manifest skill entry: {entry!r}")
        relative = PurePosixPath(entry)
        if relative.is_absolute() or ".." in relative.parts or relative.parts[0] != "skills":
            raise SkillError(f"manifest skill escapes skills directory: {entry}")
        source = repo.joinpath(*relative.parts)
        try:
            resolved = source.resolve(strict=True)
        except (OSError, RuntimeError) as exc:
            raise SkillError(f"manifest skill does not exist: {entry}") from exc
        if not within(resolved, repo / "skills") or not (source / "SKILL.md").is_file():
            raise SkillError(f"manifest skill escapes repo or is missing SKILL.md: {entry}")
        name = source.name
        if len(name) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            raise SkillError(f"invalid portable skill name: {name}")
        if name in names or resolved in paths:
            raise SkillError(f"duplicate manifest skill: {entry}")
        if linklike(source) or any(linklike(p) for p in source.rglob("*")):
            raise SkillError(f"public skill contains a link: {entry}")
        names.add(name)
        paths.add(resolved)
        skills.append((name, relative.as_posix(), source))
    return skills


def tree_signature(path):
    """Compare names, types and bytes, including unexpected local files."""
    if not path.is_dir():
        return None
    result = []
    for item in sorted(path.rglob("*")):
        relative = item.relative_to(path).as_posix()
        if linklike(item):
            return None
        if item.is_file():
            result.append((relative, "file", hashlib.sha256(item.read_bytes()).hexdigest()))
        elif item.is_dir():
            result.append((relative, "dir"))
        else:
            return None
    return result


def matches(target, source):
    if target.is_symlink():
        try:
            return target.resolve(strict=True) == source.resolve(strict=True)
        except (OSError, RuntimeError):
            return False
    if linklike(target):
        return False
    return target.is_dir() and tree_signature(target) == tree_signature(source)


def project_parents(project):
    current = project.resolve()
    while True:
        yield current
        if (current / ".git").exists() or current.parent == current:
            break
        current = current.parent


def discovery_roots(runtime, home, codex_home, project, config_home, pi_home):
    # Check all consumers of the destination, including OpenCode's Claude root.
    global_roots = {
        "codex": [home / ".agents/skills", codex_home / "skills"],
        "claude": [home / ".claude/skills"],
        "pi": [home / ".agents/skills", pi_home / "skills"],
        "opencode": [home / ".agents/skills", home / ".claude/skills", config_home / "opencode/skills"],
        "kiro": [home / ".kiro/skills"],
    }
    local_roots = {
        "codex": [".agents/skills", ".codex/skills"],
        "claude": [".claude/skills"],
        "pi": [".agents/skills", ".pi/skills"],
        "opencode": [".agents/skills", ".claude/skills", ".opencode/skills"],
        "kiro": [".kiro/skills"],
    }
    runtimes = {"shared": ["codex", "pi", "opencode"],
                "claude": ["claude", "opencode"]}.get(runtime, [runtime])
    roots = set()
    for tool in runtimes:
        roots.update(global_roots[tool])
        for parent in project_parents(project):
            roots.update(parent / suffix for suffix in local_roots[tool])
    return sorted(roots, key=str)


def declared_name(skill_md):
    # Read single-line YAML string scalars without a third-party dependency.
    # Ambiguous YAML must stop preflight rather than hide a possible duplicate.
    content = skill_md.read_text(encoding="utf-8-sig")
    if not content.startswith("---\n"):
        return skill_md.parent.name
    closing = re.search(r"^---\s*$", content[4:], re.MULTILINE)
    if not closing:
        raise SkillError(f"unclosed skill frontmatter: {skill_md}")
    header = content[4:4 + closing.start()]
    # YAML permits a uniformly indented top-level mapping; comments need not
    # share that indentation. Nested keys stay indented after this operation.
    header = textwrap.dedent("\n".join("" if line.lstrip().startswith("#") else line
                                     for line in header.splitlines()))
    matches = re.findall(r"^(?:name|\"name\"|'name')[ \t]*:[ \t]*(.*)$", header, re.MULTILINE)
    if not matches:
        return skill_md.parent.name
    if len(matches) != 1:
        raise SkillError(f"duplicate name fields: {skill_md}")
    value = matches[0].strip()
    if value.startswith("'"):
        match = re.fullmatch(r"'((?:[^']|'')*)'(?:[ \t]+#.*)?", value)
        if match:
            return match[1].replace("''", "'") or skill_md.parent.name
    elif value.startswith('"'):
        match = re.fullmatch(r'("(?:[^"\\]|\\.)*")(?:[ \t]+#.*)?', value)
        if match:
            try:
                return json.loads(match[1]) or skill_md.parent.name
            except ValueError:
                pass
    else:
        value = re.split(r"[ \t]+#", value, maxsplit=1)[0].strip()
        if not value or value.startswith("#") or value in ("null", "Null", "NULL", "~", "true", "false", "True", "False", "TRUE", "FALSE"):
            return skill_md.parent.name
        if value[0] not in "&*!|>{[" and not re.search(r":[ \t]", value):
            return value
    raise SkillError(f"cannot safely inspect YAML skill name; use a single-line string scalar: {skill_md}")


def discovered_skills(root):
    if not root.is_dir():
        return
    seen = set()
    def fail(exc):
        raise SkillError(f"cannot inspect skill discovery root: {exc}")
    for directory, dirs, files in os.walk(root, followlinks=True, onerror=fail):
        folder = Path(directory)
        resolved = folder.resolve()
        if resolved in seen:
            dirs[:] = []
            continue
        seen.add(resolved)
        if "SKILL.md" in files:
            yield declared_name(folder / "SKILL.md"), folder


def install(args):
    repo = Path(args.repo).resolve(strict=True)
    skills = manifest_skills(repo)  # Validate the entire bundle before any writes.
    home = Path(args.home).absolute()
    codex_home = Path(args.codex_home).absolute() if args.codex_home else home / ".codex"
    config_home = Path(args.config_home).absolute() if args.config_home else home / ".config"
    pi_home = Path(args.pi_home).absolute() if args.pi_home else home / ".pi/agent"
    destinations = {"shared": home / ".agents/skills", "codex": codex_home / "skills",
                    "claude": home / ".claude/skills", "kiro": home / ".kiro/skills"}
    dest = destinations[args.runtime]
    roots = discovery_roots(args.runtime, home, codex_home, Path(args.project), config_home, pi_home)
    names = {name for name, _, _ in skills}
    replace = set(args.replace)
    if not replace <= names:
        raise SkillError(f"--replace is not a published skill: {', '.join(sorted(replace - names))}")
    require_real_parents(dest)
    if within(dest.resolve(), repo) or within(repo, dest.resolve()):
        raise SkillError("installation destination overlaps the source repository")
    backup_base = dest.parent / "agent-skills-backups" / args.runtime
    require_real_parents(backup_base)
    if any(within(backup_base.resolve(), root.resolve()) for root in roots):
        raise SkillError("backup directory is inside a skill discovery root")
    conflicts, planned, unchanged = [], [], []
    for root in roots:
        for name, folder in discovered_skills(root):
            if name in names and folder.absolute() != (dest / name).absolute():
                conflicts.append(f"duplicate {name} in searched location: {folder}")
    for name, _, source in skills:
        target = dest / name
        if exists(target) and matches(target, source):
            unchanged.append(name)
        elif exists(target) and name not in replace:
            conflicts.append(f"{name}: {target} exists; preserve it or use --replace {name}")
        else:
            planned.append((name, source, target, exists(target)))
    if conflicts:
        raise SkillError("conflicts; nothing installed:\n  " + "\n  ".join(conflicts))
    for name in unchanged:
        print(f"unchanged {name}")
    if not planned:
        return
    # Stage outside discovery roots. A failed symlink preflight changes no skills.
    dest.parent.mkdir(parents=True, exist_ok=True)
    stage_root = Path(tempfile.mkdtemp(prefix=".agent-skills-stage-", dir=dest.parent))
    try:
        for name, source, _, _ in planned:
            staged = stage_root / name
            if args.copy or args.runtime == "kiro":
                shutil.copytree(source, staged)
                if not matches(staged, source):
                    raise SkillError(f"copy verification failed: {name}")
            else:
                try:
                    staged.symlink_to(source, target_is_directory=True)
                except OSError as exc:
                    raise SkillError(f"cannot create real symlinks; retry with --copy: {exc}") from exc
                if not staged.is_symlink() or not matches(staged, source):
                    raise SkillError(f"link is not a real symlink: {name}; retry with --copy")
        dest.mkdir(parents=True, exist_ok=True)
        moved = []
        try:
            for name, source, target, replacing in planned:
                if exists(target) != replacing:
                    raise SkillError(f"destination changed during installation: {target}; retry after inspection")
                step = {"name": name, "source": source, "target": target, "backup": None, "installed": False}
                moved.append(step)
                if replacing:
                    backup = backup_base / (datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid4().hex[:8]) / name
                    backup.parent.mkdir(parents=True, exist_ok=False)
                    target.rename(backup)  # Same volume; preserves directories and links.
                    step["backup"] = backup
                (stage_root / name).rename(target)
                step["installed"] = True
        except (OSError, SkillError) as exc:
            failures = []
            for step in reversed(moved):
                try:
                    target, backup = step["target"], step["backup"]
                    if step["installed"]:
                        if not matches(target, step["source"]):
                            raise SkillError(f"rollback target changed; preserving target and backup: {target}")
                        target.rename(stage_root / step["name"])
                    if backup is not None:
                        if exists(target):
                            raise SkillError(f"rollback target occupied; backup retained: {backup}")
                        backup.rename(target)
                except (OSError, SkillError) as failure:
                    failures.append(str(failure))
            if failures:
                raise SkillError(f"installation failed: {exc}; rollback incomplete; " + "; ".join(failures)) from exc
            raise SkillError(f"installation failed; changes rolled back: {exc}") from exc
        for step in moved:
            name, target, backup = step["name"], step["target"], step["backup"]
            if backup is not None:
                print(f"backup {name} -> {backup}")
            mode = "copied" if args.copy or args.runtime == "kiro" else "linked"
            print(f"{mode} {name} -> {target}")
    finally:
        # Remove only the staging directory this invocation created.
        if stage_root.parent == dest.parent and not linklike(stage_root):
            shutil.rmtree(stage_root)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("paths", "list", "install"):
        p = sub.add_parser(command)
        p.add_argument("--repo", required=True)
        if command == "install":
            p.add_argument("--runtime", choices=("shared", "codex", "claude", "kiro"), required=True)
            p.add_argument("--home", required=True)
            p.add_argument("--project", required=True)
            p.add_argument("--codex-home")
            p.add_argument("--config-home")
            p.add_argument("--pi-home")
            p.add_argument("--copy", action="store_true", help="copy instead of linking (Kiro always copies)")
            p.add_argument("--replace", action="append", default=[], metavar="SKILL_NAME",
                           help="back up and replace this destination skill; repeat for multiple skills")
    args = parser.parse_args()
    try:
        if args.command == "install":
            install(args)
        else:
            skills = manifest_skills(Path(args.repo))
            lines = [relative + ("/SKILL.md" if args.command == "list" else "") for _, relative, _ in skills]
            print("\n".join(sorted(lines) if args.command == "list" else lines))
    except (SkillError, OSError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
