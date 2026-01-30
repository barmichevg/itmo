# Copilot / AI agent instructions for this repository

Purpose
- Help code-writing agents understand this small utility repository and make safe, minimal, useful changes.

Big picture
- This repo contains small, standalone Python scripts (no web service): `api.py` and `sort_files.py` plus a sample `test_files/` directory. Changes should preserve the simple, script-based structure.
- `api.py` demonstrates platform-specific native calls via `ctypes`: on Windows it uses `user32.MessageBoxW`, on POSIX it looks up `libc` and calls `puts`. Treat this as an example of direct OS integration rather than a reusable library.
- `sort_files.py` is a procedural utility that moves files from `test_files/` into subfolders by extension. It uses `os`, `shutil`, and a hard-coded `source_dir` (see top of file).

Execution & developer workflows
- Run scripts directly from the repo root with Python 3: ``python3 api.py`` and ``python3 sort_files.py``.
- Debugging: use prints (the project uses print-based logging) or run under the debugger: ``python3 -m pdb sort_files.py``.
- There are no automated tests or build steps in this repo. If you add tests, place them under `test_files/` or a new `tests/` folder and document how to run with `pytest`.

Project-specific conventions
- Keep changes minimal and local: these are simple scripts meant to be readable and runnable without dependency management.
- Strings and messages are written in Russian; preserve language consistency unless making an explicit localization change.
- Paths are absolute/expanded (see `source_dir = os.path.expanduser("/home/username/Desktop/PL/sem6/test_files/")`). If you change paths, update both code and README/documentation.
- Prefer small, explicit edits over introducing heavy frameworks. If you add CLI flags, use `argparse` and preserve the original behavior as the default.

Integration points & external dependencies
- Native calls: `api.py` uses `ctypes.util.find_library('c')` and `ctypes.CDLL`/`ctypes.windll`. Respect platform checks in `if os.name == 'nt': ... else: ...`.
- Filesystem: `sort_files.py` uses `shutil.move` and `os.makedirs`; watch for permission errors when moving files—handle exceptions where appropriate.
- No network, package, or CI integrations are present.

Examples to reference
- To implement a safe change that prints a message on POSIX, set bytes for `puts`: see `api.py` where `message = b"Привет из Python! (ctypes Демо, POSIX)"` and `libc.puts(message)`.
- To change the directory behavior in `sort_files.py`, update the top-level `source_dir` or add an `argparse` option that defaults to the existing `source_dir` value.

What agents should NOT do
- Do not replace the repo with a framework or rearchitect into a service — keep changes lightweight and script-focused.
- Do not assume CI/tests exist; add tests only when accompanied by run instructions.

Key files
- `api.py` — platform-native call examples (ctypes)
- `sort_files.py` — file-organizer utility (filesystem operations)
- `test_files/` — sample data used by `sort_files.py`

If unclear
- Ask the human owner whether a change should be global (path, language) or local (small enhancement). Prefer conservative edits and include a short rationale in the PR description.

---
Please review this draft: tell me if you want more detail (examples, code references, or stricter rules about PRs and testing).
