# Plain-Language Explainer for AI

Use this file when the user is a beginner or non-programmer.

## Default short explanation

Before coding, we will make a small project plan.

First, we clarify what you want and what should be left out. Then we split the project into parts that can be built separately. Then we write down how to check whether each part works. Finally, we give the AI a build order so it does not jump around randomly.

You do not need to know the technical document names. I will use simple names while keeping the files organized for the AI.

## Friendly names

- Idea Brief: what you want and what counts as success.
- Design Split: how the project is split into independent parts.
- Building Blocks: modules, interfaces, data, and contracts.
- Check Plan: tests and acceptance checks.
- Build Path: implementation order and stop conditions.
- Project Map: links between idea, design, tests, tasks, and OKF.
- AI Notes: an OKF bundle of short concept pages for later context retrieval.

## Explain vibe coding safely

When the user asks what this skill does, explain it like this:

> Vibe coding works best when the AI has a small, clear project map before it starts coding. This skill helps create that map. It does not make the process heavy; it only asks the questions that prevent the AI from building the wrong thing.

## Why questions are asked

Use concrete explanations:

- Target user: "This tells us whose workflow we are designing for."
- Scope: "This prevents the AI from adding features you did not ask for."
- Success criteria: "This tells us how to test whether the project is finished."
- Data: "This decides what we need to store and protect."
- Login/permissions: "This changes the design and the tests."
- Platform: "This affects which code structure is practical."
- External services: "This affects setup, costs, errors, and testing."

## Anti-patterns

Do not say:

- "Now I will produce a full SDD package."
- "We need to align on architecture deliverables."
- "Let us build a complete documentation system."

Say instead:

- "Let's make a small plan before coding."
- "I need two answers so the AI does not build the wrong thing."
- "This part can wait; I will put it in the future ideas list."


## Explaining project setup

Use this when the user asks why setup is needed:

```text
Before writing features, I want to make the project folder predictable.
For a Python project, that means uv for dependencies, pyproject.toml for project settings, .gitignore so local junk is not committed, and tests/ so we can check each slice.
This prevents the AI from scattering files randomly.
```

## Explaining Git checkpoints

Use this when the user asks why Git/PR/merge is needed:

```text
We are treating each small task as a safe checkpoint.
A commit is the save point, a PR is the review page, and a merge puts the reviewed work back into the main version.
This makes it easier to undo mistakes and easier for another AI or person to continue later.
```
