# Python uv Project Initialization Checklist

Use this when the project is likely to be a Python app, CLI, automation, backend, bot, or data tool.

## Decide project kind

- [ ] `app`: command-line tool, script collection, backend, bot, automation, or service.
- [ ] `lib`: reusable Python package imported by other projects.
- [ ] Another stack is chosen only if it better fits the user's goal.

## Required files

- [ ] `pyproject.toml`
- [ ] `.gitignore`
- [ ] `README.md`
- [ ] source folder or entry file
- [ ] `tests/`
- [ ] `.python-version` when using uv/Python pinning

## Recommended commands

For an app:

```bash
uv init --app .
uv add --dev pytest ruff
uv sync
```

For a library:

```bash
uv init --lib .
uv add --dev pytest ruff
uv sync
```

## Do not add yet

- [ ] Web frameworks before MDD/TDD requires them.
- [ ] Databases before data needs are clear.
- [ ] Auth/payment/cloud dependencies before URD confirms them.
- [ ] Generated files, `.venv`, or secrets to git.
