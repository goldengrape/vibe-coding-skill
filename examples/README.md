# Example Flow

A typical beginner-friendly flow:

1. User says: "I want to build a small habit tracker app."
2. Use `explain_plainly` mode if the user is new or unsure.
3. Use `discover_urd` mode and ask 3–5 useful questions.
4. Write the Idea Brief in `docs/URD.md` with confirmed requirements, assumptions, and open questions.
5. Use `analyze_add` mode to create the Design Split: FRs, DPs, and the design matrix.
6. If the design is coupled, retry decomposition up to 3 times.
7. Use `design_mdd` mode to define Building Blocks: modules, interfaces, and contracts.
8. Use `write_tdd` mode to define the Check Plan: tests and oracles.
9. Use `plan_rmd` mode to order the Build Path.
10. Compile a short OKF bundle in `okf/`, with concept pages, index links, and citations when needed.
11. Run `python scripts/check_project_docs.py --root <project>`.

Recommended first user prompt:

```text
I want to build ____.
Please use the Vibe Coding Skill.
Explain the process in beginner-friendly language, then ask only the questions needed before coding.
```
