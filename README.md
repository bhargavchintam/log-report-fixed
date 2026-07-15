# log-report — fixed Terminal-Bench 2 (Harbor) task

A repaired TB2 task. The task itself is small, everyday software engineering: parse an
Apache-style access log into a small JSON summary report. The point of this repo is that
the **authoring is now correct Harbor format** — reproducible environment, no leaked
solution, an honest verifier, a valid manifest, and a clear instruction consistent with
the tests.

## The task

The agent reads `/app/access.log` and writes `/app/report.json`, a single JSON object:

| key | type | meaning |
| --- | --- | --- |
| `total_requests` | int | number of requests (one per non-empty log line) |
| `unique_ips` | int | distinct client IPs (first field of each line) |
| `top_path` | string | the request path seen most often |

For the six-line fixture the correct answer is
`{"total_requests": 6, "unique_ips": 3, "top_path": "/index.html"}`.

## How verification works

After the agent stops, Harbor runs `tests/test.sh` in a fresh container built from the
single `environment/Dockerfile`. It runs pytest and writes the result to
`/logs/verifier/reward.txt` (`1` or `0`) plus `/logs/verifier/ctrf.json`.
`tests/test_outputs.py` parses `/app/report.json` and asserts the exact schema and the
exact values above — so a missing file, a wrong value, or a wrong shape all score 0.
The expected values are hardcoded ground truth (not recomputed from the agent-writable
log), so the check can't be gamed by editing the input.

## Reproduce locally

From the repo root (needs Docker + Harbor):

```bash
harbor run -p log-report -a oracle     # reference solution -> reward 1
harbor run -p log-report --agent nop   # no-op agent        -> reward 0
```

## What was fixed

- **`task.toml`** — `artifacts` was a string pointing at a file the task never writes;
  now `["/app/report.json"]`.
- **`environment/Dockerfile`** — base was `python:latest` (unpinned) and it copied the
  reference solution into the image; now digest-pinned with the leak removed.
- **`tests/`** — reward went to `/app/reward.txt` with no `ctrf.json`, and the check only
  confirmed the file existed; now reports to `/logs/verifier/` and asserts the real
  values.
- **`instruction.md`** — vague, no paths/schema, missing the required timeout line; now
  pins the paths, states the three-key schema, and ends with the `You have 120 seconds…`
  line.

## Note on the base image

The Project Dynamo allowlist recommends a `public.ecr.aws` Python image, but its published
digest did not resolve and ECR was rate-limiting during local validation. The Dockerfile
therefore pins the equivalent official `python:3.13-slim-bookworm` by digest — still fully
reproducible and digest-locked, which is what the "reproducible environment" requirement
asks for.
