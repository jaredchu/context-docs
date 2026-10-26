"""Run two fresh, explicitly invoked Codex refresh passes on one synthetic project.

Uses existing subscription authentication. Creates a new output directory; never
repairs outputs or retries a model session. Semantic scoring remains a human or
coordinator review of the retained artifacts, separate from these equality checks.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROMPT = """Use $context-docs at .agents/skills/context-docs/SKILL.md to refresh this
adopted project's context against current project evidence.
Only docs/current.md may be edited. Do not alter source evidence,
setup, skills or Git state, run application tests, contact external systems, use
other agents or create scratch files. Briefly report the result.
"""
NOTE = """
## Working note

Uncommitted operator note: retain the recovery envelope until the restore fixture
exists; the legacy reader cannot parse a bare payload.

```yaml
recovery_envelope:
  format: legacy-v1
  retain_until: restore-fixture-verified
```
"""


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def hashes(directory):
    return {p.relative_to(directory).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(directory.rglob("*"))
            if p.is_file() and ".git" not in p.relative_to(directory).parts}


def snapshot(workspace, target):
    shutil.copytree(workspace, target, ignore=shutil.ignore_patterns(".git"))


def clean_env():
    # Keep existing subscription auth discovery, removing API/provider overrides.
    return {k: v for k, v in os.environ.items()
            if not k.startswith(("OPENAI_", "ANTHROPIC_", "AZURE_", "GIT_"))
            and k not in ("GH_TOKEN", "GITHUB_TOKEN", "CLAUDECODE")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path,
                        help="new local evidence directory outside the input fixture")
    args = parser.parse_args()
    out = args.out.resolve()
    if out == ROOT or ROOT in out.parents and ".local" not in out.relative_to(ROOT).parts:
        parser.error("use a new temporary directory or a directory under .local/")
    out.mkdir(parents=True, exist_ok=False)
    env = clean_env()
    workspace = out / "workspace"
    shutil.copytree(HERE / "fixture", workspace)

    def source_git(*arguments):
        return subprocess.check_output(["git", *arguments], cwd=ROOT, env=env,
                                       stderr=subprocess.PIPE)

    release = source_git("rev-parse", "v0.2.6^{commit}").decode().strip()
    package_paths = source_git("ls-files", "-z", "skills/context-docs").decode().split("\0")
    package_paths = [p for p in package_paths if p]
    release_entries = source_git("ls-tree", "-r", "-z", release, "skills/context-docs").decode().split("\0")
    release_modes = {entry.split("\t", 1)[1]: entry.split(" ", 1)[0]
                     for entry in release_entries if entry}
    if sorted(package_paths) != sorted(release_modes):
        raise RuntimeError("Tracked package file set differs from published v0.2.6")
    package = workspace / ".agents/skills/context-docs"
    for relative in package_paths:
        source = ROOT / relative
        if source.is_symlink() or bool(source.stat().st_mode & 0o111) != (release_modes[relative] == "100755"):
            raise RuntimeError(f"Baseline package mode differs from published v0.2.6: {relative}")
        if source.read_bytes() != source_git("show", f"{release}:{relative}"):
            raise RuntimeError(f"Baseline package differs from published v0.2.6: {relative}")
        target = package / Path(relative).relative_to("skills/context-docs")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    candidate = hashes(package)

    def source_package_hashes():
        return {Path(p).relative_to("skills/context-docs").as_posix():
                hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in package_paths}

    def git(*arguments):
        return subprocess.check_output(["git", *arguments], cwd=workspace, env=env,
                                       stderr=subprocess.PIPE, text=True).strip()

    git("init", "-q")
    git("add", ".")
    git("-c", "user.name=Synthetic Fixture", "-c", "user.email=fixture@example.invalid",
        "-c", "core.hooksPath=/dev/null", "commit", "--no-gpg-sign", "-qm",
        "Synthetic refresh input\n\nCo-authored-by: Codex <noreply@openai.com>\n"
        "Co-authored-by: Claude <noreply@anthropic.com>")
    current = workspace / "docs/current.md"
    current.write_text(current.read_text() + NOTE)
    baseline = hashes(workspace)
    head = git("rev-parse", "HEAD")
    snapshot(workspace, out / "before")
    version = subprocess.check_output(["codex", "--version"], env=env, text=True).strip()
    flags = ["codex", "exec", "--ignore-user-config", "--ignore-rules", "--ephemeral",
             "--sandbox", "workspace-write", "--model", "gpt-6.1-sol",
             "-c", 'model_reasoning_effort="high"', "-c", 'approval_policy="never"',
             "-c", "features.memories=false", "-c", "features.multi_agent=false",
             "--json"]
    frozen = {"prompt": PROMPT, "append_before_pass_1": NOTE, "client": version,
              "source_root_revision": source_git("rev-parse", "HEAD").decode().strip(),
              "source_worktree_status": source_git("status", "--short").decode(),
              "published_release_revision": release, "package_matches_published_release": True,
              "model": "gpt-6.1-sol", "reasoning_effort": "high", "flags": flags,
              "seconds_cap_per_pass": 240, "fixture_hashes": hashes(HERE / "fixture"),
              "candidate_hashes": candidate, "before_hashes": baseline,
              "protocol_sha256": hashlib.sha256((HERE / "protocol.md").read_bytes()).hexdigest(),
              "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    save(out / "frozen.json", frozen)
    (out / "frozen.sha256").write_text(
        hashlib.sha256((out / "frozen.json").read_bytes()).hexdigest() + "\n")
    trials = []
    previous = baseline
    for number in (1, 2):
        print(f"START pass {number}: {version}, gpt-6.1-sol, High", flush=True)
        stem = out / f"pass-{number}"
        command = flags + ["--output-last-message", str(stem) + ".txt", "-"]
        start = time.monotonic()
        with Path(str(stem) + ".jsonl").open("w") as stream, \
                Path(str(stem) + ".stderr").open("w") as err:
            process = subprocess.Popen(command, cwd=workspace, env=env, text=True,
                                       stdin=subprocess.PIPE, stdout=stream, stderr=err,
                                       start_new_session=True)
            timed_out = False
            try:
                process.communicate(PROMPT, timeout=240)
            except subprocess.TimeoutExpired:
                timed_out = True
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.communicate(timeout=10)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.communicate()
        after = hashes(workspace)
        snapshot(workspace, out / f"after-{number}")
        events = []
        for line in Path(str(stem) + ".jsonl").read_text().splitlines():
            try:
                events.append(json.loads(line))
            except ValueError:
                pass
        changed = sorted(k for k in set(previous) | set(after)
                         if previous.get(k) != after.get(k))
        trial = {"pass": number, "returncode": process.returncode, "timed_out": timed_out,
                 "elapsed_seconds": round(time.monotonic() - start, 2),
                 "turn_completed": any(e.get("type") == "turn.completed" for e in events),
                 "changed_files": changed, "only_allowed_edits": set(changed) <= {"docs/current.md"},
                 "head_unchanged": git("rev-parse", "HEAD") == head,
                 "index_unchanged": not git("diff", "--cached", "--name-only"),
                 "after_hashes": after}
        trials.append(trial)
        save(out / "trials.json", trials)
        print(json.dumps({k: v for k, v in trial.items() if k != "after_hashes"}), flush=True)
        previous = after
        if process.returncode or timed_out or not trial["turn_completed"]:
            break
    summary = {"trials": trials, "candidate_source_unchanged": candidate == source_package_hashes(),
               "both_completed": len(trials) == 2 and all(
                   t["returncode"] == 0 and t["turn_completed"] and not t["timed_out"] for t in trials),
               "first_pass_changed_context": bool(trials and "docs/current.md" in trials[0]["changed_files"]),
               "second_pass_exactly_unchanged": len(trials) == 2 and trials[1]["after_hashes"] == trials[0]["after_hashes"],
               "semantic_review": "pending; equality checks do not establish content correctness"}
    save(out / "mechanical.json", summary)
    print(f"Evidence: {out}", flush=True)


if __name__ == "__main__":
    main()
