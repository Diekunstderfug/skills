# modularity-review

Usable independently, or together with `cohesion-locality` through the optional `module-structure` entrypoint. See the [repository README](../README.md) for standalone and combined installation.

First-party skill. Forked from [tyshkovskii/reviewing-code-modularity-skill](https://github.com/tyshkovskii/reviewing-code-modularity-skill) (MIT, see `LICENSE`) at upstream snapshot 2026-06-14 (upstream's last commit; the repo is inactive since).

Since 2026-09-08 this is a **full fork**: no upstream tracking, no porting workflow. The split with `cohesion-locality` (stay-together / change-axis decisions) is our own boundary, carved into `SKILL.md` and the `principles.md` / `red-flags.md` / `language.md` references. If upstream ever revives and looks worth absorbing, diff against the GitHub repo directly — there is no local clone anymore.

This skill owns **public-surface complexity** only. Route both skills with `/module-structure`; the routing regression set lives in `module-structure/evals/routing-queries.json`.
