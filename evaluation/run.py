#!/usr/bin/env python3
"""Opt-in live evaluations. Calls configured providers; never run this in CI."""

import argparse
import base64
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time
import zipfile

REPO = Path(__file__).resolve().parents[1]
SCENARIOS = {
    "small": (["hold-your-horses", "prove-it"],
              'Change greet("Ada") to return "Hello, Ada!" by adding the missing punctuation. '
              'Keep this small and verify the completion claim. An earlier check passed; its receipt is in evidence/earlier-check.json.'),
    "api": (["hold-your-horses", "prove-it"],
            "Add a numeric total field in dollars to GET /invoice for the UI. Keep the change compatible with existing users of the response. Verify important compatibility facts."),
    "bug": (["bug-hunter", "prove-it"],
            "Bulk quotes undercharge. The first explanation was stale cache; clearing it appeared to help once. Diagnose and fix the supported cause, retaining experimental evidence."),
    "council": (["council"],
                "Review billing.py using council both. The checkout is clean; the explicit scope is billing.py. "
                "The synthetic recorded reports in review-evidence/ disagree. Check each finding, keep those reports intact, "
                "and distinguish them from any live reviewer result or unavailable CLI. Do not fix code."),
    "verifier": (["create-verifier"],
                 "Create a verify-project skill for this repository, targeting {target} only. Reuse the existing harness, "
                 "exercise the create-and-list-task feature, save durable evidence, and check it survives cleanup. "
                 "Make it usable by a fresh session without this conversation."),
    "handoff": (["verify-project"],
                "Use the generated verify-project skill and its needed references to run create-and-list-task from a fresh session. "
                "Save new evidence under artifacts/verification/cold-session, clean up, and check the evidence remains readable. "
                "Report only what you actually ran; do not use the previous session's receipt as this run's result."),
}


def git(*args, cwd=REPO):
    return subprocess.check_output(["git", "-c", "core.fsmonitor=false", *args], cwd=cwd)


def fingerprint(folder):
    digest = hashlib.sha256()
    for path in sorted(folder.rglob("*")):
        if path.is_file():
            digest.update(path.relative_to(folder).as_posix().encode())
            digest.update(b"\0" + path.read_bytes())
    return digest.hexdigest()


def skill_root(runtime):
    return ".claude/skills" if runtime == "claude" else ".agents/skills"


