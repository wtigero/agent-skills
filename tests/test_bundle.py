"""Portable package and installer checks; no provider calls or real HOME writes."""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import importlib.util

REPO = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("skills", REPO / "scripts/skills.py")
SKILLS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SKILLS)
BASH = os.environ.get("BASH_EXE") or (
    r"C:\Program Files\Git\bin\bash.exe" if os.name == "nt" and Path(r"C:\Program Files\Git\bin\bash.exe").is_file()
    else shutil.which("bash"))


class BundleTests(unittest.TestCase):
    def test_public_metadata_and_references(self):
        skills = SKILLS.manifest_skills(REPO)
        self.assertEqual(len(skills), 6)
        for name, relative, source in skills:
            with self.subTest(skill=name):
                text = (source / "SKILL.md").read_text(encoding="utf-8")
                self.assertTrue(text.startswith("---\n"))
                header = text.split("---", 2)[1]
                self.assertEqual(SKILLS.declared_name(source / "SKILL.md"), name)
                description = re.search(r"^description: (.+)$", header, re.MULTILINE)
                self.assertIsNotNone(description)
                self.assertTrue(1 <= len(description[1]) <= 1024)
                metadata = (source / "agents/openai.yaml").read_text(encoding="utf-8")
                for field in ("display_name", "short_description", "default_prompt"):
                    self.assertRegex(metadata, rf'  {field}: "[^"\n]+"')
                short = re.search(r'  short_description: "([^"\n]+)"', metadata)[1]
                self.assertTrue(25 <= len(short) <= 64)
                self.assertIn("$" + name, metadata)
                for md in source.rglob("*.md"):
                    prose = re.sub(r"```.*?```", "", md.read_text(encoding="utf-8"), flags=re.DOTALL)
                    for target in re.findall(r"\]\(([^)\s]+)\)", prose):
                        if ":" not in target and not target.startswith("#"):
                            ref = (md.parent / target.split("#")[0]).resolve()
                            self.assertTrue(SKILLS.within(ref, source.resolve()), (md, target))
                            self.assertTrue(ref.exists(), (md, target))
                for readme in ("README.md", "README.th.md"):
                    self.assertIn(relative + "/SKILL.md", (REPO / readme).read_text(encoding="utf-8"))

    def test_list_and_absolute_paths(self):
        listed = subprocess.run([BASH, (REPO / "scripts/list-skills.sh").as_posix()],
                                text=True, capture_output=True)
        self.assertEqual(listed.returncode, 0, listed.stderr)
        self.assertEqual(listed.stdout.splitlines(), sorted(r + "/SKILL.md" for _, r, _ in SKILLS.manifest_skills(REPO)))
        paths = subprocess.run([BASH, (REPO / "scripts/published-skill-dirs.sh").as_posix()],
                               text=True, capture_output=True)
        self.assertEqual(paths.returncode, 0, paths.stderr)
        self.assertEqual(len(paths.stdout.splitlines()), 6)
        self.assertTrue(all(p.startswith("/") for p in paths.stdout.splitlines()))

    def test_missing_python_preflight(self):
        with tempfile.TemporaryDirectory(prefix="no python ") as folder:
            result = subprocess.run([BASH, "-c", 'source "$1"', "preflight", (REPO / "scripts/python.sh").as_posix()],
                                    env={**os.environ, "PATH": folder}, text=True, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Python 3.9+ is required", result.stderr)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="agent skills space ")
        self.base = Path(self.temp.name).resolve()
        self.repo = self.base / "checkout with spaces"
        shutil.copytree(REPO / "scripts", self.repo / "scripts")
        shutil.copytree(REPO / "skills", self.repo / "skills")
        shutil.copytree(REPO / ".claude-plugin", self.repo / ".claude-plugin")
        (self.repo / ".git").mkdir()  # Stop parent discovery before the real HOME.
        self.home = self.base / "temporary home"
        self.home.mkdir()
        self.env = {k: v for k, v in os.environ.items() if k not in
                    ("CODEX_HOME", "XDG_CONFIG_HOME", "PI_CODING_AGENT_DIR")}
        self.env["HOME"] = self.home.as_posix()

    def tearDown(self):
        self.temp.cleanup()

    def run_install(self, runtime="agent", *args):
        return subprocess.run([BASH, (self.repo / f"scripts/link-{runtime}-skills.sh").as_posix(), *args],
                              cwd=self.repo, env=self.env, text=True, capture_output=True)

    def destination(self, runtime="agent"):
        return self.home / {"agent": ".agents", "codex": ".codex", "claude": ".claude", "kiro": ".kiro"}[runtime] / "skills"

    def old_skill(self, path, name="hold-your-horses"):
        path.mkdir(parents=True)
        (path / "SKILL.md").write_text(f"---\nname: {name}\ndescription: old skill\n---\nOriginal", encoding="utf-8")
        (path / "keep.txt").write_bytes(b"do not lose this\x00\xff")

    def make_link(self, target, source):
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            target.symlink_to(source, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"native symlink privilege unavailable: {exc}")
        self.assertTrue(target.is_symlink())

    def test_copy_install_and_repeat_preserves_timestamps_all_entrypoints(self):
        for runtime in ("agent", "codex", "claude", "kiro"):
            with self.subTest(runtime=runtime):
                # Independent homes: shared + Claude would correctly conflict in OpenCode.
                self.env["HOME"] = (self.home / runtime).as_posix()
                result = self.run_install(runtime, "--copy")
                self.assertEqual(result.returncode, 0, result.stderr)
                dest = self.home / runtime / {"agent": ".agents", "codex": ".codex", "claude": ".claude", "kiro": ".kiro"}[runtime] / "skills"
                self.assertEqual(len(list(dest.iterdir())), 6)
                before = {p: p.stat().st_mtime_ns for p in dest.rglob("*")}
                result = self.run_install(runtime, "--copy")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout.count("unchanged "), 6)
                self.assertEqual(before, {p: p.stat().st_mtime_ns for p in dest.rglob("*")})

    def test_real_symlinks_and_repeat(self):
        probe = self.base / "probe link"
        self.make_link(probe, self.repo)
        result = self.run_install()
        self.assertEqual(result.returncode, 0, result.stderr)
        dest = self.destination()
        before = {p: p.lstat().st_mtime_ns for p in dest.iterdir()}
        for name, _, src in SKILLS.manifest_skills(self.repo):
            self.assertTrue((dest / name).is_symlink())
            self.assertEqual((dest / name).resolve(), src.resolve())
        result = self.run_install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(before, {p: p.lstat().st_mtime_ns for p in dest.iterdir()})

    def test_conflict_preserves_directory_and_installs_nothing(self):
        old = self.destination() / "hold-your-horses"
        self.old_skill(old)
        before = (old / "keep.txt").read_bytes()
        result = self.run_install("agent", "--copy")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("conflicts; nothing installed", result.stderr)
        self.assertEqual((old / "keep.txt").read_bytes(), before)
        self.assertEqual([p.name for p in self.destination().iterdir()], ["hold-your-horses"])

    def test_replace_backs_up_entire_original_outside_discovery(self):
        old = self.destination() / "hold-your-horses"
        self.old_skill(old)
        result = self.run_install("agent", "--copy", "--replace", "hold-your-horses")
        self.assertEqual(result.returncode, 0, result.stderr)
        backups = list((self.home / ".agents/agent-skills-backups").rglob("keep.txt"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), b"do not lose this\x00\xff")
        self.assertFalse(SKILLS.within(backups[0], self.destination()))
        self.assertNotIn("Original", (old / "SKILL.md").read_text(encoding="utf-8"))
        again = self.run_install("agent", "--copy", "--replace", "hold-your-horses")
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertNotIn("backup ", again.stdout)

    def test_foreign_and_broken_symlinks_preserved_then_backed_up(self):
        foreign = self.base / "foreign"
        self.old_skill(foreign)
        target = self.destination() / "hold-your-horses"
        self.make_link(target, foreign)
        result = self.run_install("agent", "--copy")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(target.resolve(), foreign)
        shutil.rmtree(foreign)  # Owned fixture only; intentionally break the link.
        result = self.run_install("agent", "--copy")
        self.assertNotEqual(result.returncode, 0)
        result = self.run_install("agent", "--copy", "--replace", "hold-your-horses")
        self.assertEqual(result.returncode, 0, result.stderr)
        backup = next((self.home / ".agents/agent-skills-backups").rglob("hold-your-horses"))
        self.assertTrue(backup.is_symlink())
        self.assertEqual(os.readlink(backup), str(foreign))

    def test_duplicate_names_in_user_and_project_roots_are_preserved(self):
        roots = [self.home / ".claude/skills", self.home / ".codex/skills",
                 self.home / ".pi/agent/skills", self.home / ".config/opencode/skills",
                 self.repo / ".agents/skills", self.repo / ".pi/skills",
                 self.repo / ".opencode/skills", self.repo / ".claude/skills"]
        for root in roots:
            with self.subTest(root=root):
                old = root / "different-folder"
                self.old_skill(old)
                result = self.run_install("agent", "--copy", "--replace", "hold-your-horses")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("duplicate hold-your-horses", result.stderr)
                self.assertEqual((old / "keep.txt").read_bytes(), b"do not lose this\x00\xff")
                self.assertFalse(self.destination().exists())
                shutil.rmtree(root)  # Verified fixture path below self.base.

    def test_linked_install_root_refused_without_touching_source(self):
        self.make_link(self.destination(), self.repo / "skills")
        before = sorted(p.relative_to(self.repo).as_posix() for p in self.repo.rglob("SKILL.md"))
        result = self.run_install("agent", "--copy", "--replace", "hold-your-horses")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("linked directory", result.stderr)
        self.assertEqual(before, sorted(p.relative_to(self.repo).as_posix() for p in self.repo.rglob("SKILL.md")))

    def test_linked_backup_root_refused(self):
        target = self.home / ".agents/agent-skills-backups"
        elsewhere = self.base / "elsewhere"
        elsewhere.mkdir()
        self.make_link(target, elsewhere)
        result = self.run_install("agent", "--copy")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(elsewhere.iterdir()), [])

    def test_invalid_manifest_is_atomic_and_unknown_replace_is_rejected(self):
        path = self.repo / ".claude-plugin/plugin.json"
        original = path.read_text(encoding="utf-8")
        good = json.loads(original)["skills"]
        for bad in ("../outside", "/absolute", "skills/missing", good[0], 23):
            with self.subTest(bad=bad):
                path.write_text(json.dumps({"skills": good + [bad]}), encoding="utf-8")
                result = self.run_install("agent", "--copy")
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(self.destination().exists())
                paths = subprocess.run([BASH, (self.repo / "scripts/published-skill-dirs.sh").as_posix()],
                                       cwd=self.repo, env=self.env, text=True, capture_output=True)
                self.assertNotEqual(paths.returncode, 0)
                self.assertEqual(paths.stdout, "")
        path.write_text(original, encoding="utf-8")
        result = self.run_install("agent", "--copy", "--replace", "unknown")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.destination().exists())

    def test_symlink_failure_does_not_masquerade_as_copy(self):
        args = type("Args", (), dict(repo=str(self.repo), home=str(self.home), runtime="shared",
                    project=str(self.repo), codex_home=None, config_home=None, pi_home=None,
                    replace=[], copy=False))()
        with patch.object(Path, "symlink_to", side_effect=OSError("symlink privilege denied")):
            with self.assertRaisesRegex(SKILLS.SkillError, "retry with --copy"):
                SKILLS.install(args)
        self.assertFalse(self.destination().exists())

    def test_fake_symlink_copy_is_rejected(self):
        args = type("Args", (), dict(repo=str(self.repo), home=str(self.home), runtime="shared",
                    project=str(self.repo), codex_home=None, config_home=None, pi_home=None,
                    replace=[], copy=False))()
        def fake_link(path, source, **kwargs):
            shutil.copytree(source, path)
        with patch.object(Path, "symlink_to", fake_link):
            with self.assertRaisesRegex(SKILLS.SkillError, "not a real symlink"):
                SKILLS.install(args)
        self.assertFalse(self.destination().exists())

    @unittest.skipUnless(os.name == "nt", "Windows junction protection")
    def test_windows_junction_install_root_is_refused(self):
        target = self.destination()
        target.parent.mkdir(parents=True)
        result = subprocess.run(["cmd.exe", "/c", "mklink", "/J", str(target), str(self.repo / "skills")],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(SKILLS.linklike(target))
        result = self.run_install("agent", "--copy")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("linked directory", result.stderr)

    def test_codex_home_override_is_respected(self):
        override = self.base / "custom codex home"
        self.env["CODEX_HOME"] = str(override)
        result = self.run_install("codex", "--copy")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(list((override / "skills").iterdir())), 6)
        self.assertFalse(self.destination("codex").exists())


if __name__ == "__main__":
    unittest.main()
