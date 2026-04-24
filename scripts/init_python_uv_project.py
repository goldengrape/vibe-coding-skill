#!/usr/bin/env python3
"""Initialize a small Python project for Vibe Coding.

This script prefers `uv init` when uv is available. If uv is not installed,
it writes the essential starter files so the project still has a clean shape.

Usage:
    python scripts/init_python_uv_project.py --target . --name my-project --kind app --force
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

KINDS = {"app", "lib"}

GITIGNORE = """# Python
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/
.ruff_cache/
.mypy_cache/
.coverage
htmlcov/

# Virtual environments
.venv/
venv/
env/

# Build outputs
dist/
build/
*.egg-info/

# Local config and secrets
.env
.env.*
!.env.example
*.sqlite
*.db

# OS / editors
.DS_Store
.idea/
.vscode/
"""


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.returncode, proc.stdout


def write_if_missing(path: Path, content: str, force: bool = False) -> bool:
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def fallback_pyproject(name: str, kind: str, python: str) -> str:
    base = (
        '[project]\n'
        f'name = "{name}"\n'
        'version = "0.1.0"\n'
        'description = "Add your description here"\n'
        'readme = "README.md"\n'
        f'requires-python = ">={python}"\n'
        'dependencies = []\n\n'
        '[dependency-groups]\n'
        'dev = [\n'
        '    "pytest>=8",\n'
        '    "ruff>=0.8",\n'
        ']\n\n'
        '[tool.ruff]\n'
        'line-length = 100\n'
    )
    if kind == "lib":
        base += (
            '\n[build-system]\n'
            'requires = ["uv_build>=0.11.6,<0.12"]\n'
            'build-backend = "uv_build"\n'
        )
    return base


def initialize_with_uv(target: Path, kind: str, python: str) -> tuple[bool, str]:
    uv = shutil.which("uv")
    if not uv:
        return False, "uv not found on PATH; wrote fallback files instead."

    if (target / "pyproject.toml").exists():
        return True, "pyproject.toml already exists; skipped uv init."

    flag = "--lib" if kind == "lib" else "--app"
    cmd = [uv, "init", flag, ".", "--python", python]
    code, out = run(cmd, target)
    if code != 0:
        return False, f"uv init failed; wrote fallback files instead. Output:\n{out}"

    # Add common dev tools, but keep failure non-fatal. In offline environments,
    # the user can run these commands later.
    run([uv, "add", "--dev", "pytest", "ruff"], target)
    run([uv, "sync"], target)
    return True, "initialized with uv."


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a Python uv project for Vibe Coding.")
    parser.add_argument("--target", default=".", help="Target project directory")
    parser.add_argument("--name", default=None, help="Project name for pyproject fallback")
    parser.add_argument("--kind", default="app", choices=sorted(KINDS), help="Project kind")
    parser.add_argument("--python", default="3.11", help="Minimum Python version")
    parser.add_argument("--force", action="store_true", help="Overwrite starter files managed by this script")
    args = parser.parse_args()

    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)
    name = args.name or target.name.replace("_", "-").lower()

    _used_uv, message = initialize_with_uv(target, args.kind, args.python)

    written: list[str] = []
    if write_if_missing(target / ".gitignore", GITIGNORE, force=args.force):
        written.append(".gitignore")
    if write_if_missing(target / "README.md", f"# {name}\n\nProject initialized for Vibe Coding.\n", force=False):
        written.append("README.md")
    if write_if_missing(target / ".python-version", args.python + "\n", force=False):
        written.append(".python-version")

    if not (target / "pyproject.toml").exists() or args.force:
        if write_if_missing(target / "pyproject.toml", fallback_pyproject(name, args.kind, args.python), force=args.force):
            written.append("pyproject.toml")

    if args.kind == "lib":
        package = name.replace("-", "_")
        if write_if_missing(target / "src" / package / "__init__.py", '"""Package entry point."""\n', force=False):
            written.append(f"src/{package}/__init__.py")
        (target / "src" / package).mkdir(parents=True, exist_ok=True)
    else:
        if not (target / "main.py").exists() and not (target / "src").exists() and not (target / "app").exists():
            main_py = 'def main():\n    print("Hello from Vibe Coding!")\n\n\nif __name__ == "__main__":\n    main()\n'
            if write_if_missing(target / "main.py", main_py, force=False):
                written.append("main.py")

    if write_if_missing(target / "tests" / "test_smoke.py", "def test_smoke():\n    assert True\n", force=False):
        written.append("tests/test_smoke.py")

    print(f"Python project target: {target}")
    print(f"Project kind: {args.kind}")
    print(message)
    if written:
        print("Files written:")
        for item in written:
            print(f"- {item}")
    else:
        print("No fallback files written; existing files were preserved.")
    print("Next step: run tests/checks, then create the first git checkpoint.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
