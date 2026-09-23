# Research project rules — synthetic evals

Maintainer-only checks; do not load or run them during ordinary research tasks.
The skill entry and normal analysis workflow do not invoke this suite.

The directory roles are inspired by common local research layouts. Every study
name, question, filename, value, identifier, and instruction in the fixtures was
written synthetically. No real project tree, source content, record, project name,
host path, account, or credential belongs in this bundle. Never copy real project
files into fixtures. Review and anonymize skill snapshots before execution too.

## Behavior cases

| Case | Observable outcome |
|---|---|
| Initialize a study | Minimal usable layout, question/method orientation, proportionate data rules, truthful dependency status |
| Update result navigation | Only the requested documents change; existing layout/inputs/results remain intact |
| Repair an analysis entry | Fresh `Rscript` and `source()` work after relocation; missing input fails clearly; upstream analysis never runs |
| Changed human review | Preserve unconfirmed edits and confirmation state; explain the next step without exposing record content or launching analysis |

`evals.json` uses the current Anthropic `skill-creator` case schema.
The fixture data are synthetic, including the fake sensitive-record canaries.
The data-boundary case supplies a simulated validation summary; its private file
is a two-row canary stub, not a full dataset matching every simulated count.
This case tests handling the supplied state, not recomputing the validation.
Checks inspect artifacts and actual runtime behavior, not required wording or headings.
Semantic judgments require an explicit verdict and concrete evidence.

`trigger-evals.json` contains 12 positive/negative native-selection candidates.
They must be tested separately through actual skill discovery. A forced/preloaded
skill run or a model's yes/no prediction is not evidence of native triggering.
The initial behavior pilot does not claim trigger coverage.

## Run a focused comparison

Use an isolated scratch location, an already configured Claude Code CLI, Python 3,
and R for the independent-script case. These tools do not install dependencies.
Authentication and provider routing must already be available in the process
environment. Do not copy credentials or user settings into fixtures or reports.

```sh
python3 evals/prepare.py --skill /path/to/current-skill \
  --baseline-skill /path/to/anonymized-old-skill --out /tmp/skill-eval/iteration-1
python3 evals/execute.py /tmp/skill-eval/iteration-1 --workers 2
```

Run those commands from the skill directory. Paths above are generic examples.
Omit `--baseline-skill` for `with_skill` versus `without_skill`. Use `--case-id N`
to prepare only an affected case in a new empty output directory. Previous runs
are never overwritten. Snapshots exclude `evals/`, preventing recursive copying.

Each executor has a fresh context and a restricted synthetic task directory;
global configuration, hooks, skills, MCP and memory are disabled. The selected
skill entry is preloaded, with its references available on demand. This is
**behavioral evaluation**, not a test of the native router. Actors get file tools;
required empty directories are materialized through a narrow harness request.
Generated code execution happens separately. Therefore no-shell/no-install
behavior is partly enforced by the harness and is not independently proven by it.

Inspect the artifacts, captured tool messages, and generated R before grading.
Exported transcripts preserve visible responses, tool inputs, and tool results;
provider signatures, internal reasoning, and original tool IDs are omitted.
Provide semantic judgments for initialize expectations 1/2 and data-boundary
expectations 0/3, using zero-based indices. Example `review.json` structure:

```json
{
  "eval-1-initialize/new_skill/run-1": {
    "1": {"passed": true, "evidence": "Cite the actual project guidance and its status claims."},
    "2": {"passed": false, "evidence": "Cite a concrete missing or excessive boundary."}
  }
}
```

Supply both configurations' applicable judgments. Never reuse an old verdict
without reviewing the new outputs. Then:

```sh
python3 evals/grade.py /tmp/skill-eval/iteration-1 --review review.json --run-r
python3 evals/report.py /tmp/skill-eval/iteration-1 \
  --official-skill-creator /path/to/official/plugins/skill-creator/skills/skill-creator
```

The grader checks original-file hashes, synthetic disclosure canaries, changed
artifacts, real numerical outputs, and missing-input failure. Generated R runs
only on disposable relocated copies with `--vanilla`, never a real study.
Reports include real API token usage and wall time. The report wrapper corrects
the official aggregator's default run-count/model placeholders, and refuses
missing token counts rather than substituting character counts.

For a first iteration, one run per case is a **pilot**, not a stability estimate.
Keep failed infrastructure attempts and selection reasons; do not tune a rubric
after seeing outputs merely to improve scores. Record unexpected behavior as
additional observations and design future cases separately. Use no mandatory
full-suite reruns for unrelated skill edits.

## Official reference

Checked 2026-09-22 against the official
[skill-creator implementation](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator/skills/skill-creator),
commit `c447c3207a425bc4e2a0d068435f64b0477ae981`.
The original tools generate the benchmark and static review page; they are not
vendored into this skill. Obtain the public repository and use that revision for
reproducibility; reassess deliberately before changing the reference version.

See the [official eval update](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills)
and [schemas](https://github.com/anthropics/claude-plugins-official/blob/c447c3207a425bc4e2a0d068435f64b0477ae981/plugins/skill-creator/skills/skill-creator/references/schemas.md).
