# References Used for This Skill

This package is derived from the user's requested design direction and these source ideas:

1. Agent-driven normative development from URD to LLM-Wiki: analysis framework, empirical evidence, and research agenda.
   - URL: https://quaily.com/goldengrape/p/agent-driven-normative-development-from-urd-to-llm-wiki-analysis-framework-empirical-evidence-research-agenda.md
   - Used for: URD/ADD/MDD/TDD/RMD pipeline, derived knowledge pages, issue pages, traceability, and failure routing.

2. Open Knowledge Format (OKF) announcement.
   - URL: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
   - Used for: replacing the previous LLM-Wiki output with a portable, agent- and human-readable OKF bundle.

3. Open Knowledge Format (OKF) v0.1 specification.
   - URL: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
   - Used for: `okf/` bundle structure, Concept ID rules, Markdown concept files, YAML frontmatter, required `type`, recommended fields, reserved `index.md` / `log.md`, bundle-relative links, citations, `references/`, version declaration, and permissive consumption rules.

4. Agent-driven specification design / SDD / axiomatic design / knowledge system paradigm shift.
   - URL: https://quaily.com/goldengrape/p/agent-driven-specification-design-sdd-axiomatic-design-knowledge-system-paradigm-shift.md
   - Used for: SDD lifecycle, URD as structured intent capture, ADD with FR/DP matrix, MDD decomposition, TDD as executable specification, RMD as route planning, and derived knowledge as a retrieval layer.

5. User-provided markdown on structured Vibe Coding with AD, DbC, FP, DOD, and Ockham's razor.
   - Used for: engineering discipline principles, contracts, pure-function preference, data-oriented design when justified, and Ockham razor checks to prevent document bloat.

The package does not copy full source articles. It turns the ideas into a reusable skill, templates, checklists, and scripts.


## uv and GitHub workflow references

The skill's Python initialization guidance follows uv's current project workflow: `uv init` creates a project with `pyproject.toml`, and uv uses `uv sync` / `uv run` to keep the environment and lockfile aligned.

The Git workflow follows the common GitHub branch → pull request → merge pattern: changes are proposed from a branch through a pull request, then merged once complete and allowed by repository rules.