def prepare(runtime, scenario, variant, root, baseline):
    case = "verifier" if scenario == "handoff" else scenario
    workspace = root / "workspaces" / runtime / case / variant
    if scenario == "handoff":
        if not (workspace / skill_root(runtime) / "verify-project/SKILL.md").is_file():
            raise RuntimeError("generator has not created verify-project; handoff is blocked")
        return workspace
    if workspace.exists():
        raise RuntimeError(f"workspace already exists; use a new --output root to preserve earlier evidence: {workspace}")
    shutil.copytree(REPO / "evaluation/fixtures" / case, workspace)
    source = REPO
    if variant == "baseline":
        source = root / "sources" / runtime / baseline
        if not source.exists():
            archive = git("archive", "--format=zip", baseline)
            source.mkdir(parents=True)
            with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
                bundle.extractall(source)
    manifest = json.loads((source / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    for entry in manifest["skills"]:
        src = source / entry
        shutil.copytree(src, workspace / skill_root(runtime) / src.name)
    if (workspace / "verification").exists():
        (workspace / "verification").rename(workspace / skill_root(runtime) / "verify-project")
    git("init", "--quiet", cwd=workspace)
    git("add", ".", cwd=workspace)
    git("-c", "user.name=Skill evaluation", "-c", "user.email=eval@localhost",
        "-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "Isolated evaluation fixture", cwd=workspace)
    return workspace


def environment(runtime, home, original_home, openai_subscription=False, timeout=360):
    env = os.environ.copy()
    env.update(HOME=str(home), USERPROFILE=str(home), XDG_CONFIG_HOME=str(home / ".config"),
               XDG_DATA_HOME=str(home / ".local/share"), XDG_STATE_HOME=str(home / ".local/state"),
               XDG_CACHE_HOME=str(home / ".cache"), PI_CODING_AGENT_DIR=str(home / ".pi/agent"), PI_TELEMETRY="0")
    # Credentials remain at their original configured location. No copies/symlinks
    # of auth files are made. Optional subscription reuse passes access only in
    # child env, through the runtime's native provider; never a refresh token.
    env["CODEX_HOME"] = os.environ.get("CODEX_HOME", str(original_home / ".codex"))
    env["CLAUDE_CONFIG_DIR"] = os.environ.get("CLAUDE_CONFIG_DIR", str(original_home / ".claude"))
    if runtime == "codex" and os.name == "nt":
        # Native sandbox credentials/profile belong to the real Windows user.
        env["USERPROFILE"] = str(original_home)
    secrets = []
    if openai_subscription:
        if runtime not in ("pi", "opencode"):
            raise RuntimeError("subscription reuse is only for Pi/OpenCode")
        configured = json.loads((Path(env["CODEX_HOME"]) / "auth.json").read_text(encoding="utf-8"))
        token = configured.get("tokens", {}).get("access_token", "")
        try:
            claims = json.loads(base64.urlsafe_b64decode(token.split(".")[1] + "==="))
            expires = claims["exp"]
            account = claims.get("https://api.openai.com/auth", {}).get("chatgpt_account_id")
        except (ValueError, KeyError, IndexError, TypeError):
            raise RuntimeError("configured Codex subscription token metadata is unavailable") from None
        if configured.get("auth_mode") != "chatgpt" or not account:
            raise RuntimeError("a configured ChatGPT subscription is required; no auth file changed")
        if not isinstance(expires, (int, float)) or expires <= time.time() + timeout + 60:
            raise RuntimeError("subscription access expires too soon; refresh it in Codex before retrying")
        secrets.append(token)
        if runtime == "pi":
            env["AGENT_SKILLS_OPENAI_ACCESS_TOKEN"] = token
            auth_dir = Path(env["PI_CODING_AGENT_DIR"])
            auth_dir.mkdir(parents=True)
            # A configuration reference only, never the resolved credential.
            (auth_dir / "models.json").write_text(json.dumps({"providers": {"openai-codex": {
                "apiKey": "$AGENT_SKILLS_OPENAI_ACCESS_TOKEN"}}}), encoding="utf-8")
        else:
            env["OPENCODE_AUTH_CONTENT"] = json.dumps({"openai": {
                "type": "oauth", "access": token, "refresh": "", "expires": int(expires * 1000),
                "accountId": account}})
    if runtime == "opencode":
        env["OPENCODE_CONFIG_CONTENT"] = json.dumps({"autoupdate": False, "share": "disabled",
            "permission": {"*": "allow", "external_directory": "deny", "webfetch": "deny", "websearch": "deny", "task": "deny"}})
    return env, secrets


def command(runtime, config, workspace, prompt_file):
    base, model, effort = config["command"], config["model"], config["effort"]
    if runtime == "codex":
        return base + ["exec", "--ignore-user-config", "--ignore-rules", "--ephemeral", "--json",
                       "--disable", "plugins", "--disable", "apps", "--disable", "memories", "--disable", "hooks", "--disable", "multi_agent",
                       "--enable", "skip_host_skill_discovery",
                       *( ["-c", 'windows.sandbox="elevated"'] if os.name == "nt" else [] ),
                       "--sandbox", "workspace-write", "-c", 'approval_policy="never"',
                       "-c", f'model_reasoning_effort="{effort}"', "--model", model, "--cd", str(workspace), "-"]
    if runtime == "claude":
        return base + ["-p", "--output-format", "stream-json", "--verbose", "--no-session-persistence",
                       "--strict-mcp-config", "--setting-sources", "", "--permission-mode", "acceptEdits",
                       "--permission-prompts", "none", "--allowedTools", "Read,Edit,Write,Bash,Glob,Grep,Skill",
                       "--model", model, "--effort", effort]
    if runtime == "pi":
        return base + ["--print", "--mode", "json", "--no-session", "--no-extensions", "--no-mcp",
                       "--no-prompt-templates", "--no-context-files", "--approve", "--model", model,
                       "--thinking", effort]
    return base + ["run", "Follow the attached evaluation task.", "--pure", "--format", "json", "--auto", "--model", model, "--variant", effort,
                   "--dir", str(workspace), "--file", str(prompt_file)]


def review_unavailable_path(home, env):
    """Actual CLI availability failure, not fake model output."""
    folder = home / "reviewer-cli-unavailable"
    folder.mkdir(parents=True)
    for name in ("codex", "claude"):
        script = folder / name
        script.write_text('#!/usr/bin/env bash\nprintf "%s\\n" "FIXTURE_UNAVAILABLE: reviewer deliberately disabled in this trial" >&2\nexit 78\n', encoding="utf-8")
        script.chmod(0o755)
        (folder / (name + ".cmd")).write_text('@echo off\necho FIXTURE_UNAVAILABLE: reviewer deliberately disabled in this trial 1>&2\nexit /b 78\n', encoding="utf-8")
    env["PATH"] = str(folder) + os.pathsep + env["PATH"]


def parse_metrics(runtime, output):
    events = []
    for line in output.splitlines():
        try:
            value = json.loads(line)
            if isinstance(value, dict):
                events.append(value)
        except ValueError:
            pass
    usage, actual_model, final = None, None, []
    if runtime == "codex":
        for event in events:
            if event.get("type") == "turn.completed":
                usage = event.get("usage")
            item = event.get("item", {})
            if event.get("type") == "item.completed" and item.get("type") == "agent_message":
                final.append(item.get("text", ""))
    elif runtime == "claude":
        for event in events:
            if event.get("type") == "system" and event.get("subtype") == "init":
                actual_model = event.get("model")
            if event.get("type") == "result":
                usage = event.get("usage")
                final.append(event.get("result", ""))
    elif runtime == "pi":
        totals = {}
        for event in events:
            message = event.get("message", {})
            if event.get("type") == "message_end" and message.get("role") == "assistant":
                actual_model = message.get("model", actual_model)
                for key, value in message.get("usage", {}).items():
                    if isinstance(value, (int, float)):
                        totals[key] = totals.get(key, 0) + value
                blocks = message.get("content", [])
                text = "\n".join(b.get("text", "") for b in blocks if b.get("type") == "text")
                if text:
                    final.append(text)
        usage = totals or None
    elif runtime == "opencode":
        totals = {}
        for event in events:
            part = event.get("part", {})
            if event.get("type") == "step_finish":
                for key, value in part.get("tokens", {}).items():
                    if isinstance(value, (int, float)):
                        totals[key] = totals.get(key, 0) + value
                    elif key == "cache" and isinstance(value, dict):
                        for cache_key, count in value.items():
                            if isinstance(count, (int, float)):
                                name = "cache_" + cache_key
                                totals[name] = totals.get(name, 0) + count
            if event.get("type") == "text":
                final.append(part.get("text", ""))
        usage = totals or None
    return {"usage": usage, "actual_model": actual_model, "final_text": "\n\n".join(final), "event_count": len(events)}


def call_session(cmd, workspace, env, prompt, timeout):
    options = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt" else {"start_new_session": True}
    process = subprocess.Popen(cmd, cwd=workspace, env=env, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True, encoding="utf-8", errors="replace", **options)
    try:
        stdout, stderr = process.communicate(prompt, timeout=timeout)
        return stdout, stderr, process.returncode
    except subprocess.TimeoutExpired:
        # Kill only this evaluator-owned process tree, never a process by name.
        if os.name == "nt":
            subprocess.run(["taskkill.exe", "/PID", str(process.pid), "/T", "/F"], capture_output=True, timeout=15)
        else:
            os.killpg(process.pid, signal.SIGTERM)
        stdout, stderr = process.communicate(timeout=15)
        return stdout, stderr + f"\nEvaluation timeout after {timeout}s; owned process tree stopped; partial output retained.", None


def oracle(scenario, workspace, result_dir):
    """Independent mechanical checks. Human review of behavior is still required."""
    if scenario == "small":
        code = 'from greeting import greet; assert greet("Ada") == "Hello, Ada!"; print("greeting assertion passed")'
    elif scenario == "api":
        code = 'import json,subprocess,sys; subprocess.run([sys.executable,"verify_api.py","--evidence",sys.argv[1]],check=True); p=json.load(open(sys.argv[1]))["response"]; assert p["total"] == 12.5 and type(p["total_cents"]) is int and p["total_cents"] == 1250; print("wire and consumer assertions passed")'
    elif scenario == "bug":
        code = 'from quote import quote,CACHE; CACHE.clear(); assert all(quote(100,q,c) == 100*q for q in (1,9,10,11) for c in (True,False)); print("quote assertions passed")'
    else:
        return {"status": "manual_required", "note": "Check transcript, raw reviews or generated references, real feature receipts, and cleanup."}
    result = subprocess.run([sys.executable, "-c", code, str(result_dir / "oracle-api.json")], cwd=workspace,
                            capture_output=True, text=True, timeout=30)
    return {"status": "passed" if result.returncode == 0 else "failed", "exit_code": result.returncode,
            "stdout": result.stdout, "stderr": result.stderr}


def run(args):
    root = Path(args.output).resolve()
    config = json.loads(Path(args.config).read_text(encoding="utf-8"))[args.runtime]
    result_dir = root / "results" / args.runtime / args.scenario / args.variant
    if result_dir.exists():
        raise RuntimeError("result already exists; preserve it and select a new output root for a justified rerun")
    result_dir.mkdir(parents=True)
    original_home = Path.home()
    record = {"runtime": args.runtime, "scenario": args.scenario, "variant": args.variant,
              "baseline_revision": git("rev-parse", args.baseline).decode().strip(),
              "candidate_revision": git("rev-parse", "HEAD").decode().strip(),
              "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "provider": config["provider"], "model": config["model"], "effort": config["effort"],
              "started_at": datetime.now(timezone.utc).isoformat(), "status": "blocked"}
    start = time.monotonic()
    try:
        if args.openai_subscription_auth:
            expected = {"pi": "openai-codex/", "opencode": "openai/"}.get(args.runtime)
            if not expected or not config["model"].startswith(expected):
                raise RuntimeError("subscription reuse requires the native OpenAI provider model prefix")
            record["auth_method"] = "existing Codex ChatGPT access token; native provider; child environment only; no refresh"
        workspace = prepare(args.runtime, args.scenario, args.variant, root, args.baseline)
        home = root / "homes" / args.runtime / args.scenario / args.variant
        home.mkdir(parents=True)
        env, secrets = environment(args.runtime, home, original_home, args.openai_subscription_auth, args.timeout)
        version = subprocess.run(config["command"] + ["--version"], env=env, capture_output=True, text=True, timeout=30)
        record["version"] = version.stdout.strip()
        target = skill_root(args.runtime)
        skills, task = SCENARIOS[args.scenario]
        paths = [workspace / target / name / "SKILL.md" for name in skills]
        record["skill_fingerprints"] = {name: fingerprint(workspace / target / name) for name in skills}
        prompt = ("This is an isolated local skill evaluation. Use ONLY the designated project skill copies, even if a global skill has the same name. "
                  "Read each SKILL.md and its needed references before following it:\n" + "\n".join(str(p) for p in paths) + "\n\n" +
                  task.format(target=target) + "\n\nWork only in this fixture. Use the available shell/Python. "
                  "Do not read credentials, change user config, install dependencies, contact other people, push, deploy, or use subagents. "
                  "Do not create a new verifier unless the task requests one. Keep one concise completion report with claims, evidence and limitations. "
                  "You may save evaluation evidence inside this fixture. Reviewer availability failures in the council case are intentional.\n")
        if args.runtime == "pi":
            # @file is an attachment block in Pi, not a native skill command.
            # stdin preserves /skill expansion at the start of the user prompt.
            prompt = "/skill:" + skills[0] + " " + prompt
            record["invocation"] = "native /skill command through stdin"
        if args.scenario == "council" and args.runtime == "codex":
            # Native Windows sandbox shells can reconstruct PATH, bypassing a
            # parent-environment shim. Pin the controlled CLI boundary explicitly.
            suffix = ".cmd" if os.name == "nt" else ""
            wrappers = home / "reviewer-cli-unavailable"
            prompt += ("\nFor this controlled availability trial, use ONLY these evaluator-provided reviewer executables "
                       "with the skill's normal review flags; do not invoke global reviewer installations:\n"
                       f"Codex: {wrappers / ('codex' + suffix)}\nClaude: {wrappers / ('claude' + suffix)}\n")
            record["reviewer_boundary"] = "explicit controlled CLI wrappers (native sandbox may reconstruct PATH)"
        prompt_file = result_dir / "prompt.txt"
        prompt_file.write_text(prompt, encoding="utf-8")
        cmd = command(args.runtime, config, workspace, prompt_file)
        record["command"] = cmd
        if args.scenario == "council":
            review_unavailable_path(home, env)
        stdout, stderr, exit_code = call_session(cmd, workspace, env,
            prompt if args.runtime in ("codex", "claude", "pi") else None, args.timeout)
        for secret in secrets:
            stdout, stderr = stdout.replace(secret, "[REDACTED]"), stderr.replace(secret, "[REDACTED]")
        (result_dir / "stdout.jsonl").write_text(stdout, encoding="utf-8")
        (result_dir / "stderr.txt").write_text(stderr, encoding="utf-8")
        metrics = parse_metrics(args.runtime, stdout)
        final = metrics.pop("final_text")
        (result_dir / "final.md").write_text(final, encoding="utf-8")
        record.update(metrics)
        record["exit_code"] = exit_code
        record["status"] = "completed_needs_review" if exit_code == 0 and final else "blocked"
        record["oracle"] = oracle(args.scenario, workspace, result_dir) if record["status"] != "blocked" else {"status": "not_run"}
        record["working_tree_diff"] = git("diff", "--stat", cwd=workspace).decode("utf-8", "replace")
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        record["blocker"] = str(exc)
    record["elapsed_seconds"] = round(time.monotonic() - start, 3)
    record["finished_at"] = datetime.now(timezone.utc).isoformat()
    (result_dir / "run.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
    print(json.dumps({k: record.get(k) for k in ("runtime", "scenario", "variant", "status", "elapsed_seconds", "blocker")}))
    return 0 if record["status"] == "completed_needs_review" else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", choices=("codex", "claude", "pi", "opencode"), required=True)
    parser.add_argument("--scenario", choices=tuple(SCENARIOS), required=True)
    parser.add_argument("--variant", choices=("baseline", "candidate"), required=True)
    parser.add_argument("--baseline", default="e003656")
    parser.add_argument("--config", required=True, help="JSON with command/provider/model/effort per runtime; no credentials")
    parser.add_argument("--output", default=str(REPO / ".evaluation"))
    parser.add_argument("--timeout", type=int, default=360)
    parser.add_argument("--openai-subscription-auth", action="store_true", help="reuse configured Codex ChatGPT access in Pi/OpenCode native OpenAI providers, child env only")
    raise SystemExit(run(parser.parse_args()))
