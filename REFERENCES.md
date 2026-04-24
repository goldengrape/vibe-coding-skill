# References Used for This Skill

This package is derived from the user's requested design direction and these source ideas:

1. Agent-driven normative development from URD to LLM-Wiki: analysis framework, empirical evidence, and research agenda.
   - URL: https://quaily.com/goldengrape/p/agent-driven-normative-development-from-urd-to-llm-wiki-analysis-framework-empirical-evidence-research-agenda.md
   - Used for: URD/ADD/MDD/TDD/RMD pipeline, LLM-Wiki page types, issue pages, traceability, and failure routing.

2. Agent-driven specification design / SDD / axiomatic design / knowledge system paradigm shift.
   - URL: https://quaily.com/goldengrape/p/agent-driven-specification-design-sdd-axiomatic-design-knowledge-system-paradigm-shift.md
   - Used for: SDD lifecycle, URD as structured intent capture, ADD with FR/DP matrix, MDD decomposition, TDD as executable specification, RMD as route planning, and LLM-Wiki as derived knowledge.

3. User-provided markdown on structured Vibe Coding with AD, DbC, FP, DOD, and Ockham's razor.
   - Used for: engineering discipline principles, contracts, pure-function preference, data-oriented design when justified, and Ockham razor checks to prevent document bloat.

The package does not copy full source articles. It turns the ideas into a reusable skill, templates, checklists, and scripts.


## uv and GitHub workflow references

The skill's Python initialization guidance follows uv's current project workflow: `uv init` creates a project with `pyproject.toml`, and uv uses `uv sync` / `uv run` to keep the environment and lockfile aligned.

The Git workflow follows the common GitHub branch → pull request → merge pattern: changes are proposed from a branch through a pull request, then merged once complete and allowed by repository rules.
