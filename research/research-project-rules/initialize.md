# Initialize an Analysis Project

Use for requested project setup or establishment of missing working conventions. The outcome is a usable project with understandable entry points, applicable data rules, and a practical dependency setup. This is a collaborative workflow, not a mandatory questionnaire, directory template, or full audit.

## Establish enough context to act

Use the conversation and existing project files to identify the research objective, data types and sensitivity, intended first deliverable, implementation language, and available environment. Distinguish methods already chosen from proposals; do not choose scientific methods simply to fill the project overview.

Ask only about consequential gaps that cannot be inferred, such as the target location, restricted data access, or a required shared environment. Bundle related questions and continue independent setup where possible. State reasonable reversible layout defaults and implement them within the user's request; do not ask for confirmation of every folder or repeat settled choices.

For an existing project, inspect its entry documentation, layout, and dependency declarations. Reuse them and fill actual gaps. Taking over a project does not authorize rearranging its data, replacing its environment, or rebuilding existing outputs.

## Create a useful layout and entry guidance

Use `scripts/`, `data/`, and `results/` as the default roles in a new analysis project, adapting to an existing layout. During explicit setup these base directories can be created before outputs exist; do not add speculative nested trees. Add `src/` when shared functions exist and `docs/` when supporting material needs a home.

Create or update the following only to the extent needed:

- `README.md`: purpose, current scope, environment/setup instructions, available execution and result entry points, and links to detail. Do not present a planned script or result as existing.
- `AGENTS.md` or the established equivalent: short research and technology overview, essential data and execution boundaries, current input authority, and an index describing when to read detailed guidance. It should orient a fresh agent without previous memory or skill access.
- Existing configuration or a small configuration file when variable input paths or parameters actually need a maintained home. Do not invent a registry, hash-approval system, or universal review schema.
- Relevant ignore rules for private data, local environments, secrets, and generated artifacts as appropriate to this project. An ignore rule does not untrack existing files; report a discovered tracking issue without deleting or rewriting history as part of setup.

Keep essential applicable rules directly in the project entry so it can be used independently of this skill. Maintain long procedures and project facts in one canonical location. Do not create duplicate agent files or empty logs. Substantial documentation organization can use `research-log-maintainer` if available; setup must remain usable without it.

## Establish project-specific data rules

Read [data-rules.md](references/data-rules.md) for the skill’s baseline and adapt it to this scientific research analysis project.

Adapt the skill's data defaults into concise, concrete project instructions. Use existing `AGENTS.md`, user choices, data descriptions, and permitted metadata; do not inspect restricted records to decide their sensitivity.

Capture the applicable distinctions: original versus derived or human-maintained files; authorized local processing versus model-visible inspection; permitted outputs versus Git or external transmission; and the project's actual current-input and correction authority.

Put the few essential applicable rules directly in the project entry so a fresh agent can act without a skill lookup. Keep concrete source paths and correction precedence in the project; refer to the baseline for proportionality rather than copying an entire generic policy.

## Make dependencies usable

Inspect the available runtime and existing environment or manifest before installing anything. Reuse the project's environment and package manager. Declare dependencies actually needed for the first authorized work; avoid a broad scientific package bundle or placeholder dependencies.

For R, retain existing project tooling, including `renv` or `myutils` when already used. For a new project, choose an environment approach proportionate to reproducibility and collaboration needs; neither tool is mandatory. For Python or mixed projects, use the established isolated environment and dependency declaration rather than modifying a shared system environment by default.

Create or update the needed dependency declaration and concise setup command. Install or restore required dependencies when that is within the setup request and available permissions. Do not fabricate a lockfile, claim an unperformed install, or automatically upgrade unrelated packages. If installation is blocked, leave an actionable declaration and identify the unresolved dependency precisely.

Create an executable entry only when a concrete initial computation or useful startup path is known. Initialize paths and required dependencies explicitly; avoid fake analyses, dummy results, and a mandatory full-pipeline wrapper.

## Finish with lightweight evidence

Check only what establishes that setup is usable: relevant links/paths and, where useful, a runtime or required-package startup check that does not read sensitive records or execute the study. Do not run a full analysis merely to initialize the project.

Report what was created or reused, the next usable entry, and any genuine unresolved setup issue. Distinguish declared dependencies from installed and verified ones. Stop once the requested setup works; ordinary follow-up edits return to the main skill's proportionate workflow.
