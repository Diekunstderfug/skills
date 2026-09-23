# R Analysis Workflow

Follow the existing project's R conventions; this is not an R package-development guide.

## Startup and paths

Keep each standalone R analysis entry usable both through `Rscript` and through `source()` in a fresh R session, with its declared environment and input files available. Shared helper files are not standalone analysis entries. Preserve that capability without executing the full analysis twice after every edit. Check both startup modes when a change to initialization or dependencies makes that useful.

Load only required packages and explicitly load shared functions. Do not depend on interactive objects or restored `.RData`; clearing the workspace is not a substitute for explicit dependencies. Shared helpers should not launch hidden analyses or reset the working directory. Use the existing package/module layout; `src/` is a default for genuinely shared functions, not the only allowed dependency mechanism.

## myutils: project and workspace paths

The locally installed `myutils` 0.4.2 documents three primary functions. Reuse it where it is the project's convention; other projects need not adopt it or `data.table`.

| Function | Purpose and relevant behavior |
| --- | --- |
| `ensure_wd(workdir = "study_project")` | Locate that named project among the executing script's directory and ancestors, initialize path context, and change the working directory by default. It does not search sibling folders or silently choose another project. |
| `wd_path("data", "input.rds")` | Construct a path within the selected analysis project. |
| `ws_path("shared_data", "input.rds")` | Construct a path within the nearest marked workspace at or above the selected project. It errors when no workspace is known. |

Call `ensure_wd()` before loading analysis packages: by default it activates the nearest applicable `renv` environment. Small projects can share an enclosing workspace environment. No lockfile means path setup only; this call does not install analysis dependencies. A session already bound to a different environment needs a new R session rather than an attempted environment switch.

Without a project name, `ensure_wd()` selects the nearest marker (`.here`, `.git`, `renv.lock`, `DESCRIPTION`, or an Rproj file). Use the actual small-project name when the only marker belongs to a larger workspace. Markers are not created automatically. Switching small projects requires another `ensure_wd()` call; changing editor tabs alone does not reset its context.

When execution does not provide a reliable script location, supply `start_dir`. Use `workspace_root` for an explicit workspace and `set_wd = FALSE` only when the caller should retain its working directory. `renv = FALSE` is an explicit path-only option, not a workaround for a broken project environment. For Unicode path problems, consult the package's UTF-8 notes rather than guessing that the file is absent or changing system locale settings automatically.

In projects using `myutils`, retain its initialization and path helpers instead of introducing ad hoc `setwd()` calls or machine-specific absolute paths. If a `ws_path("..", ...)` traversal intentionally leaves the workspace, explain that destination briefly and confirm it when changing the path.

### Copyable entry example

[myutils-analysis-example.R](../assets/myutils-analysis-example.R) is a runnable path-setup example. Copy it into the project's `scripts/`, replace `study_project` with the actual directory name, and replace the example input/output names. It initializes the project, declares paths, and creates an output directory; it intentionally performs no research computation or data reads. Add only the packages, helpers, and analysis needed for the task.

The example supports direct `Rscript` execution and `source()` from a fresh R session. Its optional workspace/helper lines are commented so it does not require a sibling dataset or a placeholder helper.

### Package documentation

Use the installed package's help for the exact installed version rather than treating this summary as a complete API specification:

```r
help("ensure_wd", package = "myutils")
help("wd_path", package = "myutils")
help("ws_path", package = "myutils")
system.file("README.md", package = "myutils")
```

## Adapting scripts and existing result records

Apply these checks only when the corresponding boundary changes:

- When adapting a wrapper or analysis to another cohort, check the changed paths, sample/cohort identifiers, and endpoint labels for stale source-cohort references. A focused search can help; no whole-project scan is required.
- Label copied source-cohort results as reference material until the target analysis produces its own outputs. Retain source identity when reusing an existing valid artifact; copying or renaming it does not establish a new-cohort result.
- When modifying an existing results registry, confirm the changed `source_path` values resolve and retain the stable code/model IDs and display names required by its schema. This does not require introducing a registry where none exists.

## Focused checks and shell quoting

A lightweight syntax check for a changed R file is:

```bash
Rscript -e 'parse(file="scripts/path/to_script.R")'
```

Run the affected entry when computation is needed to validate the change. Missing inputs should produce an actionable error rather than silently selecting another dataset. A syntax check does not establish numerical or analytical correctness.

Use single quotes around inline R expressions containing `$column` so the shell does not expand them. A temporary R script is preferable for more involved expressions.
